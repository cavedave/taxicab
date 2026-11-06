#!/usr/bin/env python3
"""family_k.py -- special values of the F9 family: for k = 1..K, n(k) = (9k^2-3k+1)(9k^2+3k+1)(27k^4+9k^2+1) has
three collinear coprime representations by construction; count ALL its coprime representations exactly
(divisor method, factoring the three polynomial factors separately) and report k with >= 4."""
import sys, time
from collections import Counter
from multiprocessing import Pool
from collisions import all_reps, factor_batch

def work(ks):
    facs = factor_batch([f for k in ks for f in (9*k*k - 3*k + 1, 9*k*k + 3*k + 1, 27*k**4 + 9*k*k + 1)], "/opt/homebrew/bin/gp")
    out = []
    for i, k in enumerate(ks):
        fac = {}
        for f in facs[3*i:3*i + 3]:
            for p, e in f: fac[p] = fac.get(p, 0) + e
        n = (9*k*k - 3*k + 1) * (9*k*k + 3*k + 1) * (27*k**4 + 9*k*k + 1)
        reps = all_reps(n, sorted(fac.items()))
        out.append((k, n, reps))
    return out

if __name__ == "__main__":
    K = int(sys.argv[1]); t0 = time.time()
    chunks = [list(range(i, min(i + 500, K + 1))) for i in range(1, K + 1, 500)]
    hist = Counter(); hits = []
    with Pool(6) as pool:
        for res in pool.imap(work, chunks):
            for k, n, reps in res:
                hist[len(reps)] += 1
                if len(reps) >= 4: hits.append((k, n, sorted(reps)))
    print(f"k = 1..{K}: representation counts {dict(sorted(hist.items()))} [{time.time()-t0:.0f}s]")
    for k, n, reps in hits:
        print(f"  k={k}: n={n} ({len(str(n))} digits) has {len(reps)}: " + ", ".join(f"{x}:{y}" for x, y in reps))
