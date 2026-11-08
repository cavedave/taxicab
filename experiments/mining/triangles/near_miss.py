#!/usr/bin/env python3
"""near_miss.py -- how close does a bowtie (or any k-way) come to a sixth representation by a new chord?

Points of x^3 + y^3 = n: every representation (x, y) and its swap (y, x). With the flex at infinity as origin, three
points are collinear iff A + B + C = 0, so the chord through two known points P, Q meets the cubic again in the rational
point R = -(P + Q). A triangle (three lines, pairwise meeting in known points) is a six-way; for a bowtie it means some
chord R = -(P + Q) between its two lines is an integral coprime point. For every pair P, Q of points not already on a
known line of three (and not P, swap(P), whose chord is parallel to x + y = 0), compute R and its denominator d(R)
(R = (X/d, Y/d) in lowest terms). d(R) = 1 with gcd(X, Y) = 1 would be a new representation.

Usage: python3 near_miss.py results/five_ways_all.txt [more files: n;k;x:y,... rows] --out near_miss.txt
"""
import argparse, math, sys
from fractions import Fraction as Fr
from itertools import combinations
if hasattr(sys, "set_int_max_str_digits"): sys.set_int_max_str_digits(0)

def third(P, Q, n):
    (p1, p2), (q1, q2) = P, Q
    u, v = q1 - p1, q2 - p2
    den = u**3 + v**3
    if den == 0: return None
    t = Fr(-3 * (p1 * u * u + p2 * v * v), den) - 1
    R = (p1 + t * u, p2 + t * v)
    assert R[0]**3 + R[1]**3 == n
    return R

def analyse(n, reps):
    pts = sorted({p for x, y in reps for p in ((x, y), (y, x))})
    known = set(pts)
    lines = []                                          # known lines of three among the points
    for A, B, C in combinations(pts, 3):
        if (B[0] - A[0]) * (C[1] - A[1]) == (B[1] - A[1]) * (C[0] - A[0]): lines.append({A, B, C})
    out = []
    for P, Q in combinations(pts, 2):
        if Q == (P[1], P[0]) or any(P in L and Q in L for L in lines): continue
        R = third(P, Q, n)
        if R is None or R in known: continue
        d = R[0].denominator * R[1].denominator // math.gcd(R[0].denominator, R[1].denominator)
        X, Y = R[0] * d, R[1] * d
        out.append((d, int(X), int(Y), P, Q))
    return len(lines) // 2, out                         # each line appears twice (as L and its swap)

def main():
    ap = argparse.ArgumentParser(); ap.add_argument("files", nargs="+"); ap.add_argument("--out", required=True)
    ap.add_argument("--kmin", type=int, default=4)
    A = ap.parse_args()
    seen = set()
    with open(A.out, "w") as f:
        f.write("# near_miss.py: n;k;lines;chords;min d(R);log10 min d / log10 n;R at min d (X:Y/d);P;Q\n")
        for fn in A.files:
            for l in open(fn):
                if not l[0].isdigit(): continue
                g = l.strip().split(";"); n = int(g[0])
                if n in seen: continue
                reps = [tuple(map(int, p.split(":"))) for p in g[2].split(",")]
                if len(reps) < A.kmin: continue
                seen.add(n)
                nl, ch = analyse(n, reps)
                if not ch: continue
                d, X, Y, P, Q = min(ch)
                hit = d == 1 and math.gcd(X, Y) == 1
                f.write(f"{n};{len(reps)};{nl};{len(ch)};{d};{math.log10(d) / math.log10(n) if d > 1 else 0:.4f};{X}:{Y}/{d};{P[0]}:{P[1]};{Q[0]}:{Q[1]}\n")
                if hit: print(f"*** NEW REPRESENTATION: n = {n}, ({X}, {Y})", flush=True)
                if d == 1 and not hit: print(f"integral but not coprime: n = {n}, ({X}, {Y}), gcd {math.gcd(X, Y)}", flush=True)

if __name__ == "__main__":
    main()
