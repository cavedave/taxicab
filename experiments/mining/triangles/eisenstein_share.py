#!/usr/bin/env python3
"""eisenstein_share.py -- E_3 = N(pi_Q - pi_P) / g^2 with pi = x + y w in Z[w] (n = s * N(pi)). Hypothesis: E | n needs
pi_P, pi_Q to share most of their prime ideals; bowtie cross pairs share little. share = log N(gcd) / log N(pi)."""
import sys, math, collections
sys.path.insert(0, '.'); sys.path.insert(0, 'triangles')
if hasattr(sys, "set_int_max_str_digits"): sys.set_int_max_str_digits(0)
from near_miss import analyse
from bowtie_mine import lines_of

# Eisenstein integers a + b w, w^2 = -1 - w; N = a^2 - ab + b^2
def mul(z, w): a, b = z; c, d = w; return (a*c - b*d, a*d + b*c - b*d)
def conj(z): a, b = z; return (a - b, -b)
def N(z): a, b = z; return a*a - a*b + b*b
def rdiv(p, q):                           # nearest integer to p/q
    return (2*p + q) // (2*q)
def divmod_e(z, w):
    num = mul(z, conj(w)); n = N(w)
    qt = (rdiv(num[0], n), rdiv(num[1], n))
    r = (z[0] - mul(qt, w)[0], z[1] - mul(qt, w)[1])
    return qt, r
def egcd(z, w):
    while w != (0, 0):
        _, r = divmod_e(z, w); z, w = w, r
    return z
def tau(P, p): x, y = P; return 1 if x % p == 0 else (-1 if y % p == 0 else 0)

C = collections.defaultdict(list)
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
            piP, piQ = (P[0], P[1]), (Q[0], Q[1])
            rho = egcd(piP, piQ); share = math.log(N(rho)) / math.log(min(N(piP), N(piQ))) if N(rho) > 1 else 0.0
            rp, rq = tuple(sorted(P)), tuple(sorted(Q))
            if tag == 'five' and len(ls) >= 2 and any(rp in L and rq not in L for L in online) and any(rq in L and rp not in L for L in online):
                kind = 'bowtie cross chord'
            elif tag == 'four':
                kind = 'four-way chord, E | n' if n % (a*a + a*b + b*b) == 0 else 'four-way chord, E does not divide n'
            else: continue
            C[kind].append(share)
    print('done', fn, flush=True)
for k, v in C.items():
    v.sort(); q = lambda f: v[int(f * (len(v) - 1))]
    print(f'{k:38s} {len(v):7d} chords; share of Eisenstein gcd: min {v[0]:.3f}  10% {q(.1):.3f}  median {q(.5):.3f}  90% {q(.9):.3f}  max {v[-1]:.3f}')
