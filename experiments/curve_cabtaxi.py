#!/usr/bin/env python3
"""curve_cabtaxi.py -- Cabtaxi upper bounds Ca(k) from rational points on x^3 + y^3 = M.

Same method as the taxicab work (curve_bounds.py + curve_ilp.py), but a rational point (x, y)
counts whether or not one coordinate is negative: n = M L^3 = (xL)^3 + (yL)^3 with integers of
either sign is a cabtaxi representation. P and -P give the same unordered pair.

For each curve: generators (ellrank + ellsaturation), every point of height <= HMAX (qfminim),
PARI factorisation of the denominators, then for each k the exact smallest L (integer program)
that is a multiple of >= k point denominators. Results are compared with cabtaxi_known.csv
(Boyer 2008, Su 2016) and every reported n is re-verified with exact integer arithmetic.

Usage:  python3 curve_cabtaxi.py --curve 3956875867 --kmin 19 --kmax 57 [--hmax 80] [--out file]
"""
import argparse, math, os, subprocess, sys, tempfile, time
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from curve_ilp import solve

GP = r"""
default(parisizemax, 4*10^9);
M = %(M)d; hmax = %(hmax)s;
E = ellinit([0,0,0,0,-432*M^2]);
R = ellrank(E, %(effort)d);
if(R[1] != R[2], print("#WARN rank only bounded: ", R[1], " <= r <= ", R[2]));
G = ellsaturation(E, R[4], 1000);
print("#RANK ", #G);
V = qfminim(ellheightmatrix(E, G), hmax, 2000000, 2)[3];
print("#VECTORS ", #V);
{
  for(j = 1, #V,
    my(v = V[,j], P = [0], x, y, w, F);
    for(i = 1, #G, if(v[i], P = elladd(E, P, ellmul(E, G[i], v[i]))));
    if(P == [0], next);
    x = (36*M + P[2])/(6*P[1]); y = (36*M - P[2])/(6*P[1]);
    if(x == 0 || y == 0, next);
    w = lcm(denominator(x), denominator(y)); F = factor(w, %(flim)s);
    print("P;", w, ";", numerator(x*w), ";", numerator(y*w), ";", Vec(F[,1]), ";", Vec(F[,2])));
}
quit;
"""

def points(gp, M, hmax, effort, flim="0"):
    """flim = 0: full factorisation; else trial division to flim, any cofactor kept as one unit (still exact)."""
    with tempfile.NamedTemporaryFile("w", suffix=".gp", delete=False) as f:
        f.write(GP % dict(M=M, hmax=hmax, effort=effort, flim=flim)); path = f.name
    try:
        out = subprocess.run([gp, "-q", path], capture_output=True, text=True, check=True).stdout
    finally:
        os.unlink(path)
    pts, fac, info = {}, {}, {}
    for line in out.replace(" ", "").splitlines():
        if line.startswith("#"):
            key = line[1:].split(":")[0] if line.startswith("#WARN") else line[1:]
            info[line[1:6]] = line[1:]
        elif line.startswith("P;"):
            _, w, u, v, ps, es = line.split(";")
            w, u, v = int(w), int(u), int(v)
            assert u**3 + v**3 == M * w**3, "point check failed"
            a, b = sorted((u, v))
            pts[(w, a, b)] = True
            fac[w] = list(zip(eval(ps), eval(es)))
    return sorted(pts), fac, info

def sci(n):                                                 # 1.234567e+400 without going through float
    s = str(n); return f"{s[0]}.{s[1:7]}e+{len(s) - 1}"

def load_known(path):
    known = {}
    for line in open(path):
        if line.startswith("#"): continue
        k, n, _ = line.split(";", 2); known[int(k)] = int(n)
    return known

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--gp", default="gp")
    ap.add_argument("--curve", type=int, required=True)
    ap.add_argument("--kmin", type=int, default=10)
    ap.add_argument("--kmax", type=int, default=57)
    ap.add_argument("--hmax", default="80")
    ap.add_argument("--effort", type=int, default=1)
    ap.add_argument("--flim", default="0", help="0 = factor denominators fully; else trial-divide to this bound")
    ap.add_argument("--slack", type=float, default=1e6, help="search up to this factor above the published bound")
    ap.add_argument("--tlim", type=float, default=600)
    ap.add_argument("--nolimit", type=float, default=600, help="digits allowed when there is no published bound")
    ap.add_argument("--known", default=os.path.join(os.path.dirname(os.path.abspath(__file__)), "cabtaxi_known.csv"))
    ap.add_argument("--out", help="append k;n;M;L;pairs for every bound found")
    a = ap.parse_args()
    M = a.curve; known = load_known(a.known)
    t = time.time()
    pts, fac, info = points(a.gp, M, a.hmax, a.effort, a.flim)
    print(f"curve M={M}: {' '.join(info.values())}; {len(pts)} points (both signs), {time.time()-t:.0f}s", flush=True)
    ws = [w for w, _, _ in pts]
    for k in range(a.kmin, a.kmax + 1):
        ref = known.get(k)
        cap = (math.log(ref) + math.log(a.slack) if ref else math.log(10.0) * a.nolimit) - math.log(M)
        sol, dt, st = solve(fac, ws, k, cap / 3, tlim=a.tlim)
        if sol is None:
            print(f"  k={k:2d}: nothing within {a.slack:.0e} x published ({dt:.1f}s, status {st})", flush=True); continue
        L, cnt = sol; n = M * L**3
        good = sorted({(u * (L // w), v * (L // w)) for w, u, v in pts if L % w == 0})
        assert len(good) >= k and all(x**3 + y**3 == n for x, y in good), "verification failed"
        cmp = "no published bound" if not ref else ("BEATS published" if n < ref else
              "equals published" if n == ref else f"{sci(n // ref)}x published")
        print(f"  k={k:2d}: n = {sci(n)} ({len(str(n))} digits, {len(good)} reps) {cmp}  "
              f"[{dt:.1f}s{'' if st == 0 else ', status ' + str(st)}]", flush=True)
        if a.out:
            with open(a.out, "a") as f:
                f.write(f"{k};{n};{M};{L};" + ",".join(f"{x}:{y}" for x, y in good) + "\n")

if __name__ == "__main__":
    main()
