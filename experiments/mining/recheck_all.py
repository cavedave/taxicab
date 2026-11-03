#!/usr/bin/env python3
"""recheck_all.py -- re-run the exact checks of THEOREMS.md (and the two open observations) on n;k;x:y,... files.

Per number n (all representations P and their swaps as points of x^3 + y^3 = n):
  basic  every representation is coprime and on the curve, no repeats
  T5     for p = 2 or p = 2 (mod 3) dividing n: v_p(s) = v_p(n) in every representation; v_3(t) <= 1; 3 | t iff 3 | s;
         v_3(n) != 1                                                      (needs the factorisation of n: PARI)
  L6     xy mod 3 is the same in every representation
  T7     every chord through two points (a x + b y = c, a != b, c != 0): the denominator D of the third point divides
         (b - a) E, E = a^2 + ab + b^2
  T8     p-types (p = 2 for n odd, p = 3 for n = +-1 mod 9) are defined at every point; a chord between opposite types
         has a third point that is not p-integral; the three points of every integral collinear triple share their type
  open   (T7 second half) a, b both odd and D > 1 => D even;
         (item 11) P, Q on a common integral line => the chord P, swap(Q) keeps a 3 in its denominator
Prints counts and every failure.  Usage: python3 recheck_all.py file [file ...] [--gp gp] [--procs 8]
"""
import argparse, gzip, sys
from fractions import Fraction as F
from itertools import combinations
from math import gcd
from multiprocessing import Pool
from collisions import factor_batch

def third(P, Q):
    (x, y), (x1, y1) = P, Q; d = x * y - x1 * y1
    return None if d == 0 else (F(x1 * x1 * y - x * x * y1, d), F(x * y1 * y1 - x1 * y * y, d))

def vp(m, p):
    m = abs(m); v = 0
    while m and m % p == 0: m //= p; v += 1
    return v

def ptype(P, p):
    x, y = P
    if x % p == 0 and y % p: return 0
    if y % p == 0 and x % p: return 1
    return None

def check(n, reps, fac):
    c = dict.fromkeys(("basic", "T5", "L6", "T7", "T8", "open7", "open11"), 0)
    tests = dict.fromkeys(c, 0)
    def fail(key, msg):
        c[key] += 1; print(f"FAIL {key} n={n}: {msg}", flush=True)
    tests["basic"] += 1
    if len(set(reps)) != len(reps) or any(x**3 + y**3 != n or gcd(x, y) != 1 for x, y in reps): fail("basic", reps)
    # Theorem 5
    if fac is not None:
        tests["T5"] += 1
        if vp(n, 3) == 1: fail("T5", "v3(n) = 1")
        for x, y in reps:
            s, t = x + y, x * x - x * y + y * y
            if vp(t, 3) > 1 or ((t % 3 == 0) != (s % 3 == 0)): fail("T5", f"3-part at {x}:{y}")
            for p, e in fac:
                if (p == 2 or p % 3 == 2) and vp(s, p) != e: fail("T5", f"p={p} at {x}:{y}")
    # Lemma 6
    tests["L6"] += 1
    if len({(x * y) % 3 for x, y in reps}) > 1: fail("L6", reps)
    pts = reps + [(y, x) for x, y in reps]
    ps = [p for p, ok in ((2, n % 2 == 1), (3, n % 9 in (1, 8))) if ok]
    for p in ps:
        tests["T8"] += 1
        if any(ptype(P, p) is None for P in pts): fail("T8", f"type undefined at p={p}")
    lines = []
    for P, Q in combinations(pts, 2):
        if Q == (P[1], P[0]): continue                      # P and its swap: the chord is x + y = s, third point at infinity
        R = third(P, Q)
        if R is None: continue
        a, b = Q[1] - P[1], P[0] - Q[0]; g = gcd(a, b); a, b = a // g, b // g; cc = a * P[0] + b * P[1]
        D = R[0].denominator * R[1].denominator // gcd(R[0].denominator, R[1].denominator)
        if a != b and cc != 0:
            tests["T7"] += 1
            if ((b - a) * (a * a + a * b + b * b)) % D: fail("T7", f"{P} {Q} D={D}")
            if D > 1 and a % 2 and b % 2:
                tests["open7"] += 1
                if D % 2: fail("open7", f"{P} {Q} a={a} b={b} D={D}")
        for p in ps:
            tP, tQ = ptype(P, p), ptype(Q, p)
            if tP is not None and tQ is not None and tP != tQ:
                tests["T8"] += 1
                if D % p: fail("T8", f"opposite {p}-types {P} {Q} give a {p}-integral third point")
        if D == 1:
            Rp = (int(R[0]), int(R[1]))
            if Rp in pts and Rp != P and Rp != Q: lines.append(frozenset((P, Q, Rp)))
    for L in set(lines):
        for p in ps:
            tests["T8"] += 1
            if len({ptype(P, p) for P in L}) > 1: fail("T8", f"line {sorted(L)} mixes {p}-types")
        for P, Q in combinations(sorted(L), 2):
            for A, B in ((P, Q), (Q, P)):
                Bs = (B[1], B[0])
                if Bs == A: continue
                R = third(A, Bs)
                if R is None: continue
                tests["open11"] += 1
                if R[0].denominator % 3 and R[1].denominator % 3: fail("open11", f"{A} {Bs}")
    return c, tests

def job(args):
    rows, gp = args
    facs = factor_batch([n for n, _ in rows], gp) if gp else [None] * len(rows)
    C, T = {}, {}
    for (n, reps), f in zip(rows, facs):
        c, t = check(n, reps, f)
        for k in c: C[k] = C.get(k, 0) + c[k]; T[k] = T.get(k, 0) + t[k]
    return C, T, len(rows)

def read(fn):
    for l in (gzip.open(fn, "rt") if fn.endswith(".gz") else open(fn)):
        if l[0].isdigit():
            n, k, r = l.strip().split(";")
            yield int(n), [tuple(map(int, p.split(":"))) for p in r.split(",")]

def main():
    ap = argparse.ArgumentParser(); ap.add_argument("files", nargs="+"); ap.add_argument("--gp", default="gp")
    ap.add_argument("--procs", type=int, default=8); A = ap.parse_args()
    rows = [r for fn in A.files for r in read(fn)]
    chunks = [(rows[i:i + 2000], A.gp) for i in range(0, len(rows), 2000)]
    C, T, done = {}, {}, 0
    with Pool(A.procs) as pool:
        for c, t, m in pool.imap_unordered(job, chunks):
            done += m
            for k in c: C[k] = C.get(k, 0) + c[k]; T[k] = T.get(k, 0) + t[k]
    print(f"{done} numbers")
    for k in C: print(f"  {k:7s} {T[k]:>10,} tests  {C[k]} failures")

if __name__ == "__main__":
    main()
