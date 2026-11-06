#!/usr/bin/env python3
"""certify_M.py -- exact certificate for the height bounds of the complete line searches (THEOREMS.md Lemma 15).

For every direction (a, b):
  1. M = line_heights.prod_min(S) as the runs computed it (floating point), and M_cert = M (1 - 1e-12), an exact rational.
  2. P = S1 S2 S3 is a binary sextic with integer coefficients and constant sign (each S_i is definite, Lemma 15).
     On the three edges of the half-square (s = 1, r = t in [-1, 1]; r = +-1, s = t in [0, 1]) the polynomial
     sign(P) P - M_cert has no real root (PARI polsturm, exact) and is positive at the left end: so |P| >= M_cert on
     max(|s|, |r|) = 1, and |S1 S2 S3| >= M_cert h^6 for every slope.
  3. For each bound B and every G-level the enumeration uses (Glo; Glo prod p^(j - lo) for the tier-2 level sets),
     the integer height used, floor(H(G, M) (1 - 1e-13)) + 1 (a margin for another machine's floating point), covers every integer
     height h <= H(G, M_cert): (used + 1)^6 > B (a - b)^2 G^3 / (E M_cert) in exact rationals.
Any failure is printed; the run ends with counts.
Usage: python3 certify_M.py --cmax 1.2e12 --B 1000000000000000019884624838656 999999999999999945575230987042816 [--procs 8]
"""
import argparse, math, subprocess, sys, time
from fractions import Fraction as Fr
from itertools import combinations, product
from multiprocessing import Pool
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
import line_enum as L
from line_heights import raw_forms, prod_min
from line_complete import Direction

def sextic(S):
    """coefficients c[k] of s^(6-k) r^k in S1 S2 S3"""
    c = [1]
    for A, B, C in S:
        f = [A, B, C]; n = [0] * (len(c) + 2)
        for i, x in enumerate(c):
            for j, y in enumerate(f): n[i + j] += x * y
        c = n
    return c

def polys(c, sign):
    """the three edge polynomials in t (lists of coefficients, constant term first)"""
    e1 = [sign * c[k] for k in range(7)]                               # s = 1, r = t:  sum c_k t^k
    e2 = [sign * c[6 - k] for k in range(7)]                           # r = 1, s = t:  sum c_k t^(6-k)
    e3 = [sign * c[6 - k] * (-1)**(6 - k) for k in range(7)]           # r = -1, s = t
    return [(e1, -1, 1), (e2, 0, 1), (e3, 0, 1)]

def gp_poly(co):
    return "+".join(f"({x})*t^{k}" for k, x in enumerate(co) if x) or "0"

def check(job):
    dirs, P0s, Bs, gp = job
    lines, meta, fails = [], [], []
    for (a, b), P0 in zip(dirs, P0s):
        raw, coord, S = raw_forms(a, b, P0)
        M = prod_min(S); Mc = Fr(M) * (1 - Fr(1, 10**12))
        c = sextic(S); sign = 1 if c[0] > 0 else -1
        for co, lo, hi in polys(c, sign):
            lines.append(f"print(polsturm({gp_poly(co)} - ({Mc.numerator})/({Mc.denominator}), [{lo},{hi}]) + (subst({gp_poly(co)},t,{lo}) <= ({Mc.numerator})/({Mc.denominator})));")
        meta.append((a, b))
        E = a*a + a*b + b*b
        for B in Bs:
            d = Direction(a, b, P0, B)
            Gs = {d.Glo}
            ex = d.extra
            for k in range(1, len(ex) + 1):
                for T in combinations(ex, k):
                    for lv in product(*[sorted(levels) for p, lo, hi, levels in T]):
                        Gs.add(d.Glo * math.prod(p**(jj - lo) for (p, lo, hi, _), jj in zip(T, lv)))
            for G in Gs:
                used = int(d.H(G) * (1 - 1e-13)) + 1
                need6 = Fr(B * (a - b)**2 * G**3) / (E * Mc)
                if Fr(used + 1)**6 <= need6:                          # an integer height above `used` would still be needed
                    fails.append(f"HEIGHT ({a},{b}) B={B} G={G} used {used}, needs up to {float(need6)**(1/6):.6f}")
    out = subprocess.run([gp, "-q", "-D", "parisizemax=1000000000"], input="\n".join(lines), capture_output=True, text=True).stdout.split()
    for i, (a, b) in enumerate(meta):
        r = out[3 * i: 3 * i + 3]
        if r != ["0", "0", "0"]: fails.append(f"STURM ({a},{b}) edge results {r}")
    return len(meta), fails

def main():
    ap = argparse.ArgumentParser(); ap.add_argument("--cmax", type=float, default=1.2e12)
    ap.add_argument("--B", nargs="+", type=int, required=True); ap.add_argument("--procs", type=int, default=8)
    ap.add_argument("--gp", default="gp"); ap.add_argument("--batch", type=int, default=400); ap.add_argument("--only", default="")
    A = ap.parse_args(); t0 = time.time()
    if A.only: dirs = [tuple(map(int, d.split(","))) for d in A.only.split(";")]
    else: dirs = [(a, b) for c, a, b in L.dirs_by_cost(int(A.cmax), L.allowed_f)]
    P = L.conic_points(dirs, A.gp)
    jobs = [(dirs[i:i + A.batch], P[i:i + A.batch], A.B, A.gp) for i in range(0, len(dirs), A.batch)]
    print(f"{len(dirs):,} directions, {len(jobs)} batches, setup {time.time() - t0:.0f} s", flush=True)
    done = nfail = 0
    with Pool(A.procs) as pool:
        for n, fails in pool.imap_unordered(check, jobs):
            done += n; nfail += len(fails)
            for f in fails: print(f, flush=True)
            if done % 100000 < A.batch: print(f"  {done:,} directions checked, {nfail} failures, {time.time() - t0:.0f} s", flush=True)
    print(f"CERTIFIED {done:,} directions, {nfail} failures, {time.time() - t0:.0f} s", flush=True)

if __name__ == "__main__":
    main()
