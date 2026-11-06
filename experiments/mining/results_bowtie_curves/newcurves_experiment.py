import sys, time, subprocess, re
from fractions import Fraction as Fr
from math import isqrt
sys.path.insert(0, "/Users/davidcurran/Documents/taxicab/experiments/mining")
import line_enum as L
from bowtie_mine import Curve
from bowtie_hunt import gp_points, factor_many, count_reps
import math
t0 = time.time()
pool = [(a, b) for c, a, b in L.dirs_by_cost(10**9, lambda f: True)]          # any coprime direction (second line need not be 'allowed')
dirs2 = []
for a, b in pool[:400]:
    for d in ((a, b), (b, a)): dirs2.append(d)
known_pairs = set()
res = {"curves": 0, "with point": 0, "rank>0": 0}; five = {}
H = int(sys.argv[1]) if len(sys.argv) > 1 else 150
for (a2, b2) in dirs2:
    if (a2, b2) in ((3, 4), (4, 3)): continue
    for i in range(3):
        C = Curve(3, 4, i, a2, b2); res["curves"] += 1
        qp = C.gp_poly()
        out = subprocess.run(["gp", "-q"], input=f"print(hyperellratpoints({qp}, {H}));", capture_output=True, text=True).stdout
        pts = re.findall(r"\[(-?\d+(?:/\d+)?), (-?\d+(?:/\d+)?)\]", out)
        pts = [(Fr(x), Fr(y)) for x, y in pts if Fr(y) != 0]
        if not pts: continue
        res["with point"] += 1
        xs, rank = gp_points(C, pts[:4], 2, 206, "gp", 60)
        if rank and rank.split()[0] not in ("0", "-1"): res["rank>0"] += 1
        for x in xs | {p[0] for p in pts}:
            o, why = C.bowtie(x.denominator, x.numerator)
            if o and o[0] < 10**300: five[o[0]] = (C, o)
print(res, f"{len(five)} distinct bowtie numbers < 1e300, {time.time() - t0:.0f} s")
cat = {int(l.split(';')[0]) for l in open('/Users/davidcurran/Documents/taxicab/results/a047697_catalogue.txt') if l[0].isdigit()}
new = [n for n in five if n not in cat]
print("new to the catalogue:", len(new), "digits:", sorted(len(str(n)) for n in new)[:30])
import pickle; pickle.dump({n: (five[n][0].a2, five[n][0].b2, five[n][0].i, five[n][1]) for n in five}, open(sys.argv[2], "wb"))
