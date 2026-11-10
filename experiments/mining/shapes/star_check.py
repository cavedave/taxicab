#!/usr/bin/env python3
"""star_check.py -- step 1 of the shape plan: are four-ways 'stars' (one representation P whose chords to all three
others run in cheap directions)? Statistic: min over centres P (both orientations) of the max over the other three
representations Q (best orientation) of the chord cost |b^3 - a^3|. Exhaustive range n <= 2.5e23, by shape; control:
the same with the three partners taken from the next three four-ways (points not on the same curve)."""
import sys, math, collections, statistics
sys.path.insert(0, '.')
if hasattr(sys, "set_int_max_str_digits"): sys.set_int_max_str_digits(0)
from bowtie_mine import lines_of
def cost(P, Q):
    dx, dy = Q[0] - P[0], Q[1] - P[1]; g = math.gcd(dx, dy)
    if g == 0: return math.inf
    a, b = dy // g, -dx // g; return abs(b**3 - a**3)
def star(centres, others):
    best = math.inf
    for P0 in centres:
        for P in (P0, (P0[1], P0[0])):
            worst = max(min(cost(P, Q), cost(P, (Q[1], Q[0]))) for Q in others(P0))
            best = min(best, worst)
    return best
rows = []
for l in open('../../results/a047697_catalogue.txt'):
    if not l[0].isdigit(): continue
    g = l.split(';'); n = int(g[0]); reps = [tuple(map(int, p.split(':'))) for p in g[2].split(',')]
    if len(reps) == 4 and n <= 25 * 10**22: rows.append((n, reps, 'one line + free' if lines_of(reps) else 'no line'))
rows.sort()
th = [10**6, 10**9, 10**12]; res = collections.defaultdict(collections.Counter); N = collections.Counter(); vals = collections.defaultdict(list)
for i, (n, reps, shape) in enumerate(rows):
    s = star(reps, lambda P0: [r for r in reps if r != P0])
    N[shape] += 1; vals[shape].append(math.log10(s) / math.log10(n))
    for t in th: res[shape][t] += s <= t
    if i + 3 < len(rows):                                       # control: partners from the next three numbers
        others = [rows[i + 1][1][0], rows[i + 2][1][0], rows[i + 3][1][0]]
        c = star(reps[:1], lambda P0: others)
        N['control'] += 1; vals['control'].append(math.log10(c) / math.log10(n))
        for t in th: res['control'][t] += c <= t
print("four-ways n <= 2.5e23: share that are 'stars' (all three chords from one centre cost <= T)")
for k in ('one line + free', 'no line', 'control'):
    print(f"  {k:16s} N={N[k]:5d}  " + "  ".join(f"<=1e{int(math.log10(t))}: {res[k][t] / N[k]:6.1%}" for t in th)
          + f"   median log(worst cost)/log n {statistics.median(vals[k]):.3f}")
