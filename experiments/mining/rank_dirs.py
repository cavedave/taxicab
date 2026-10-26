#!/usr/bin/env python3
"""rank_dirs.py -- which line directions are productive? Joins line_enum.py output (n;a;b;c;points) with
cheap_search.py output (n;k;reps) and reports, per direction (a, b): candidates written, four-ways and
five-or-more-ways found on it, and the four-way rate. The top directions are the ones to search deeper
(larger --height / --nmax) next.

Usage: python3 rank_dirs.py lines.txt multi.txt [--top 40]
"""
import argparse
from collections import Counter, defaultdict

def main():
    ap = argparse.ArgumentParser(); ap.add_argument("lines"); ap.add_argument("multi")
    ap.add_argument("--top", type=int, default=40)
    a = ap.parse_args()
    kof = {}
    for l in open(a.multi):
        n, k, _ = l.split(";", 2); kof[int(n)] = int(k)
    cand = Counter(); hits = defaultdict(Counter)
    for l in open(a.lines):
        n, A, B, _ = l.split(";", 3)
        d = (int(A), int(B)); cand[d] += 1
        k = kof.get(int(n))
        if k: hits[d][min(k, 5)] += 1
    rows = sorted(cand, key=lambda d: (-hits[d][5], -hits[d][4] / cand[d]))
    print(f"{len(cand)} directions, {sum(cand.values())} candidates, "
          f"{sum(h[4] for h in hits.values())} four-way and {sum(h[5] for h in hits.values())} five+-way line hits")
    print(f"{'direction':>14} {'cands':>8} {'4-ways':>7} {'5+':>4} {'4-way rate':>11}")
    for d in rows[:a.top]:
        print(f"{str(d):>14} {cand[d]:>8} {hits[d][4]:>7} {hits[d][5]:>4} {hits[d][4] / cand[d]:>11.2e}")

if __name__ == "__main__":
    main()
