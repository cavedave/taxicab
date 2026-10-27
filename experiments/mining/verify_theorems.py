#!/usr/bin/env python3
"""verify_theorems.py -- regression check of THEOREMS.md against line data (line_enum.py output files).

For every triple n;a;b;c;x:y,x:y,x:y it checks:
  T1(a)  a*b > 0, a != b, every prime p = 2 (mod 3) divides a*b to an even power
  T1(b)  a*b even
  T2     E = a^2 + ab + b^2 divides c and n
  T3     E divides t = x^2 - xy + y^2 at each of the three points
  basic  the points are distinct, coprime, on the line and on the curve
Any failure is printed; the run ends with counts.

Usage: python3 verify_theorems.py lines1.txt [lines2.txt ...] [--limit N]
       python3 verify_theorems.py --reps cab.txt [...]   (n;k;x:y,... files: finds EVERY collinear triple among
                                                         the points and their swaps, independently of line_enum,
                                                         so Theorem 1 is tested on directions nobody chose)
"""
from itertools import combinations
import sys
from math import gcd

def factor_small(m):
    f = {}; p = 2
    while p * p <= m:
        while m % p == 0: f[p] = f.get(p, 0) + 1; m //= p
        p += 1
    if m > 1: f[m] = f.get(m, 0) + 1
    return f

def reps_to_lines(fn):
    """yield n;a;b;c;pts lines for every collinear triple of distinct points among the representations"""
    for l in open(fn):
        if l[0] == "#": continue
        n, k, r = l.strip().split(";")
        if int(k) < 3: continue
        P = [tuple(map(int, q.split(":"))) for q in r.split(",")]
        P = P + [(y, x) for x, y in P]
        for T in combinations(P, 3):
            if len({tuple(sorted(p)) for p in T}) < 3: continue        # a point and its swap: not 3 representations
            (x1, y1), (x2, y2), (x3, y3) = T
            if (x2 - x1) * (y3 - y1) != (y2 - y1) * (x3 - x1): continue
            a, b = y2 - y1, x1 - x2; g = gcd(a, b); a //= g; b //= g
            if a < 0 or (a == 0 and b < 0): a, b = -a, -b
            yield f"{n};{a};{b};{a*x1+b*y1};" + ",".join(f"{x}:{y}" for x, y in T)

def main():
    if "--reps" in sys.argv:
        import tempfile, os
        tmp = tempfile.NamedTemporaryFile("w", delete=False, suffix=".txt")
        for fn in sys.argv[sys.argv.index("--reps") + 1:]:
            for line in reps_to_lines(fn): tmp.write(line + "\n")
        tmp.close(); sys.argv = [sys.argv[0], tmp.name]
    args = [x for x in sys.argv[1:] if not x.startswith("--")]
    limit = int(sys.argv[sys.argv.index("--limit") + 1]) if "--limit" in sys.argv else None
    if limit: args = [x for x in args if x != str(limit)]
    dir_ok = {}; checked = 0; fails = 0
    for fn in args:
        for i, l in enumerate(open(fn)):
            if limit and i >= limit: break
            n, a, b, c, ps = l.strip().split(";")
            n, a, b, c = int(n), int(a), int(b), int(c)
            pts = [tuple(map(int, q.split(":"))) for q in ps.split(",")]
            E = a * a + a * b + b * b
            if (a, b) not in dir_ok:
                f = factor_small(a * b)
                dir_ok[(a, b)] = (a * b > 0 and a != b and all(e % 2 == 0 for p, e in f.items() if p % 3 == 2),
                                  (a * b) % 2 == 0)
            t1a, t1b = dir_ok[(a, b)]
            basic = (len(set(pts)) == 3 and all(gcd(x, y) == 1 and x**3 + y**3 == n and a * x + b * y == c for x, y in pts))
            t2 = c % E == 0 and n % E == 0
            t3 = all((x * x - x * y + y * y) % E == 0 for x, y in pts)
            checked += 1
            if not (basic and t1a and t1b and t2 and t3):
                fails += 1
                print(f"FAIL {fn}:{i+1} basic={basic} T1a={t1a} T1b={t1b} T2={t2} T3={t3}: {l.strip()[:120]}")
    print(f"{checked} triples in {len(dir_ok)} directions checked; {fails} failures")

if __name__ == "__main__":
    main()
