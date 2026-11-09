#!/usr/bin/env python3
"""e3_structure.py -- (1) bowtie cross chords: E_3 g^2 = N(t2 beta2 - t1 beta1) (beta = b - a w, t_i = (s_S - s_X)/(a_i - b_i));
does E_3's part outside n share primes with t1 t2 (the s-differences)? (2) hubs: is a chord with E | n one whose third point
R is also the third point of another chord of the same n?"""
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
def Nn(a, b): return a*a - a*b + b*b
C = collections.Counter()
# (1) bowtie cross chords
for l in open('../../results/five_ways_all.txt'):
    if not l[0].isdigit(): continue
    g = l.split(';'); n = int(g[0]); reps = [tuple(map(int, p.split(':'))) for p in g[2].split(',')]
    ls = lines_of(reps)
    if len(ls) < 2: continue
    (d1, T1), (d2, T2) = ls[0], ls[1]
    pts1 = set(T1); pts2 = set(T2)
    Sset = {tuple(sorted(p)) for p in T1} & {tuple(sorted(p)) for p in T2}
    if len(Sset) != 1: continue
    types = n % 2 == 1 and n % 9 in (1, 8)
    for P in T1:
        if tuple(sorted(P)) in Sset: continue
        S1 = next(p for p in T1 if tuple(sorted(p)) in Sset)
        for Q in T2:
            if tuple(sorted(Q)) in Sset: continue
            S2 = next(p for p in T2 if tuple(sorted(p)) in Sset)
            for QQ, SS2 in ((Q, S2), ((Q[1], Q[0]), (S2[1], S2[0]))):
                if SS2 != S1: continue                      # use the orientation where both lines pass through the same point S
                if types and (tau(P, 2) != tau(QQ, 2) or tau(P, 3) != tau(QQ, 3)): C['(1) cross, wrong orientation'] += 1; continue
                d, e = QQ[0] - P[0], QQ[1] - P[1]; gg = math.gcd(d, e)
                E3 = Nn(d, e) // (gg * gg)
                if E3 * gg * gg != Nn(d, e): C['(1) norm check failed'] += 1
                t1 = (S1[0] + S1[1]) - (P[0] + P[1]); t2 = (S1[0] + S1[1]) - (QQ[0] + QQ[1])
                Eo = strip(E3, n)
                C['(1) cross chords (S-orientation, types ok)'] += 1
                C['(1) outside part shares a prime with s_S - s_P or s_S - s_Q'] += math.gcd(Eo, t1 * t2) > 1
                C['(1) outside part coprime to both s-differences'] += math.gcd(Eo, t1 * t2) == 1
# (2) hubs among four-way chords
for l in open('../../results/a047697_catalogue.txt'):
    if not l[0].isdigit(): continue
    g = l.split(';'); n = int(g[0]); reps = [tuple(map(int, p.split(':'))) for p in g[2].split(',')]
    if len(reps) != 4: continue
    ch = analyse(n, reps)[1]
    thirds = collections.Counter((X, Y, dR) for dR, X, Y, P, Q in ch)
    for dR, X, Y, P, Q in ch:
        a, b = Q[1] - P[1], P[0] - Q[0]; gg = math.gcd(a, b); a, b = a // gg, b // gg
        if a * b <= 0 or (a * b) % 4: continue
        hub = thirds[(X, Y, dR)] > 1 or thirds[(Y, X, dR)] > 0
        en = n % (a*a + a*b + b*b) == 0
        C[f'(2) four-way chord, E|n={en}, hub={hub}'] += 1
for k in sorted(C): print(f'{k:62s} {C[k]}')
