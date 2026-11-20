#!/usr/bin/env python3
"""check_big_lists.py -- counterexample search on the big generated lists (19 Nov 2026).

Runs every claim of THEOREMS.md / TOPROVE.md / FINDINGS that can be tested on n;k;x:y,... files WITHOUT factoring n
(the numbers go up to 320 digits): exact rational arithmetic for chords, lines and tangents, and only the small primes
(< SMALL) of n where a statement is about primes of n. Collinear triples are found from the points themselves
(every pair of points and the third point of their chord), not taken from the generator.

PROVED (a failure means a wrong proof or bad data):
  basic  points coprime, on the curve, distinct; exact k = number of listed representations
  T1     lines: ab > 0, a != b, primes = 2 (mod 3) to even powers in ab (when ab < 10^12), ab even
  T2,T3  lines: E | c, E | n, E | t at the three points
  P4     no line has three positive points (TOPROVE 4)
  T5     small p = 2 or 2 (mod 3) dividing n: p does not divide t; v3(t) <= 1; 3 | t iff 3 | s; v3(n) != 1
  L6     xy mod 3 the same for all representations
  T7     chords: D | (b - a) E; D even => a, b odd
  T8a/b  p-types (2: n odd; 3: n = +-1 mod 9): opposite types => p | D; the points of a line share their type
  T9     chords: gcd(X, D) = gcd(Y, D) = gcd(a, D) = gcd(b, D) = 1 and (D | X + Y <=> D | b - a)
  T10    chords: gcd(X, Y) = 1
  P11    m_k f <= (4n)^(1/3), f = small-prime (p != 1 mod 3) part of s, a lower bound for the true f
  T12    n even => no line
  T13    s-cubic identities on lines and on every chord (rational third root); 13a for small p != 1 (mod 3)
  T14    chords, small p != 1 (mod 3): v_p(b - a) >= v_p(s); n even: v_2(b - a) >= v_2(s) + 1; 14a: den(s_R) | E
  L17    the class mu = tau2 tau3 is the same on each line (n odd, n = +-1 mod 9)
  L18    two lines of one n: same small-prime non-split part of b - a, lcm(E, E') | n, b - a odd, n odd
  L19    chords whose third point is not a representation: the part of E prime to 3n divides D
BELIEVED, NOT PROVED:
  TP5    (TOPROVE 5, sketch) tangent at P with |x^3 - y^3| > 3: third point not integral
  TP11   (TOPROVE 11, numerator step open) P, Q on a line: the chord P, swap(Q) has 3 | D unless it is a representation
  T7b    (recheck_all 'open') chord with a, b both odd and D > 1 => D even
  DL     (FINDINGS F31) D-lines, 1 < D <= 6: D odd => ab even, D even => ab odd; ab > 0 and ab a norm (ab < 10^12)
STATISTICS (not claims): n mod 9, 7 | n, number of lines per n.

Usage: python3 check_big_lists.py [file ...] [--procs 8]   (default: the two big lists in results/)
"""
import argparse, sys
from collections import Counter
from fractions import Fraction as Fr
from itertools import combinations
from math import gcd, isqrt
from multiprocessing import Pool
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SMALL = 100000
PR = [p for p in range(2, SMALL) if all(p % q for q in range(2, isqrt(p) + 1))]
PRIMORIAL = 1
for p in PR: PRIMORIAL *= p
M_K = {4: 19, 5: 31, 6: 37}

def vp(m, p):
    if m == 0: return 99
    m = abs(m); v = 0
    while m % p == 0: m //= p; v += 1
    return v

def factor_small(m, lim=10**6):
    f = {}; p = 2
    while p * p <= m:
        if p > lim: return None
        while m % p == 0: f[p] = f.get(p, 0) + 1; m //= p
        p += 1
    if m > 1: f[m] = f.get(m, 0) + 1
    return f

def norm_ok(ab):
    """every prime = 2 (mod 3) to an even power (None: too big to factor)"""
    if ab <= 0 or ab >= 10**12: return None
    f = factor_small(ab)
    return all(e % 2 == 0 for p, e in f.items() if p % 3 == 2)

def third(P, Q):
    (x, y), (x1, y1) = P, Q; d = x * y - x1 * y1
    if d == 0: return None
    return (Fr(x1 * x1 * y - x * x * y1, d), Fr(x * y1 * y1 - x1 * y * y, d))

def line_of(P, Q):
    a, b = Q[1] - P[1], P[0] - Q[0]; g = gcd(a, b); a, b = a // g, b // g
    if a < 0 or (a == 0 and b < 0): a, b = -a, -b
    return a, b, a * P[0] + b * P[1]

def ptype(P, p):
    x, y = P
    if x % p == 0 and y % p: return 0
    if y % p == 0 and x % p: return 1
    return None

