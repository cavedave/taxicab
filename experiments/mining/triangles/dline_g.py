#!/usr/bin/env python3
"""dline_g.py -- what makes a chord between two representations of n cheap? The chord direction is (dx, dy)/g with
g = gcd(dx, dy); cheap means g ~ size of the points. Factor g and attribute its primes."""
import sys, math, collections, statistics
sys.path.insert(0, '.')
if hasattr(sys, "set_int_max_str_digits"): sys.set_int_max_str_digits(0)
from bowtie_mine import lines_of
def fac(m):
    m = abs(m); f = {}; p = 2
    while p * p <= m and p < 10**6:
        while m % p == 0: f[p] = f.get(p, 0) + 1; m //= p
        p += 1 if p == 2 else 2
    if m > 1: f[m] = f.get(m, 0) + 1
    return f
C = collections.Counter(); share = collections.defaultdict(list); ex = []
for l in open('../../results/a047697_catalogue.txt'):
    if not l[0].isdigit(): continue
    g_ = l.split(';'); n = int(g_[0]); reps = [tuple(map(int, p.split(':'))) for p in g_[2].split(',')]
    if len(reps) != 4 or lines_of(reps) or len(g_[0]) > 26: continue
    best = None
    for i, P in enumerate(reps):
        for Q0 in reps[i + 1:]:
            for Q in (Q0, (Q0[1], Q0[0])):
                dx, dy = Q[0] - P[0], Q[1] - P[1]; g = math.gcd(dx, dy); a, b = dy // g, -dx // g
                c = abs(b**3 - a**3)
                if best is None or c < best[0]: best = (c, P, Q, g, (a, b))
    c, P, Q, g, (a, b) = best
    sP, sQ = P[0] + P[1], Q[0] + Q[1]; lg = math.log(g) if g > 1 else 0
    parts = collections.Counter()
    for p, e in fac(g).items():
        w = e * math.log(p)
        if n % p == 0: parts['prime of n, split' if p % 3 == 1 else 'prime of n, not split'] += w
        elif (sP - sQ) % p == 0: parts['divides s_P - s_Q only'] += w
        else: parts['unrelated to n'] += w
    for k in ('prime of n, split', 'prime of n, not split', 'divides s_P - s_Q only', 'unrelated to n'):
        share[k].append(parts[k] / lg if lg else 0)
    C['numbers'] += 1
    if len(ex) < 6: ex.append((len(str(n)), (a, b), g, dict(fac(g)), n % 9))
print(C['numbers'], "no-line four-ways (<= 26 digits); for the cheapest chord, share of log g from:")
for k, v in share.items(): print(f"  {k:28s} mean {statistics.mean(v):.3f}  median {statistics.median(v):.3f}")
print("examples (digits, direction, g, factorisation of g):")
for e in ex: print("  ", e)
