#!/usr/bin/env python3
"""pell_orbit.py -- F82: pairs of equal sums along a direction. For P, Q = P + lam (b, -a) with x_P^3 + y_P^3 = x_Q^3 + y_Q^3,
the midpoint M = (P + Q)/2 satisfies b Mx^2 - a My^2 = -lam^2 (b^3 - a^3) / 12, i.e. with U = 2b Mx, V = 2 My:
U^2 - ab V^2 = -lam^2 b (b^3 - a^3) / 3. Units of Z[sqrt(ab)] act; a power of the fundamental unit that is the
identity mod 4b keeps integrality, so one pair gives an infinite orbit of equal-sum pairs (same direction, same lam)."""
import sys, math, collections
from math import gcd, isqrt
sys.path.insert(0, '.')
if hasattr(sys, "set_int_max_str_digits"): sys.set_int_max_str_digits(0)
from bowtie_mine import lines_of

def fund_unit(D):
    """smallest (t, u), t^2 - D u^2 = 1, u > 0 (continued fractions)"""
    a0 = isqrt(D); m, d, a = 0, 1, a0; p0, p1, q0, q1 = 1, a0, 0, 1
    while p1 * p1 - D * q1 * q1 != 1:
        m = d * a - m; d = (D - m * m) // d; a = (a0 + m) // d
        p0, p1 = p1, a * p1 + p0; q0, q1 = q1, a * q1 + q0
    return p1, q1

def orbit_step(D, mod):
    """a power (T, W) of the fundamental unit congruent to the identity mod `mod` (T = 1, W = 0 mod mod)"""
    t, u = fund_unit(D); T, W = t, u
    for k in range(1, 10**6):
        if T % mod == 1 and W % mod == 0: return T, W, k
        T, W = T * t + D * W * u, T * u + W * t
    raise ValueError

pairs = []
for l in open('../../results/a047697_catalogue.txt'):
    if not l[0].isdigit(): continue
    g = l.split(';'); n = int(g[0]); reps = [tuple(map(int, p.split(':'))) for p in g[2].split(',')]
    if n > 25 * 10**22: continue
    for i, P in enumerate(reps):
        for Q0 in reps[i + 1:]:
            for Q in (Q0, (Q0[1], Q0[0])):
                dx, dy = Q[0] - P[0], Q[1] - P[1]; gg = gcd(dx, dy); a, b = dy // gg, -dx // gg
                if a < 0 or (a == 0 and b < 0): a, b = -a, -b
                lam = dx // b if b else dy // (-a)
                if (P[0] + lam * b, P[1] - lam * a) != Q: continue
                if a * b > 0 and abs(b**3 - a**3) <= 10**6: pairs.append((n, P, Q, a, b, lam))
print(len(pairs), "cheap chords (cost <= 1e6, ab > 0) between representations of exhaustive k-ways")
C = collections.Counter(); cat = {int(l.split(';')[0]) for l in open('../../results/a047697_catalogue.txt') if l[0].isdigit()}
hits = []
for n, P, Q, a, b, lam in pairs:
    Mx2, My2 = P[0] + Q[0], P[1] + Q[1]                   # 2 M
    lhs = b * Mx2 * Mx2 - a * My2 * My2; rhs = -lam * lam * (b**3 - a**3) // 3
    C['midpoint hyperbola holds'] += 3 * lhs == -lam * lam * (b**3 - a**3)
    D = a * b
    if isqrt(D)**2 == D: C['ab a square (no unit group)'] += 1; continue
    T, W, k = orbit_step(D, 2 * b)
    U, V = b * Mx2, My2                                    # U = 2b Mx, V = 2 My
    ok = True
    for j in range(1, 4):                                  # three orbit steps
        U, V = T * U + D * W * V, W * U + T * V
        if (U - lam * b * b) % (2 * b) or (V + lam * a) % 2: ok = False; C['orbit point not integral'] += 1; break
        x, y = (U - lam * b * b) // (2 * b), (V + lam * a) // 2
        P2, Q2 = (x, y), (x + lam * b, y - lam * a)
        n1, n2 = P2[0]**3 + P2[1]**3, Q2[0]**3 + Q2[1]**3
        if n1 != n2: ok = False; C['orbit pair NOT equal sums'] += 1; break
        C['orbit pairs: equal sums'] += 1
        C['orbit pairs: both coprime'] += gcd(*P2) == 1 and gcd(*Q2) == 1
        if abs(n1) in cat: hits.append((j, len(str(abs(n1)))))
print(dict(C))
print("orbit numbers that are themselves catalogue k-ways (k >= 4):", len(hits), hits[:10])
