#!/usr/bin/env python3
"""free_controls.py -- (1) order skew of free points vs controls (random Theorem-5 candidate s, uniform and weighted by
1/sqrt(m)); (2) the directions of chords from free points: allowed (Theorem 1)? cheap? recurring across numbers?"""
import sys, math, collections, random
from multiprocessing import Pool
sys.path.insert(0, '.')
if hasattr(sys, "set_int_max_str_digits"): sys.set_int_max_str_digits(0)
from collisions import factor_batch
from bowtie_mine import lines_of
from bowtie_hunt import icbrt
import line_enum as L

def cands(n, fac, cap=20000):
    f = 1; blocks = []
    for p, e in fac:
        if p % 3 == 1: blocks.append(p**e)
        elif p == 3: f *= 3**(e - 1)
        else: f *= p**e
    S = icbrt(4 * n); out = []; stack = [(f, 0)]; blocks.sort()
    if f > S: return out
    while stack and len(out) < cap:
        s, i = stack.pop()
        for j in range(i, len(blocks)):
            c = s * blocks[j]
            if c > S: break
            stack.append((c, j + 1))
        t = 4 * (n // s) - s * s
        if t > 0 and t % 3 == 0: out.append((s, 1 / math.sqrt(t // 3)))
    return out
def rank(sv, sL): return sorted(sL + [sv]).index(sv) + 1

def work(part):
    random.seed(part[0][0] % 1000003); res = []
    for (n, T, F), fac in zip(part, factor_batch([n for n, T, F in part], "gp")):
        sL = [x + y for x, y in T]; known = set(sL) | {F[0] + F[1]}
        cs = [(s, w) for s, w in cands(n, fac) if s not in known]
        if not cs: continue
        u = random.choice(cs)[0]
        tot = sum(w for s, w in cs); r = random.random() * tot; acc = 0
        for s, w in cs:
            acc += w
            if acc >= r: wt = s; break
        res.append((rank(F[0] + F[1], sL), rank(u, sL), rank(wt, sL)))
    return res

def norm_ok(a, b):
    if a * b <= 0 or (a * b) % 4: return False
    m = abs(a * b); p = 3
    while m % 2 == 0: m //= 2
    k = 0
    for p in range(3, 10**5, 2):
        if m % p == 0:
            e = 0
            while m % p == 0: m //= p; e += 1
            if p % 3 == 2 and e % 2: return False
        if p * p > m: break
    return m == 1 or m % 3 != 2      # leftover prime: allowed unless = 2 mod 3 (odd power)
if __name__ == "__main__":
    rows = []
    for l in open('../../results/a047697_catalogue.txt'):
        if not l[0].isdigit(): continue
        g = l.split(';'); n = int(g[0]); reps = [tuple(map(int, p.split(':'))) for p in g[2].split(',')]
        if len(reps) != 4: continue
        ls = lines_of(reps)
        if len(ls) != 1: continue
        on = {tuple(sorted(p)) for p in ls[0][1]}; F = [r for r in reps if tuple(sorted(r)) not in on][0]
        rows.append((n, list(ls[0][1]), F))
    # (1) order skew vs controls
    parts = [rows[i:i + 400] for i in range(0, len(rows), 400)]; R = []
    with Pool(6) as P:
        for r in P.imap_unordered(work, parts): R += r
    N = len(R)
    for k, name in ((0, 'free point'), (1, 'uniform candidate'), (2, '1/sqrt(m)-weighted candidate')):
        c = collections.Counter(r[k] for r in R)
        print(f"(1) {name:30s}: " + "  ".join(f"rank {i}: {c[i] / N:.1%}" for i in range(1, 5)) + f"   (N = {N})")
    # (2) directions of chords from F, vs chords line point -> swap of another line point
    dirF = collections.Counter(); dirC = collections.Counter(); C = collections.Counter()
    for n, T, F in rows:
        for kind, pairs in (('free', [(P, Q) for P in T for Q in (F, (F[1], F[0]))]),
                            ('ctrl', [(T[i], (T[j][1], T[j][0])) for i in range(3) for j in range(3) if i != j])):
            for P, Q in pairs:
                a, b = Q[1] - P[1], P[0] - Q[0]; g = math.gcd(a, b); a, b = a // g, b // g
                if a < 0 or (a == 0 and b < 0): a, b = -a, -b
                C[(kind, 'chords')] += 1; C[(kind, 'allowed')] += norm_ok(a, b) or norm_ok(b, a)
                cost = abs(b**3 - a**3); C[(kind, 'cost <= 1e6')] += cost <= 10**6
                (dirF if kind == 'free' else dirC)[(min(abs(a), abs(b)), max(abs(a), abs(b)), a * b > 0)] += 1
    for kind in ('free', 'ctrl'):
        t = C[(kind, 'chords')]
        print(f"(2) {kind}: {t} chords; allowed direction {C[(kind, 'allowed')] / t:.2%}; cost <= 1e6 {C[(kind, 'cost <= 1e6')] / t:.2%}")
    for name, D in (('free', dirF), ('ctrl', dirC)):
        rep = [(d, c) for d, c in D.most_common(6) if c > 1]
        print(f"    most repeated directions ({name}): {rep}; directions seen more than once: {sum(1 for c in D.values() if c > 1)} of {len(D)}")
