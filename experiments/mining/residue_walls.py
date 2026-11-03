#!/usr/bin/env python3
"""residue_walls.py -- FINDINGS F45: residue classes of n (m < 400) empty among the exhaustive four-ways, tested
against k = 1 census windows, the complete three-ways 1e17 - 1e19 (argv[1]/worf/k3_*.txt) and a geometric slope in k.
Usage: python3 residue_walls.py SCRATCH   (SCRATCH holds worf/ and ctrl/ from control_windows.py)"""
import sys, glob, random
from collections import Counter
S = sys.argv[1]; B = 25 * 10**22; random.seed(1)
def read(fn):
    for l in open(fn):
        if l[0].isdigit():
            p = l.split(";"); yield int(p[0]), int(p[1])
cat = [(n, k) for n, k in read("results/a047697_catalogue.txt") if n <= B]
E4 = [n for n, k in cat if k == 4]; E5 = [n for n, k in cat if k >= 5]
K3 = [n for f in glob.glob(S + "/worf/k3_*.txt") for n, k in read(f) if k == 3]
C1 = [n for f in glob.glob(S + "/ctrl/w_*.txt") for n, k in read(f) if k == 1]
C1 += random.sample([n for n, k in read(S + "/ctrl/wide_3e17.txt") if k == 1], 100000)
print(f"groups: k=1 {len(C1):,}  k=3 {len(K3):,}  k=4 {len(E4):,}  k=5 {len(E5)}")
walls = []
for m in range(2, 400):
    c1 = Counter(n % m for n in C1); c3 = Counter(n % m for n in K3); c4 = Counter(n % m for n in E4); c5 = Counter(n % m for n in E5)
    for r in c1:
        f1 = c1[r] / len(C1)
        e4 = f1 * len(E4)                         # expected four-ways in class r if k did not care
        if c4[r] == 0 and e4 >= 8:
            walls.append((m, r, f1, c3[r] / len(K3), e4))
# keep only "primitive" walls (not implied by a wall mod a divisor of m)
prim = []
for m, r, f1, f3, e4 in sorted(walls):
    if any(m % m2 == 0 and m2 < m and r % m2 == r2 for m2, r2, *_ in prim): continue
    prim.append((m, r, f1, f3, e4))
print(f"classes r mod m (m < 400) holding >= 8 expected four-ways but none observed: {len(walls)}; primitive: {len(prim)}")
for m, r, f1, f3, e4 in prim[:40]:
    print(f"  n = {r:3d} mod {m:3d}: k=1 share {100*f1:5.2f}%   k=3 share {100*f3:6.3f}%   four-ways expected {e4:6.1f}, seen 0")
print("\nclasses where even the k = 3 rate predicts >= 5 four-ways, but none are seen (m < 400, odd-n classes):")
c3all = {}
hits = []
for m in range(2, 400):
    c3 = Counter(n % m for n in K3); c4 = Counter(n % m for n in E4)
    for r, v in c3.items():
        e = v / len(K3) * len(E4)
        if c4[r] == 0 and e >= 5: hits.append((e, m, r, v))
for e, m, r, v in sorted(hits, reverse=True)[:25]:
    print(f"  n = {r} mod {m}: k=3 count {v:,}, four-ways expected {e:.1f} at the k=3 rate, seen 0")
print("\nlocal solution counts of x^3 + y^3 = r mod 13 (gcd(x, y, 13) = 1):")
N = Counter((x**3 + y**3) % 13 for x in range(13) for y in range(13) if (x, y) != (0, 0))
print({r: N[r] for r in range(13)})
print("share by k for n mod 13 = 1 or 12 / 5 or 8 / 0 / rest:")
for name, g in [("k=1", C1), ("k=3", K3), ("k=4", E4), ("k=5", E5)]:
    cl = Counter("+-1" if n % 13 in (1, 12) else "+-5" if n % 13 in (5, 8) else "0" if n % 13 == 0 else "other" for n in g)
    print(f"  {name}: " + "  ".join(f"{c} {100*cl[c]/len(g):.2f}%" for c in ("+-1", "+-5", "0", "other")))
import math
print("\nslope test: k=4 share predicted as share3 * sqrt(share3/share1) (geometric in k); classes seen 0 with prediction >= 3:")
res = []; ntests = 0
for m in range(2, 400):
    c1 = Counter(n % m for n in C1); c3 = Counter(n % m for n in K3); c4 = Counter(n % m for n in E4)
    for r in c3:
        s1 = c1[r] / len(C1); s3 = c3[r] / len(K3)
        if s1 == 0 or c1[r] < 30: continue
        pred = s3 * math.sqrt(s3 / s1) * len(E4); ntests += 1
        if pred >= 3 and c4[r] == 0: res.append((pred, m, r))
        if c4[r] > 0 and pred > 0: pass
print(f"  tests {ntests:,}; classes with 0 seen and >= 3 predicted: {len(res)}")
for pred, m, r in sorted(res, reverse=True)[:10]:
    print(f"  n = {r} mod {m}: predicted {pred:.1f}, P(0) = {math.exp(-pred):.1e}")
# calibration: overall predicted vs observed four-ways summed over the mod-13 classes
for m in (7, 9, 13, 19):
    c1 = Counter(n % m for n in C1); c3 = Counter(n % m for n in K3); c4 = Counter(n % m for n in E4)
    pr = {r: c3[r]/len(K3) * math.sqrt((c3[r]/len(K3)) / (c1[r]/len(C1))) for r in c3 if c1[r]}
    tot = sum(pr.values())
    print(f"  mod {m}: " + ", ".join(f"{r}: {len(E4)*pr[r]/tot:.0f}/{c4[r]}" for r in sorted(pr)))
