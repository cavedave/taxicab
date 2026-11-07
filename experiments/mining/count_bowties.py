#!/usr/bin/env python3
"""count_bowties.py -- exact representation count for the bowtie numbers of bowtie_decide.py (six-way tests).

Input lines n;k|?;x:y,... (five representations);known|new;(a, b, i, a2, b2). Known (catalogue) numbers are skipped.
Primes of n: by Theorem 13 (n = E s1 s2 s3 / (a - b)^2 on any integral line), every prime of n divides E of one of
the bowtie's lines or an s = x + y of its representations, so n is factored from the five s-values and the two E's
(PARI, with a time limit per number; anything left over is factored too and must vanish). The count is then exact
(bowtie_hunt.count_reps: s = f * subset of split blocks <= (4n)^(1/3), Theorem 5).
Output n;k;x:y,...;key (k = ? if factoring timed out); k >= 6 is also printed to stdout.

Usage: python3 count_bowties.py file [file ...] --out counted.txt [--maxdig 150] [--tlim 600] [--tcount 600] [--procs 8]
       [--skip earlier_counted.txt ...]   (numbers with k = ? also go to counted.txt.unk, with the reason)
"""
import argparse, gzip, math, sys, time
from multiprocessing import Pool
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
sys.set_int_max_str_digits(0)
from bowtie_mine import lines_of
from bowtie_hunt import factor_many, count_reps

def read(fn):
    for l in (gzip.open(fn, "rt") if fn.endswith(".gz") else open(fn)):
        f = l.strip().split(";")
        if len(f) >= 5 and f[0].isdigit():
            yield int(f[0]), [tuple(map(int, p.split(":"))) for p in f[2].split(",")], f[3], f[4]

def job(args):
    n, five, key, tlim, tcount, gp = args
    t0 = time.time()
    Es = {a * a + a * b + b * b for (a, b), T in lines_of(five)}
    pieces = sorted({abs(x + y) for x, y in five} | Es)
    facs = factor_many(pieces, gp, tlim)
    if None in facs:
        bad = [str(q) for q, fac in zip(pieces, facs) if fac is None]
        return n, None, five, key, time.time() - t0, "factor:" + ",".join(bad)
    m, F = n, {}
    for p in sorted({p for fac in facs for p, e in fac}):
        while m % p == 0: m //= p; F[p] = F.get(p, 0) + 1
    if m > 1:                                                   # not expected (Theorem 13); factor what is left
        rest = factor_many([m], gp, tlim)[0]
        if rest is None: return n, None, five, key, time.time() - t0, f"factor:{m}"
        for p, e in rest: F[p] = F.get(p, 0) + e
    F = sorted(F.items())
    assert math.prod(p**e for p, e in F) == n, "factorisation does not multiply to n"
    nsplit = sum(p % 3 == 1 for p, e in F)
    reps = count_reps(n, F, time.time() + tcount)
    if reps is None:                                            # too many split primes for the time limit
        return n, None, five, key, time.time() - t0, f"count:{nsplit} split primes;" + "*".join(f"{p}^{e}" for p, e in F)
    assert set(five) <= set(reps) | {(y, x) for x, y in reps}, "a known representation was not found"
    return n, reps, five, key, time.time() - t0, ""

def main():
    ap = argparse.ArgumentParser(); ap.add_argument("files", nargs="+"); ap.add_argument("--out", required=True)
    ap.add_argument("--maxdig", type=int, default=150); ap.add_argument("--tlim", type=int, default=600)
    ap.add_argument("--procs", type=int, default=8); ap.add_argument("--gp", default="gp")
    ap.add_argument("--tcount", type=int, default=600, help="time limit (s) for the subset search per number")
    ap.add_argument("--skip", nargs="*", default=[], help="earlier count_bowties outputs: numbers with a k there are skipped")
    A = ap.parse_args(); t0 = time.time()
    done = set()
    for fn in A.skip:
        for l in open(fn):
            g = l.split(";")
            if g[0].isdigit() and len(g) > 1 and g[1] != "?": done.add(int(g[0]))
    todo = {}
    for fn in A.files:
        for n, five, kn, key in read(fn):
            if kn == "new" and len(str(n)) <= A.maxdig and n not in done: todo.setdefault(n, (five, key))
    jobs = [(n, five, key, A.tlim, A.tcount, A.gp) for n, (five, key) in sorted(todo.items())]
    print(f"{len(jobs)} new bowtie numbers with <= {A.maxdig} digits ({len(done)} skipped as already counted)", flush=True)
    hist, unk = {}, 0
    with open(A.out, "w") as f, open(A.out + ".unk", "w") as fu, Pool(A.procs) as pool:
        f.write(f"# count_bowties.py {' '.join(A.files)}: n;k;x:y,...;curve\n")
        fu.write("# numbers left with k = ?: n;reason (factor:<unfactored pieces> | count:<split primes>;<factorisation>);curve\n")
        for i, (n, reps, five, key, dt, why) in enumerate(pool.imap_unordered(job, jobs), 1):
            if reps is None:
                unk += 1; f.write(f"{n};?;" + ",".join(f"{x}:{y}" for x, y in five) + f";{key}\n")
                fu.write(f"{n};{why};{key}\n"); fu.flush()
            else:
                hist[len(reps)] = hist.get(len(reps), 0) + 1
                f.write(f"{n};{len(reps)};" + ",".join(f"{x}:{y}" for x, y in sorted(reps, reverse=True)) + f";{key}\n")
                if len(reps) >= 6: print(f"*** SIX-WAY OR MORE: k = {len(reps)}, n = {n}", flush=True)
            f.flush()
            if i % 10 == 0 or i == len(jobs):
                print(f"{i}/{len(jobs)} done, k counts {dict(sorted(hist.items()))}, {unk} timed out, {time.time() - t0:.0f} s", flush=True)
    print(f"done: k counts {dict(sorted(hist.items()))}, {unk} with k unknown, {time.time() - t0:.0f} s", flush=True)

if __name__ == "__main__":
    main()
