#!/usr/bin/env python3
"""cheap_search.py -- for every n carrying a collinear triple on a cheap direction (line_enum.py output),
keep n with at least --rmin distinct split primes (p = 1 mod 3) below --pmax (local-density filter, F1:
every known five-way has 4-8 such primes below 200), factor the survivors (PARI) and count ALL coprime
representations exactly (collisions.all_reps). Reports every n with >= --kmin representations.
Counting runs in --procs parallel processes (one PARI per process), in sorted chunks of 20,000.

Usage: python3 cheap_search.py lines.txt --rmin 4 --pmax 200 --kmin 5 [--procs 6] [--start N]
"""
import argparse, time
from multiprocessing import Pool
from collisions import all_reps, factor_batch

GP = "gp"
def _init(gp):
    global GP
    GP = gp

def _count(part):
    return part, [all_reps(n, fac) for n, fac in zip(part, factor_batch(part, GP))]

def main():
    ap = argparse.ArgumentParser(); ap.add_argument("lines")
    ap.add_argument("--rmin", type=int, default=4); ap.add_argument("--pmax", type=int, default=200)
    ap.add_argument("--kmin", type=int, default=5); ap.add_argument("--gp", default="gp")
    ap.add_argument("--procs", type=int, default=6)
    ap.add_argument("--save", type=int, default=4, help="write every n with >= SAVE reps (with its reps) to --out")
    ap.add_argument("--out", help="file for n;k;x:y,... lines (k >= --save)")
    ap.add_argument("--start", type=int, default=0, help="resume: skip the first START filtered n (sorted order)")
    a = ap.parse_args()
    SP = [p for p in range(7, a.pmax) if p % 3 == 1 and all(p % q for q in range(2, int(p**0.5) + 1))]
    t0 = time.time(); ns = set(); tot = 0
    for l in open(a.lines):
        n = int(l.split(";", 1)[0]); tot += 1
        if sum(1 for p in SP if n % p == 0) >= a.rmin: ns.add(n)
    ns = sorted(ns)
    print(f"{tot} triples; {len(ns)} distinct n pass the filter (>= {a.rmin} split primes < {a.pmax}) [{time.time()-t0:.0f}s]", flush=True)
    if a.start: print(f"resuming at {a.start}", flush=True)
    hist = {}; done = a.start
    chunks = [ns[i:i + 20000] for i in range(a.start, len(ns), 20000)]
    fo = open(a.out, "a") if a.out else None
    with Pool(a.procs, initializer=_init, initargs=(a.gp,)) as pool:
        for part, repss in pool.imap(_count, chunks):        # imap keeps sorted order, so --start stays valid
            for n, reps in zip(part, repss):
                k = len(reps); hist[k] = hist.get(k, 0) + 1
                if fo and k >= a.save:
                    fo.write(f"{n};{k};" + ",".join(f"{x}:{y}" for x, y in sorted(reps)) + "\n"); fo.flush()
                if k >= a.kmin: print(f"  *** n = {n} ({len(str(n))} digits): {k} coprime representations", flush=True)
            done += len(part)
            print(f"  [{time.time()-t0:.0f}s] {done}/{len(ns)} counted; reps histogram {dict(sorted(hist.items()))}", flush=True)

if __name__ == "__main__":
    main()
