#!/usr/bin/env python3
"""thm14_check.py -- THEOREMS.md Theorem 14 on every pair of points (representations and swaps) of the catalogue and of
every three-way 1e17 - 1e19 (argv[1]/worf/k3_*.txt): the non-split part of s divides b - a (at 2: one power more)."""
import sys, glob
from math import gcd
from itertools import combinations
S = sys.argv[1]
def vp(m, p):
    m = abs(m); v = 0
    while m and m % p == 0: m //= p; v += 1
    return v
def nonsplit_primes(m):
    m = abs(m); ps = []; p = 2
    while p * p <= m:
        if m % p == 0:
            if p % 3 != 1: ps.append(p)
            while m % p == 0: m //= p
        p += 1
    if m > 1 and m % 3 != 1: ps.append(m)
    return ps
pairs = bad = 0
for fn in glob.glob(S + "/worf/k3_*.txt") + ["results/a047697_catalogue.txt"]:
    for l in open(fn):
        if not l[0].isdigit(): continue
        n, k, r = l.strip().split(";")
        reps = [tuple(map(int, p.split(":"))) for p in r.split(",")]; pts = reps + [(y, x) for x, y in reps]
        ps = nonsplit_primes(reps[0][0] + reps[0][1])
        for P, Q in combinations(pts, 2):
            if Q == (P[1], P[0]): continue
            a, b = Q[1] - P[1], P[0] - Q[0]; g = gcd(a, b); a, b = a // g, b // g
            s = P[0] + P[1]; pairs += 1
            for p in ps:
                if vp(b - a, p) < vp(s, p) + (1 if p == 2 else 0): bad += 1; print("FAIL", n, P, Q, p); break
print(f"pairs of points (all representations and swaps): {pairs:,}; nonsplit(s) | b - a (2: one more) fails: {bad}")
