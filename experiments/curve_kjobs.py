#!/usr/bin/env python3
"""curve_kjobs.py -- exact taxicab / cabtaxi bounds on ONE curve, one parallel job per k (for 7of9).

PARI computes every point of height <= HMAX once (curve_cabtaxi.points, denominators factored by
trial division to FLIM). Then each (problem, k) is an independent exact integer program
(curve_ilp.solve), run in parallel:
  Ta  taxicab: points with x, y > 0          Ca  cabtaxi: all points (either sign)
Each job only searches below its cap, the best known bound from --caps (prob;k;n lines; built on
the Mac from the published tables plus our own results), so "no improvement" is fast. For k with no
cap the search allows --nolimit digits. Every result is re-verified with exact integer arithmetic
before it is written. Rerunning the same command skips the jobs already in --out.

Output (--out):  prob;k;status;n;M;L;x:y,...      status: optimal | timelimit (valid, maybe not optimal)
                 prob;k;none;;;; or prob;k;same;;;;   nothing below the cap / ties it

Example (7of9):
  python3 curve_kjobs.py --gp ~/pari/bin/gp --curve 3956875867 --hmax 110 --flim 1000000 \
          --caps caps.csv --jobs Ca:50-72,Ta:29-34 --procs 30 --tlim 3600 --out h110.txt
"""
import argparse, math, os, sys, time
from multiprocessing import Pool
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from curve_cabtaxi import points
from curve_ilp import solve

PTS = FAC = A = CAPS = None

def parse_jobs(spec):
    jobs = []
    for part in spec.split(","):
        prob, rng = part.split(":")
        lo, hi = (int(x) for x in rng.split("-")) if "-" in rng else (int(rng), int(rng))
        jobs += [(prob, k) for k in range(lo, hi + 1)]
    return jobs

def init(pts, fac, args, caps):                            # each worker gets the shared data once
    global PTS, FAC, A, CAPS
    PTS, FAC, A, CAPS = pts, fac, args, caps

def run(job):
    prob, k = job
    t = time.time()
    plist = [p for p in PTS if p[1] > 0] if prob == "Ta" else PTS
    ws = [w for w, _, _ in plist]
    cap = CAPS.get((prob, k))
    lim = (math.log(cap) + 1e-9 if cap else math.log(10.0) * A.nolimit) - math.log(A.curve)
    try:
        sol, _, st = solve(FAC, ws, k, lim / 3, tlim=A.tlim)
    except Exception as e:
        return prob, k, f"error {type(e).__name__}: {str(e)[:80]}", None, time.time() - t
    if sol is None:
        return prob, k, "none", None, time.time() - t
    L = sol[0]; n = A.curve * L**3
    if cap and n >= cap:                                   # the optimum only ties the best known bound
        return prob, k, "same", None, time.time() - t
    good = sorted({(u * (L // w), v * (L // w)) for w, u, v in plist if L % w == 0})
    assert len(good) >= k and all(x**3 + y**3 == n for x, y in good), "verification failed"
    if prob == "Ta": assert all(0 < x < y for x, y in good)
    return prob, k, "optimal" if st == 0 else "timelimit", (n, L, good), time.time() - t

def main():
    global PTS, FAC, A, CAPS
    ap = argparse.ArgumentParser()
    ap.add_argument("--gp", default="gp")
    ap.add_argument("--curve", type=int, required=True)
    ap.add_argument("--hmax", default="110")
    ap.add_argument("--flim", default="1000000")
    ap.add_argument("--caps", required=True)
    ap.add_argument("--jobs", required=True, help="e.g. Ca:50-72,Ta:29-34")
    ap.add_argument("--procs", type=int, default=os.cpu_count())
    ap.add_argument("--tlim", type=float, default=3600)
    ap.add_argument("--nolimit", type=float, default=700, help="digits allowed when there is no cap")
    ap.add_argument("--out", required=True)
    A = ap.parse_args()
    CAPS = {}
    for line in open(A.caps):
        if line.strip() and not line.startswith("#"):
            p, k, n = line.strip().split(";")[:3]; CAPS[(p, int(k))] = int(n)
    done = set()
    if os.path.exists(A.out):
        done = {(l.split(";")[0], int(l.split(";")[1])) for l in open(A.out) if l.strip()}
    todo = [j for j in parse_jobs(A.jobs) if j not in done]
    todo.sort(key=lambda j: -j[1])                         # largest k (slowest) first
    t0 = time.time()
    PTS, FAC, info = points(A.gp, A.curve, A.hmax, 1, A.flim)
    print(f"curve {A.curve}, height {A.hmax}: {' '.join(info.values())}, {len(PTS)} points "
          f"({time.time()-t0:.0f}s); {len(done)} jobs done, {len(todo)} to run", flush=True)
    with open(A.out, "a") as fo, Pool(A.procs, initializer=init, initargs=(PTS, FAC, A, CAPS)) as pool:
        for prob, k, status, res, dt in pool.imap_unordered(run, todo):
            cap = CAPS.get((prob, k))
            if res is None:
                fo.write(f"{prob};{k};{status};;;;\n")
                print(f"  {prob}({k}): {status} ({dt:.0f}s)", flush=True)
            else:
                n, L, good = res
                tag = "NEW (no known bound)" if not cap else f"IMPROVES best known by {cap / n:.4g}x"
                fo.write(f"{prob};{k};{status};{n};{A.curve};{L};" + ",".join(f"{x}:{y}" for x, y in good) + "\n")
                print(f"  {prob}({k}): {len(str(n))} digits, {tag}, {status} ({dt:.0f}s)", flush=True)
            fo.flush()
    print(f"all done in {time.time()-t0:.0f}s", flush=True)

if __name__ == "__main__":
    main()
