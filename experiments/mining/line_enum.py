#!/usr/bin/env python3
"""line_enum.py -- enumerate coprime collinear triples on x^3 + y^3 = n, direction by direction.

A line a x + b y = c (a, b > 0 coprime, a < b; the mirror b x + a y = c gives the same triples swapped) meets
x^3 + y^3 = n where (b^3 - a^3) x^3 + 3 a^2 c x^2 - 3 a c^2 x + (c^3 - b^3 n) = 0. With u = x / c the root sum
and pair-sum are fixed: s0 = -3a^2/D, p0 = -3a/D (D = b^3 - a^3), whatever n is. Eliminating u3 and shifting
v = u - s0/3 gives the conic  X^2 + X Y + Y^2 = 3 a b^3  with X = D v1, Y = D v2.  One rational point of it
(PARI qfsolve) and the pencil of lines through it (slopes r/s) give every rational point, hence every
triple (u1, u2, u3); c is then the least positive integer making all x_i = c u_i and y_i = c (1 - a u_i)/b
integral. Triples with all three points coprime are kept (n > 0 after an overall sign flip).

Directions follow finding F10: a b even and a norm (primes = 2 mod 3 to even powers), cheapest |b^3 - a^3| first.

Output: n;a;b;c;x:y,x:y,x:y   (one line per primitive coprime triple with n <= --nmax)
Usage: python3 line_enum.py --dirs 200 --height 400 --nmax 1e17 --out lines.txt
"""
import argparse, subprocess, sys, time
from multiprocessing import Pool
from fractions import Fraction as F
from math import gcd

def factor(n):
    f = {}; p = 2
    while p * p <= n:
        while n % p == 0: f[p] = f.get(p, 0) + 1; n //= p
        p += 1
    if n > 1: f[n] = f.get(n, 0) + 1
    return f

def allowed(a, b):
    f = factor(a * b)
    return f.get(2, 0) >= 2 and all(e % 2 == 0 for p, e in f.items() if p % 3 == 2)

def directions(count, amax=2000):
    c = []
    for a in range(1, amax):
        for b in range(a + 1, amax):
            if b**3 - a**3 > 10**10: break
            if gcd(a, b) == 1 and allowed(a, b): c.append((b**3 - a**3, a, b))
    c.sort()
    return [(a, b) for _, a, b in c[:count]]

def conic_points(dirs, gp="gp"):
    """one integer solution (X, Y, Z) of X^2 + X Y + Y^2 = M Z^2, M = 3 a b^3, per direction"""
    src = "\n".join(f"v=qfsolve([2,1,0;1,2,0;0,0,{-2*3*a*b**3}]); print(v[1],\" \",v[2],\" \",v[3]);" for a, b in dirs)
    out = subprocess.run([gp, "-q"], input=src, capture_output=True, text=True, check=True).stdout.split("\n")
    pts = []
    for (a, b), line in zip(dirs, out):
        X, Y, Z = map(int, line.split())
        assert X*X + X*Y + Y*Y == 3*a*b**3 * Z*Z
        pts.append((F(X, Z), F(Y, Z)))
    return pts

def triples(a, b, P0, H, nmax):
    D = b**3 - a**3
    s0 = F(-3 * a * a, D)
    M = 3 * a * b**3
    X0, Y0 = P0
    seen = set(); out = []
    for s in range(0, H + 1):
        for r in range(-H, H + 1):
            if (s == 0 and r != 1) or gcd(r, s) != 1: continue
            Q = s*s + s*r + r*r
            Bv = 2*X0*s + X0*r + Y0*s + 2*Y0*r
            m = -Bv / Q
            X1, Y1 = X0 + m*s, Y0 + m*r
            u1 = X1 / D + s0 / 3; u2 = Y1 / D + s0 / 3; u3 = s0 - u1 - u2
            us = (u1, u2, u3)
            vals = []
            for u in us: vals += [u, (1 - a*u) / b]
            c = 1
            for v in vals: c = c * v.denominator // gcd(c, v.denominator)
            pts = [(int(c*u), int(c*(1 - a*u) / b)) for u in us]
            n = pts[0][0]**3 + pts[0][1]**3
            if n < 0: pts = [(-x, -y) for x, y in pts]; n = -n; cc = -c
            else: cc = c
            if n == 0 or n > nmax: continue
            if any(gcd(abs(x), abs(y)) != 1 or x == 0 or y == 0 for x, y in pts): continue
            if len({tuple(sorted(p)) for p in pts}) < 3: continue
            key = frozenset(tuple(sorted(p)) for p in pts)
            if key in seen: continue
            seen.add(key)
            assert all(x**3 + y**3 == n for x, y in pts) and all(a*x + b*y == cc for x, y in pts)
            out.append((n, cc, pts))
    return out

def run_dir(job):
    a, b, P0, H, nmax = job
    return (a, b), triples(a, b, P0, H, nmax)

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dirs", type=int, default=50)
    ap.add_argument("--height", type=int, default=200)
    ap.add_argument("--nmax", type=float, default=1e17)
    ap.add_argument("--gp", default="gp")
    ap.add_argument("--procs", type=int, default=6)
    ap.add_argument("--out", required=True)
    a_ = ap.parse_args()
    dirs = directions(a_.dirs)
    P = conic_points(dirs, a_.gp)
    t0 = time.time(); total = 0
    jobs = [(a, b, P0, a_.height, int(a_.nmax)) for (a, b), P0 in zip(dirs, P)]
    with open(a_.out, "w") as f, Pool(a_.procs) as pool:
        for (a, b), T in pool.imap(run_dir, jobs):
            for n, c, pts in T:
                f.write(f"{n};{a};{b};{c};" + ",".join(f"{x}:{y}" for x, y in pts) + "\n")
            f.flush(); total += len(T)
            print(f"  ({a},{b}) D={b**3-a**3}: {len(T)} triples  [{time.time()-t0:.0f}s]", flush=True)
    print(f"{total} triples from {len(dirs)} directions -> {a_.out}")

if __name__ == "__main__":
    main()
