#!/usr/bin/env python3
"""e3_witness.py -- step 1 of E3_plan: for bowtie cross chords (after the F70 filters), where does E_3 fail to
divide n? E_3' = part of E_3 coprime to n (all primes of n removed); deficit primes p | n with v_p(E_3) > v_p(n)."""
import sys, math, collections
sys.path.insert(0, '.'); sys.path.insert(0, 'triangles')
if hasattr(sys, "set_int_max_str_digits"): sys.set_int_max_str_digits(0)
from near_miss import analyse
from bowtie_mine import lines_of
def tau(P, p): x, y = P; return 1 if x % p == 0 else (-1 if y % p == 0 else 0)
def strip(E, n):
    g = math.gcd(E, n)
    while g > 1:
        while E % g == 0: E //= g
        g = math.gcd(E, n)
    return E
SMALL = [p for p in range(2, 2000) if all(p % q for q in range(2, int(p**.5) + 1))]
C = collections.Counter(); smallw = collections.Counter(); per_curve = collections.defaultdict(collections.Counter)
for l in open('../../results/five_ways_all.txt'):
    if not l[0].isdigit(): continue
    g = l.split(';'); n = int(g[0]); reps = [tuple(map(int, p.split(':'))) for p in g[2].split(',')]
    ls = lines_of(reps)
    if len(ls) < 2: continue
    online = [{tuple(sorted(p)) for p in T} for d, T in ls]
    key = g[3].strip()[-20:]
    types = n % 2 == 1 and n % 9 in (1, 8)
    for dR, X, Y, P, Q in analyse(n, reps)[1]:
        rp, rq = tuple(sorted(P)), tuple(sorted(Q))
        if not (any(rp in L and rq not in L for L in online) and any(rq in L and rp not in L for L in online)): continue
        if types and (tau(P, 2) != tau(Q, 2) or tau(P, 3) != tau(Q, 3)): continue
        a, b = Q[1] - P[1], P[0] - Q[0]; gg = math.gcd(a, b); a, b = a // gg, b // gg
        if a * b <= 0 or (a * b) % 4: continue
        E = a*a + a*b + b*b; Eo = strip(E, n)
        C['cross chords'] += 1
        C['E_3 has a prime outside n'] += Eo > 1
        C['outside part shares a prime with D (third-point denominator)'] += Eo > 1 and math.gcd(Eo, dR) > 1
        C['outside part divides D'] += Eo > 1 and dR % Eo == 0
        C['D divides E_3'] += E % dR == 0
        deficit = [p for p in SMALL if E % p == 0 and n % p == 0 and (lambda e, f: e > f)(*[next(k for k in range(200) if v % p**(k + 1)) for v in (E, n)])]
        C['deficit at a prime of n (small primes)'] += bool(deficit)
        ws = [p for p in SMALL if Eo % p == 0]
        for p in ws: smallw[p] += 1
        C['some outside prime < 2000'] += bool(ws)
        per_curve[key]['chords'] += 1; per_curve[key]['has 7 or 13 or 19 outside'] += any(p in ws for p in (7, 13, 19))
for k, v in C.items(): print(f'{k:62s} {v}')
print('most common small outside primes:', smallw.most_common(12))