def check(item):
    n, kfield, reps = item
    F = []; C = Counter()
    def fail(tag, msg): F.append(f"{tag}: n={str(n)[:30]}... ({len(str(n))} digits) {msg}")
    def ok(tag, cond, msg=""):
        C[tag] += 1
        if not cond: fail(tag, msg)
    # basic
    for x, y in reps:
        ok("basic", x**3 + y**3 == n and gcd(x, y) == 1, f"bad point {x}:{y}")
    ok("basic", len({tuple(sorted(r)) for r in reps}) == len(reps), "repeated representation")
    k = int(kfield.lstrip(">="))
    if not kfield.startswith(">="): ok("basic", len(reps) == k, "count != listed k")
    # small primes of n
    g = gcd(n, PRIMORIAL); sp = [p for p in PR if g % p == 0]
    v3n = vp(n, 3)
    # T5
    for x, y in reps:
        s, t = x + y, x * x - x * y + y * y
        for p in sp:
            if p == 2 or p % 3 == 2: ok("T5", t % p != 0, f"p={p} divides t")
        ok("T5", vp(t, 3) <= 1 and ((t % 3 == 0) == (s % 3 == 0)), "3-adic t")
    ok("T5", v3n != 1, "v3(n) = 1")
    # L6
    ok("L6", len({(x * y) % 3 for x, y in reps}) == 1, "xy mod 3 differs")
    # P11 with the small-prime part of s (a lower bound for f)
    s0 = reps[0][0] + reps[0][1]; f = 1
    for p in sp:
        if p % 3 != 1: f *= p ** vp(s0, p)
    if k in M_K: ok("P11", (M_K[k] * f) ** 3 <= 4 * n, f"m_k f = {M_K[k]*f} > (4n)^(1/3)")
    # points and types
    P = reps + [(y, x) for x, y in reps]
    rep_set = set(P)
    tdef = {2: n % 2 == 1, 3: n % 9 in (1, 8)}
    for p in (2, 3):
        if tdef[p]:
            for Q in P: ok("T8", ptype(Q, p) is not None, f"type undefined at p={p}")
    nonsplit_dirs = {}
    lines = set()
    # chords
    for Q1, Q2 in combinations(P, 2):
        if Q2 == (Q1[1], Q1[0]): continue
        R = third(Q1, Q2)
        if R is None: C["chord_d0"] += 1; continue
        a, b, c = line_of(Q1, Q2); E = a * a + a * b + b * b
        D = R[0].denominator * R[1].denominator // gcd(R[0].denominator, R[1].denominator)
        X, Y = R[0] * D, R[1] * D; X, Y = X.numerator, Y.numerator
        C["chords"] += 1
        ok("T7", ((b - a) * E) % D == 0, f"D={D} (a,b)=({a},{b})")
        if D % 2 == 0: ok("T7", a % 2 and b % 2, "D even, a or b even")
        ok("T9", gcd(X, D) == gcd(Y, D) == gcd(a, D) == gcd(b, D) == 1, "gcd with D")
        ok("T9", ((X + Y) % D == 0) == ((b - a) % D == 0), f"D | X+Y vs D | b-a, D={D}")
        ok("T10", gcd(X, Y) == 1, "gcd(X, Y) > 1")
        s1, s2, s3 = sum(Q1), sum(Q2), R[0] + R[1]
        ok("T13", E * (s1 + s2 + s3) == 3 * c * (a + b) and E * (s1 * s2 + s1 * s3 + s2 * s3) == 3 * c * c
           and E * s1 * s2 * s3 == (a - b) ** 2 * n, "s-cubic identities")
        for p in sp:
            if p % 3 != 1: ok("T14", vp(b - a, p) >= vp(s1, p), f"p={p}")
        if n % 2 == 0: ok("T14", vp(b - a, 2) >= vp(s1, 2) + 1, "p=2, n even")
        if D > 1: ok("T14a", E % s3.denominator == 0, "den(s_R) does not divide E")
        for p in (2, 3):
            if tdef[p] and ptype(Q1, p) != ptype(Q2, p): ok("T8", D % p == 0, f"opposite {p}-types, R {p}-integral")
        if a % 2 and b % 2 and D > 1: ok("T7b", D % 2 == 0, f"a, b odd, D={D} odd")
        if R not in rep_set:
            e = E
            while e % 3 == 0: e //= 3
            h = gcd(e, n)
            while h > 1: e //= h; h = gcd(e, n)
            ok("L19", D % e == 0, f"part of E prime to 3n = {e} does not divide D = {D}")
        if 1 < D <= 6:
            C["DL_chords"] += 1
            ok("DL", (a * b) % 2 == (0 if D % 2 else 1), f"D={D} ab={a*b} parity")
            ok("DL", a * b > 0, f"D={D} ab={a*b} <= 0")
            nk = norm_ok(a * b)
            if nk is not None: ok("DL", nk, f"D={D} ab={a*b} not a norm")
        if D == 1:
            lines.add(frozenset((Q1, Q2, (int(R[0]), int(R[1])))))
    # tangents (TOPROVE 5)
    for x, y in P:
        if abs(x**3 - y**3) > 3 and x**3 + y**3 == n:
            d = x**3 - y**3; R = (Fr(x * (x**3 + 2 * y**3), d), Fr(-y * (2 * x**3 + y**3), d))
            assert R[0] ** 3 + R[1] ** 3 == n
            ok("TP5", not (R[0].denominator == 1 and R[1].denominator == 1), f"tangent at {x}:{y} integral")
    # lines
    L = []
    for T in lines:
        T = sorted(T); a, b, c = line_of(T[0], T[1]); E = a * a + a * b + b * b
        if (a, b, c) in [l[:3] for l in L]: continue
        L.append((a, b, c, E, T)); C["lines"] += 1
    if n % 2 == 0: ok("T12", not L, "even n has a line")
    for a, b, c, E, T in L:
        ok("T1", a * b > 0 and a != b and (a * b) % 2 == 0, f"(a,b)=({a},{b})")
        nk = norm_ok(a * b)
        if nk is not None: ok("T1", nk, f"ab={a*b} not a norm")
        ok("T2", c % E == 0 and n % E == 0, f"E={E}")
        for x, y in T: ok("T3", (x * x - x * y + y * y) % E == 0, f"E={E} t")
        ok("P4", not all(x > 0 and y > 0 for x, y in T), "three positive points")
        for p in sp:
            if p % 3 != 1:
                for x, y in T: ok("T13a", vp(b - a, p) == vp(x + y, p) and c % p ** vp(x + y, p) == 0, f"p={p}")
        for p in (2, 3):
            if tdef[p]: ok("T8", len({ptype(Q, p) for Q in T}) == 1, f"line mixes {p}-types")
        if tdef[2] and tdef[3]:
            ok("L17", len({(1 if Q[0] % 2 == 0 else -1) * (1 if Q[0] % 3 == 0 else -1) for Q in T}) == 1, "class")
        # TOPROVE 11: chord P, swap(Q) for P, Q on the line
        for Q1, Q2 in combinations(T, 2):
            for A, B in ((Q1, Q2), (Q2, Q1)):
                Bs = (B[1], B[0])
                if Bs == A: continue
                R = third(A, Bs)
                if R is None or R in rep_set: continue
                D = R[0].denominator * R[1].denominator // gcd(R[0].denominator, R[1].denominator)
                ok("TP11", D % 3 == 0, f"D={D}")
    for (a, b, c, E, T), (a2, b2, c2, E2, T2) in combinations(L, 2):
        ns1 = [vp(b - a, p) for p in sp if p % 3 != 1]; ns2 = [vp(b2 - a2, p) for p in sp if p % 3 != 1]
        lcm = E * E2 // gcd(E, E2)
        ok("L18", ns1 == ns2 and n % lcm == 0 and (b - a) % 2 and (b2 - a2) % 2 and n % 2, "two lines")
    stats = (n % 9, n % 7 == 0, len(L))
    return F, C, stats

