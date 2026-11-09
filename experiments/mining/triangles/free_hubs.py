#!/usr/bin/env python3
"""free_hubs.py -- are the 'free' fourth representations of one-line numbers (calibrate_free.py) tied to the line by a
hub (two chords through different pairs of points meeting at the same rational point)?"""
import sys, math, collections
from multiprocessing import Pool
sys.path.insert(0, '.'); sys.path.insert(0, 'triangles')
if hasattr(sys, "set_int_max_str_digits"): sys.set_int_max_str_digits(0)
from collisions import all_reps, factor_batch
from bowtie_mine import lines_of
from near_miss import third
def work(part):
    out = []
    for n, f in zip(part, factor_batch(part, "gp")):
        reps = sorted(all_reps(n, f)); ls = lines_of(reps)
        if len(ls) != 1: continue
        on = {tuple(sorted(p)) for p in ls[0][1]}; free = [r for r in reps if tuple(sorted(r)) not in on]
        if not free: continue
        pts = sorted({p for x, y in reps for p in ((x, y), (y, x))})
        thirds = collections.defaultdict(set)
        for i in range(len(pts)):
            for j in range(i + 1, len(pts)):
                P, Q = pts[i], pts[j]
                if Q == (P[1], P[0]): continue
                R = third(P, Q, n)
                if R is None or (R[0].denominator == 1 and R[1].denominator == 1): continue
                key = tuple(sorted((R[0], R[1])))
                thirds[key].add(frozenset({tuple(sorted(P)), tuple(sorted(Q))}))
        Fr = {tuple(sorted(r)) for r in free}
        hub_with_free = any(len(v) > 1 and any(Fr & set(pr) for pr in v) for v in thirds.values())
        out.append((n, len(free), hub_with_free))
    return out
if __name__ == "__main__":
    ns = sorted({int(l.split(';')[0]) for l in open(sys.argv[1]) if l[0].isdigit()})
    parts = [ns[i:i + 500] for i in range(0, len(ns), 500)]; rows = []
    with Pool(6) as P:
        for r in P.imap_unordered(work, parts): rows += r
    c = collections.Counter(h for n, k, h in rows)
    print(f"one-line numbers with a free representation: {len(rows)}; free point in a hub: {c[True]}; not: {c[False]}")
