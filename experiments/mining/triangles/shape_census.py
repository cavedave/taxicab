#!/usr/bin/env python3
"""shape_census.py -- incidence shapes of every known coprime four-way and five-way (lines of three representations),
and the 'two disjoint lines' near-misses: five-ways = one line + two free points F, G; the chord FG (either orientation
of G) would be a second, disjoint line if its third point were integral -- its denominator is the distance."""
import sys, math, collections
sys.path.insert(0, '.'); sys.path.insert(0, 'triangles')
if hasattr(sys, "set_int_max_str_digits"): sys.set_int_max_str_digits(0)
from bowtie_mine import lines_of
from near_miss import third
def tau(P, p): x, y = P; return 1 if x % p == 0 else (-1 if y % p == 0 else 0)
shape = collections.Counter(); near = []; seen = set()
for fn, kmin in [('../../results/a047697_catalogue.txt', 4), ('../../results/five_ways_all.txt', 5)]:
    pass
    for l in open(fn):
        if not l[0].isdigit(): continue
        g = l.split(';'); n = int(g[0])
        if n in seen: continue
        seen.add(n)
        reps = [tuple(map(int, p.split(':'))) for p in g[2].split(',')]
        k = len(reps)
        if k < kmin: continue
        ls = lines_of(reps); sets = [{tuple(sorted(p)) for p in T} for d, T in ls]
        cov = set().union(*sets) if sets else set()
        free = [r for r in reps if tuple(sorted(r)) not in cov]
        if len(ls) == 0: s = f'{k} free points (no line)'
        elif len(ls) == 1: s = f'1 line + {len(free)} free'
        elif len(ls) == 2 and len(sets[0] & sets[1]) == 1: s = f'bowtie (2 lines sharing a point) + {len(free)} free'
        elif len(ls) == 2: s = f'2 disjoint lines + {len(free)} free'
        else: s = f'{len(ls)} lines + {len(free)} free'
        shape[(k, s)] += 1
        if k == 5 and len(ls) == 1 and len(free) == 2:
            F, G = free; types = n % 2 == 1 and n % 9 in (1, 8); best = None
            for GG in (G, (G[1], G[0])):
                R = third(F, GG, n)
                if R is None: continue
                ok = not types or (tau(F, 2) == tau(GG, 2) and tau(F, 3) == tau(GG, 3))
                d = math.lcm(R[0].denominator, R[1].denominator)
                if ok and (best is None or d < best): best = d
            near.append((best, n))
print('shapes of the known coprime k-ways:')
for (k, s), c in sorted(shape.items()): print(f'  k = {k}: {s:45s} {c:6d}')
near = [x for x in near if x[0] is not None]; near.sort()
print(f'\n"two disjoint lines" near-misses: {len(near)} five-ways = 1 line + 2 free points; best denominators of the chord F-G')
for d, n in near[:10]: print(f'  d = {d:<10d} n = {n} ({len(str(n))} digits), log d / log n = {math.log(d) / math.log(n):.3f}')
