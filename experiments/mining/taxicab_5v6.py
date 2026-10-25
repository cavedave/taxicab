#!/usr/bin/env python3
"""taxicab_5v6.py -- compare taxicab (positive cubes) five-ways with six-ways at the level of curves.

Every N = a^3 + b^3 (k ways) is reduced to its curve x^3 + y^3 = M, where M is the cube-free part of N and
N = M g^3. Each pair (a, b) is the rational point (a/g, b/g) on that curve, with denominator
w = g / gcd(g, a, b). Scaling (N -> m^3 N) keeps M and all the points, so grouping by M removes it.

Input: results/k5plus.csv (seed;m;N;k;new pairs; the other pairs are m * the seed's pairs from seeds.csv)
       and results/sixways.csv (N;k;seed;m;all pairs, the complete b12 run).
Output: per-k tables of curve features, plus per-curve rows to --out.
"""
from __future__ import annotations

import argparse, csv, os, re, subprocess
from collections import Counter, defaultdict
from math import gcd

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..")


def factor_batch(ns, gp):
    out = []
    for i in range(0, len(ns), 2000):
        part = ns[i:i + 2000]
        res = subprocess.run([gp, "-q"], input="\n".join(f"print(factor({n}));" for n in part),
                             capture_output=True, text=True, check=True).stdout.strip().splitlines()
        for f in res:
            body = re.search(r"\[([^\[\]]*)\]", f.replace("Mat(", "")).group(1)
            out.append([tuple(int(v) for v in r.split(",")) for r in body.replace(" ", "").split(";")])
    return out


def load(gp):
    seeds = {}
    for line in open(os.path.join(ROOT, "results", "seeds.csv")):
        f = line.strip().split(";")
        if len(f) >= 4: seeds[int(f[0])] = [tuple(map(int, p.split(":"))) for p in f[3].split(",") if p]
    rows = {}                                              # N -> (k, set of pairs, source)
    missing = 0
    for line in open(os.path.join(ROOT, "results", "k5plus.csv")):
        f = line.strip().split(";")
        seed, m, N, k = int(f[0]), int(f[1]), int(f[2]), int(f[3])
        new = [tuple(map(int, p.split(":"))) for p in f[4].split(",") if p]
        if seed not in seeds: missing += 1; continue
        pairs = {tuple(sorted(p)) for p in new} | {tuple(sorted((m * a, m * b))) for a, b in seeds[seed]}
        rows[N] = (k, pairs, "b9")
    for line in open(os.path.join(ROOT, "results", "sixways.csv")):
        f = line.strip().split(";")
        N, k = int(f[0]), int(f[1])
        rows[N] = (k, {tuple(sorted(map(int, p.split(":")))) for p in f[4].split(",") if p}, "b12")
    return rows, missing


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--gp", default="gp")
    ap.add_argument("--out", default="taxicab_curves.csv")
    a = ap.parse_args()
    rows, missing = load(a.gp)
    bad = [N for N, (k, ps, _) in rows.items() if len(ps) != k or any(x**3 + y**3 != N for x, y in ps)]
    print(f"{len(rows)} numbers rebuilt ({missing} rows skipped: seed not in seeds.csv); "
          f"{len(bad)} fail the exact check (count or identity)")
    rows = {N: v for N, v in rows.items() if N not in bad}
    Ns = sorted(rows)
    facs = dict(zip(Ns, factor_batch(Ns, a.gp)))
    curves = defaultdict(lambda: {"k": 0})                 # M -> best (largest k, then smallest N) example
    for N in Ns:
        k, ps, src = rows[N]
        fac = facs[N]
        M = 1; g = 1
        for p, e in fac: M *= p ** (e % 3); g *= p ** (e // 3)
        dens = sorted(g // gcd(g, gcd(x, y)) for x, y in ps)
        c = curves[M]
        if k > c["k"] or (k == c["k"] and N < c["N"]):
            curves[M] = dict(k=k, N=N, g=g, dens=dens, src=src, primitive=sum(gcd(x, y) == 1 for x, y in ps))
    Ms = sorted(curves)
    mfac = dict(zip(Ms, factor_batch(Ms, a.gp)))
    dfac_vals = sorted({w for c in curves.values() for w in c["dens"] if w > 1})
    dfac = dict(zip(dfac_vals, factor_batch(dfac_vals, a.gp))) if dfac_vals else {}
    with open(a.out, "w", newline="") as fo:
        w = csv.writer(fo); w.writerow(["M", "k", "N", "g", "M_digits", "M_split", "M_nonsplit", "n_dens_1",
                                        "dens", "den_primes", "max_den_prime", "src"])
        for M in Ms:
            c = curves[M]; fac = mfac[M]
            dp = sorted({p for d in c["dens"] if d > 1 for p, _ in dfac[d]})
            w.writerow([M, c["k"], c["N"], c["g"], len(str(M)), sum(p % 3 == 1 for p, _ in fac),
                        " ".join(str(p) for p, _ in fac if p % 3 != 1), sum(d == 1 for d in c["dens"]),
                        " ".join(map(str, c["dens"])), " ".join(map(str, dp)), max(dp) if dp else 1, c["src"]])
    print(f"{len(curves)} distinct curves M; best k per curve: {dict(sorted(Counter(c['k'] for c in curves.values()).items()))}")


if __name__ == "__main__":
    main()
