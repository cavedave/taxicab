#!/usr/bin/env python3
"""curve_hunt.py -- run the curve_bounds method over many seeds, in parallel.

Seeds are reduced to their cube-free core M (x^3+y^3 = N and = N/g^3 are the same curve), so
each curve is processed once; the seed's pairs become rational points (a/g, b/g) on it.
For every curve we keep the smallest M*L^3 found for each way-count k >= --kmin, and the
global best per k is compared with the published Ta(k) upper bounds.

Input:  seed files in seedgen format  N;k;p:e,...;a:b,...   (e.g. seeds_1e15.csv)
Output: <out>          k;n;M;L;pairs        every per-curve best with k >= --kmin
        <out>.ckpt     M                    curves finished (resume: rerun the same command)
Each reported n is re-verified (a^3+b^3 == n for all k pairs) before it is written.

Example (7of9):
  python3 curve_hunt.py --gp ~/pari/bin/gp --seeds seeds_1e15.csv --procs 64 --out hunt.csv
"""
import argparse, math, os, sys, time
from multiprocessing import Pool
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import curve_bounds as cb

def core(N, fac):
    M, g = 1, 1
    for p, e in fac:
        M *= p ** (e % 3); g *= p ** (e // 3)
    return M, g

def load(paths):
    curves = {}                                         # M -> list of rational points (a/g, b/g)
    for path in paths:
        for line in open(path):
            f = line.strip().split(";")
            if len(f) < 4: continue
            N = int(f[0])
            fac = [(int(x.split(":")[0]), int(x.split(":")[1])) for x in f[2].split(",") if x]
            pairs = [tuple(map(int, x.split(":"))) for x in f[3].split(",") if x]
            M, g = core(N, fac)
            assert M * g**3 == N
            curves.setdefault(M, set()).update((a, b, g) for a, b in pairs)
    return curves

ARGS = None
def init(args):                                         # workers do not inherit globals under spawn
    global ARGS
    ARGS = args

def work(item):
    M, pts = item
    t = time.time()
    try:
        rank, plist = cb.run_gp(ARGS.gp, M, sorted(pts), ARGS.hmax, int(ARGS.wmax), timeout=ARGS.timeout, verbose=False)
    except Exception as e:
        return M, None, f"{type(e).__name__}: {str(e)[:120]}", time.time() - t
    bases = {1} | {g for _, _, g in pts}
    if ARGS.width:
        best = cb.beam(M, plist, int(ARGS.ub), bases, ARGS.width)
    else:
        best = cb.search(M, plist, ARGS.maxset, int(ARGS.ub), bases)
    rows = []
    for k, (n, L) in best.items():
        if k < ARGS.kmin: continue
        good = sorted({(u * (L // w), v * (L // w)) for w, u, v in plist if L % w == 0})
        assert len(good) >= k and all(x**3 + y**3 == n for x, y in good), "verification failed"
        rows.append((k, n, M, L, good))
    return M, rows, rank, time.time() - t

def main():
    global ARGS
    ap = argparse.ArgumentParser()
    ap.add_argument("--gp", default="gp")
    ap.add_argument("--seeds", nargs="+", required=True)
    ap.add_argument("--out", default="hunt.csv")
    ap.add_argument("--procs", type=int, default=os.cpu_count())
    ap.add_argument("--hmax", default="80")
    ap.add_argument("--wmax", type=float, default=1e15)   # denominators on the cube-free core are larger
    ap.add_argument("--maxset", type=int, default=5)
    ap.add_argument("--ub", type=float, default=1e60)
    ap.add_argument("--kmin", type=int, default=6)
    ap.add_argument("--timeout", type=float, default=300)
    ap.add_argument("--limit", type=int, default=0, help="only the first N curves (testing)")
    ap.add_argument("--width", type=int, default=0, help="beam search with this width instead of exhaustive --maxset")
    ARGS = ap.parse_args()

    curves = load(ARGS.seeds)
    done = set()
    if os.path.exists(ARGS.out + ".ckpt"):
        done = {int(x) for x in open(ARGS.out + ".ckpt") if x.strip()}
    todo = [(M, p) for M, p in curves.items() if M not in done]   # seed-file order: best curves first
    if ARGS.limit: todo = todo[:ARGS.limit]
    print(f"{len(curves)} distinct curves from {', '.join(ARGS.seeds)}; {len(done)} done, {len(todo)} to run",
          flush=True)

    best = {}
    if os.path.exists(ARGS.out):
        for line in open(ARGS.out):
            k, n = map(int, line.split(";")[:2])
            if k not in best or n < best[k][0]: best[k] = (n, line.split(";")[2])
    t0 = time.time(); fails = 0; ranks = {}
    with open(ARGS.out, "a") as fo, open(ARGS.out + ".ckpt", "a") as fc, Pool(ARGS.procs, initializer=init, initargs=(ARGS,)) as pool:
        for i, (M, rows, info, dt) in enumerate(pool.imap_unordered(work, todo, chunksize=1), 1):
            if rows is None:
                fails += 1
                print(f"  curve {M}: {info}", flush=True)
            else:
                ranks[info] = ranks.get(info, 0) + 1
                for k, n, MM, L, good in rows:
                    fo.write(f"{k};{n};{MM};{L};" + ",".join(f"{x}:{y}" for x, y in good) + "\n")
                    if k not in best or n < best[k][0]:
                        best[k] = (n, MM)
                        ref = cb.KNOWN.get(k)
                        if ref and n < ref:
                            print(f"*** k={k}: {n} BEATS published {ref} (curve {MM}, L={L}) ***", flush=True)
            fo.flush()
            if rows is not None: fc.write(f"{M}\n"); fc.flush()   # failures are retried on rerun
            if i % 500 == 0 or i == len(todo):
                el = time.time() - t0
                print(f"[{el:7.0f}s] {i}/{len(todo)} curves, {fails} failed, ETA {el/i*(len(todo)-i):.0f}s", flush=True)
    print("\nrank distribution:", dict(sorted(ranks.items())))
    print(f"\n{'k':>3}  {'best n':>62}  {'curve M':>20}  vs published")
    for k in sorted(best):
        n, M = best[k]; ref = cb.KNOWN.get(k)
        cmp = "" if ref is None else ("BEATS published" if n < ref else "equals published" if n == ref
                                      else f"{n/ref:.3g}x published")
        print(f"{k:>3}  {n:>62}  {M:>20}  {cmp}")

if __name__ == "__main__":
    main()
