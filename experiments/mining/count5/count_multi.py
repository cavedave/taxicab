#!/usr/bin/env python3
"""count_multi.py -- exact counts for the uncounted four-ways (results/four_ways_generated.txt, '>=4') and five-ways
(results/five_ways_all.txt, '>=5'), using count_bowties.job: n is factored from the s = x + y of the known representations
and the E of every line among them (Theorem 13: one line suffices), then counted exactly (Theorem 5).
Easy first: short limits; numbers that time out go to OUT.unk for a later pass with longer limits.
Usage: python3 count5/count_multi.py --maxdig 150 --tlim 120 --tcount 120 --procs 6 --out count5/counted_multi_le150.txt"""
import argparse, sys, time
from multiprocessing import Pool
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
if hasattr(sys, "set_int_max_str_digits"): sys.set_int_max_str_digits(0)
from count_bowties import job
ROOT = Path(__file__).resolve().parents[3]

def read(fn, tag):
    for l in open(fn):
        f = l.rstrip("\n").split(";")
        if f[0].isdigit() and f[1] == tag:
            yield int(f[0]), [tuple(map(int, p.split(":"))) for p in f[2].split(",")], (f[3] if len(f) > 3 else "")

def main():
    ap = argparse.ArgumentParser(); ap.add_argument("--out", required=True); ap.add_argument("--maxdig", type=int, default=150)
    ap.add_argument("--mindig", type=int, default=0); ap.add_argument("--tlim", type=int, default=120)
    ap.add_argument("--tcount", type=int, default=120); ap.add_argument("--procs", type=int, default=6); ap.add_argument("--gp", default="gp")
    A = ap.parse_args(); t0 = time.time()
    todo = {}
    for fn, tag, kmin in ((ROOT / "results/five_ways_all.txt", ">=5", 5), (ROOT / "results/four_ways_generated.txt", ">=4", 4)):
        for n, reps, src in read(fn, tag):
            if A.mindig <= len(str(n)) <= A.maxdig: todo.setdefault(n, (reps, f"{kmin}|{src}"))
    jobs = [(n, reps, key, A.tlim, A.tcount, A.gp) for n, (reps, key) in sorted(todo.items())]
    print(f"{len(jobs)} numbers ({sum(k.startswith('5') for _, (r, k) in todo.items())} listed >=5, "
          f"{sum(k.startswith('4') for _, (r, k) in todo.items())} listed >=4), {A.mindig}-{A.maxdig} digits", flush=True)
    hist, unk, up = {}, 0, []
    with open(A.out, "w") as f, open(A.out + ".unk", "w") as fu, Pool(A.procs) as pool:
        f.write("# count_multi.py: n;k;x:y,...;listed k|source\n"); fu.write("# n;reason;listed k|source\n")
        for i, (n, reps, known, key, dt, why) in enumerate(pool.imap_unordered(job, jobs), 1):
            kmin = int(key[0])
            if reps is None:
                unk += 1; fu.write(f"{n};{why};{key}\n"); fu.flush()
                if why.startswith("BUG"): print(f"*** {why}: n = {n}", flush=True)
            else:
                k = len(reps); hist[(kmin, k)] = hist.get((kmin, k), 0) + 1
                f.write(f"{n};{k};" + ",".join(f"{x}:{y}" for x, y in sorted(reps, reverse=True)) + f";{key}\n"); f.flush()
                if k > kmin: up.append((n, kmin, k))
                if k >= 6: print(f"*** SIX-WAY OR MORE: k = {k}, n = {n}", flush=True)
            if i % 50 == 0 or i == len(jobs):
                print(f"{i}/{len(jobs)}: (listed, counted) {dict(sorted(hist.items()))}, {unk} unknown, {time.time() - t0:.0f} s", flush=True)
    print(f"done: (listed, counted) {dict(sorted(hist.items()))}, {unk} unknown, {time.time() - t0:.0f} s")
    for n, a, b in sorted(up): print(f"UPGRADE {a} -> {b}: {n}")

if __name__ == "__main__":
    main()