def load(fn):
    for l in open(fn):
        if l[0] == "#" or not l.strip(): continue
        p = l.strip().split(";")
        yield int(p[0]), p[1], [tuple(map(int, q.split(":"))) for q in p[2].split(",")]

if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("files", nargs="*", default=[str(ROOT / "results/five_ways_all.txt"),
                                                 str(ROOT / "results/four_ways_generated.txt")])
    ap.add_argument("--procs", type=int, default=8)
    A = ap.parse_args()
    for fn in A.files:
        items = list(load(fn)); allF = []; tot = Counter(); m9 = Counter(); s7 = 0; nl = Counter()
        with Pool(A.procs) as pool:
            for F, C, (r9, d7, k) in pool.imap_unordered(check, items, chunksize=8):
                allF += F; tot += C; m9[r9] += 1; s7 += d7; nl[k] += 1
        print(f"== {fn}: {len(items)} numbers")
        for tag in sorted(tot): print(f"  {tag:10s} {tot[tag]:>10,} checks")
        print(f"  FAILURES: {len(allF)}")
        for f in allF[:40]: print("   ", f)
        fails = Counter(f.split(":")[0] for f in allF)
        if fails: print("  failures by tag:", dict(fails))
        print(f"  stats: n mod 9 {dict(sorted(m9.items()))}; 7 | n: {s7}/{len(items)}; lines per n {dict(sorted(nl.items()))}")
