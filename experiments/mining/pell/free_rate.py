#!/usr/bin/env python3
"""free_rate.py -- empirical rate of a free extra representation per number with a line, by decade, to 1e36.
Numerator: lf36 (certified; every n <= 1e36 with a line in the 23 cheapest directions counted exactly; k >= 4 listed):
numbers whose representations form exactly one line + free points. Denominator: numbers with such a line,
N(X) = N0 (X / 1e21)^(1/3) (517,976 at 1e21; 51,828 at 1e18; consistent with lf36's 5.18e10 triples at 1e36).
Then fit rate ~ C n^(-alpha) and apply it to the five-ways (bowtie + free point)."""
import sys, math, collections
sys.path.insert(0, '.')
if hasattr(sys, "set_int_max_str_digits"): sys.set_int_max_str_digits(0)
from bowtie_mine import lines_of
N0 = 517976
def Nx(X): return N0 * (X / 1e21) ** (1 / 3)
num = collections.Counter(); free_by_k = collections.Counter()
for l in open('night_7of9/results_lf_1e36/lf_k4.txt'):
    if not l[0].isdigit(): continue
    f = l.strip().split(';'); n = int(f[0]); reps = [tuple(map(int, p.split(':'))) for p in f[2].split(',')]
    ls = lines_of(reps)
    if len(ls) == 1: num[len(f[0]) - 1] += 1      # decade index d: 10^d <= n < 10^(d+1)
rows = []
print(" decade   numbers with a line   one line + free    rate")
for d in range(9, 36):
    den = Nx(10.0 ** (d + 1)) - Nx(10.0 ** d); r = num[d] / den
    rows.append((d + 0.5, r, num[d], den)); print(f"  1e{d:<2d}   {den:16,.0f}   {num[d]:10d}   {r:9.2e}")
# least squares on log10 rate vs log10 n, for decades with >= 20 events
pts = [(x, math.log10(r)) for x, r, k, den in rows if k >= 20]
m = len(pts); sx = sum(x for x, y in pts); sy = sum(y for x, y in pts); sxx = sum(x * x for x, y in pts); sxy = sum(x * y for x, y in pts)
alpha = -(m * sxy - sx * sy) / (m * sxx - sx * sx); c = (sy + alpha * sx) / m
print(f"fit (decades with >= 20 events, {m} points): rate ~ 10^{c:.2f} * n^-{alpha:.3f}")
# apply to the five-ways: expected free sixth representations, extrapolating the fit
tot = 0.0; by = collections.Counter()
for l in open('../../results/five_ways_all.txt'):
    if not l[0].isdigit(): continue
    n = int(l.split(';')[0]); lg = math.log10(n); e = 10 ** (c - alpha * lg)
    tot += e; by[min(int(lg) // 25 * 25, 300)] += e
print(f"applied to the 2,645 five-ways (one free extra representation beyond the bowtie, per number, from the line rate): expected {tot:.3g}")
for k in sorted(by): print(f"   {k}-{k + 24} digits: {by[k]:.3g}")
