#!/usr/bin/env python3
"""bowtie_hunt.py -- six-way hunt on the bowtie curves (FINDINGS F53): for every curve from the catalogue's bowties,
enumerate its points as small integer combinations of known points (group law on the quartic, bowtie_mine.Group),
keep the coprime five-ways with n < 10^NMAX, and count every one exactly.

Exact count: n = E s1 s2 s3 / (a - b)^2 (Theorem 13) for the curve's base line, so n is factored from E, a - b and the
three s-values of the base triple (PARI, one process per curve). Representations are then searched only at
s = f * (product of a subset of the split-prime blocks) <= (4n)^(1/3) (Theorem 5), with 4n/s - s^2 = 3 d^2.
Every n is written as n;k;x:y,... ; a k >= 6 line is also printed to stdout immediately.

Usage: python3 bowtie_hunt.py --out hunt.txt [--cmax 4] [--basis 6] [--nmax 300] [--procs 60] [--curves 0-9]
"""
import argparse, itertools, math, re, subprocess, sys, time
from fractions import Fraction as Fr
from math import gcd, isqrt
from multiprocessing import Pool
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
import line_enum as L
from line_complete import Direction, setup_canon, canon_slope
from bowtie_mine import Curve, Group, lines_of, peval, height

ROOT = Path(__file__).resolve().parents[2]

