#!/usr/bin/env python3
"""gen_fourways.py -- step 3 of the shape route: generate 'line + free' four-ways from a genus-1 curve. On the bowtie
curve (3,4)+(9,52), a rational point gives a base triple and a second line through the shared point; if exactly one of
the second line's two points is a coprime integer point, the configuration is base line + one free point."""
import sys, itertools, collections, subprocess, math
from fractions import Fraction as Fr
from math import gcd, isqrt
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
if hasattr(sys, "set_int_max_str_digits"): sys.set_int_max_str_digits(0)
import bowtie_decide as BD
from bowtie_mine import Curve, lines_of
from bowtie_hunt import curves_from_catalogue
from bowtie_components2 import seed_of
from collisions import all_reps, factor_batch

def classify(C, s, r):
    if s < 0: s, r = -s, -r
    if gcd(s, r) != 1: return None
    R = C.raw(s, r); G = 0
    for x, y in R: G = gcd(G, gcd(x, y))
    if G == 0: return None
    pts = [(x // G, y // G) for x, y in R]
    if any(p == 0 or q == 0 or gcd(p, q) != 1 for p, q in pts): return 'base not coprime', pts, []
    x, y = pts[C.i]; vx, vy = C.b2, -C.a2
    A = vx**3 + vy**3; Bq = 3 * (x * vx * vx + y * vy * vy); Cq = 3 * (x * x * vx + y * y * vy); D = Bq * Bq - 4 * A * Cq
    w = isqrt(D)
    if w * w != D: return None
    good = []
    for e in (1, -1):
        t = Fr(-Bq + e * w, 2 * A); X, Y = x + t * vx, y + t * vy
        if X.denominator == 1 and Y.denominator == 1 and X != 0 and Y != 0 and gcd(int(X), int(Y)) == 1: good.append((int(X), int(Y)))
    return {2: 'bowtie (five-way)', 1: 'line + free (four-way?)', 0: 'base line only'}[len(good)], pts, good

key = (3, 4, 0, 9, 52); C = Curve(*key)
slopes = next(c[5] for c in curves_from_catalogue() if tuple(c[:5]) == key)
seed = seed_of(C, slopes, 300); head, x0 = BD.setup(C, seed, [])
box = [c + (0,) for c in itertools.product(range(-2, 3), repeat=5) if any(c)]
xs = BD.gp(BD.pts_src(head, x0, box))
cnt = collections.Counter(); cand = []
for l in xs.splitlines():
    if not l.startswith("PT "): continue
    x = Fr(l.split()[2]); res = classify(C, x.denominator, x.numerator)
    if res is None: cnt['not integral base'] += 1; continue
    kind, pts, good = res; cnt[kind] += 1
    if kind.startswith('line + free'):
        n = pts[0][0]**3 + pts[0][1]**3
        cand.append((abs(n), pts, good))
print(dict(cnt))
cand = sorted({c[0]: c for c in cand}.values())
small = [c for c in cand if len(str(c[0])) <= 45]
print(f"distinct 'line + free' candidates: {len(cand)}; <= 45 digits (exact count): {len(small)}")
ks = collections.Counter(); ex = []
for (n, pts, good), f in zip(small, factor_batch([c[0] for c in small], "gp")):
    reps = sorted(all_reps(n, f)); ks[len(reps)] += 1
    if len(ex) < 4: ex.append((len(str(n)), len(reps), [len(l[1]) for l in lines_of(reps)]))
print("exact representation counts of the small candidates:", dict(sorted(ks.items())), "| examples (digits, k, line sizes):", ex)

# larger candidates: exact count via count_bowties.job (factor from the s-values and E's), up to 120 digits
import count_bowties as CB
from multiprocessing import Pool
mid = [c for c in cand if 45 < len(str(c[0])) <= 120]
jobs = [(n, [tuple(p) for p in pts] + good, 'gen', 300, 300, 'gp') for n, pts, good in mid]
ks2 = collections.Counter(); unk = 0
if __name__ == '__main__':
    with Pool(6) as P:
        for n, reps, five, k, dt, why in P.imap_unordered(CB.job, jobs):
            if reps is None: unk += 1
            else: ks2[len(reps)] += 1
    print(f"candidates of 46-120 digits: {len(mid)}; exact counts {dict(sorted(ks2.items()))}; unfinished {unk}")
