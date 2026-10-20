#!/usr/bin/env python3
"""near_misses.py -- which curves came closest to the published Ta(k) bounds?

Reads curve_hunt output (k;n;M;L;pairs) and, for every curve, its best ratio n / published Ta(k)
over k = 7..22 (1.0 = equals the record, < 1 would be a new record). Prints the closest curves
and, per k, the runner-up curves behind the record holder: these are the candidates for a
wider / deeper search.

Usage:  python3 near_misses.py hunt18.csv [--top 30]
"""
import argparse, math, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from curve_bounds import KNOWN

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("hunt", nargs="+")
    ap.add_argument("--top", type=int, default=30)
    ap.add_argument("--kmin", type=int, default=7)
    a = ap.parse_args()
    best = {}                                   # M -> (log10 ratio, k, n)
    perk = {}                                   # k -> list of (log10 ratio, M)
    for path in a.hunt:
        for line in open(path):
            f = line.split(";", 4)
            if len(f) < 4: continue
            k, n, M = int(f[0]), int(f[1]), int(f[2])
            if k < a.kmin or k not in KNOWN: continue
            r = math.log10(n) - math.log10(KNOWN[k])
            perk.setdefault(k, []).append((r, M))
            if M not in best or r < best[M][0]: best[M] = (r, k, n)
    print(f"{len(best)} curves with a {a.kmin}+ way result\n")
    print(f"closest curves overall (ratio = n / published bound; 1 = ties the record):")
    print(f"{'curve M':>22} {'k':>3} {'ratio':>10}")
    for M, (r, k, n) in sorted(best.items(), key=lambda x: x[1][0])[:a.top]:
        print(f"{M:>22} {k:>3} {10**r:>10.3g}")
    print(f"\nper k: record holder and the next 3 curves")
    for k in sorted(perk):
        L = sorted(set(perk[k]))[:4]
        print(f"  Ta({k:2d}): " + ", ".join(f"{M} ({10**r:.3g})" for r, M in L))

if __name__ == "__main__":
    main()
