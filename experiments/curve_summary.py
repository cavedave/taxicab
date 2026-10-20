#!/usr/bin/env python3
"""curve_summary.py -- one compact line per curve from curve_hunt output, for near-miss analysis.

Reads curve_hunt files (k;n;M;L;pairs) and the curve_sieve ranking (M;S) and writes
    M;score;rank_in_ranking;r6;r7;...;r22
where rK = log10(best n for k / published Ta(K) bound), empty if the curve had no K-way result.
0 means "equals the record"; negative would beat it. Only the first four fields of each hunt
line are parsed, so the big pairs column costs nothing.

Usage (7of9):
  python3 ~/taxi/curve_summary.py --ranked /mnt/scratch/dcurran/ranked_split.csv \
          --hunt /mnt/scratch/dcurran/hunt_split.csv --out /mnt/scratch/dcurran/split_summary.csv
  gzip -k /mnt/scratch/dcurran/split_summary.csv
"""
import argparse, math, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from curve_bounds import KNOWN

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--ranked", required=True)
    ap.add_argument("--hunt", nargs="+", required=True)
    ap.add_argument("--out", required=True)
    a = ap.parse_args()
    ks = sorted(KNOWN)
    logref = {k: math.log10(KNOWN[k]) for k in ks}
    best = {}                                            # M -> {k: log10 ratio}
    for path in a.hunt:
        with open(path) as f:
            for line in f:
                p = line.split(";", 4)
                if len(p) < 4: continue
                k = int(p[0])
                if k not in logref: continue
                n = int(p[1]); M = int(p[2])
                r = math.log10(n) - logref[k]
                d = best.setdefault(M, {})
                if k not in d or r < d[k]: d[k] = r
    seen = 0
    with open(a.ranked) as f, open(a.out, "w") as fo:
        fo.write("M;score;rank;" + ";".join(f"r{k}" for k in ks) + "\n")
        for i, line in enumerate(f, 1):
            M, S = line.strip().split(";")
            d = best.get(int(M))
            if d is None: continue                       # curve not hunted (yet)
            seen += 1
            fo.write(f"{M};{S};{i};" + ";".join("" if k not in d else f"{d[k]:.3f}" for k in ks) + "\n")
    print(f"{len(best)} curves with results in {', '.join(a.hunt)}; {seen} matched to the ranking -> {a.out}")

if __name__ == "__main__":
    main()
