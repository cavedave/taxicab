#!/usr/bin/env python3
"""primes_lines.py -- FINDINGS F46: for each small prime p, how often n with p | n carries a line, and which of a, b,
b - a, a + b, E, c the lines of such n are divisible by (argv[1]/worf/k3_*.txt and the catalogue)."""
import sys, glob, pickle
from math import gcd
from itertools import combinations
from collections import Counter, defaultdict
S = sys.argv[1]
data = []        # (n, k, [lines (a, b, c)])
for f in glob.glob(S + "/worf/k3_*.txt") + ["results/a047697_catalogue.txt"]:
    for l in open(f):
        if not l[0].isdigit(): continue
        n, k, r = l.strip().split(";"); n = int(n)
        reps = [tuple(map(int, p.split(":"))) for p in r.split(",")]; pts = reps + [(y, x) for x, y in reps]
        L = set()
        for P, Q, R in combinations(pts, 3):
            if len({tuple(sorted(p)) for p in (P, Q, R)}) < 3: continue
            (x1, y1), (x2, y2), (x3, y3) = P, Q, R
            if (x2 - x1) * (y3 - y1) != (y2 - y1) * (x3 - x1): continue
            a, b = y2 - y1, x1 - x2; g = gcd(a, b); a, b = a // g, b // g
            if a < 0 or (a == 0 and b < 0): a, b = -a, -b
            L.add((a, b, a * x1 + b * y1))
        data.append((n, int(k), sorted(L)))
pickle.dump(data, open(S + "/lines_data.pkl", "wb"))
def vp(m, p):
    m = abs(m); v = 0
    while m and m % p == 0: m //= p; v += 1
    return v
print(f"{len(data):,} numbers with k >= 3")
print(f"{'p':>3} {'p|n: N':>8} {'with line':>9} {'p∤n: with line':>15} | lines with p|n: share with p dividing  a      b     b-a    a+b     E      c")
for p in [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53]:
    A = [d for d in data if d[0] % p == 0]; B = [d for d in data if d[0] % p]
    la = sum(1 for d in A if d[2]) / max(1, len(A)); lb = sum(1 for d in B if d[2]) / len(B)
    lines = [(a, b, c) for n, k, Ls in A for a, b, c in Ls]
    if lines:
        sh = [sum(1 for a, b, c in lines if f(a, b, c) % p == 0) / len(lines) for f in
              (lambda a, b, c: a, lambda a, b, c: b, lambda a, b, c: b - a, lambda a, b, c: a + b, lambda a, b, c: a*a + a*b + b*b, lambda a, b, c: c)]
        tail = "  ".join(f"{100*x:5.1f}" for x in sh)
    else: tail = "(no lines)"
    print(f"{p:>3} {len(A):>8,} {100*la:>8.1f}% {100*lb:>14.1f}% | {len(lines):>7,} lines: {tail}")
