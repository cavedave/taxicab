#!/usr/bin/env python3
"""e3_step0.py -- circularity check for F70: is there any chord (two known coprime points, not on a known line)
with E | n (E = a^2 + ab + b^2 of the chord's direction)? If E | n always forced an integral third point, F70 would
only restate 'no third line'. Also: for known LINES, confirm E | n (Theorem 2) as a control."""
import sys, math, collections
sys.path.insert(0, '.'); sys.path.insert(0, 'triangles')
if hasattr(sys, "set_int_max_str_digits"): sys.set_int_max_str_digits(0)
from near_miss import analyse
from bowtie_mine import lines_of
C = collections.Counter(); ex = []
for fn, kmin in [('../../results/a047697_catalogue.txt', 4), ('../../results/five_ways_all.txt', 5)]:
    seen = set()
    for l in open(fn):
        if not l[0].isdigit(): continue
        g = l.split(';'); n = int(g[0])
        if n in seen: continue
        seen.add(n)
        reps = [tuple(map(int, p.split(':'))) for p in g[2].split(',')]
        if len(reps) < kmin: continue
        for d, T in lines_of(reps):
            a, b = d; C['lines'] += 1; C['lines with E | n'] += n % (a*a + a*b + b*b) == 0
        for dR, X, Y, P, Q in analyse(n, reps)[1]:
            a, b = Q[1] - P[1], P[0] - Q[0]; gg = math.gcd(a, b); a, b = a // gg, b // gg
            E = a*a + a*b + b*b
            C['chords (not lines)'] += 1
            if E <= n: C['chords with E <= n'] += 1
            if n % E == 0:
                C['chords with E | n'] += 1
                if len(ex) < 8: ex.append((len(str(n)), (a, b), E, dR))
for k in ['lines', 'lines with E | n', 'chords (not lines)', 'chords with E <= n', 'chords with E | n']: print(f'{k:22s} {C[k]:9d}')
print('examples (digits of n, direction, E, denominator of third point):', ex)
