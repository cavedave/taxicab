#!/usr/bin/env python3
"""j4_nearmiss.py -- four-ways made of a line (P1, P2, P3) and a free representation F: the triangles with corners F, Pi, Pj
(sides: the line, F-Pi, F-Pj) have 4 integral points; the distance to a six-way is d(R_i) d(R_j), the denominators of the
two chord third points. Best triangle per four-way; ranking and clustering."""
import sys, math, collections
from fractions import Fraction as Fr
sys.path.insert(0, '.'); sys.path.insert(0, 'triangles')
if hasattr(sys, "set_int_max_str_digits"): sys.set_int_max_str_digits(0)
from near_miss import third
from bowtie_mine import lines_of
def den(R): return math.lcm(R[0].denominator, R[1].denominator)
rows = []
for l in open('../../results/a047697_catalogue.txt'):
    if not l[0].isdigit(): continue
    g = l.split(';'); n = int(g[0])
    if g[1] != '4': continue
    reps = [tuple(map(int, p.split(':'))) for p in g[2].split(',')]
    ls = lines_of(reps)
    if len(ls) != 1: continue
    d, T = ls[0]; on = {tuple(sorted(p)) for p in T}
    free = [r for r in reps if tuple(sorted(r)) not in on]
    if len(free) != 1: continue
    best = None
    for F in (free[0], (free[0][1], free[0][0])):
        for i in range(3):
            for j in range(i + 1, 3):
                Ri, Rj = third(F, T[i], n), third(F, T[j], n)
                if Ri is None or Rj is None: continue
                dist = den(Ri) * den(Rj)
                if best is None or dist < best[0]: best = (dist, den(Ri), den(Rj), F, T[i], T[j])
    if best: rows.append((best[0], n, d, best))
rows.sort()
print(len(rows), "four-ways of type line + free point")
print("best 15 (distance = d1 * d2):")
for dist, n, d, b in rows[:15]:
    print(f"  {dist:>10d} = {b[1]} x {b[2]:<8d} n = {n} ({len(str(n))} digits), line direction {d}")
# clustering: line directions among the best 2% vs all
top = rows[:max(1, len(rows) // 50)]
cnt_all = collections.Counter(d for _, _, d, _ in rows); cnt_top = collections.Counter(d for _, _, d, _ in top)
print(f"\nline directions: top 2% ({len(top)}) vs all ({len(rows)}); enrichment = share in top / share in all")
for d, c in cnt_top.most_common(10):
    print(f"  {str(d):12s} top {c:4d}  all {cnt_all[d]:5d}  enrichment {c / len(top) / (cnt_all[d] / len(rows)):5.2f}")
# size: log(distance) / log(n)
import statistics
r = [math.log(dist) / math.log(n) for dist, n, d, b in rows]
print(f"\nlog(distance)/log(n): min {min(r):.3f}, median {statistics.median(r):.3f}")
by = collections.defaultdict(list)
for dist, n, d, b in rows: by[len(str(n)) // 5 * 5].append(math.log(dist) / math.log(n))
for k in sorted(by): print(f"  n {k}-{k + 4} digits: {len(by[k]):5d} four-ways, median {statistics.median(by[k]):.3f}, min {min(by[k]):.3f}")
open('triangles/j4_nearmiss.txt', 'w').write("# distance;d1;d2;n;line direction;F;Pi;Pj\n" + "\n".join(f"{dist};{b[1]};{b[2]};{n};{d};{b[3]};{b[4]};{b[5]}" for dist, n, d, b in rows) + "\n")
