#!/usr/bin/env python3
"""line_heights.py -- rigorous per-direction slope heights for line_enum.py (six_way_ideas.md, idea 1).

For a direction (a, b) and the conic point P0 that line_enum uses, the raw points of slope (s, r) are
(b p_i, T - a p_i), quadratic forms in (s, r); line_enum divides them by G = gcd of the six values. By Theorem 13,
  n = E * S1 S2 S3 / ((a - b)^2 G^3),   S_i(s, r) = x_i + y_i of raw point i (a quadratic form).
- Each S_i is definite (discriminant -3 k^2, checked here), so |S_i| >= lam_i (s^2 + r^2) >= lam_i h^2, h = max(|r|, s).
- G divides R0 = gcd of the pairwise resultants of the six coordinate forms (gcd of two binary forms at coprime
  (s, r) divides their resultant), so G = gcd(values mod p^e) prime by prime and depends on (s, r) mod R0.
Hence for a slope whose gcd is G:  |n| >= E lam1 lam2 lam3 h^6 / ((a - b)^2 G^3), and n <= B forces
  h <= H(G) = (B (a - b)^2 G^3 / (E lam1 lam2 lam3))^(1/6).
The search is complete for n <= B if every slope with G = g is enumerated to height H(g).

Usage: python3 line_heights.py --dirs 3,4 12,13 --B 1e30 [--check-B 1e17 --check-factor 3]
  --check-B: brute-force every slope to check-factor x H(Gmax) and confirm no triple with n <= check-B lies beyond its bound.
"""
import argparse, math
from math import gcd
from collections import Counter
import line_enum as L

def raw_forms(a, b, P0):
    """the six coordinate forms and the three S forms, as coefficient triples (A, B, C) of A s^2 + B s r + C r^2"""
    D = b**3 - a**3; X0, Y0 = P0
    Z = X0.denominator * Y0.denominator // gcd(X0.denominator, Y0.denominator); x0, y0 = int(X0 * Z), int(Y0 * Z); a2 = a * a
    def raw(s, r):
        Q = s*s + s*r + r*r; Bn = 2*x0*s + x0*r + y0*s + 2*y0*r
        NX = x0*Q - Bn*s; NY = y0*Q - Bn*r; W = Z*Q; T = W*D
        ps = (NX - a2*W, NY - a2*W, -a2*W - NX - NY)
        return [(b*p, T - a*p) for p in ps]
    def coeffs(f):
        A = f(1, 0); C = f(0, 1); return (A, f(1, 1) - A - C, C)
    coord = [coeffs(lambda s, r, i=i, j=j: raw(s, r)[i][j]) for i in range(3) for j in range(2)]
    S = [coeffs(lambda s, r, i=i: sum(raw(s, r)[i])) for i in range(3)]
    return raw, coord, S

def res(f, g):
    """resultant of two binary quadratic forms"""
    (a1, b1, c1), (a2, b2, c2) = f, g
    return (a1*c2 - a2*c1)**2 - (a1*b2 - a2*b1) * (b1*c2 - b2*c1)

def lam_min(f):
    """smallest |eigenvalue| of a definite form, a lower bound for |f(s, r)| / (s^2 + r^2)"""
    A, B, C = f
    disc = B*B - 4*A*C
    assert disc < 0, "form not definite"
    tr = abs(A + C); return (tr - math.sqrt((A - C)**2 + B*B)) / 2

def prod_min(S):
    """exact min of |S1 S2 S3| on the square max(|s|, |r|) = 1 (s >= 0 half suffices: the forms are even in (s, r)):
    edges s = 1, r in [-1, 1] and r = +-1, s in [0, 1]; each is a degree-6 polynomial, minimised at the ends or at real
    roots of its derivative (numpy, then the true values are evaluated in exact rationals)"""
    from fractions import Fraction as Fr
    try:
        import numpy as np
    except ImportError:
        np = None
    def P(s, r):
        v = 1
        for A, B_, C in S: v *= A*s*s + B_*s*r + C*r*r
        return abs(v)
    best = None
    for edge in ("s1", "r+1", "r-1"):
        # sample the polynomial at 7 points to get its coefficients in t, t in [-1, 1] (edge s1) or [0, 1]
        ts = [Fr(k, 6) for k in range(-6, 7, 2)] if edge == "s1" else [Fr(k, 6) for k in range(7)]
        f = (lambda t: P(1, t)) if edge == "s1" else (lambda t: P(t, 1 if edge == "r+1" else -1))
        lo, hi = (-1, 1) if edge == "s1" else (0, 1)
        if np is not None:
            V = np.array([[float(t)**j for j in range(7)] for t in ts]); y = np.array([float(f(t)) for t in ts])
            c = np.linalg.solve(V, y)                                  # coefficients c0..c6
            crit = [r_.real for r_ in np.roots(np.polyder(c[::-1])) if abs(r_.imag) < 1e-9]
            cand = [lo, hi] + [t for t in crit if lo <= t <= hi]
            m = min(float(f(Fr(t).limit_denominator(10**12))) for t in cand)
        else:
            raise SystemExit("prod_min needs numpy (pip3 install --user numpy); no non-rigorous fallback")

        best = m if best is None else min(best, m)
    return best * (1 - 1e-9)                                           # small safety margin for the root location

