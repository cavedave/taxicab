#!/usr/bin/env python3
"""count_all.py -- exact coprime representation counts for every n in a file (one n per line, or n;... rows), streamed.
Uses collisions.all_reps (PARI factorisation + divisor test), about 0.1 ms per n on 8 processes.

Writes n;k;x:y,... for every n with k >= --kmin to --out, and the histogram of k to stdout.
Usage: python3 count_all.py ns.txt --out multi.txt [--kmin 4] [--procs 8] [--gp gp]
"""
import argparse, gzip, time
from collections import Counter
from multiprocessing import Pool
from collisions import all_reps, factor_batch

def _count(job):
    part, gp = job
    return [(n, all_reps(n, f)) for n, f in zip(part, factor_batch(part, gp))]

def batches(fn, size):
    part = []
    for l in (gzip.open(fn, "rt") if fn.endswith(".gz") else open(fn)):
        part.append(int(l.split(";", 1)[0]))
        if len(part) == size: yield part; part = []
    if part: yield part

def main():
    ap = argparse.ArgumentParser(); ap.add_argument("ns"); ap.add_argument("--out", required=True)
    ap.add_argument("--kmin", type=int, default=4); ap.add_argument("--procs", type=int, default=8)
    ap.add_argument("--gp", default="gp")
    A = ap.parse_args(); t0 = time.time(); hist = Counter(); done = 0
    with open(A.out, "w") as g, Pool(A.procs) as pool:
        for res in pool.imap_unordered(_count, ((p, A.gp) for p in batches(A.ns, 2000))):
            for n, r in res:
                hist[len(r)] += 1
                if len(r) >= A.kmin: g.write(f"{n};{len(r)};" + ",".join(f"{x}:{y}" for x, y in sorted(r)) + "\n"); g.flush()
            done += len(res)
            if done % 500000 < 2000: print(f"  {done} counted [{time.time()-t0:.0f}s] {dict(sorted(hist.items()))}", flush=True)
    print(f"{done} n in {time.time()-t0:.0f}s: {dict(sorted(hist.items()))}")

if __name__ == "__main__":
    main()
