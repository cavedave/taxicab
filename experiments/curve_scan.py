#!/usr/bin/env python3
"""curve_scan.py -- run many curves x^3 + y^3 = M through the exact ILP, for taxicab AND cabtaxi.

One PARI run per curve (curve_cabtaxi.points: all points of height <= HMAX, both signs, with
factored denominators). Then for each k the exact smallest L (curve_ilp.solve):
  taxicab  k = 6..TKMAX on the points with x, y > 0, compared with curve_bounds.KNOWN plus our
           own Ta(23..28) bounds (results/taxicab_23_28_bounds.txt);
  cabtaxi  k = CKMIN..CKMAX on all points, compared with cabtaxi_known.csv plus our own
           improved bounds (results/cabtaxi_bounds.txt).
The ILP only looks for n below SLACK x the best known value, so hopeless curves cost little.
Prints one line per curve (best log10 ratio per problem) and flags anything that beats the best
known bound; every flagged n is re-verified with exact integer arithmetic.

Usage:  python3 curve_scan.py --curves list.txt --procs 8 --out scan.csv
        (list.txt: one M per line, best first)
"""
import argparse, math, os, sys, time
from multiprocessing import Pool
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)
import curve_bounds as cb
from curve_cabtaxi import points, load_known
from curve_ilp import solve

def best_known():
    ta = dict(cb.KNOWN); ca = load_known(os.path.join(HERE, "cabtaxi_known.csv"))
    for path, d in ((os.path.join(ROOT, "results", "taxicab_23_28_bounds.txt"), ta),
                    (os.path.join(ROOT, "results", "taxicab_29_30_bounds.txt"), ta),
                    (os.path.join(ROOT, "results", "cabtaxi_bounds.txt"), ca)):
        if os.path.exists(path):
            for line in open(path):
                if line.startswith("#"): continue
                k, n = map(int, line.split(";")[:2])
                if k not in d or n < d[k]: d[k] = n
    return ta, ca

A = None
def init(args):
    global A, TA, CA
    A = args; TA, CA = best_known()

def scan(M):
    t = time.time()
    try:
        pts, fac, info = points(A.gp, M, A.hmax, 1)
    except Exception as e:
        return M, None, f"{type(e).__name__}: {str(e)[:100]}", time.time() - t
    res = {"ta": {}, "ca": {}}; beats = []
    for prob, plist, ks, known in (("ta", [p for p in pts if p[1] > 0], range(6, A.tkmax + 1), TA),
                                   ("ca", pts, range(A.ckmin, A.ckmax + 1), CA)):
        ws = [w for w, _, _ in plist]
        for k in ks:
            if len(ws) < k or k not in known: continue
            cap = (math.log(known[k]) + math.log(A.slack) - math.log(M)) / 3
            try:
                sol, _, _ = solve(fac, ws, k, cap, tlim=A.tlim)
            except Exception as e:                            # one bad solve must not stop the scan
                print(f"  {M} {prob} k={k}: solver error {type(e).__name__}: {str(e)[:80]}", flush=True); continue
            if sol is None: continue
            L = sol[0]; n = M * L**3
            r = (len(str(n)) - len(str(known[k]))) + math.log10(int(str(n)[:15]) / int(str(known[k])[:15]))
            res[prob][k] = r
            if n < known[k]:
                good = sorted({(u * (L // w), v * (L // w)) for w, u, v in plist if L % w == 0})
                assert len(good) >= k and all(x**3 + y**3 == n for x, y in good)
                if prob == "ta": assert all(x > 0 and y > 0 for x, y in good)
                beats.append((prob, k, n, L, good))
    return M, (res, beats), " ".join(info.values()), time.time() - t

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--gp", default="gp")
    ap.add_argument("--curves", required=True)
    ap.add_argument("--procs", type=int, default=os.cpu_count())
    ap.add_argument("--hmax", default="80")
    ap.add_argument("--tkmax", type=int, default=28)
    ap.add_argument("--ckmin", type=int, default=10)
    ap.add_argument("--ckmax", type=int, default=70)
    ap.add_argument("--slack", type=float, default=1e3)
    ap.add_argument("--tlim", type=float, default=120)
    ap.add_argument("--out", default="scan.csv")
    a = ap.parse_args()
    Ms = [int(l.split(";")[0]) for l in open(a.curves) if l.strip() and not l.startswith("#")]
    done = set()
    if os.path.exists(a.out):
        done = {int(l.split(";")[0]) for l in open(a.out) if l[0].isdigit()}
    todo = [M for M in Ms if M not in done]
    print(f"{len(Ms)} curves, {len(done)} done, {len(todo)} to scan", flush=True)
    t0 = time.time()
    with open(a.out, "a") as fo, Pool(a.procs, initializer=init, initargs=(a,)) as pool:
        for i, (M, r, info, dt) in enumerate(pool.imap_unordered(scan, todo), 1):
            if r is None:
                print(f"  {M}: FAILED {info}", flush=True); continue
            res, beats = r
            bt = min(res["ta"].values(), default=None); bc = min(res["ca"].values(), default=None)
            f = lambda x: "" if x is None else f"{x:.2f}"
            fo.write(f"{M};{f(bt)};{f(bc)};" + ",".join(f"t{k}:{v:.2f}" for k, v in sorted(res["ta"].items()))
                     + ";" + ",".join(f"c{k}:{v:.2f}" for k, v in sorted(res["ca"].items())) + "\n"); fo.flush()
            for prob, k, n, L, good in beats:
                tag = "Ta" if prob == "ta" else "Ca"
                print(f"*** {tag}({k}) <= {n} BEATS best known (curve {M}, L={L}) ***", flush=True)
                with open(a.out + ".beats", "a") as fb:
                    fb.write(f"{prob};{k};{n};{M};{L};" + ",".join(f"{x}:{y}" for x, y in good) + "\n")
            if i % 50 == 0 or i == len(todo) or beats:
                el = time.time() - t0
                print(f"[{el:6.0f}s] {i}/{len(todo)}  last {M} ({info.strip()}) best log10 ratio ta {f(bt)} ca {f(bc)}"
                      f"  ETA {el/i*(len(todo)-i):.0f}s", flush=True)

if __name__ == "__main__":
    main()
