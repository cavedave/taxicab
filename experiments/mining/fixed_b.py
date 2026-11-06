#!/usr/bin/env python3
"""fixed_b.py -- run the line enumerator on the family of directions (a, B) for one fixed B (all allowed a < B),
to test whether directions sharing a coefficient pair up into bowties more often than chance."""
import sys, time
from math import gcd
from multiprocessing import Pool
from line_enum import allowed, conic_points, triples

def run(job):
    a, b, P0, H, nmax = job
    return (a, b), triples(a, b, P0, H, nmax)

if __name__ == "__main__":
    B, H, nmax, out = int(sys.argv[1]), int(sys.argv[2]), int(float(sys.argv[3])), sys.argv[4]
    dirs = [(a, B) for a in range(1, B) if gcd(a, B) == 1 and allowed(a, B)]
    P = conic_points(dirs, "/opt/homebrew/bin/gp")
    t0 = time.time(); tot = 0
    with open(out, "w") as f, Pool(6) as pool:
        for (a, b), T in pool.imap_unordered(run, [(a, b, p, H, nmax) for (a, b), p in zip(dirs, P)]):
            for n, c, pts in T: f.write(f"{n};{a};{b};{c};" + ",".join(f"{x}:{y}" for x, y in pts) + "\n")
            tot += len(T)
    print(f"B={B}: {len(dirs)} directions, {tot} triples, {time.time()-t0:.0f}s -> {out}")
