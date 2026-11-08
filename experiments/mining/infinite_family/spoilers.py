#!/usr/bin/env python3
"""spoilers.py -- for points m*Q (Q = small combinations of the generators, P0 = origin) that fail to be bowties,
which primes spoil them? Step 1 of the proof plan says: only primes of E1, b - a, E2, b2 - a2."""
import sys, itertools, collections
from fractions import Fraction as Fr
from math import gcd, isqrt
sys.path.insert(0, str(__import__('pathlib').Path(__file__).resolve().parent))
sys.path.insert(0, str(__import__('pathlib').Path(__file__).resolve().parent.parent))
if hasattr(sys, "set_int_max_str_digits"): sys.set_int_max_str_digits(0)
import bowtie_decide as BD
from bowtie_mine import Curve
from bowtie_hunt import curves_from_catalogue
from bowtie_components2 import seed_of
from coset_test import points

def small_primes(m, lim=10**5):
    out = set(); p = 2
    m = abs(m)
    while p < lim and m > 1:
        if m % p == 0:
            out.add(p)
            while m % p == 0: m //= p
        p += 1 if p == 2 else 2
    return out, m

def why_primes(C, s, r):
    """the primes responsible for the failure (G = common factor of the raw triple; second-line denominators; gcds)"""
    R = C.raw(s, r); G = 0
    for x, y in R: G = gcd(G, gcd(x, y))
    pts = [(x // G, y // G) for x, y in R]
    bad = set()
    for p, q in pts: bad |= small_primes(gcd(p, q))[0]
    x, y = pts[C.i]; vx, vy = C.b2, -C.a2
    A = vx**3 + vy**3; Bq = 3 * (x * vx * vx + y * vy * vy); Cq = 3 * (x * x * vx + y * y * vy); D = Bq * Bq - 4 * A * Cq
    w = isqrt(D)
    for e in (1, -1):
        t = Fr(-Bq + e * w, 2 * A); X, Y = x + t * vx, y + t * vy
        den = X.denominator * Y.denominator
        bad |= {("den", p) for p in small_primes(den)[0]}
        if den == 1: bad |= {("gcd2", p) for p in small_primes(gcd(int(X), int(Y)))[0]}
    return bad

key = tuple(map(int, sys.argv[1:6])); ms = list(map(int, sys.argv[6].split(",")))
C = Curve(*key); slopes = next((c[5] for c in curves_from_catalogue() if tuple(c[:5]) == key), [])
seed = seed_of(C, slopes, 300); a, b, i, a2, b2 = key
rel = sorted(BD.pf(a*a + a*b + b*b) | BD.pf(b - a) | BD.pf(a2*a2 + a2*b2 + b2*b2) | BD.pf(b2 - a2))
head, x0 = BD.setup(C, seed, rel)
info = BD.gp(head + ['print("RANK ", R[1], " ", R[2], " ", #G, " ", ord);']); r = int(info.split()[3])
ntor = len([v for v in info.split("[")[1].rstrip("]\n ").split(",") if v.strip()]) - r
print("relevant primes", rel)
for m in ms:
    small = [list(c) + [0] * ntor for c in itertools.product(range(-1, 2), repeat=r) if any(c)]
    xs = points(head, x0, [[m * v for v in c] for c in small])
    tally = collections.Counter()
    for x in xs:
        o, w = C.bowtie(x.denominator, x.numerator)
        if o: continue
        for p in why_primes(C, x.denominator, x.numerator): tally[p] += 1
    print(f"m = {m}: spoiling primes {dict(tally)}")
