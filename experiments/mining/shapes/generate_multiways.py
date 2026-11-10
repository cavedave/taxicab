#!/usr/bin/env python3
"""generate_multiways.py -- generate certified four- and five-ways from every known bowtie curve and measure the CPU cost.
For each curve (direction pair + shared point, from all bowties in results/five_ways_all.txt), take the points
sum c_k G_k with |c_1| + ... + |c_r| <= LMAX (G_k generators of the elliptic curve, origin a known bowtie). Each point gives a
base triple and a second line; second line with 2 coprime integral points = bowtie (k >= 5, all five checked); with 1 =
line + free point (k >= 4, four checked). No counting needed: the representations are verified directly."""
import sys, itertools, collections, time, resource, math
from fractions import Fraction as Fr
from math import gcd, isqrt
from multiprocessing import Pool
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
if hasattr(sys, "set_int_max_str_digits"): sys.set_int_max_str_digits(0)
import bowtie_decide as BD
import line_enum as L
from bowtie_mine import Curve, lines_of
from line_complete import Direction, setup_canon, canon_slope
from bowtie_components2 import seed_of
ROOT = Path(__file__).resolve().parents[3]; LMAX = 3

def curves_from_file(fn):
    pairs = {}
    for l in open(fn):
        if not l[0].isdigit(): continue
        f = l.strip().split(";"); reps = [tuple(map(int, p.split(":"))) for p in f[2].split(",")]
        ls = lines_of(reps)
        if len(ls) < 2: continue
        (d1, T1), (d2, T2) = sorted(ls[:2], key=lambda t: abs(t[0][1]**3 - t[0][0]**3))
        inter = set(T1) & set(T2)
        if not inter: T2 = tuple((y, x) for x, y in T2); d2 = (d2[1], d2[0]); inter = set(T1) & set(T2)
        if not inter: continue
        if d1[0] > d1[1]:
            T1 = tuple((y, x) for x, y in T1); T2 = tuple((y, x) for x, y in T2); d1 = (d1[1], d1[0]); d2 = (d2[1], d2[0])
            inter = set(T1) & set(T2)
        pairs.setdefault((d1, d2), []).append((T1, next(iter(inter))))
    out = []
    for ((a, b), (a2, b2)), bts in sorted(pairs.items()):
        if a <= 0 or b <= 0 or a == b: continue
        try: P0 = L.conic_points([(a, b)])[0]
        except Exception: continue
        d = Direction(a, b, P0, 10**60); setup_canon(d, P0); byi = {}
        for T1, cs in bts:
            h, s, r = canon_slope(d, list(T1))
            R = d.raw(s, r); G = 0
            for x, y in R: G = gcd(G, gcd(x, y))
            red = [(x // G, y // G) for x, y in R]
            idx = [k for k, p in enumerate(red) if p == cs or (-p[0], -p[1]) == cs]
            if idx: byi.setdefault(idx[0], []).append((s, r))
        for i, sl in byi.items(): out.append(((a, b, i, a2, b2), sl[:3]))
    return out

def classify(C, s, r):
    if s < 0: s, r = -s, -r
    if gcd(s, r) != 1: return None
    R = C.raw(s, r); G = 0
    for x, y in R: G = gcd(G, gcd(x, y))
    if G == 0: return None
    pts = [(x // G, y // G) for x, y in R]
    if any(p == 0 or q == 0 or gcd(p, q) != 1 for p, q in pts): return None
    x, y = pts[C.i]; vx, vy = C.b2, -C.a2
    A = vx**3 + vy**3; Bq = 3 * (x * vx * vx + y * vy * vy); Cq = 3 * (x * x * vx + y * y * vy); D = Bq * Bq - 4 * A * Cq
    w = isqrt(D)
    if D < 0 or w * w != D: return None
    good = []
    for e in (1, -1):
        t = Fr(-Bq + e * w, 2 * A); X, Y = x + t * vx, y + t * vy
        if X.denominator == 1 and Y.denominator == 1 and X != 0 and Y != 0 and gcd(int(X), int(Y)) == 1: good.append((int(X), int(Y)))
    allp = pts + good
    if len({tuple(sorted(p)) for p in allp}) < len(allp): return None
    n = allp[0][0]**3 + allp[0][1]**3
    if n < 0: allp = [(-p, -q) for p, q in allp]; n = -n
    assert all(p**3 + q**3 == n for p, q in allp)
    return len(good), n, allp

def _cpu():
    a = resource.getrusage(resource.RUSAGE_SELF); b = resource.getrusage(resource.RUSAGE_CHILDREN)
    return a.ru_utime + a.ru_stime + b.ru_utime + b.ru_stime

def work(item):
    key, slopes = item; c0 = _cpu()
    try:
        C = Curve(*key); seed = seed_of(C, slopes, 300)
        if seed is None: return key, [], [], 'no seed', _cpu() - c0
        head, x0 = BD.setup(C, seed, [])
        info = BD.gp(head + ['print("RANK ", #G, " ", #Gt);'])
        r, ng = [int(v) for v in info.split("RANK")[1].split()[:2]]
        if r == 0: return key, [], [], 'rank 0', _cpu() - c0
        combos = [c + (0,) * (ng - r) for c in itertools.product(range(-LMAX, LMAX + 1), repeat=r) if 0 < sum(map(abs, c)) <= LMAX]
        xs = BD.gp(BD.pts_src(head, x0, combos))
        five, four = {}, {}
        for l in xs.splitlines():
            if not l.startswith("PT "): continue
            x = Fr(l.split()[2]); res = classify(C, x.denominator, x.numerator)
            if res is None: continue
            k, n, allp = res
            if k == 2: five[n] = allp
            elif k == 1: four[n] = allp
        return key, list(five.items()), list(four.items()), f'rank {r}, {len(combos)} points', _cpu() - c0
    except Exception as e:
        return key, [], [], f'error {e!r}'[:80], _cpu() - c0

if __name__ == "__main__":
    import json
    BD.GPTIME = 600
    curves = curves_from_file(ROOT / 'results/five_ways_all.txt')
    print(len(curves), "bowtie curves", flush=True)
    LOG = Path(__file__).resolve().parent / 'generated.jsonl'          # one line per curve: resumable
    done = set()
    if LOG.exists():
        for l in open(LOG): done.add(tuple(json.loads(l)['key']))
    todo = [c for c in curves if tuple(c[0]) not in done]
    print(len(done), "done,", len(todo), "to do", flush=True)
    t0 = time.time()
    with Pool(6) as P, open(LOG, 'a') as out:
        for i, (key, f5, f4, note, cpu) in enumerate(P.imap_unordered(work, todo, chunksize=1)):
            out.write(json.dumps({'key': list(key), 'note': note, 'cpu': cpu,
                                  'five': [[str(n), p] for n, p in f5], 'four': [[str(n), p] for n, p in f4]}) + '\n'); out.flush()
            if i % 20 == 0: print(f"{i + 1}/{len(todo)} curves, {time.time() - t0:.0f} s", flush=True)
    print("wall", round(time.time() - t0), "s")
