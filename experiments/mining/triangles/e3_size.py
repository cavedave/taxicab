#!/usr/bin/env python3
"""e3_size.py -- is 'no E_3 | n on bowtie cross chords' a size effect? Rate of E | n among filtered four-way chords as a
function of r = log E / log n, then the expected number for bowtie cross chords from their own r-distribution."""
import sys, math, collections
sys.path.insert(0, '.'); sys.path.insert(0, 'triangles')
if hasattr(sys, "set_int_max_str_digits"): sys.set_int_max_str_digits(0)
from near_miss import analyse
from bowtie_mine import lines_of
def tau(P, p): x, y = P; return 1 if x % p == 0 else (-1 if y % p == 0 else 0)
B = 20
four = collections.defaultdict(lambda: [0, 0]); cross = collections.Counter(); cross_n = []
for fn, kmin, tag in [('../../results/a047697_catalogue.txt', 4, 'four'), ('../../results/five_ways_all.txt', 5, 'five')]:
    for l in open(fn):
        if not l[0].isdigit(): continue
        g = l.split(';'); n = int(g[0]); reps = [tuple(map(int, p.split(':'))) for p in g[2].split(',')]
        if len(reps) != kmin: continue
        ls = lines_of(reps); online = [{tuple(sorted(p)) for p in T} for d, T in ls]
        types = n % 2 == 1 and n % 9 in (1, 8)
        for dR, X, Y, P, Q in analyse(n, reps)[1]:
            if types and (tau(P, 2) != tau(Q, 2) or tau(P, 3) != tau(Q, 3)): continue
            a, b = Q[1] - P[1], P[0] - Q[0]; gg = math.gcd(a, b); a, b = a // gg, b // gg
            if a * b <= 0 or (a * b) % 4: continue
            E = a*a + a*b + b*b; r = math.log(E) / math.log(n); bk = min(int(r * B), B - 1)
            if tag == 'four':
                four[bk][0] += 1; four[bk][1] += n % E == 0
            else:
                rp, rq = tuple(sorted(P)), tuple(sorted(Q))
                if len(ls) >= 2 and any(rp in L and rq not in L for L in online) and any(rq in L and rp not in L for L in online):
                    cross[bk] += 1
print(f"{'r = log E / log n':18s} {'four-way chords':>15s} {'E | n':>7s} {'rate':>8s} {'bowtie cross':>13s}")
exp = 0.0
for bk in range(B):
    f, e = four[bk]; c = cross[bk]
    if f or c:
        rate = e / f if f else float('nan')
        print(f"{bk / B:.2f}-{(bk + 1) / B:.2f}         {f:15d} {e:7d} {rate:8.3%} {c:13d}")
        if f: exp += c * e / f
print(f"expected E | n among bowtie cross chords at the four-way rate of their size band: {exp:.1f} (observed 0)")
