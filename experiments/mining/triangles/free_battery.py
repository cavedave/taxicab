#!/usr/bin/env python3
"""free_battery.py -- experimental checks on the 'free' representations (not on any line of three) of known k-ways:
A proven rules, B order, C shared factors, D nearly on a line, E exact multiplicative relations among s-values."""
import sys, math, collections, statistics
sys.path.insert(0, '.'); sys.path.insert(0, 'triangles')
if hasattr(sys, "set_int_max_str_digits"): sys.set_int_max_str_digits(0)
from bowtie_mine import lines_of
from near_miss import third
def fac(m):
    m = abs(m); f = {}; p = 2
    while p * p <= m and p < 2 * 10**6:
        while m % p == 0: f[p] = f.get(p, 0) + 1; m //= p
        p += 1 if p == 2 else 2
    if m > 1: f[m] = f.get(m, 0) + 1
    return f
def nonsplit(m): return math.prod(p**e for p, e in fac(m).items() if p % 3 != 1)
def v(p, m):
    k = 0
    while m and m % p == 0: m //= p; k += 1
    return k
def tau(P, p): x, y = P; return 1 if x % p == 0 else (-1 if y % p == 0 else 0)
C = collections.Counter(); rankS = collections.Counter(); rankX = collections.Counter(); gF = []; gL = []; dF = []; dCtl = []
for l in open('../../results/a047697_catalogue.txt'):
    if not l[0].isdigit(): continue
    g = l.split(';'); n = int(g[0]); reps = [tuple(map(int, p.split(':'))) for p in g[2].split(',')]
    if len(reps) not in (4, 5): continue
    ls = lines_of(reps); on = set()
    for d, T in ls: on |= {tuple(sorted(p)) for p in T}
    free = [r for r in reps if tuple(sorted(r)) not in on]
    if not ls:                                   # control: four-ways with no line -- best chord denominator of any pair
        if len(reps) == 4:
            best = min(math.lcm(*(c.denominator for c in third(P, Q, n))) for i, P in enumerate(reps) for Q in reps[i + 1:] for Q in (Q, (Q[1], Q[0])) if third(P, Q, n))
            dCtl.append(math.log(best) / math.log(n))
        continue
    if len(ls) != 1 or not free: continue
    T = ls[0][1]; sL = [x + y for x, y in T]
    for F in free:
        C['free points'] += 1; sF = F[0] + F[1]
        # A. proven rules
        C['A1 nonsplit(s_F) = nonsplit(s_line)'] += nonsplit(sF) == nonsplit(sL[0])
        C['A2 x y mod 3 equal (Lemma 6)'] += (F[0] * F[1]) % 3 == (T[0][0] * T[0][1]) % 3
        C['A3 exactly one even coordinate'] += (F[0] % 2 == 0) != (F[1] % 2 == 0)
        ok14 = True
        for P in T:
            for Q in (F, (F[1], F[0])):
                a, b = Q[1] - P[1], P[0] - Q[0]; gg = math.gcd(a, b); a, b = a // gg, b // gg
                for p, e in fac(nonsplit(sF)).items():
                    need = e + (1 if p == 2 else 0) - (1 if p == 3 else 0)
                    if v(p, b - a) < min(need, e): ok14 = False
        C['A4 Theorem 14 on chords F-P'] += ok14
        # B. order among the four s-values and sizes
        allS = sorted(sL + [sF]); rankS[allS.index(sF) + 1] += 1
        sz = sorted([max(abs(x), abs(y)) for x, y in T] + [max(abs(F[0]), abs(F[1]))]); rankX[sz.index(max(abs(F[0]), abs(F[1]))) + 1] += 1
        # C. shared factors: log gcd(s_F, s_P) vs log gcd(s_P, s_Q), normalised by log n
        ln = math.log(n)
        gF.append(statistics.mean(math.log(math.gcd(sF, s)) for s in sL) / ln)
        gL.append(statistics.mean(math.log(math.gcd(sL[i], sL[j])) for i in range(3) for j in range(i + 1, 3)) / ln)
        # D. nearly on a line: best chord F - P (either orientation of F) third-point denominator
        best = min(math.lcm(*(c.denominator for c in third(P, Q, n))) for P in T for Q in (F, (F[1], F[0])) if third(P, Q, n))
        dF.append(math.log(best) / ln)
        # E. exact multiplicative relations
        rel = any(abs(sF * sL[i]) == abs(sL[j] * sL[k]) for i in range(3) for j in range(3) for k in range(3) if len({i, j, k}) == 3)
        C['E1 s_F s_Pi = +- s_Pj s_Pk'] += rel
        C['E2 s_F divides s_P1 s_P2 s_P3'] += math.prod(sL) % sF == 0
for k in sorted(C): print(f'{k:40s} {C[k]}')
N = C['free points']
print('B rank of s_F among the four s-values (1 = smallest):', {k: f'{v / N:.1%}' for k, v in sorted(rankS.items())})
print('B rank of F by largest coordinate (1 = smallest):  ', {k: f'{v / N:.1%}' for k, v in sorted(rankX.items())})
print(f'C mean log gcd(s_F, s_line) / log n: median {statistics.median(gF):.4f};  line points among themselves: {statistics.median(gL):.4f}')
print(f'D best chord denominator from F, log d / log n: median {statistics.median(dF):.3f}, 10% {sorted(dF)[len(dF) // 10]:.3f}, min {min(dF):.3f}')
print(f'  control (four-ways with no line, best chord between any two): median {statistics.median(dCtl):.3f}, 10% {sorted(dCtl)[len(dCtl) // 10]:.3f}, min {min(dCtl):.3f} ({len(dCtl)} numbers)')
