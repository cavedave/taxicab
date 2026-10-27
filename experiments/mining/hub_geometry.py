#!/usr/bin/env python3
"""hub_geometry.py -- the meeting points R of hubs (four-ways with P1 + P2 = P3 + P4), in s = x + y, v = x - y.

The curve x^3 + y^3 = n is s (s^2 + 3 v^2) = 4 n. A chord through two integer points with primitive direction
(p, q) in the (s, v) plane (p = b - a, q = a + b of the line a x + b y = c, up to sign) satisfies
  (p^2 + 3 q^2) s^3 + 6 q kappa s^2 + 3 kappa^2 s - 4 n p^2 = 0,   kappa = p v - q s (constant on the line).
A hub has two chords meeting the curve again at R ("same") or at R and its mirror (s_R, -v_R) ("mirror").

Usage: python3 hub_geometry.py ls_rows.csv fourways.txt [...]   (pairs: line_structure.py CSV, its input file)
Prints one line per meeting point with integer s_R, and a summary.
"""
import csv, itertools, subprocess, sys
from collections import Counter
from fractions import Fraction as F
from math import gcd
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
from line_structure import third

def sv(P): return (P[0] + P[1], P[0] - P[1])

def prim(ds, dv):
    g = gcd(ds, dv); p, q = ds // g, dv // g
    if p < 0 or (p == 0 and q < 0): p, q = -p, -q
    return p, q

def relations(pts):
    """(R, (P, Q), (P2, Q2)): two chords on disjoint pairs whose third points agree up to swap"""
    ch = {}
    for i, j in itertools.combinations(range(len(pts)), 2):
        for Q in (pts[j], pts[j][::-1]):
            R = third(pts[i], Q)
            if R: ch.setdefault(R, []).append((pts[i], Q))
    out = []
    for R, L in ch.items():
        for (P, Q), (P2, Q2) in itertools.combinations(L, 2):
            if {tuple(sorted(P)), tuple(sorted(Q))} & {tuple(sorted(P2)), tuple(sorted(Q2))}: continue
            out.append((R, (P, Q), (P2, Q2)))
    return out

def views(pts):
    """per relation: s_R, |v_R|, same/mirror, the two chords' p and their integer points"""
    out = []
    for R, c1, c2 in relations(pts):
        sR = F(R[0] + R[1]); va = abs(F(R[0] - R[1])); signs, ps = [], []
        for A, B in (c1, c2):
            (s1, v1), (s2, v2) = sv(A), sv(B)
            signs.append([g for g in (1, -1) if (s2 - s1) * (g * va - v1) == (v2 - v1) * (sR - s1)][0])
            ps.append(prim(s2 - s1, v2 - v1))
        out.append((sR, va, "same" if signs[0] == signs[1] else "mirror", ps, (c1, c2)))
    return out

def load(csvfile, txtfile, shapes=("hub",)):
    keep = {r["n"] for r in csv.DictReader(open(csvfile)) if r["shape"] in shapes}
    for l in open(txtfile):
        n, k, r = l.strip().split(";")
        if n in keep: yield int(n), [tuple(map(int, q.split(":"))) for q in r.split(",")]

def main():
    args = sys.argv[1:]; hubs = []
    for c, t in zip(args[::2], args[1::2]): hubs += list(load(c, t))
    rows, stat = [], Counter()
    for n, pts in hubs:
        V = views(pts)
        stat["hubs"] += 1; stat["hubs with an integer s_R"] += any(v[0].denominator == 1 for v in V)
        for sR, va, kind, ps, chords in V:
            if sR.denominator != 1: continue
            rows.append((n, int(sR), va, kind, ps, chords, sorted(p[0] + p[1] for p in pts)))
    gp = "\n".join(f"print(factor({abs(r[1])}),\" | \",factor({r[2].denominator}))" for r in rows)
    fac = subprocess.run(["gp", "-q"], input=gp, capture_output=True, text=True).stdout.strip().split("\n")
    for (n, S, va, kind, ps, chords, ss), f in zip(rows, fac):
        d, w = va.denominator, va.numerator
        T = F(4 * n, S) - S * S                       # = 3 v_R^2
        print(f"n={n} S={S} d={d} {kind:6s} S|n:{n % S == 0}  4n/S-S^2 = 3v^2 = {T}  p:{[p for p, q in ps]}  s_i:{ss}  [S | d: {f}]")
    for k, v in stat.items(): print(k, v)

if __name__ == "__main__":
    main()
