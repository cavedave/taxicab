"""curve_ilp.py -- exact smallest L = lcm of >= k point denominators (integer program, SciPy/HiGHS). Pilot, 20 Oct 2026."""
import pickle, sys, math, time
import numpy as np
from scipy.optimize import milp, LinearConstraint, Bounds
from scipy.sparse import lil_matrix
sys.path.insert(0, "/Users/davidcurran/Documents/taxicab/experiments")
from curve_bounds import KNOWN

def solve(fac, ws, k, lmax_log, tlim=120):
    ws = [w for w in ws if math.log(w) <= lmax_log + 1e-9]
    levels = {}                                   # (p, e) -> var index
    for w in ws:
        for p, e in fac[w]:
            for j in range(1, e + 1): levels.setdefault((p, j), None)
    lv = sorted(levels); nx = len(ws); ny = len(lv)
    for i, key in enumerate(lv): levels[key] = nx + i
    n = nx + ny
    c = np.zeros(n); 
    for (p, j), idx in levels.items(): c[idx] = math.log(p)
    rows = []
    for i, w in enumerate(ws):
        for p, e in fac[w]: rows.append({i: 1, levels[(p, e)]: -1})          # x_w <= y_{p,e}
    for (p, j), idx in levels.items():
        if j > 1: rows.append({idx: 1, levels[(p, j - 1)]: -1})               # y_{p,j} <= y_{p,j-1}
    A = lil_matrix((len(rows) + 2, n))
    for r, row in enumerate(rows):
        for col, v in row.items(): A[r, col] = v
    A[len(rows), :nx] = 1                                                    # sum x >= k
    A[len(rows) + 1, :] = c                                                  # log L <= lmax
    lb = np.r_[np.full(len(rows), -np.inf), k, -np.inf]
    ub = np.r_[np.zeros(len(rows)), np.inf, lmax_log + 1e-9]
    t = time.time()
    res = milp(c, constraints=LinearConstraint(A.tocsr(), lb, ub), integrality=np.ones(n),
               bounds=Bounds(0, 1), options={"time_limit": tlim})
    if res.x is None: return None, time.time() - t, res.status
    L = 1
    for (p, j), idx in levels.items():
        if res.x[idx] > 0.5: L *= p
    cnt = sum(1 for w in ws if L % w == 0)
    return (L, cnt), time.time() - t, res.status

if __name__ == "__main__":
    f, kmin, kmax, wcap = sys.argv[1], int(sys.argv[2]), int(sys.argv[3]), float(sys.argv[4])
    M, r, pts, fac = pickle.load(open(f, "rb"))
    ws = [w for w, _, _ in pts if w <= wcap]
    for k in range(kmin, kmax + 1):
        lmax_log = (math.log(KNOWN[k]) - math.log(M)) / 3          # only L at least as good as published
        sol, dt, st = solve(fac, ws, k, lmax_log)
        if sol is None:
            print(f"M={M} k={k:2d} w<={wcap:.0e}: no L <= published ({dt:.1f}s, status {st})", flush=True); continue
        L, cnt = sol; n = M * L**3
        tag = "BEATS" if n < KNOWN[k] else "equals" if n == KNOWN[k] else "worse?"
        print(f"M={M} k={k:2d} w<={wcap:.0e}: optimum L={L} ({cnt} pts) -> n/published = {n/KNOWN[k]:.6g} {tag} ({dt:.1f}s, status {st})", flush=True)
