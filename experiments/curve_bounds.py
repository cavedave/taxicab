#!/usr/bin/env python3
"""curve_bounds.py -- taxicab upper bounds from rational points on x^3 + y^3 = N.

For a seed N (a sum of two cubes in k ways), every positive rational point (u/w, v/w) on
x^3 + y^3 = N gives a representation of N*w^3. So N*L^3 has one representation for each
positive point whose denominator w divides L. We:

  1. ask PARI/GP for generators of the Mordell-Weil group (ellrank + ellsaturation),
  2. list every point of canonical height <= HMAX (Fincke-Pohst via qfminim) and keep the
     positive ones with denominator <= WMAX,
  3. search lcms L of small sets of those denominators, recording for each way-count k the
     smallest N*L^3 found, and compare with the published Ta(k) upper bounds.

Every reported bound is re-verified independently: the k pairs are recomputed from the
points and checked with exact integer arithmetic a^3 + b^3 == N*L^3.

Usage:  python3 curve_bounds.py [--gp ~/pari/bin/gp] [--hmax 80] [--wmax 1e9] [--maxset 4]
        (seed defaults to Ta(5); --seed N --pairs a:b,a:b,... for another one)
"""
import argparse, itertools, math, os, subprocess, sys, tempfile, time
from fractions import Fraction

TA5 = (48988659276962496, [(38787,365757),(107839,362753),(205292,342952),(221424,336588),(231518,331954)])
# best published upper bounds (Boyer 2006-2008, Su 2013); Ta(6) is exact.
# Su (2014-2016) gives Ta(22..24) bounds too; recheck OEIS A011541 before claiming a record.
KNOWN = {6: 24153319581254312065344,
         7: 24885189317885898975235988544,
         8: 50974398750539071400590819921724352,
         9: 136897813798023990395783317207361432493888,
         10: 7335345315241855602572782233444632535674275447104,
         11: 87039729655193781808322993393446581825405320183232000,
         12: 16119148654034302034428760115512552827992287460693283776000,
         # 13..22: Boyer & Wroblewski, April 2008 (refs/boyer_lists/TaxibigUpdated.txt)
         13: 98785992977316717572070208794037178343163969803121800608526912000,
         14: 6181115942163278484307116174514304039670628856329988877227399275142976000,
         15: 786630615595626829796137755567437844038832146564530660386728812791938555036352000,
         16: 1407430328457240141244921568479580896498768360005757901394557724136294559835243494681088000,
         17: 108883358434560363503260016942467566965657808716401027019007732065428469239764403684536752685040128000,
         18: 32704115261272222010108668321371490956498583891096244871994833214348230808345220932546725287574509356813791744000,
         19: 89155799373431424956779039683208074195259067508030416952016859893056008200986665364956362114476625742414288155368000000000,
         20: 6897380753715950027554119762858815120976857451913869723850868496922922856256366585322070924221550029921862628606999892276808000000000,
         21: 108017480260055891349349434078007118409816211596074421874782013152781209964290521967447172971431469705047741717793222992124981940703226072000000000,
         22: 4680247859298792255465896583920257161776853980641720488623945439873944558056759119053262369879441902130153472288312996410513410535472957059046536164424000000000}

GP_SCRIPT = r"""
default(parisizemax, 4*10^9);
N = %(N)d; hmax = %(hmax)s; wmax = %(wmax)d;
E = ellinit([0,0,0,0,-432*N^2]);
toW(x,y) = my(s = x + y); [12*N/s, 36*N*(x - y)/s];
known = [%(known)s];
R = ellrank(E, 1, known);
if(R[1] != R[2], print("#WARN rank only bounded: ", R[1], " <= r <= ", R[2]));
G = ellsaturation(E, R[4], 1000);
print("#RANK ", #G);
H = ellheightmatrix(E, G);
V = qfminim(H, hmax, 500000, 2)[3];
print("#VECTORS ", #V);
{
  for(j = 1, #V,
    my(v = V[,j], P = [0], x, y, w);
    for(i = 1, #G, if(v[i], P = elladd(E, P, ellmul(E, G[i], v[i]))));
    if(P == [0], next);
    x = (36*N + P[2])/(6*P[1]); y = (36*N - P[2])/(6*P[1]);
    if(x > 0 && y > 0,
      w = lcm(denominator(x), denominator(y));
      if(w <= wmax, print("P ", w, " ", numerator(x*w), " ", numerator(y*w)))));
  \\ the identity is excluded by qfminim; the seed's own pairs are points with w = 1
}
quit;
"""