def curves_from_catalogue():
    """[(a, b, i, a2, b2, [(s, r), ...])]: one entry per curve, with the slopes of its known bowties"""
    pairs = {}
    for l in open(ROOT / "results/a047697_catalogue.txt"):
        if not l[0].isdigit(): continue
        n, k, r = l.strip().split(";")
        if int(k) < 5: continue
        reps = [tuple(map(int, p.split(":"))) for p in r.split(",")]
        ls = lines_of(reps)
        if len(ls) < 2: continue
        (d1, T1), (d2, T2) = sorted(ls[:2], key=lambda t: abs(t[0][1]**3 - t[0][0]**3))
        inter = set(T1) & set(T2)
        if not inter: T2 = tuple((y, x) for x, y in T2); d2 = (d2[1], d2[0]); inter = set(T1) & set(T2)
        if not inter: continue
        if d1[0] > d1[1]:
            T1 = tuple((y, x) for x, y in T1); T2 = tuple((y, x) for x, y in T2); d1 = (d1[1], d1[0]); d2 = (d2[1], d2[0])
            inter = set(T1) & set(T2)
        pairs.setdefault((d1, d2), []).append((T1, next(iter(inter))))
    out = []
    for ((a, b), (a2, b2)), bts in sorted(pairs.items()):
        P0 = L.conic_points([(a, b)])[0]; d = Direction(a, b, P0, 10**60); setup_canon(d, P0)
        byi = {}
        for T1, cs in bts:
            h, s, r = canon_slope(d, list(T1))
            R = d.raw(s, r); G = 0
            for x, y in R: G = gcd(G, gcd(x, y))
            red = [(x // G, y // G) for x, y in R]
            idx = [k for k, p in enumerate(red) if p == cs or (-p[0], -p[1]) == cs]
            if idx: byi.setdefault(idx[0], []).append((s, r))
        for i, sl in byi.items(): out.append((a, b, i, a2, b2, sl))
    return out

def factor_many(nums, gp, tlim=600):
    """PARI factorisations; a factorisation over the time limit comes back as None"""
    # alarm() RETURNS an error object on timeout (it does not raise), so test its type; iferr catches other errors
    src = "\n".join(f'print(iferr(my(r = alarm({tlim}, factor({abs(v)}))); if(type(r) == "t_ERROR", "TIMEOUT", r), e, "TIMEOUT"));'
                    for v in nums)
    txt = subprocess.run([gp, "-q", "-D", "parisizemax=4000000000"], input=src, capture_output=True, text=True).stdout
    if len(txt.strip().splitlines()) != len(nums): return [None] * len(nums)     # gp died or printed extra: trust nothing
    res = []
    for line in txt.strip().splitlines():
        if "TIMEOUT" in line: res.append(None); continue
        body = re.search(r"\[([^\[\]]*)\]", line.replace("Mat(", ""))
        res.append([] if body is None or not body.group(1).strip() else
                   [tuple(int(v) for v in rr.split(",")) for rr in body.group(1).replace(" ", "").split(";")])
    return res

def icbrt(N):
    """floor(N^(1/3)) for an integer N >= 0"""
    if N < 2: return N
    x = 1 << ((N.bit_length() + 2) // 3)
    while True:
        y = (2 * x + N // (x * x)) // 3
        if y >= x: break
        x = y
    while x**3 > N: x -= 1
    while (x + 1)**3 <= N: x += 1
    return x

def count_reps(n, fac, deadline=None):
    """every coprime (x, y) with x^3 + y^3 = n: s = f * (subset of split blocks) <= (4n)^(1/3) (Theorem 5).
    Depth-first over the subsets (memory linear in the number of split primes; the old list of all candidates reached
    40 GB at 28 split primes, F63). With a deadline (time.time() value), returns None if it is passed."""
    f = 1; blocks = []
    for p, e in fac:
        if p % 3 == 1: blocks.append(p**e)
        elif p == 3: f *= 3**(e - 1)
        else: f *= p**e
    S = icbrt(4 * n)
    if f > S: return []
    blocks.sort(); nb = len(blocks); reps = []; stack = [(f, 0)]; steps = 0
    while stack:
        s, i = stack.pop()
        for j in range(i, nb):                          # blocks ascending: once s * block > S, all later ones are too
            c = s * blocks[j]
            if c > S: break
            stack.append((c, j + 1))
        steps += 1
        if deadline is not None and not steps & 0xFFFF and time.time() > deadline: return None
        t = 4 * (n // s) - s * s
        if t < 0 or t % 3: continue
        m = t // 3; d = isqrt(m)
        if d * d != m or (s + d) % 2: continue
        x, y = (s + d) // 2, (s - d) // 2
        if y != 0 and gcd(abs(x), abs(y)) == 1 and x**3 + y**3 == n: reps.append((x, y))
    return reps

def gp_points(C, known, cmax, hb, gp, rank_time):
    """x-coordinates (slopes r/s) of small combinations of Mordell-Weil generators, computed in PARI on the Weierstrass
    model (verify_gp/quartic2ell.gp, Washington Thm 2.17) and mapped back to the quartic; known points used as hints"""
    x0, w0 = known[0]
    qpol = "+".join(f"({c})*X^{k}" for k, c in enumerate(C.q))
    hints = ",".join(f"toE(Q, q0, {x} - ({x0}), {w})" for x, w in known[1:] if x != x0)
    src = f"""\\r {Path(__file__).resolve().parent}/verify_gp/quartic2ell.gp
Q = subst({qpol}, X, {x0} + u); q0 = {w0}; E = q2e(Q, q0);
H = [{hints}]; H = select(P -> #P == 2, H);
R = iferr(alarm({rank_time}, ellrank(E, 1, H)), e, [0, 0, 0, H]);
G = R[4]; if(#G == 0, G = H);
G = vecextract(G, Str("1..", min(#G, 6)));
print("RANK ", R[1], " ", R[2], " ", #G);
forvec(c = vector(#G, k, [-{cmax}, {cmax}]),
  my(P = [0]); for(k = 1, #G, if(c[k], P = elladd(E, P, ellmul(E, G[k], c[k]))));
  if(#P == 2, my(B = toQ(Q, q0, P)); if(B != 0, my(x = B[1] + {x0}); if(max(abs(numerator(x)), denominator(x)) < 2^{hb}, print("X ", x)))));
"""
    out = subprocess.run([gp, "-q", "-D", "parisizemax=4000000000"], input=src, capture_output=True, text=True).stdout
    xs, rank = set(), None
    for line in out.splitlines():
        if line.startswith("X "): xs.add(Fr(line[2:].strip()))
        elif line.startswith("RANK "): rank = line[5:].strip()
    return xs, rank

def hunt_curve(job):
    (a, b, i, a2, b2, slopes), cmax, nbasis, nmax, gp = job
    t0 = time.time(); C = Curve(a, b, i, a2, b2)
    known = []
    for s, r in slopes:
        x = Fr(r, s); v = peval(C.q, x)
        if v <= 0: continue
        wn, wd = isqrt(v.numerator), isqrt(v.denominator)
        if wn * wn == v.numerator and wd * wd == v.denominator: known += [(x, Fr(wn, wd)), (x, -Fr(wn, wd))]
    if not known: return (a, b, i, a2, b2), [], "no seed", 0
    hb = int(nmax * 3.33 / 6) + 40                                  # slope-height cap in bits (n ~ h^6)
    xs, rank = gp_points(C, known, cmax, hb, gp, 300)
    xs |= {x for x, w in known}
    found = {}
    for x in xs:
        out, why = C.bowtie(x.denominator, x.numerator)
        if out and out[0] < 10**nmax: found[out[0]] = out
    ns = sorted(found)
    pieces = []
    for n in ns: pieces += [C.E, abs(a - b) or 1] + [abs(v) for v in found[n][2]]
    facs = factor_many(pieces, gp) if pieces else []
    rows = []
    for j, n in enumerate(ns):
        fE, fD, f1, f2, f3 = facs[5 * j: 5 * j + 5]
        if None in (fE, fD, f1, f2, f3): rows.append((n, None, found[n][1])); continue      # factoring timed out: k unknown
        F = {}
        for fac, sgn in ((fE, 1), (f1, 1), (f2, 1), (f3, 1), (fD, -2)):
            for p, e in fac: F[p] = F.get(p, 0) + sgn * e
        F = sorted((p, e) for p, e in F.items() if e)
        assert all(e > 0 for p, e in F) and math.prod(p**e for p, e in F) == n, "factorisation does not multiply to n"
        reps = count_reps(n, F)
        assert len(reps) >= 5, "fewer than the five known representations"
        rows.append((n, reps, found[n][1]))
    return (a, b, i, a2, b2), rows, f"rank {rank}, {len(xs)} slopes", time.time() - t0

def main():
    ap = argparse.ArgumentParser(); ap.add_argument("--out", required=True); ap.add_argument("--cmax", type=int, default=4)
    ap.add_argument("--basis", type=int, default=6); ap.add_argument("--nmax", type=int, default=300)
    ap.add_argument("--procs", type=int, default=8); ap.add_argument("--gp", default="gp"); ap.add_argument("--curves", default="")
    A = ap.parse_args(); t0 = time.time()
    cs = curves_from_catalogue()
    if A.curves: lo, hi = map(int, A.curves.split("-")); cs = cs[lo:hi + 1]
    print(f"{len(cs)} curves, setup {time.time() - t0:.0f} s", flush=True)
    seen = set(); tot = 0; best = 0; unk = 0
    with open(A.out, "w") as f, Pool(A.procs) as pool:
        f.write(f"# bowtie_hunt.py: cmax {A.cmax}, basis {A.basis}, n < 1e{A.nmax}; n;k;x:y,...\n")
        for key, rows, note, dt in pool.imap_unordered(hunt_curve, [(c, A.cmax, A.basis, A.nmax, A.gp) for c in cs]):
            new = 0
            for n, reps, five in rows:
                if n in seen: continue
                seen.add(n); new += 1; tot += 1
                if reps is None:                                   # unknown k: write the five known representations
                    unk += 1; f.write(f"{n};?;" + ",".join(f"{x}:{y}" for x, y in five) + "\n"); continue
                best = max(best, len(reps))
                f.write(f"{n};{len(reps)};" + ",".join(f"{x}:{y}" for x, y in sorted(reps, reverse=True)) + "\n")
                if len(reps) >= 6: print(f"*** SIX-WAY OR MORE: k = {len(reps)}, n = {n}", flush=True)
            f.flush()
            print(f"curve {key}: {note}, {len(rows)} five-ways (< 1e{A.nmax}), {new} new to this run, {dt:.0f} s; total {tot}, largest k {best}", flush=True)
    print(f"done: {tot} distinct numbers, {tot - unk} counted exactly (largest k {best}), {unk} with k unknown (factoring time limit), {time.time() - t0:.0f} s", flush=True)

if __name__ == "__main__":
    main()
