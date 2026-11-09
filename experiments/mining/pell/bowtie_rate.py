#!/usr/bin/env python3
"""bowtie_rate.py -- bowtie (five-way with two lines sharing a point) rate per number with a line, by decade, from lf36
(certified to 1e36, 23 cheapest directions); denominator N(X) = 517,976 (X / 1e21)^(1/3) as in free_rate.py."""
import sys, math, collections
sys.path.insert(0, '.')
if hasattr(sys, "set_int_max_str_digits"): sys.set_int_max_str_digits(0)
from bowtie_mine import lines_of
def Nx(X): return 517976 * (X / 1e21) ** (1 / 3)
bt = collections.Counter()
for l in open('night_7of9/results_lf_1e36/lf_k4.txt'):
    if not l[0].isdigit(): continue
    f = l.strip().split(';'); reps = [tuple(map(int, p.split(':'))) for p in f[2].split(',')]
    ls = lines_of(reps)
    if len(ls) >= 2:
        S = [{tuple(sorted(p)) for p in T} for d, T in ls]
        if len(S[0] & S[1]) == 1: bt[len(f[0]) - 1] += 1
rows = []; cum = 0
print(" decade   bowties   rate per number with a line   cumulative bowties")
for d in range(9, 36):
    den = Nx(10.0 ** (d + 1)) - Nx(10.0 ** d); cum += bt[d]
    rows.append((d + 0.5, bt[d] / den if bt[d] else None, bt[d])); print(f"  1e{d:<2d}   {bt[d]:6d}   {bt[d] / den:12.2e}   {cum:8d}")
pts = [(x, math.log10(r)) for x, r, k in rows if r and k >= 3]
m = len(pts); sx = sum(x for x, y in pts); sy = sum(y for x, y in pts); sxx = sum(x * x for x, y in pts); sxy = sum(x * y for x, y in pts)
beta = -(m * sxy - sx * sy) / (m * sxx - sx * sx); c = (sy + beta * sx) / m
print(f"fit over {m} decades with >= 3 bowties: bowtie rate ~ 10^{c:.2f} n^-{beta:.3f};  bowties <= X grow like X^(1/3 - beta) = X^{1/3 - beta:.3f}")
cx = [(math.log10(10.0 ** (d + 1)), sum(bt[e] for e in range(9, d + 1))) for d in range(20, 36)]
a = (math.log10(cx[-1][1]) - math.log10(cx[0][1])) / (cx[-1][0] - cx[0][0])
print(f"direct: cumulative bowties from 1e21 to 1e36 grow like X^{a:.3f}")
