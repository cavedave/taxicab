#!/usr/bin/env python3
"""pos_slopes.py -- where on the slope circle are the lines with two POSITIVE points? (cubefree_plan.md step 3)

For a direction (a, b) every slope r/s of the conic parametrisation gives a line with three real points. Convexity
allows at most two positive ones. This measures, per direction:
  arcs   the angle intervals of (s, r) where the line has two positive points (scan of 20,000 angles);
  frac   the share of the enumerated lattice (0 <= s <= H, |r| <= H, gcd 1) inside those arcs = the cost saving;
  dl     D-lines found (n <= NMAX, D <= DMAX, no filter) in all slopes, and those whose two integer points are both
         positive (these lie inside the arcs by definition).
Usage: python3 pos_slopes.py --dirs-file night_7of9/dirs/hubs_even_150000.txt --sample 20 --height 300
"""
import argparse, math
from math import gcd
from multiprocessing import Pool
import line_enum as L
import dline_enum as DL

def float_pts(a, b, P0, s, r):
    """the three real points of the line for real (s, r), scaled so that x^3 + y^3 > 0"""
    D = b**3 - a**3; x0, y0 = float(P0[0]), float(P0[1]); a2 = a * a
    Q = s*s + s*r + r*r; Bn = 2*x0*s + x0*r + y0*s + 2*y0*r
    NX = x0*Q - Bn*s; NY = y0*Q - Bn*r; W = Q; T = W*D
    ps = (NX - a2*W, NY - a2*W, -a2*W - NX - NY)
    P = [(b*p, T - a*p) for p in ps]
    if P[0][0]**3 + P[0][1]**3 < 0: P = [(-x, -y) for x, y in P]
    return P

def npos(P): return sum(x > 0 and y > 0 for x, y in P)

def arcs(a, b, P0, M=20000):
    """angle intervals in (-pi/2, pi/2] with two positive points"""
    th = [-math.pi/2 + math.pi*(i + 0.5)/M for i in range(M)]
    ok = [npos(float_pts(a, b, P0, math.cos(t), math.sin(t))) == 2 for t in th]
    out, i = [], 0
    while i < M:
        if ok[i]:
            j = i
            while j + 1 < M and ok[j + 1]: j += 1
            out.append((th[i], th[j])); i = j + 1
        else: i += 1
    return out, sum(ok) / M

def job(args):
    a, b, P0, H, nmax, dmax = args
    A, angfrac = arcs(a, b, P0)
    pts_of = L.chord_points(a, b, P0)
    tot = inside = 0
    for s in range(0, H + 1):
        for r in range(-H, H + 1):
            if (s == 0 and r != 1) or gcd(r, s) != 1: continue
            tot += 1
            Pt = pts_of(s, r)[0]
            if Pt[0][0]**3 + Pt[0][1]**3 < 0: Pt = [(-x, -y) for x, y in Pt]
            if npos(Pt) == 2: inside += 1
    T = DL.dtriples(a, b, P0, H, nmax, dmax, 0, 0, H)
    pos = [t for t in T if min(t[3]) > 0 and min(t[4]) > 0]
    return a, b, A, angfrac, tot, inside, len(T), len(pos), [t[0] for t in pos]

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dirs-file", required=True); ap.add_argument("--sample", type=int, default=20)
    ap.add_argument("--height", type=int, default=300); ap.add_argument("--nmax", type=float, default=1e30)
    ap.add_argument("--dmax", type=int, default=10**9); ap.add_argument("--procs", type=int, default=8)
    ap.add_argument("--gp", default="gp")
    A = ap.parse_args()
    dirs = [tuple(map(int, l.split(","))) for l in open(A.dirs_file) if l.strip() and l[0] != "#"]
    step = max(1, len(dirs) // A.sample); dirs = dirs[::step][:A.sample]
    P = L.conic_points(dirs, A.gp)
    jobs = [(a, b, P0, A.height, int(A.nmax), A.dmax) for (a, b), P0 in zip(dirs, P)]
    S = [0] * 4
    with Pool(A.procs) as pool:
        for a, b, Ar, af, tot, ins, ndl, npd, ns in pool.imap(job, jobs):
            print(f"({a},{b}) arcs={len(Ar)} {[(round(x, 3), round(y, 3)) for x, y in Ar]} angle={af:.3f} "
                  f"lattice={ins}/{tot}={ins/tot:.3f} dlines={ndl} pos-pos={npd}", flush=True)
            S[0] += tot; S[1] += ins; S[2] += ndl; S[3] += npd
    print(f"TOTAL lattice in arcs {S[1]}/{S[0]} = {S[1]/S[0]:.3f} (saving {S[0]/max(S[1],1):.1f}x); "
          f"D-lines {S[2]}, both integer points positive {S[3]} = {S[3]/max(S[2],1):.3f}")

if __name__ == "__main__":
    main()
