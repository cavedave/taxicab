#!/usr/bin/env python3
"""bowtie_congruence.py -- test F57 on every catalogue bowtie curve: for points of the curve (small combinations of
Mordell-Weil generators), record each prime that spoils the bowtie (base triple not coprime, second line not integral,
second line not coprime), which of E1, E2, b2 - a2 it divides, and whether the failure is decided by (s : r) mod p.
For second-line primes it also tests candidate predicates for the good classes: p | t or p | s at the shared point.
Usage: python3 bowtie_congruence.py [--cmax 2] [--procs 8] [--curves lo-hi]
"""
import argparse, subprocess, sys
from collections import Counter, defaultdict
from fractions import Fraction as Fr
from math import gcd, isqrt
from multiprocessing import Pool
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
import line_enum as L
from bowtie_mine import Curve, peval
from bowtie_hunt import curves_from_catalogue
GPF = Path(__file__).resolve().parent / "verify_gp/quartic2ell.gp"

def pf(m): return set(L.factor(abs(m))) if abs(m) > 1 else set()

def cls(s, r, p, q=None):
    q = q or p
    return ("t", r * pow(s, -1, q) % q) if s % p else ("u", s * pow(r, -1, q) % q)

def points(C, seed, cmax, ngen=4):
    x0, w0 = seed
    qpol = "+".join("(%d)*X^%d" % (c, k) for k, c in enumerate(C.q))
    src = ["\\r %s" % GPF, "Q = subst(%s, X, %s + u); q0 = %s; E = q2e(Q, q0);" % (qpol, x0, w0),
           'R = iferr(alarm(90, ellrank(E)), e, [0,0,0,[]]); G = vecextract(R[4], Str("1..", min(#R[4], %d)));' % ngen,
           'print("RANK ", R[1], " ", R[2]);',
           "forvec(c = vector(#G, k, [-%d, %d]), my(P = [0]); for(k = 1, #G, if(c[k], P = elladd(E, P, ellmul(E, G[k], c[k])))); if(#P == 2, my(B = toQ(Q, q0, P)); if(B != 0, print(B[1] + %s))));" % (cmax, cmax, x0)]
    out = subprocess.run(["gp", "-q", "-D", "parisizemax=2000000000"], input="\n".join(src), capture_output=True, text=True).stdout
    rank = next((l[5:] for l in out.splitlines() if l.startswith("RANK ")), "?")
    return {Fr(t) for l in out.splitlines() if not l.startswith("RANK") for t in l.split()}, rank

