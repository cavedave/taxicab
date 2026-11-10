#!/usr/bin/env python3
"""triangle_values.py -- on the bowtie curve (3,4)+(9,52), at actual rational points (primitive (s, r), integer w):
does gcd(Den, Nx, Ny) divide M * G(s, r), G = 8251 r^2 + 11059 r s + 13867 s^2 (the shared factor's norm), for a fixed M?
Den = x_B y_B - x_C y_C, Nx = x_C^2 y_B - x_B^2 y_C, Ny = x_B y_C^2 - x_C y_B^2 (Theorem 8a), raw coordinates scaled by 2A."""
import sys, itertools, collections, math
from fractions import Fraction as Fr
from math import gcd, isqrt
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
if hasattr(sys, "set_int_max_str_digits"): sys.set_int_max_str_digits(0)
import bowtie_decide as BD
from bowtie_mine import Curve
from bowtie_hunt import curves_from_catalogue
from bowtie_components2 import seed_of
key = (3, 4, 0, 9, 52); C = Curve(*key); a2, b2 = 9, 52; A = b2**3 - a2**3
slopes = next(c[5] for c in curves_from_catalogue() if tuple(c[:5]) == key)
seed = seed_of(C, slopes, 300); head, x0 = BD.setup(C, seed, [])
box = [c + (0,) for c in itertools.product(range(-2, 3), repeat=5) if any(c)]
xs = BD.gp(BD.pts_src(head, x0, box))
ratio = collections.Counter(); M = 1; rows = 0; dprime = []
for l in xs.splitlines():
    if not l.startswith("PT "): continue
    x = Fr(l.split()[2]); s, r = x.denominator, x.numerator
    R = C.raw(s, r); X0, Y0 = R[0]
    Bt = 3 * (X0 * b2 * b2 + Y0 * a2 * a2); Ct = 3 * (X0 * X0 * b2 - Y0 * Y0 * a2); D = Bt * Bt - 4 * A * Ct
    w = isqrt(D)
    if w * w != D: continue
    Xc, Yc = 2 * A * X0 + (-Bt + w) * b2, 2 * A * Y0 - (-Bt + w) * a2
    G = 8251 * r * r + 11059 * r * s + 13867 * s * s
    for j in (1, 2):
        Xb, Yb = 2 * A * R[j][0], 2 * A * R[j][1]
        Den = Xb * Yb - Xc * Yc; Nx = Xc * Xc * Yb - Xb * Xb * Yc; Ny = Xb * Yc * Yc - Xc * Yb * Yb
        g = gcd(gcd(Den, Nx), Ny)
        if Den == 0: ratio['degenerate (Den = 0)'] += 1; continue
        h = g // gcd(g, G)          # the part of the gcd NOT explained by G(s, r)
        M = math.lcm(M, h); rows += 1
        dprime.append(abs(Den) // g)
print(f"{rows} (point, B) cases ({dict(ratio)}); lcm of gcd(Den, Nx, Ny) / gcd(., G(s, r)): M = {M}")
f = {}; m = M; p = 2
while m > 1 and p < 10**6:
    while m % p == 0: f[p] = f.get(p, 0) + 1; m //= p
    p += 1
print("   factorisation of M:", f, "(remaining cofactor", m, ")")
print(f"reduced denominator |Den| / gcd: min {min(dprime)}, digits median {sorted(len(str(d)) for d in dprime)[len(dprime) // 2]}; equal to 1 in {sum(d == 1 for d in dprime)} cases")