def run_gp(gp, N, pairs, hmax, wmax, timeout=None, verbose=True):
    """pairs: (a, b) integer points or (a, b, g) for the rational point (a/g, b/g)"""
    known = ",".join(f"toW({p[0]}/{p[2] if len(p) > 2 else 1},{p[1]}/{p[2] if len(p) > 2 else 1})" for p in pairs)
    src = GP_SCRIPT % dict(N=N, hmax=hmax, wmax=wmax, known=known)
    with tempfile.NamedTemporaryFile("w", suffix=".gp", delete=False) as f:
        f.write(src); path = f.name
    try:
        out = subprocess.run([gp, "-q", path], capture_output=True, text=True, check=True, timeout=timeout).stdout
    finally:
        os.unlink(path)
    pts, rank = {}, None
    for line in out.splitlines():
        if line.startswith("#RANK"): rank = int(line.split()[1])
        elif line.startswith("#") and (verbose or line.startswith("#WARN")): print("  gp:", line[1:])
        elif line.startswith("P "):
            w, u, v = map(int, line.split()[1:])
            a, b = sorted((u, v))
            assert a**3 + b**3 == N * w**3, "point check failed"
            pts[(w, a, b)] = True                      # (P, -P) give the same unordered pair
    return rank, sorted(pts)

def search(N, pts, maxset, ub, bases=(1,)):
    """For each k, the smallest N*L^3 with >= k points of denominator dividing L.
    L runs over lcm(base, up to maxset denominators); a base is a seed's own denominator g,
    so a seed's pairs never use up a slot when the curve is its cube-free core."""
    dens = sorted({w for w, _, _ in pts})
    best = {}                                           # k -> (n, L)
    def consider(L):
        n = N * L**3
        if n > ub: return
        k = sum(1 for w, _, _ in pts if L % w == 0)
        for kk in range(1, k + 1):
            if kk not in best or n < best[kk][0]: best[kk] = (n, L)
    lmax = round((ub / N) ** (1/3)) + 1
    def rec(start, L, depth):
        for i in range(start, len(dens)):
            L2 = L * dens[i] // math.gcd(L, dens[i])
            if L2 > lmax: continue
            consider(L2)
            if depth + 1 < maxset: rec(i + 1, L2, depth + 1)
    for b in sorted(set(bases)):
        if b <= lmax:
            consider(b); rec(0, b, 0)
    return best

def beam(N, pts, ub, bases=(1,), width=50):
    """Beam search over L = lcm of denominators: grow one denominator at a time, keeping for
    each way-count the `width` smallest L. Reaches large sets (10+ denominators) that the
    exhaustive `search` cannot; not guaranteed optimal."""
    from collections import Counter
    cnt = Counter(w for w, _, _ in pts); dens = sorted(cnt)
    lmax = round((ub / N) ** (1/3)) + 1
    best = {}
    def count(L): return sum(c for w, c in cnt.items() if L % w == 0)
    def record(L, k):
        n = N * L**3
        if n > ub: return
        for kk in range(1, k + 1):
            if kk not in best or n < best[kk][0]: best[kk] = (n, L)
    frontier = {}
    for b in set(bases):
        if b <= lmax:
            frontier[b] = count(b); record(b, frontier[b])
    seen = set(frontier)
    while frontier:
        scored = []
        for L in frontier:
            for d in dens:
                if L % d == 0: continue
                L2 = L * d // math.gcd(L, d)
                if L2 > lmax or L2 in seen: continue
                seen.add(L2)
                k2 = count(L2); record(L2, k2); scored.append((k2, L2))
        byk = {}
        for k2, L2 in scored: byk.setdefault(k2, []).append(L2)
        frontier = {L2: k2 for k2, Ls in byk.items() for L2 in sorted(Ls)[:width]}
    return best

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--gp", default="gp")
    ap.add_argument("--seed", type=int); ap.add_argument("--pairs")
    ap.add_argument("--hmax", default="80")
    ap.add_argument("--wmax", type=float, default=1e9)
    ap.add_argument("--maxset", type=int, default=4)
    ap.add_argument("--ub", type=float, default=1e60)
    a = ap.parse_args()
    N, pairs = TA5
    if a.seed:
        N = a.seed; pairs = [tuple(map(int, p.split(":"))) for p in a.pairs.split(",")]
    for x, y in pairs: assert x**3 + y**3 == N
    t = time.time()
    rank, pts = run_gp(a.gp, N, pairs, a.hmax, int(a.wmax))
    print(f"seed N = {N}: rank {rank}, {len(pts)} positive points with denominator <= {a.wmax:.0e} "
          f"(height <= {a.hmax}), {time.time()-t:.1f}s")
    print("  smallest denominators:", sorted({w for w,_,_ in pts})[:25])
    t = time.time()
    best = search(N, pts, a.maxset, int(a.ub))
    print(f"subset search (sets of <= {a.maxset} denominators): {time.time()-t:.1f}s\n")
    print(f"{'k':>3}  {'best N*L^3 found':>62}  {'L':>14}  vs published")
    for k in sorted(best):
        if k < 6: continue
        n, L = best[k]
        # independent re-verification of the k pairs
        good = [(u*(L//w), v*(L//w)) for w, u, v in pts if L % w == 0]
        assert len(good) >= k and all(x**3 + y**3 == n for x, y in good)
        ref = KNOWN.get(k)
        cmp = "" if ref is None else ("BEATS published!" if n < ref else
              "equals published" if n == ref else f"{n/ref:.3g}x published")
        print(f"{k:>3}  {n:>62}  {L:>14}  {cmp}")

if __name__ == "__main__":
    main()