def analyse(C, s, r):
    """(spoiling primes by kind, shared point) for slope (s : r); None if the point is degenerate"""
    R = C.raw(s, r); G = 0
    for X, Y in R: G = gcd(G, gcd(X, Y))
    if G == 0: return None
    pts = [(X // G, Y // G) for X, Y in R]
    bad = {"base": set(), "den": set(), "sec": set()}
    for X, Y in pts: bad["base"] |= pf(gcd(X, Y))
    x, y = pts[C.i]; vx, vy = C.b2, -C.a2
    A = vx**3 + vy**3; Bq = 3 * (x * vx * vx + y * vy * vy); Cq = 3 * (x * x * vx + y * y * vy); D = Bq * Bq - 4 * A * Cq
    w = isqrt(D) if D >= 0 else -1
    if w < 0 or w * w != D: return None
    for e in (1, -1):
        t = Fr(-Bq + e * w, 2 * A); X, Y = x + t * vx, y + t * vy
        dn = X.denominator * Y.denominator // gcd(X.denominator, Y.denominator)
        bad["den"] |= pf(dn)
        bad["sec"] |= pf(gcd((X * dn).numerator, (Y * dn).numerator)) - pf(dn)
    return bad, (x, y)

def job(args):
    (a, b, i, a2, b2, slopes), cmax = args
    C = Curve(a, b, i, a2, b2)
    seed = None
    for s, r in slopes:
        x = Fr(r, s); v = peval(C.q, x)
        if v > 0 and isqrt(v.numerator)**2 == v.numerator and isqrt(v.denominator)**2 == v.denominator:
            seed = (x, Fr(isqrt(v.numerator), isqrt(v.denominator))); break
    if seed is None: return (a, b, i, a2, b2), "no seed", []
    xs, rank = points(C, seed, cmax)
    xs |= {Fr(r, s) for s, r in slopes}
    rows = []
    for x in xs:
        s, r = x.denominator, x.numerator
        o = analyse(C, s, r)
        if o: rows.append((s, r) + o)
    return (a, b, i, a2, b2), rank, rows

def main():
    ap = argparse.ArgumentParser(); ap.add_argument("--cmax", type=int, default=2); ap.add_argument("--procs", type=int, default=8)
    ap.add_argument("--curves", default=""); A = ap.parse_args()
    cs = curves_from_catalogue()
    if A.curves: lo, hi = map(int, A.curves.split("-")); cs = cs[lo:hi + 1]
    print(f"{len(cs)} curves")
    tot = Counter(); viol = []
    with Pool(A.procs) as pool:
        for key, rank, rows in pool.imap_unordered(job, [(c, A.cmax) for c in cs]):
            a, b, i, a2, b2 = key
            if not rows: print(f"{key}: {rank}"); continue
            E1, D1, E2, D2 = pf(a*a + a*b + b*b), pf(b - a), pf(a2*a2 + a2*b2 + b2*b2), pf(b2 - a2)
            A3 = b2**3 - a2**3
            for s_, r_, bad, (x, y) in rows:                       # exact criterion: A | 3(x b2^2 + y a2^2) and A | 3(x^2 b2 - y^2 a2)
                crit = (3 * (x * b2 * b2 + y * a2 * a2)) % A3 == 0 and (3 * (x * x * b2 - y * y * a2)) % A3 == 0
                tot[("exact criterion holds", crit == (not bad["den"]))] += 1
            nb = sum(1 for *_, bad, sh in rows if not any(bad.values()))
            msg = [f"{key} rank {rank}: {len(rows)} pts, {nb} bowties; E1 {sorted(E1)} E2 {sorted(E2)} b2-a2 {sorted(D2)} b-a {sorted(D1)}"]
            for kind in ("base", "den", "sec"):
                ps = set().union(*(bad[kind] for *_, bad, sh in rows))
                for p in sorted(ps):
                    where = "+".join(nm for nm, S in (("E1", E1), ("b-a", D1), ("E2", E2), ("b2-a2", D2)) if p in S) or "OTHER"
                    if p > 10**7: msg.append(f"   {kind:4s} p={p} [{where}] (too large to test classes)"); tot[(kind, where, "big")] += 1; continue
                    by = defaultdict(set)
                    for s, r, bad, sh in rows: by[cls(s, r, p)].add(p in bad[kind])
                    dec = all(len(v) == 1 for v in by.values())
                    if not dec:
                        by2 = defaultdict(set)
                        for s, r, bad, sh in rows: by2[cls(s, r, p, p * p)].add(p in bad[kind])
                        if all(len(v) == 1 for v in by2.values()): dec = "mod p^2"
                    nbad = sum(1 for v in by.values() if True in v); ngood = len(by) - nbad
                    extra = ""
                    if kind == "den":
                        good = [sh for s, r, bad, sh in rows if p not in bad["den"]]
                        allx = [sh for s, r, bad, sh in rows]
                        def pred(f): return all(f(*q) == (p not in bad["den"]) for (s, r, bad, q) in [(s, r, bad, sh) for s, r, bad, sh in rows])
                        extra = " good<=>p|t:%s p|s:%s p|x*b2^2+y*a2^2:%s" % (pred(lambda x, y: (x*x - x*y + y*y) % p == 0), pred(lambda x, y: (x + y) % p == 0), pred(lambda x, y: (x * b2 * b2 + y * a2 * a2) % p == 0))
                        tot[("den predicate", where, "p|x*b2^2+y*a2^2" if pred(lambda x, y: (x * b2 * b2 + y * a2 * a2) % p == 0) else "p|s" if pred(lambda x, y: (x + y) % p == 0) else "neither")] += 1
                    msg.append(f"   {kind:4s} p={p} [{where}] decided mod p: {dec}; classes seen bad {nbad} good {ngood} of {p + 1}{extra}")
                    tot[(kind, where, dec)] += 1
                    if dec is not True or where == "OTHER": viol.append((key, kind, p, where, dec))
            print("\n".join(msg), flush=True)
    print("\nSUMMARY (kind, where, decided mod p): count")
    for k, v in sorted(tot.items(), key=str): print(f"  {k}: {v}")
    print("not decided mod p or other prime:", viol)

if __name__ == "__main__":
    main()
