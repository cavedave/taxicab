"""For one curve: hunt-style beam (width 10, w <= 1e12) vs exact ILP on all points of height <= 80."""
import os, sys, math, pickle, subprocess, time
sys.path.insert(0, "/Users/davidcurran/Documents/taxicab/experiments"); sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import curve_bounds as cb
from curve_ilp import solve
M = int(sys.argv[1]); kmin, kmax = 6, 22
rank, pts = cb.run_gp("/opt/homebrew/bin/gp", M, [], "80", 10**60, timeout=3600, verbose=False)
pickle.dump((M, rank, pts), open(f"p{M}.pkl", "wb"))
subprocess.run(["python3", os.path.join(os.path.dirname(os.path.abspath(__file__)), "curve_factor_pts.py"), f"p{M}.pkl", f"f{M}.pkl"], check=True, capture_output=True)
_, _, _, fac = pickle.load(open(f"f{M}.pkl", "rb"))
capped = [p for p in pts if p[0] <= 10**12]
bm = cb.beam(M, capped, 10**165, {1}, 10)
ws = [w for w, _, _ in pts]
line = []
for k in range(kmin, kmax + 1):
    cap = (math.log(cb.KNOWN[k]) + math.log(1e40) - math.log(M)) / 3       # look up to 1e40 x published
    sol, dt, st = solve(fac, ws, k, cap, tlim=300)
    b = bm.get(k, (None,))[0]
    rb = math.log10(b / cb.KNOWN[k]) if b else None
    ri = math.log10(M * sol[0]**3 / cb.KNOWN[k]) if sol else None
    line.append((k, rb, ri, dt, st))
print(f"M={M} rank={rank} points={len(pts)} (w<=1e12: {len(capped)})")
for k, rb, ri, dt, st in line:
    f = lambda r: "   >1e40" if r is None else f"{10**r:9.3g}"
    gain = "" if (rb is None or ri is None) else f"  beam/optimum = {10**(rb-ri):.3g}"
    print(f"  k={k:2d}  beam {f(rb)}  optimum {f(ri)} x published{gain}  ({dt:.1f}s{'' if st == 0 else ', status ' + str(st)})")
