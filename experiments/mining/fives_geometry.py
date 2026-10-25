#!/usr/bin/env python3
"""fives_geometry.py -- rank-free geometry of k-ways: lines, hubs and chord near-misses (exact rationals).

For representations P = (x, y) of n (the swap (y, x) is -P), the third point of the line through two points is
R = ((x1^2 y - x^2 y1)/(x y - x1 y1), (x y1^2 - x1 y^2)/(x y - x1 y1))   (Werebrusow; Dickson vol. 2 p. 562).
- line : R is (up to swap) another representation              -> collinear triple
- hub  : two chords on disjoint pairs give the same R (up to swap) -> 4-term relation
- near-miss : for chords whose R is not a representation, the denominator of R (1 would be a new representation)
Usage: python3 fives_geometry.py file.txt   (n;k;x:y,... lines)
"""
import itertools, sys
from fractions import Fraction as F

def third(P, Q):
    (x, y), (x1, y1) = P, Q
    den = x * y - x1 * y1
    if den == 0: return None
    return (F(x1*x1*y - x*x*y1, den), F(x*y1*y1 - x1*y*y, den))

def canon(R):                           # unordered pair: identify R with its swap (-R)
    return tuple(sorted(R))

for line in open(sys.argv[1]):
    n, k, ps = line.strip().split(";"); n = int(n)
    pts = [tuple(map(int, q.split(":"))) for q in ps.split(",")]
    reps = {canon(p) for p in pts}
    lines, chords = [], {}
    for i, j in itertools.combinations(range(len(pts)), 2):
        for Q in (pts[j], (pts[j][1], pts[j][0])):                # chord through P_i and +-P_j
            R = third(pts[i], Q)
            if R is None: continue
            assert R[0]**3 + R[1]**3 == n
            c = canon(R)
            if c in {canon((F(a), F(b))) for a, b in pts}:
                l = frozenset((i, j, [canon((F(a), F(b))) for a, b in pts].index(c)))
                if len(l) == 3 and l not in lines: lines.append(l)
            else:
                chords.setdefault(c, set()).add(frozenset((i, j)))
    hubs = [(R, P) for R, P in chords.items() if any(not (a & b) for a, b in itertools.combinations(P, 2))]
    den = sorted({max(R[0].denominator, R[1].denominator) for R in chords})
    shared = set.intersection(*[set(l) for l in lines]) if len(lines) >= 2 else set()
    pos = []
    for l in lines:                                               # is the shared point between the other two on the line?
        if shared and next(iter(shared)) in l:
            s = next(iter(shared)); xs = sorted(pts[i][0] for i in l)
            pos.append("middle" if xs[1] == pts[s][0] or xs[1] == pts[s][1] else "end")
    sp = pts[next(iter(shared))] if shared else None
    print(f"{n:>30}: lines {len(lines)}, hubs {len(hubs)}, shared point {sp} ({'sum' if sp and sp[1] > 0 else 'difference' if sp else '-'}) "
          f"{pos}; smallest chord denominator {den[0] if den else '-'} (log10 {len(str(den[0])) - 1 if den else '-'})")
