#!/usr/bin/env python3
"""control_windows.py -- exhaustive control data: every n in lo < n <= hi with ALL its coprime
representations n = x^3 + y^3 (signs allowed), in the same format as the searches: n;k;x:y,...

Uses the exact integer routines of ../window_count.py (validated: 36,368 pairs to 1e7, and the 39-pair
window below 1e21). Every n hit in the window is listed with its full representation count, so the
output is a complete census of k = 1, 2, 3, ... at that size: the control groups for the mining.

Usage:  python3 control_windows.py LO HI --out ctrl_1e15.txt [--procs 8]
"""
from __future__ import annotations

import argparse, os, sys
from collections import defaultdict
from math import gcd
from multiprocessing import Pool
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
from window_count import icbrt, cmin


def chunk(args):
    lo, hi, kind, start, stop = args
    hits = []
    for t in range(start, stop):
        if kind == "sum":                               # n = a^3 + b^3, 1 <= a <= b
            a3 = t ** 3
            b0 = max(t, icbrt(lo - a3) + 1) if lo > a3 else t
            for b in range(b0, icbrt(hi - a3) + 1):
                if gcd(t, b) == 1:
                    hits.append((a3 + b ** 3, b, t))   # stored as x:y with x >= y
        else:                                           # n = (c+d)^3 - c^3
            d = t
            for c in range(cmin(d, lo + 1), cmin(d, hi + 1)):
                if gcd(c, d) == 1:
                    hits.append(((c + d) ** 3 - c ** 3, c + d, -c))
    return hits


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("lo", type=int); ap.add_argument("hi", type=int)
    ap.add_argument("--out", required=True)
    ap.add_argument("--procs", type=int, default=os.cpu_count())
    a = ap.parse_args()
    lo, hi = a.lo, a.hi
    jobs = []
    for kind, top in (("sum", icbrt(hi // 2) + 1), ("diff", icbrt(hi) + 1)):
        step = max(1, top // 512)
        jobs += [(lo, hi, kind, s, min(s + step, top + 1)) for s in range(1, top + 1, step)]
    reps = defaultdict(list)
    with Pool(a.procs) as pool:
        for part in pool.imap_unordered(chunk, jobs):
            for n, x, y in part:
                reps[n].append((x, y))
    with open(a.out, "w") as f:
        f.write(f"# control window: every n with lo < n <= hi, all coprime signed representations; lo={lo} hi={hi}\n")
        for n in sorted(reps):
            ps = sorted(set(reps[n]))
            assert len(ps) == len(reps[n]) and all(x**3 + y**3 == n and gcd(x, abs(y)) == 1 for x, y in ps)
            f.write(f"{n};{len(ps)};" + ",".join(f"{x}:{y}" for x, y in ps) + "\n")
    hist = defaultdict(int)
    for v in reps.values(): hist[len(v)] += 1
    print(f"({lo}, {hi}]: {len(reps)} numbers, by k: {dict(sorted(hist.items()))} -> {a.out}")


if __name__ == "__main__":
    main()
