#!/usr/bin/env python3
"""compare.py -- tier A / tier B tables: feature summaries by k (and dataset) from features.py CSVs.

For each (tag, k) group: count, mean number of split primes, share cube-free / squarefree, share with no
non-split prime, share divisible by 7, share with 3 | n, n mod 9 distribution, mean share of sums, and the
TODO-theorem check (every non-split prime divides every s).

Usage:  python3 compare.py feat_*.csv
"""
import csv, sys
from collections import Counter, defaultdict

rows = [r for p in sys.argv[1:] for r in csv.DictReader(open(p))]
groups = defaultdict(list)
for r in rows: groups[(r["tag"], int(r["k"]))].append(r)

def pct(xs): return f"{100 * sum(xs) / len(xs):5.1f}%"
print(f"{'dataset':>14} {'k':>2} {'count':>7} {'digits':>9} {'split':>6} {'split>=7':>8} {'cubefree':>8} "
      f"{'no-nonsplit':>11} {'7|n':>6} {'3|n':>6} {'sums':>6} {'ns|all s':>8}  mod9")
for (tag, k), g in sorted(groups.items(), key=lambda x: (x[0][0], x[0][1])):
    d = [int(r["digits"]) for r in g]; sp = [int(r["r_split"]) for r in g]
    m9 = Counter(int(r["mod9"]) for r in g)
    print(f"{tag:>14} {k:>2} {len(g):>7} {min(d):>4}-{max(d):<4} {sum(sp)/len(g):6.2f} {pct([s >= 7 for s in sp]):>8} "
          f"{pct([r['cubefree'] == '1' for r in g]):>8} {pct([r['nonsplit'] == '' for r in g]):>11} "
          f"{pct([r['has7'] == '1' for r in g]):>6} {pct([int(r['v3']) > 0 for r in g]):>6} "
          f"{100 * sum(int(r['n_sums']) for r in g) / sum(int(r['k']) for r in g):5.1f}% "
          f"{pct([r['nonsplit_divides_all_s'] == '1' for r in g]):>8}  "
          + " ".join(f"{v}:{100 * c / len(g):.0f}%" for v, c in sorted(m9.items())))
