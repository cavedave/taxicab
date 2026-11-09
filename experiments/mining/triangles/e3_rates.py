#!/usr/bin/env python3
"""e3_rates.py -- rate of E | n among chords, by kind, after the same filters as F70 (orientation by types, ab > 0, 4 | ab)."""
import sys, math, collections
sys.path.insert(0, '.'); sys.path.insert(0, 'triangles')
if hasattr(sys, "set_int_max_str_digits"): sys.set_int_max_str_digits(0)
from near_miss import analyse
from bowtie_mine import lines_of
def tau(P, p): x, y = P; return 1 if x % p == 0 else (-1 if y % p == 0 else 0)
C = collections.Counter()
for fn, kmin, tag in [('../../results/a047697_catalogue.txt', 4, 'four-way'), ('../../results/five_ways_all.txt', 5, 'five-way')]:
    for l in open(fn):
        if not l[0].isdigit(): continue
        g = l.split(';'); n = int(g[0]); reps = [tuple(map(int, p.split(':'))) for p in g[2].split(',')]
        if len(reps) != kmin: continue
        ls = lines_of(reps); online = [{tuple(sorted(p)) for p in T} for d, T in ls]
        types = n % 2 == 1 and n % 9 in (1, 8)
        for dR, X, Y, P, Q in analyse(n, reps)[1]:
            rp, rq = tuple(sorted(P)), tuple(sorted(Q))
            if tag == 'five-way' and len(ls) >= 2:
                kind = 'five-way, cross chord of a bowtie' if any(rp in L and rq not in L for L in online) and any(rq in L and rp not in L for L in online) else 'five-way, other chord'
            elif tag == 'four-way':
                kind = 'four-way, ' + ('one line' if len(ls) == 1 else 'no line' if not ls else '2+ lines')
            else: kind = tag + ', other'
            a, b = Q[1] - P[1], P[0] - Q[0]; gg = math.gcd(a, b); a, b = a // gg, b // gg
            C[(kind, 'all')] += 1
            if types and (tau(P, 2) != tau(Q, 2) or tau(P, 3) != tau(Q, 3)): continue
            if a * b <= 0 or (a * b) % 4: continue
            C[(kind, 'filtered')] += 1
            if n % (a*a + a*b + b*b) == 0: C[(kind, 'E | n')] += 1
kinds = sorted({k for k, _ in C})
print(f"{'kind':38s} {'chords':>9s} {'after F70 filters':>18s} {'E | n':>7s} {'rate':>7s}")
for k in kinds:
    f = C[(k, 'filtered')]; e = C[(k, 'E | n')]
    print(f"{k:38s} {C[(k, 'all')]:9d} {f:18d} {e:7d} {e / f if f else 0:7.2%}")
