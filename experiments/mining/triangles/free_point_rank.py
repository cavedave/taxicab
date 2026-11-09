#!/usr/bin/env python3
"""free_point_rank.py -- idea 3: rank five-ways by the expected number of FREE extra representations
lambda(n) = sum over candidate s (Theorem 5: s = f * product of split blocks, s <= (4n)^(1/3), s not a known
representation's s) of [m = (4n/s - s^2)/3 a positive integer] / (4 sqrt(m)) -- density of squares near m, times 1/2 for
parity. Crude in absolute terms, fair as a ranking (it sees divisor richness and size)."""
import sys, math, time, collections
from multiprocessing import Pool
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
if hasattr(sys, "set_int_max_str_digits"): sys.set_int_max_str_digits(0)
from bowtie_hunt import factor_many, icbrt
from bowtie_mine import lines_of

def job(args):
    n, reps = args
    pieces = sorted({abs(x + y) for x, y in reps} | {a*a + a*b + b*b for (a, b), T in lines_of(reps)})
    facs = factor_many(pieces, "gp", 60)
    if None in facs: return n, None, "factor timeout"
    m, F = n, {}
    for p in sorted({p for fac in facs for p, e in fac}):
        while m % p == 0: m //= p; F[p] = F.get(p, 0) + 1
    if m > 1:
        rest = factor_many([m], "gp", 60)[0]
        if rest is None: return n, None, "leftover"
        for p, e in rest: F[p] = F.get(p, 0) + e
    f = 1; blocks = []
    for p, e in F.items():
        if p % 3 == 1: blocks.append(p**e)
        elif p == 3: f *= 3**(e - 1)
        else: f *= p**e
    S = icbrt(4 * n); known = {abs(x + y) for x, y in reps}
    lam = 0.0; cands = 0; deadline = time.time() + 30; stack = [(f, 0)]; blocks.sort(); steps = 0
    while stack:
        s, i = stack.pop()
        for j in range(i, len(blocks)):
            c = s * blocks[j]
            if c > S: break
            stack.append((c, j + 1))
        steps += 1
        if not steps & 0xFFFF and time.time() > deadline: return n, None, "candidate timeout"
        if s in known: continue
        t = 4 * (n // s) - s * s
        if t <= 0 or t % 3: continue
        cands += 1; lam += 1 / (4 * math.sqrt(t // 3))
    return n, (lam, cands, len(blocks)), ""

if __name__ == "__main__":
    rows = []
    for l in open('../../results/five_ways_all.txt'):
        if not l[0].isdigit(): continue
        g = l.split(';')
        if g[1] == '5' and len(g[0]) <= 150: rows.append((int(g[0]), [tuple(map(int, p.split(':'))) for p in g[2].split(',')]))
    out = []; fail = collections.Counter(); t0 = time.time()
    with Pool(6) as P:
        for n, res, why in P.imap_unordered(job, rows):
            if res is None: fail[why] += 1
            else: out.append((res[0], n, res[1], res[2]))
    out.sort(reverse=True)
    print(f"{len(out)} ranked, failures {dict(fail)}, {time.time() - t0:.0f} s")
    print(f"sum of lambda over all ranked five-ways (expected free sixth representations): {sum(o[0] for o in out):.3g}")
    print("top 12 (lambda; candidates s; split prime blocks; digits):")
    for lam, n, c, k in out[:12]: print(f"  {lam:.3e}  cands {c:7d}  blocks {k:3d}  {len(str(n)):4d} digits  n = {n if len(str(n)) < 40 else str(n)[:20] + '...'}")
    by = collections.defaultdict(list)
    for lam, n, c, k in out: by[len(str(n)) // 25 * 25].append(lam)
    for k in sorted(by): print(f"  digits {k}-{k + 24}: {len(by[k])} numbers, total lambda {sum(by[k]):.3g}, max {max(by[k]):.3g}")
    open(Path(__file__).resolve().parent / 'free_point_rank.txt', 'w').write("# lambda;candidates;split blocks;n\n" + "\n".join(f"{lam:.6e};{c};{k};{n}" for lam, n, c, k in out) + "\n")
