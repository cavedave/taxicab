#!/usr/bin/env python3
"""dline_enum.py -- D-lines: lines through two coprime integer points of x^3 + y^3 = n and a third point R with
small denominator D (FINDINGS F30). Scaled by D they are ordinary integer triples on x^3 + y^3 = D^3 n whose two
outer points are multiples of D, so they come from the same conic parametrisation as line_enum.py; line_enum.py
drops them at its coprimality test. Two D-lines of the same n through the same R form a hub.

Directions (F30 conjecture): a b > 0, every prime = 2 (mod 3) to an even power; a b even for odd D, a b odd for
even D. --parity even (D = 3, 5, ...) or odd (D = 2, 4, 6, ...); triples with any 2 <= D <= --dmax are kept.

Output: n;D;a;b;c;x1:y1,x2:y2;X:Y   (n = the curve of the two integer points; R = (X/D, Y/D); c = a X + b Y on D^3 n)
Usage: python3 dline_enum.py --parity odd --dirs 30 --height 600 --nmax 1e32 --dmax 12 --out d.txt
"""
import argparse, math, time
from fractions import Fraction as F
from math import gcd
from multiprocessing import Pool
import line_enum as L

def norm_ok(parity):
    return lambda f: all(e % 2 == 0 for p, e in f.items() if p % 3 == 2) and (f.get(2, 0) > 0) == (parity == "even")

def norm_directions(count, parity):
    """the COUNT cheapest D-line directions of the given parity, true cost order (complete, like L.directions)"""
    cmax = 10**7
    while True:
        Ls = L.dirs_by_cost(cmax, norm_ok(parity))
        if len(Ls) >= count: return [(a, b) for _, a, b in Ls[:count]]
        cmax *= 2

def legacy_norm_directions(count, parity, amax=2000):
    """order used before 28 October 2026 (b < 2000 only; see L.legacy_directions)"""
    c = []
    for a in range(1, amax):
        for b in range(a + 1, amax):
            if b**3 - a**3 > 10**10: break
            if gcd(a, b) != 1: continue
            f = L.factor(a * b)
            if any(e % 2 for p, e in f.items() if p % 3 == 2): continue
            if (f.get(2, 0) > 0) != (parity == "even"): continue
            c.append((b**3 - a**3, a, b))
    c.sort()
    return [(a, b) for _, a, b in c[:count]]

def float_pts(a, b, P0, s, r):
    """the three real points of the line for real (s, r), scaled so that x^3 + y^3 > 0 (float chord_points)"""
    D = b**3 - a**3; x0, y0 = float(P0[0]), float(P0[1]); a2 = a * a
    Q = s*s + s*r + r*r; Bn = 2*x0*s + x0*r + y0*s + 2*y0*r
    NX = x0*Q - Bn*s; NY = y0*Q - Bn*r; T = Q*D
    P = [(b*p, T - a*p) for p in (NX - a2*Q, NY - a2*Q, -a2*Q - NX - NY)]
    return P if P[0][0]**3 + P[0][1]**3 > 0 else [(-x, -y) for x, y in P]

def pos_arcs(a, b, P0, M=20000, pad=2e-3):
    """angle intervals of (s, r) in [-pi/2, pi/2] whose line has two positive points (convexity: never three),
    scanned at M angles and widened by pad on each side (cubefree_plan.md step 3; checked by pos_slopes.py)"""
    th = [-math.pi/2 + math.pi*(i + 0.5)/M for i in range(M)]
    ok = [sum(x > 0 and y > 0 for x, y in float_pts(a, b, P0, math.cos(t), math.sin(t))) == 2 for t in th]
    out, i = [], 0
    while i < M:
        if ok[i]:
            j = i
            while j + 1 < M and ok[j + 1]: j += 1
            out.append((max(th[i] - pad, -math.pi/2), min(th[j] + pad, math.pi/2))); i = j + 1
        else: i += 1
    return out

def r_ranges(s, H, arcs):
    """the r in [-H, H] whose angle atan2(r, s) lies in one of the arcs (s >= 0), as merged integer ranges"""
    if arcs is None: return [(-H, H)]
    if s == 0: return [(1, 1)] if any(t2 >= math.pi/2 - 1e-12 or t1 <= -math.pi/2 + 1e-12 for t1, t2 in arcs) else []
    rs = []
    for t1, t2 in arcs:
        lo = -H if t1 <= -math.pi/2 + 1e-9 else max(-H, math.floor(s * math.tan(t1)))
        hi = H if t2 >= math.pi/2 - 1e-9 else min(H, math.ceil(s * math.tan(t2)))
        if lo <= hi: rs.append((lo, hi))
    return rs

