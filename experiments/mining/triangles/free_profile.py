#!/usr/bin/env python3
"""free_profile.py -- how do the free representations of one-line numbers differ from the line's points?"""
import sys, math, collections, statistics
from multiprocessing import Pool
sys.path.insert(0, '.')
if hasattr(sys, "set_int_max_str_digits"): sys.set_int_max_str_digits(0)
from collisions import all_reps, factor_batch
from bowtie_mine import lines_of
def tau(P, p): x, y = P; return 1 if x % p == 0 else (-1 if y % p == 0 else 0)
def mu(P): a, b = tau(P, 2), tau(P, 3); return a * b if a and b else 0
def blocks_in(s, fac): return sum(1 for p, e in fac if p % 3 == 1 and s % p == 0)
def work(part):
    out = []
    for n, f in zip(part, factor_batch(part, "gp")):
        reps = sorted(all_reps(n, f)); ls = lines_of(reps)
        if len(ls) != 1: continue
        on = {tuple(sorted(p)) for p in ls[0][1]}; free = [r for r in reps if tuple(sorted(r)) not in on]
        if not free: continue
        c = n ** (1 / 3); kb = sum(1 for p, e in f if p % 3 == 1)
        for tag, group in (('line', [r for r in reps if tuple(sorted(r)) in on]), ('free', free)):
            for x, y in group:
                s = x + y
                out.append((tag, s / c, x > 0 and y > 0, mu((x, y)) == mu(ls[0][1][0]) if mu((x, y)) and mu(ls[0][1][0]) else None,
                            blocks_in(s, f) / kb if kb else 0, max(abs(x), abs(y)) / c))
    return out
if __name__ == "__main__":
    ns = sorted({int(l.split(';')[0]) for l in open(sys.argv[1]) if l[0].isdigit()})
    parts = [ns[i:i + 500] for i in range(0, len(ns), 500)]; rows = []
    with Pool(6) as P:
        for r in P.imap_unordered(work, parts): rows += r
    for tag in ('line', 'free'):
        R = [r for r in rows if r[0] == tag]
        q = lambda v: (statistics.median(v), sorted(v)[len(v) // 10], sorted(v)[9 * len(v) // 10])
        sv = q([r[1] for r in R]); mv = q([r[5] for r in R]); bv = q([r[4] for r in R])
        same = [r[3] for r in R if r[3] is not None]
        print(f"{tag:4s}: {len(R):4d} points | s / n^(1/3): median {sv[0]:.3f} (10%-90% {sv[1]:.3f}-{sv[2]:.3f}) | "
              f"max|coord| / n^(1/3): median {mv[0]:.2f} (90% {mv[2]:.2f}) | both positive {sum(r[2] for r in R) / len(R):.1%} | "
              f"split blocks in s: median {bv[0]:.2f} of n's | same class as line {sum(same) / len(same) if same else float('nan'):.1%} (of {len(same)})")
