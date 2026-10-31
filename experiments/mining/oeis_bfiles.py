# candidate b-files: A293648 / A293651 / A293649 (not a sum of two non-coprime nonzero cubes) from complete cabtaxi output
import sys
sys.path.insert(0, "/Users/davidcurran/Documents/taxicab/experiments/mining")
from collisions import all_reps, factor_batch
def load(f):
    d = {}
    for l in open(f):
        if l[0].isdigit():
            n, k, r = l.strip().split(";"); d[int(n)] = [tuple(map(int, p.split(":"))) for p in r.split(",")]
    return d
def nonco(n, fac, positive):
    cubes = [1]
    for p, e in fac:
        cubes = [c * p**j for c in cubes for j in range(e // 3 + 1)]
    for d in cubes:
        if d == 1: continue
        m = n // d**3
        mf = []
        for p, e in fac:
            dd = 0; x = d
            while x % p == 0: x //= p; dd += 1
            if e - 3*dd: mf.append((p, e - 3*dd))
        R = all_reps(m, mf) if m > 1 else set()
        if any((not positive) or min(r) > 0 for r in R): return True
    return False
def build(a, src, B, kmin, positive, nterms=10000):
    d = load(src)
    cand = sorted(n for n, R in d.items() if n <= B and (sum(min(r) > 0 for r in R) if positive else len(R)) >= kmin)
    fs = factor_batch(cand, "gp")
    out = [n for n, f in zip(cand, fs) if not nonco(n, f, positive)][:nterms]
    with open(f"new_b{a}.txt", "w") as g:
        for i, n in enumerate(out, 1): g.write(f"{i} {n}\n")
    old = [int(l.split()[1]) for l in open(f"b{a}.txt") if l.strip() and l[0] != "#"]
    lo = [n for n in out if n <= old[-1]]
    print(f"A{a}: {len(out)} terms from {src} (complete to {B:.0e}); last {out[-1]:.4e}; old b-file {len(old)} terms; "
          f"ours <= old last: {len(lo)}; old subset of ours: {set(old) <= set(out)}; missing from old: {len(set(lo) - set(old))}")
build("293648", "k2_1e13.txt", 10**13, 2, False)
build("293649", "k2_1e13.txt", 10**13, 2, True)
build("293651", "k3_1e15.txt", 10**15, 3, False)