def dtriples(a, b, P0, H, nmax, dmax, hero, s_lo, s_hi, positive=False):
    pts_of = L.chord_points(a, b, P0); seen = set(); out = []
    arcs = pos_arcs(a, b, P0) if positive else None
    for s in range(s_lo, s_hi + 1):
      for r_lo, r_hi in r_ranges(s, H, arcs):
        for r in range(r_lo, r_hi + 1):
            if (s == 0 and r != 1) or gcd(r, s) != 1: continue
            pts, c = pts_of(s, r)
            N = pts[0][0]**3 + pts[0][1]**3
            if N < 0: pts = [(-x, -y) for x, y in pts]; N = -N; cc = -c
            else: cc = c
            if N == 0 or any(x == 0 or y == 0 for x, y in pts): continue
            g = [gcd(x, y) for x, y in pts]
            i = [k for k in range(3) if g[k] == 1]
            if len(i) != 1: continue                              # exactly one coprime point: R
            j = [k for k in range(3) if k != i[0]]
            d = g[j[0]]
            if g[j[1]] != d or d > dmax or N % d**3: continue    # the two others share exactly the factor d
            n = N // d**3
            if n > nmax: continue
            if hero and not L.hero_ok(n, hero): continue
            P1, P2 = [(pts[k][0] // d, pts[k][1] // d) for k in j]
            if positive and min(P1 + P2) <= 0: continue          # cubefree hunt: both integer points positive
            if gcd(*P1) != 1 or gcd(*P2) != 1 or tuple(sorted(P1)) == tuple(sorted(P2)): continue
            key = (n, frozenset((tuple(sorted(P1)), tuple(sorted(P2)))))
            if key in seen: continue
            seen.add(key)
            R = pts[i[0]]
            assert P1[0]**3 + P1[1]**3 == n and R[0]**3 + R[1]**3 == d**3 * n
            out.append((n, d, cc, P1, P2, R))
    return out

def run(job):
    a, b, P0, H, nmax, dmax, hero, core, lo, hi, pmax, positive = job
    L.HERO_CORE = core; L.set_hero_pmax(pmax)
    return (a, b, lo, hi), dtriples(a, b, P0, H, nmax, dmax, hero, lo, hi, positive)

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--parity", choices=["even", "odd"], required=True, help="a b even (odd D) or odd (even D)")
    ap.add_argument("--dirs", type=int, default=30); ap.add_argument("--skip", type=int, default=0)
    ap.add_argument("--only", default="", help="explicit directions 'a,b;a,b'")
    ap.add_argument("--dirs-file", default="", help="explicit directions, one 'a,b' per line")
    ap.add_argument("--hero-pmax", type=int, default=200, help="count split primes below this bound in the hero filter")
    ap.add_argument("--height", type=int, default=200); ap.add_argument("--nmax", type=float, default=1e17)
    ap.add_argument("--dmax", type=int, default=12)
    ap.add_argument("--hero", type=int, default=0); ap.add_argument("--core", type=int, default=0)
    ap.add_argument("--procs", type=int, default=6); ap.add_argument("--chunks", type=int, default=1)
    ap.add_argument("--gp", default="gp"); ap.add_argument("--out", required=True)
    ap.add_argument("--short", action="store_true", help="write only n;D;a;b")
    ap.add_argument("--positive", action="store_true", help="only D-lines with both integer points positive, "
                    "enumerating only the slope arcs where that is possible (about 5x faster)")
    A = ap.parse_args()
    if A.dirs_file:
        dirs = [tuple(map(int, l.split(","))) for l in open(A.dirs_file) if l.strip() and l[0] != "#"]
    else:
        dirs = ([tuple(map(int, d.split(","))) for d in A.only.split(";")] if A.only
                else norm_directions(A.skip + A.dirs, A.parity)[A.skip:])
    P = L.conic_points(dirs, A.gp)
    H, k = A.height, A.chunks
    cuts = [-1 + round((H + 1) * i / k) for i in range(k + 1)]
    jobs = [(a, b, P0, H, int(A.nmax), A.dmax, A.hero, A.core, cuts[i] + 1, cuts[i + 1], A.hero_pmax,
             A.positive)
            for (a, b), P0 in zip(dirs, P) for i in range(k) if cuts[i + 1] > cuts[i]]
    t0 = time.time(); total = 0
    with L.out_open(A.out) as f, Pool(A.procs) as pool:
        for (a, b, lo, hi), T in pool.imap_unordered(run, jobs):
            for n, d, c, P1, P2, R in T:
                f.write(f"{n};{d};{a};{b}\n" if A.short else f"{n};{d};{a};{b};{c};{P1[0]}:{P1[1]},{P2[0]}:{P2[1]};{R[0]}:{R[1]}\n")
            total += len(T)
            print(f"  ({a},{b}) s={lo}..{hi}: {len(T)} D-lines  [{time.time()-t0:.0f}s]", flush=True)
    print(f"{total} D-lines from {len(dirs)} directions -> {A.out}")

if __name__ == "__main__":
    main()
