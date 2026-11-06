#!/usr/bin/env python3
"""exhaustive_mining.py -- the mining statistics redone on the EXHAUSTIVE data only (FINDINGS F44), so that no
search method biases what is counted.

Data:
  four- and five-ways   results/a047697_catalogue.txt, n <= 2.5e23 (complete for every k >= 4)
  shapes                line_structure.py CSV of the catalogue (--shapes)
  three-ways            cabtaxi.cpp --kmin 3 output for 1e17 - 1e19 (--k3 files, with representations)
  controls              control_windows.py census windows (--ctrl files): every n in a window with its exact k

Prints:
  1. shape mix of the four-ways by size band (line + free / hub / independent);
  2. shapes of the five-ways and the line + free -> five-way transition rates;
  3. features by k, size-matched in 1e17 - 1e19 (k = 1, 2 from census windows; k = 3, 4 complete);
  4. split primes of four- and five-ways against the k = 1 census at the same size, band by band.
Usage: python3 exhaustive_mining.py --shapes ls_all.csv --k3 k3_*.txt --ctrl w_*.txt wide_3e17.txt [--gp gp]
"""
import argparse, csv, random, sys
from collections import Counter, defaultdict
from multiprocessing import Pool
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
from collisions import factor_batch

B = 25 * 10**22
BANDS = [(0, 10**15), (10**15, 10**17), (10**17, 10**19), (10**19, 10**21), (10**21, 10**22), (10**22, 10**23), (10**23, B)]

def read(fn, kcol=True):
    for l in open(fn):
        if l[0].isdigit():
            p = l.strip().split(";"); yield int(p[0]), int(p[1])

def _fac(args):
    ns, gp = args
    return list(zip(ns, factor_batch(ns, gp)))

def factor_all(ns, gp, procs=8):
    ns = sorted(set(ns)); parts = [(ns[i:i + 2000], gp) for i in range(0, len(ns), 2000)]
    out = {}
    with Pool(procs) as pool:
        for res in pool.imap_unordered(_fac, parts): out.update(res)
    return out

def feats(n, fac):
    ps = [p for p, e in fac]
    return {"split": sum(1 for p in ps if p % 3 == 1), "7|n": n % 7 == 0, "3|n": n % 3 == 0, "even": n % 2 == 0,
            "n=+-2 mod 9": n % 9 in (2, 7), "all split": all(p % 3 == 1 for p in ps),
            "cubefree": all(e < 3 for p, e in fac)}

def band(n):
    for lo, hi in BANDS:
        if lo < n <= hi: return f"{lo:.0e}-{hi:.1e}" if hi == B else f"{lo:.0e}-{hi:.0e}"

def table(groups, F):
    keys = ["split", "7|n", "3|n", "even", "n=+-2 mod 9", "all split", "cubefree"]
    print(f"{'group':34s} {'N':>8s} " + " ".join(f"{k:>11s}" for k in keys))
    for name, ns in groups:
        if not ns: continue
        row = [F[n] for n in ns]
        vals = [sum(r[k] for r in row) / len(row) for k in keys]
        print(f"{name:34s} {len(ns):>8,} " + " ".join(f"{v:>11.2f}" if k == "split" else f"{100 * v:>10.0f}%" for k, v in zip(keys, vals)))