def factor(m):
    return L.factor(m)

def g_classes(raw, R0):
    """distribution of G over projective residues (s : r) prime by prime: {p: Counter(v_p(G))} and the attained G values"""
    out = {}
    for p, e in factor(R0).items():
        q = p**e; cnt = Counter()
        pts = [(1, r) for r in range(q)] + [(s, 1) for s in range(0, q, p)]          # projective points mod p^e
        for s, r in pts:
            g = 0
            for x, y in raw(s, r): g = gcd(g, gcd(x, y))
            g = gcd(g, q); cnt[g] += 1
        out[p] = cnt
    vals = [1]
    for p, cnt in out.items(): vals = [v * g for v in vals for g in cnt]
    return out, sorted(set(vals))

def heights(a, b, P0, B):
    raw, coord, S = raw_forms(a, b, P0)
    R0 = 0
    for i in range(6):
        for j in range(i + 1, 6):
            R0 = gcd(R0, res(coord[i], coord[j]))
    discs = [B_*B_ - 4*A*C for A, B_, C in S]
    lam = [lam_min(f) for f in S]
    E = a*a + a*b + b*b
    M = prod_min(S)                                                     # |S1 S2 S3| >= M h^6 (tighter than lam1 lam2 lam3)
    H = lambda g: (B * (a - b)**2 * g**3 / (E * M)) ** (1 / 6)
    cls, vals = g_classes(raw, R0)
    return dict(R0=R0, discs=discs, lam=lam, M=M, classes=cls, G=vals, H={g: H(g) for g in vals}, raw=raw)

def brute_check(a, b, P0, Bc, factor_=3):
    """every slope up to factor_ x H(Gmax): no triple (coprime, n <= Bc) may lie beyond its own class bound"""
    info = heights(a, b, P0, Bc); raw = info["raw"]; Hmax = max(info["H"].values())
    E = a*a + a*b + b*b; lam = info["lam"]; worst = 0.0; found = 0; beyond = 0
    lim = int(factor_ * Hmax) + 1
    for s in range(0, lim + 1):
        for r in range(-lim, lim + 1):
            if (s == 0 and r != 1) or gcd(r, s) != 1: continue
            pts = raw(s, r); G = 0
            for x, y in pts: G = gcd(G, gcd(x, y))
            n = abs((pts[0][0] // G)**3 + (pts[0][1] // G)**3)
            if n == 0 or n > Bc: continue
            h = max(abs(r), s); found += 1
            Hg = (Bc * (a - b)**2 * G**3 / (E * info["M"])) ** (1 / 6)
            worst = max(worst, h / Hg); beyond += h > Hg
    return found, beyond, worst, lim

def main():
    ap = argparse.ArgumentParser(); ap.add_argument("--dirs", nargs="+", default=["3,4", "12,13", "3,16", "16,21", "27,28"])
    ap.add_argument("--B", type=float, default=1e30); ap.add_argument("--check-B", type=float, default=0)
    ap.add_argument("--check-factor", type=float, default=3); ap.add_argument("--gp", default="gp")
    A = ap.parse_args()
    dirs = [tuple(map(int, d.split(","))) for d in A.dirs]
    for (a, b), P0 in zip(dirs, L.conic_points(dirs, A.gp)):
        info = heights(a, b, P0, A.B)
        share = {}
        for p, cnt in info["classes"].items():
            tot = sum(cnt.values()); share[p] = {g: f"{c/tot:.3f}" for g, c in sorted(cnt.items())}
        print(f"({a},{b}) cost {b**3 - a**3:,} E {a*a + a*b + b*b}: S discriminants {sorted(set(info['discs']))}; R0 = {info['R0']:,} = {factor(info['R0'])}")
        print(f"   G classes per prime (G-part: share of slopes): {share}")
        print(f"   heights for B = {A.B:.0e}: " + ", ".join(f"G={g}: {h:,.0f}" for g, h in info["H"].items()))
        if A.check_B:
            found, beyond, worst, lim = brute_check(a, b, P0, A.check_B, A.check_factor)
            print(f"   brute check B = {A.check_B:.0e}, all slopes to height {lim:,}: {found:,} triples with n <= B; beyond their bound: {beyond}; max h / H(G) = {worst:.3f}")

if __name__ == "__main__":
    main()
