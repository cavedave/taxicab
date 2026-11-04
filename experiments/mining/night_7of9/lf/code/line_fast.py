#!/usr/bin/env python3
"""line_fast.py -- line_complete.py with the inner loops in C++ (lc_fast.cpp). Same jobs, same rules, same outputs.

Python (line_complete.Direction, validated) prepares each job: heights, G-levels, class lattices, conic point,
factorisations of E and |a - b|; a persistent lc_fast process per worker enumerates, keeps canonical coprime triples
with n <= B and counts each n exactly from n = E s1 s2 s3 / (a - b)^2 (Theorem 13). Jobs that would overflow 128 bits
are rerun with line_complete.run_dir (Python).

Usage: python3 line_fast.py --B 1e33 --cmax 1e4 --out k4.txt --log jobs.log [--procs 60] [--gp gp] [--resume]
       python3 line_fast.py --B 1e19 --cmax 1e7 --triples --out triples.txt     (validation: every triple)
"""
import argparse, math, os, subprocess, sys, time
from itertools import combinations, product
from multiprocessing import Pool
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
import line_enum as L
from line_complete import Direction, class_lattice, run_dir
from line_heights import raw_forms

HERE = Path(__file__).resolve().parent
EXE = str(HERE / "lc_fast")

def job_lines(a, b, P0, B, chunk):
    """the job lines of one direction (split into s-chunks for cheap directions, as line_complete.main)"""
    d = Direction(a, b, P0, B)
    X0, Y0 = P0
    Z = X0.denominator * Y0.denominator // math.gcd(X0.denominator, Y0.denominator)
    x0, y0 = int(X0 * Z), int(Y0 * Z)
    E = a*a + a*b + b*b; D = b**3 - a**3
    Ef = sorted(L.factor(E).items()); Df = sorted(L.factor(abs(a - b)).items()) if a != b else []
    H1 = int(d.H(d.Glo)) + 1
    ex = sorted(d.extra, key=lambda t: t[0])
    ext = []
    for p, lo, hi, levels in ex:
        q = p**hi
        ext.append(f"{p} {lo} {hi} {q} " + " ".join(f"{A % q} {B_ % q} {C % q}" for A, B_, C in d.prim))
    ents = []
    for k in range(1, len(ex) + 1):
        for T in combinations(ex, k):
            for lv in product(*[sorted(levels) for p, lo, hi, levels in T]):
                want = sorted((p, jj) for (p, *_), jj in zip(T, lv))
                Hx = int(d.H(d.Glo * math.prod(p**(jj - lo) for (p, lo, hi, _), jj in zip(T, lv)))) + 1
                for combo in product(*[[(p**jj, cs, cr) for cs, cr in levels[jj]] for (p, lo, hi, levels), jj in zip(T, lv)]):
                    u, v = class_lattice(combo)
                    ents.append(f"{Hx} {len(want)} " + " ".join(f"{p} {vv}" for p, vv in want) + f" {u[0]} {u[1]} {v[0]} {v[1]}")
    tail = (f" {x0} {y0} {Z} {E} {D} {a - b} {d.Glo} {len(Ef)} " + " ".join(f"{p} {e}" for p, e in Ef) +
            f" {len(Df)} " + " ".join(f"{p} {e}" for p, e in Df) + f" {len(ext)} " + " ".join(ext) + f" {len(ents)} " + " ".join(ents))
    k = 1
    if b**3 - a**3 <= 10**6:
        est = 2.5 * d.H(d.Glo)**2 + sum(2.5 * d.H(d.Glo * p**(jj - lo))**2 * len(lv[jj]) / p**jj for p, lo, hi, lv in d.extra for jj in lv)
        k = max(1, int(est / chunk))
    if k == 1: return [(a, b, 0, None, f"{a} {b} 0 -1 {H1}" + tail)]
    hm = d.hmax(); cuts = [round(hm * i / k) for i in range(k + 1)]
    return [(a, b, cuts[i] + (i > 0), cuts[i + 1], f"{a} {b} {cuts[i] + (i > 0)} {cuts[i + 1]} {H1}" + tail) for i in range(k)]

_proc = None
def _worker_init(B, triples):
    global _proc, _B
    _B = B
    args = [EXE, str(B)] + (["--triples"] if triples else [])
    _proc = subprocess.Popen(args, stdin=subprocess.PIPE, stdout=subprocess.PIPE, text=True, bufsize=1)