def main():
    ap = argparse.ArgumentParser(); ap.add_argument("--shapes", required=True); ap.add_argument("--k3", nargs="+", required=True)
    ap.add_argument("--ctrl", nargs="+", required=True); ap.add_argument("--gp", default="gp"); ap.add_argument("--seed", type=int, default=1)
    A = ap.parse_args(); random.seed(A.seed)
    cat = {n: k for n, k in read("results/a047697_catalogue.txt") if n <= B}
    shape = {int(r["n"]): r["shape"] for r in csv.DictReader(open(A.shapes)) if int(r["n"]) <= B}
    E4 = sorted(n for n, k in cat.items() if k == 4); E5 = sorted(n for n, k in cat.items() if k >= 5)
    print(f"exhaustive: {len(E4)} four-ways, {len(E5)} five-ways <= 2.5e23")

    # 1. shape mix by band
    print("\n1. shape mix of the four-ways by size")
    bs = defaultdict(Counter)
    for n in E4: bs[band(n)][shape[n]] += 1
    print(f"{'band':22s} {'N':>5s} {'line+free':>10s} {'hub':>7s} {'indep':>7s} {'hub %':>6s} {'indep %':>8s}")
    for lo, hi in BANDS:
        c = bs[band(hi)]; N = sum(c.values())
        print(f"{band(hi):22s} {N:>5} {c['line+free']:>10} {c['hub']:>7} {c['independent']:>7} {100 * c['hub'] / N:>6.1f} {100 * c['independent'] / N:>8.1f}")

    # 2. five-way shapes and transition rates
    print("\n2. five-ways: " + ", ".join(f"{n} {shape[n]}" for n in E5))
    lf = sum(1 for n in E4 if shape[n] == "line+free"); s5 = Counter(shape[n] for n in E5)
    print(f"   line+free four-ways {lf}; bowties {s5['bowtie']} ({s5['bowtie'] / lf:.1e}); line+2free {s5['line+2free']} ({s5['line+2free'] / lf:.1e})")
    print(f"   five-ways : four-ways = {len(E5)} : {len(E4)} = 1 : {len(E4) / len(E5):.0f}")

    # 3. features by k, 1e17 - 1e19
    k3 = [n for fn in A.k3 for n, k in read(fn) if k == 3]
    ctrl = defaultdict(list)
    for fn in A.ctrl:
        for n, k in read(fn): ctrl[(Path(fn).stem, k)].append(n)
    lo, hi = 10**17, 10**19
    c1 = [n for (w, k), ns in ctrl.items() if k == 1 and w in ("w_1e+18", "wide_3e17") for n in ns]
    c1 = random.sample(c1, min(20000, len(c1)))
    c2 = [n for (w, k), ns in ctrl.items() if k == 2 and w in ("w_1e+18", "wide_3e17") for n in ns]
    k3s = random.sample(k3, min(40000, len(k3)))
    e4 = [n for n in E4 if lo < n <= hi]
    allc1 = {w: random.sample(ns, min(6000, len(ns))) for (w, k), ns in ctrl.items() if k == 1 and w.startswith("w_")}
    need = c1 + c2 + k3s + E4 + E5 + [n for ns in allc1.values() for n in ns]
    print(f"\nfactorising {len(set(need)):,} numbers ...", flush=True)
    fac = factor_all(need, A.gp); F = {n: feats(n, f) for n, f in fac.items()}
    print("\n3. features by k, all n in 1e17 - 1e19 (k = 1, 2 census windows at 3e17 and 1e18)")
    table([("k = 1 (census sample)", c1), ("k = 2 (census)", c2), ("k = 3 (complete, sample)", k3s),
           ("k = 4 (complete)", e4), ("k = 5 (all 12, 5e14 - 2.5e23)", E5)], F)

    # 4. split primes by size against the k = 1 census at the same size
    print("\n4. split primes: four-ways by band against the k = 1 census near the band")
    cent = {w: int(float(w[2:])) for w in allc1}
    def ctrl_for(lo, hi):
        ws = [w for w, c in cent.items() if lo < c <= hi * 2] or [min(cent, key=lambda w: abs(cent[w] - hi))]
        return [n for w in ws for n in allc1[w]]
    print(f"{'band':22s} {'four-ways':>9s} {'split':>6s} {'k=1 ctrl':>9s} {'split':>6s} {'excess':>7s}")
    for lo, hi in BANDS:
        g = [n for n in E4 if lo < n <= hi]; c = ctrl_for(lo, hi)
        a = sum(F[n]["split"] for n in g) / len(g); b = sum(F[n]["split"] for n in c) / len(c)
        print(f"{band(hi):22s} {len(g):>9} {a:>6.2f} {len(c):>9,} {b:>6.2f} {a - b:>+7.2f}")
    a = sum(F[n]["split"] for n in E5) / len(E5)
    c = [n for w in allc1 for n in allc1[w] if cent[w] >= 10**14]; b = sum(F[n]["split"] for n in c) / len(c)
    print(f"{'five-ways 5e14-2.5e23':22s} {len(E5):>9} {a:>6.2f} {len(c):>9,} {b:>6.2f} {a - b:>+7.2f}")
    print("   five-way split counts:", sorted(F[n]["split"] for n in E5))

if __name__ == "__main__":
    main()
