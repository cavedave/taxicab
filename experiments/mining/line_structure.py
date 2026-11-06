#!/usr/bin/env python3
"""line_structure.py -- the line structure of each k-way, and where the line search would (or could not) find it.

For every n;k;x:y,... line it finds, exactly:
  - every collinear triple among the representations and their swaps (a line a x + b y = c, Theorem 1 direction);
  - for each line: the canonical direction (a < b, as line_enum.py uses), its cost D = b^3 - a^3, its cost RANK
    among all allowed directions, and the smallest slope height max(|r|, s) at which line_enum.py reaches it
    (minimum over the 6 orderings of the triple);
  - hubs: two chords on disjoint pairs with the same third point (a 4-term relation, as fives_geometry.py);
  - the shape: independent / line+free / hub / bowtie / ... and the --core 0 filter verdict.
Output: one row per (n, line) to --out (CSV), and a summary on stdout.

Usage: python3 line_structure.py file.txt [file.txt ...] --out rows.csv [--kmin 4] [--gp gp]
"""
import argparse, csv, itertools, subprocess, sys
from fractions import Fraction as F
from math import gcd
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
import line_enum as L

def all_directions(dmax=10**10):
    """rank of every allowed direction with cost <= DMAX, in true cost order (L.dirs_by_cost, complete)"""
    return {(a, b): i + 1 for i, (_, a, b) in enumerate(L.dirs_by_cost(dmax, L.allowed_f))}

def lines_of(pts):
    """all collinear triples among the points and their swaps, as (a, b, c, triple) with 0 < a < b"""
    P = pts + [(y, x) for x, y in pts]
    out = {}
    for T in itertools.combinations(P, 3):
        if len({tuple(sorted(p)) for p in T}) < 3: continue
        (x1, y1), (x2, y2), (x3, y3) = T
        if (x2 - x1) * (y3 - y1) != (y2 - y1) * (x3 - x1): continue
        a, b = y2 - y1, x1 - x2; g = gcd(a, b); a //= g; b //= g
        if a < 0 or (a == 0 and b < 0): a, b = -a, -b
        T = list(T)
        if a > b: a, b = b, a; T = [(y, x) for x, y in T]       # swap coordinates: direction (b, a) -> (a, b)
        key = frozenset(tuple(sorted(p)) for p in T)
        if key not in out: out[key] = (a, b, a * T[0][0] + b * T[0][1], T)
    return list(out.values())

def height(a, b, c, T, P0):
    """smallest slope height at which line_enum.triples(a, b, P0, ...) produces this triple"""
    D = b**3 - a**3; s0 = F(-3 * a * a, D); X0, Y0 = P0; best = None
    for cc, TT in ((c, T), (-c, [(-x, -y) for x, y in T])):
        us = [F(x, cc) for x, y in TT]
        for u1, u2, _ in itertools.permutations(us):
            X1, Y1 = (u1 - s0 / 3) * D, (u2 - s0 / 3) * D
            dX, dY = X1 - X0, Y1 - Y0
            if dX == 0 and dY == 0: h = 0
            else:
                g = F(dX).numerator * F(dY).denominator, F(dY).numerator * F(dX).denominator   # (s, r) up to scale
                s_, r_ = g; d = gcd(s_, r_); s_ //= d; r_ //= d
                if s_ < 0 or (s_ == 0 and r_ < 0): s_, r_ = -s_, -r_
                h = max(abs(r_), s_)
            best = h if best is None else min(best, h)
    return best

def third(P, Q):
    (x, y), (x1, y1) = P, Q
    den = x * y - x1 * y1
    if den == 0: return None
    return tuple(sorted((F(x1*x1*y - x*x*y1, den), F(x*y1*y1 - x1*y*y, den))))

def hubs(pts):
    reps = {tuple(sorted(p)) for p in pts}; ch = {}
    for i, j in itertools.combinations(range(len(pts)), 2):
        for Q in (pts[j], pts[j][::-1]):
            R = third(pts[i], Q)
            if R is None or tuple(int(v) for v in R) in reps and all(v.denominator == 1 for v in R): continue
            ch.setdefault(R, set()).add(frozenset((i, j)))
    return sum(1 for S in ch.values() if any(not (p & q) for p, q in itertools.combinations(S, 2)))

def shape(k, lines, nh):
    if not lines: return "hub" if nh else "independent"
    if len(lines) == 1: return "line+" + ("free" if k == 4 else f"{k-3}free") + ("+hub" if nh and k > 4 else "")
    if len(lines) == 2:
        shared = set.intersection(*[{tuple(sorted(p)) for p in l[3]} for l in lines])
        return ("bowtie" if shared else "2 disjoint lines") + (f"+{k-5}free" if k > 5 else "")
    return f"{len(lines)} lines"

def main():
    ap = argparse.ArgumentParser(); ap.add_argument("files", nargs="+"); ap.add_argument("--out", required=True)
    ap.add_argument("--kmin", type=int, default=4); ap.add_argument("--gp", default="gp")
    A = ap.parse_args()
    rows, seen = [], set()
    for fn in A.files:
        for l in open(fn):
            if l[0] == "#" or ";" not in l: continue
            p = l.strip().split(";")
            n, k = int(p[0]), int(p[1]); pts = [tuple(map(int, q.split(":"))) for q in p[-1].split(",")]
            if k < A.kmin or n in seen: continue
            seen.add(n); assert len(pts) == k and all(x**3 + y**3 == n for x, y in pts)
            rows.append((n, k, pts))
    rank = all_directions()
    found = [(n, k, pts, lines_of(pts)) for n, k, pts in rows]
    dirs = sorted({(a, b) for *_, ls in found for a, b, _, _ in ls})
    P0 = dict(zip(dirs, L.conic_points(dirs, A.gp))) if dirs else {}
    L.HERO_CORE = 0
    with open(A.out, "w", newline="") as f:
        w = csv.writer(f); w.writerow(["n", "k", "shape", "core0", "a", "b", "D", "rank", "c_over_E", "height"])
        stats = {}
        for n, k, pts, ls in found:
            sh = shape(k, ls, hubs(pts) if len(ls) < 2 else 0); core = L.hero_ok(n, 4)
            stats.setdefault((k, sh), 0); stats[(k, sh)] += 1
            if not ls: w.writerow([n, k, sh, int(core), "", "", "", "", "", ""])
            for a, b, c, T in ls:
                E = a*a + a*b + b*b; assert c % E == 0
                w.writerow([n, k, sh, int(core), a, b, b**3 - a**3, rank.get((a, b), ">" + str(len(rank))),
                            c // E, height(a, b, c, T, P0[(a, b)])])
    for (k, sh), v in sorted(stats.items()): print(f"k={k}  {sh:20s} {v}")

if __name__ == "__main__":
    main()