def run_one(job):
    """job = (a, b, P0, chunk, gp, skip): prepare the direction's jobs, run them in this worker's lc_fast"""
    a, b, P0, chunk, gp, skip = job
    out = []
    for (a_, b_, lo, hi, line) in job_lines(a, b, P0, _B, chunk):
        if (str(a_), str(b_), str(lo), str(hi)) in skip: continue
        _proc.stdin.write(line + "\n"); _proc.stdin.flush()
        rows = []
        while True:
            l = _proc.stdout.readline()
            if not l: raise RuntimeError("lc_fast died")
            if l.startswith("C "): out.append(("C", l[2:].strip(), rows)); break
            if l.startswith("F "):                                    # 128-bit overflow somewhere: Python fallback
                (_, _, lo2, hi2, tried, ntrip, km), res = run_dir((a, b, P0, _B, lo, hi, gp))
                rows = ["R " + f"{n};{len(r)};" + ",".join(f"{x}:{y}" for x, y in sorted(r, reverse=True)) for n, r in res]
                out.append(("C", f"{a};{b};{lo};{hi};{tried};{ntrip};{km};python", rows)); break
            rows.append(l.strip())
    return out

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--B", type=float, default=1e19); ap.add_argument("--cmax", type=float, default=1e6)
    ap.add_argument("--cmin", type=float, default=0); ap.add_argument("--only", default="")
    ap.add_argument("--out", required=True); ap.add_argument("--log", default="")
    ap.add_argument("--procs", type=int, default=8); ap.add_argument("--gp", default="gp")
    ap.add_argument("--chunk", type=float, default=2e7); ap.add_argument("--triples", action="store_true")
    ap.add_argument("--resume", action="store_true")
    A = ap.parse_args()
    if not os.path.exists(EXE) or os.path.getmtime(EXE) < os.path.getmtime(HERE / "lc_fast.cpp"):
        subprocess.run(["g++", "-O2", "-std=c++17", "-o", EXE, str(HERE / "lc_fast.cpp")], check=True)
    B = int(A.B)
    if A.only: dirs = [tuple(map(int, d.split(","))) for d in A.only.split(";")]
    else: dirs = [(a, b) for c, a, b in L.dirs_by_cost(int(A.cmax), L.allowed_f) if c > A.cmin]
    t0 = time.time(); P = L.conic_points(dirs, A.gp)
    skip = set()
    if A.resume and A.log and Path(A.log).exists():
        skip = {tuple(l.split(";")[:4]) for l in open(A.log) if l.strip()}
    jobs = [(a, b, P0, A.chunk, A.gp, skip) for (a, b), P0 in zip(dirs, P)]
    print(f"{len(dirs):,} directions, conic points {time.time() - t0:.0f} s" + (f", resume: {len(skip):,} jobs done" if skip else ""), flush=True)
    mode = "a" if A.resume else "w"; log = open(A.log, mode) if A.log else None
    slopes = trip = hits = nfall = 0; kmax = 0
    with open(A.out, mode) as f, Pool(A.procs, initializer=_worker_init, initargs=(B, A.triples)) as pool:
        if not A.resume: f.write(f"# line_fast.py: every coprime collinear triple with n <= {B} in {len(dirs)} directions "
                                 f"(cost {A.cmin:.3g} < c <= {A.cmax:.3g}{', only ' + A.only if A.only else ''}); "
                                 f"{'every triple (T n;pts)' if A.triples else 'every n counted exactly, k >= 4 listed as n;k;x:y,...'}\n")
        for res in pool.imap_unordered(run_one, jobs, chunksize=1):
            for kind, cert, rows in res:
                c = cert.split(";"); slopes += int(c[4]); trip += int(c[5]); kmax = max(kmax, int(c[6])); nfall += cert.endswith("python")
                for r in rows:
                    if r[0] == ("T" if A.triples else "R"): f.write(r[2:] + "\n"); hits += r[0] == "R"
                if log: log.write(cert + "\n")
            f.flush()
            if log: log.flush()
    print(f"done: {trip:,} triples, {slopes:,} slopes, {hits:,} rows with k >= 4, largest k {kmax}, python fallbacks {nfall}, "
          f"{time.time() - t0:.0f} s", flush=True)

if __name__ == "__main__":
    main()
