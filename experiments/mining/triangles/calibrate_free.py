#!/usr/bin/env python3
"""calibrate_free.py -- calibrate F78's lambda. Every n <= B carrying a line in the 23 cheapest directions (line_fast
--triples): count all coprime representations exactly; for numbers with exactly one line, observed = number of free
representations (off the line), predicted = lambda(n) = sum over Theorem 5 candidates s outside the line's three of
[m = (4n/s - s^2)/3 positive integer] / (4 sqrt m). Compare totals, by size band and by split-prime count."""
import sys, math, collections, time
from multiprocessing import Pool
sys.path.insert(0, '.')
if hasattr(sys, "set_int_max_str_digits"): sys.set_int_max_str_digits(0)
from collisions import all_reps, factor_batch
from bowtie_mine import lines_of
from bowtie_hunt import icbrt

def lam_of(n, fac, exclude):
    f = 1; blocks = []
    for p, e in fac:
        if p % 3 == 1: blocks.append(p**e)
        elif p == 3: f *= 3**(e - 1)
        else: f *= p**e
    S = icbrt(4 * n); lam = 0.0; stack = [(f, 0)]; blocks.sort()
    if f > S: return 0.0, len(blocks)
    while stack:
        s, i = stack.pop()
        for j in range(i, len(blocks)):
            c = s * blocks[j]
            if c > S: break
            stack.append((c, j + 1))
        if s in exclude: continue
        t = 4 * (n // s) - s * s
        if t <= 0 or t % 3: continue
        lam += 1 / (4 * math.sqrt(t // 3))
    return lam, len(blocks)

def work(part):
    out = []
    for n, f in zip(part, factor_batch(part, "gp")):
        reps = sorted(all_reps(n, f)); ls = lines_of(reps)
        if len(ls) != 1: out.append((n, len(reps), len(ls), None, None, None)); continue
        line = {abs(x + y) for x, y in ls[0][1]}; on = {tuple(sorted(p)) for p in ls[0][1]}
        free = sum(1 for r in reps if tuple(sorted(r)) not in on)
        lam, k = lam_of(n, f, line)
        out.append((n, len(reps), 1, free, lam, k))
    return out

if __name__ == "__main__":
    fn = sys.argv[1]
    ns = sorted({int(l.split(';')[0]) for l in open(fn) if l[0].isdigit()})
    print(len(ns), "distinct n with a line", flush=True); t0 = time.time()
    parts = [ns[i:i + 500] for i in range(0, len(ns), 500)]; rows = []
    with Pool(6) as P:
        for r in P.imap_unordered(work, parts): rows += r
    one = [r for r in rows if r[2] == 1]
    print(f"{time.time() - t0:.0f} s; numbers with exactly one line: {len(one)}; with 2+ lines: {sum(r[2] >= 2 for r in rows)}")
    obs = sum(r[3] for r in one); pred = sum(r[4] for r in one); withfree = sum(r[3] > 0 for r in one)
    print(f"ONE LINE: observed free representations {obs} (in {withfree} numbers); predicted sum lambda {pred:.2f}; ratio observed/predicted {obs / pred if pred else float('nan'):.2f}")
    by = collections.defaultdict(lambda: [0, 0.0, 0])
    for n, k, nl, fr, lam, kb in one:
        b = len(str(n)) // 3 * 3; by[b][0] += fr; by[b][1] += lam; by[b][2] += 1
    print("by digits of n: count, observed free, predicted, ratio")
    for b in sorted(by): o, p, c = by[b]; print(f"  {b:2d}-{b + 2:2d}: {c:7d} {o:6d} {p:9.2f} {o / p if p else float('nan'):7.2f}")
    bk = collections.defaultdict(lambda: [0, 0.0, 0])
    for n, k, nl, fr, lam, kb in one: bk[min(kb, 12)][0] += fr; bk[min(kb, 12)][1] += lam; bk[min(kb, 12)][2] += 1
    print("by number of split prime blocks: count, observed, predicted, ratio")
    for b in sorted(bk): o, p, c = bk[b]; print(f"  {b:2d}: {c:7d} {o:6d} {p:9.2f} {o / p if p else float('nan'):7.2f}")
