#!/usr/bin/env python3
"""bowtie_localfilter.py -- a local test for bowtie curves (F58). At a prime p || E2 (p not dividing 3 E1 (b - a) (b2 - a2))
the second line is integral iff p | x b2^2 + y a2^2 at the shared point (x, y), which is a quadratic form in the
slope: at most 2 good classes mod p. A bowtie needs a p-adic point of w^2 = q(r) in one of them. We search integer slopes
r = r0 + p u (u < ULIM) in each good class (and s = p in the class at infinity) for q a p-adic square; if none is found the
direction pair is flagged 'no local point at p' (for ULIM >= p^2 the search covers the class to precision p^3).
Usage: python3 bowtie_localfilter.py --seeded | --base 3,4 --ndir 400 [--pmax 2000] [--procs 8]
"""
import argparse, sys
from fractions import Fraction as Fr
from math import gcd
from multiprocessing import Pool
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
import line_enum as L
from bowtie_mine import Curve
from bowtie_hunt import curves_from_catalogue

def pf(m): return set(L.factor(abs(m))) if abs(m) > 1 else set()

def vp(m, p):
    v = 0
    while m % p == 0: m //= p; v += 1
    return v, m

def padic_square(v, p):
    if v == 0: return True
    m, u = vp(v, p)
    return m % 2 == 0 and pow(u % p, (p - 1) // 2, p) == 1

def qhom(C, s, r):
    """s^4 q(r / s): an integer, a p-adic square iff q(r / s) is"""
    return sum(c * r**k * s**(4 - k) for k, c in enumerate(C.q))

def good(C, s, r, p):
    R = C.raw(s, r); x, y = R[C.i]
    if x % p == 0 and y % p == 0: return None                     # p | G: not decided here
    return (x * C.b2**2 + y * C.a2**2) % p == 0

def test(args):
    (a, b, i, a2, b2), pmax, ulim = args
    C = Curve(a, b, i, a2, b2)
    bad = 3 * (a*a + a*b + b*b) * (b - a) * (b2 - a2)
    E2 = a2*a2 + a2*b2 + b2*b2
    out = []
    for p in sorted(pf(E2)):
        if p > pmax or bad % p == 0 or E2 % (p * p) == 0: continue
        classes = [(1, r) for r in range(p)] + [(p, 1)]
        gc = [(s, r) for s, r in classes if good(C, s, r, p)]
        und = [(s, r) for s, r in classes if good(C, s, r, p) is None]
        found = bool(und)
        for s, r in gc:
            if found: break
            for u in range(min(ulim, p * p)):
                ss, rr = (1, r + p * u) if s == 1 else (p * u, 1)            # the class at infinity: s = p u, r = 1
                if gcd(ss, rr) != 1: continue
                if padic_square(qhom(C, ss, rr), p): found = True; break
        out.append((p, len(gc), found))
    return (a, b, i, a2, b2), out

def main():
    ap = argparse.ArgumentParser(); ap.add_argument("--seeded", action="store_true"); ap.add_argument("--base", default="3,4")
    ap.add_argument("--ndir", type=int, default=400); ap.add_argument("--pmax", type=int, default=2000)
    ap.add_argument("--ulim", type=int, default=4000); ap.add_argument("--procs", type=int, default=8); A = ap.parse_args()
    if A.seeded: keys = [c[:5] for c in curves_from_catalogue()]
    else:
        a, b = map(int, A.base.split(",")); keys = []
        for c, a2, b2 in L.dirs_by_cost(10**9, lambda f: True)[:A.ndir]:
            for d in ((a2, b2), (b2, a2)):
                if set(d) != {a, b}: keys += [(a, b, i) + d for i in range(3)]
    n = {"curves": len(keys), "tested at >= 1 prime": 0, "no good class at some p": 0, "no local point at some p": 0}
    with Pool(A.procs) as pool:
        for key, out in pool.imap_unordered(test, [(k, A.pmax, A.ulim) for k in keys], chunksize=8):
            if out: n["tested at >= 1 prime"] += 1
            if any(g == 0 for p, g, f in out): n["no good class at some p"] += 1
            if any(not f for p, g, f in out):
                n["no local point at some p"] += 1
                if A.seeded: print("SEEDED CURVE FAILS:", key, out)
    print(n)

if __name__ == "__main__":
    main()
