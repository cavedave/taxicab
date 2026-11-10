#!/usr/bin/env python3
"""branch_check.py -- genus of the configuration curve with fixed directions: m square conditions w_i^2 = Delta_{d_i}(x, y)
over P^1 give genus 1 + 2^(m-1)(m - 2) if the 2m branch points are distinct. Delta_d's bracket form
q_d = (b(4a^3 - b^3), 6a^2 b^2, a(4b^3 - a^3)); two forms share a root iff their resultant is 0."""
import sys, math, collections
sys.path.insert(0, '.')
if hasattr(sys, "set_int_max_str_digits"): sys.set_int_max_str_digits(0)
from bowtie_mine import lines_of
def q(a, b): return (b * (4 * a**3 - b**3), 6 * a * a * b * b, a * (4 * b**3 - a**3))
def res(f, g):
    (A1, B1, C1), (A2, B2, C2) = f, g
    return (A1 * C2 - A2 * C1)**2 - (A1 * B2 - A2 * B1) * (B1 * C2 - B2 * C1)
def direction(P, Q):
    dx, dy = Q[0] - P[0], Q[1] - P[1]; g = math.gcd(dx, dy); return dy // g, -dx // g
def ok(dirs):
    fs = [q(a, b) for a, b in dirs]
    if any(f[1]**2 - 4 * f[0] * f[2] == 0 for f in fs): return 'repeated root'
    if any(res(fs[i], fs[j]) == 0 for i in range(len(fs)) for j in range(i + 1, len(fs))): return 'shared branch point'
    return 'distinct'
C = collections.Counter()
for fn, kmin in [('../../results/a047697_catalogue.txt', 4), ('../../results/five_ways_all.txt', 5)]:
    for l in open(fn):
        if not l[0].isdigit(): continue
        g = l.split(';'); n = int(g[0]); reps = [tuple(map(int, p.split(':'))) for p in g[2].split(',')]
        if len(reps) != kmin: continue
        ls = lines_of(reps)
        if kmin == 5 and len(ls) >= 2:
            C[('bowtie, 2 line directions (m = 2)', ok([ls[0][0], ls[1][0]]))] += 1
        elif kmin == 4 and len(ls) == 1:
            T = ls[0][1]; on = {tuple(sorted(p)) for p in T}; F = [r for r in reps if tuple(sorted(r)) not in on][0]
            d3 = min((direction(T[0], Q) for Q in (F, (F[1], F[0]))), key=lambda d: abs(d[1]**3 - d[0]**3))
            C[('line + free, line + chord (m = 2)', ok([ls[0][0], d3]))] += 1
        elif kmin == 4 and not ls:
            best = None
            for P0 in reps:
                for P in (P0, (P0[1], P0[0])):
                    ds = [min((direction(P, Q) for Q in (Q0, (Q0[1], Q0[0]))), key=lambda d: abs(d[1]**3 - d[0]**3)) for Q0 in reps if Q0 != P0]
                    w = max(abs(b**3 - a**3) for a, b in ds)
                    if best is None or w < best[0]: best = (w, ds)
            C[('no-line star, 3 chords (m = 3)', ok(best[1]))] += 1
for k in sorted(C): print(k, C[k])
