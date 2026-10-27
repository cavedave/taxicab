#!/usr/bin/env python3
"""collisions.py -- numbers n carried by two or more collinear triples (from line_enum.py output), with an
exact count of ALL their coprime representations.

Exact representation count of one n (independent of the lines): every representation n = x^3 + y^3 has
s = x + y > 0 dividing n, with s <= (4n)^(1/3) and (4n/s - s^2)/3 = d^2 a perfect square; then
x = (s + d)/2, y = (s - d)/2. Enumerating the divisors of n (PARI factorisation) finds all of them.

Usage: python3 collisions.py lines.txt [--gp gp]
"""
import argparse, re, subprocess
from collections import defaultdict
from math import gcd, isqrt

def icbrt(n):
    x = 1 << ((n.bit_length() + 2) // 3)
    while True:
        y = (2 * x + n // (x * x)) // 3
        if y >= x: break
        x = y
    while x ** 3 > n: x -= 1
    while (x + 1) ** 3 <= n: x += 1
    return x

def divisors(fac):
    ds = [1]
    for p, e in fac:
        ds = [d * p**k for d in ds for k in range(e + 1)]
    return ds

SQ64 = {(i * i) % 64 for i in range(64)}

def all_reps(n, fac):
    """every coprime (x, y) with x^3 + y^3 = n: s = x + y runs over the divisors of n up to (4n)^(1/3)
    (generated pruned at that bound), and 4 n / s - s^2 = 3 d^2 must hold"""
    smax = icbrt(4 * n)
    ds = [1]
    for p, e in fac:
        new = []
        for d in ds:
            for k in range(e + 1):
                if d > smax: break
                new.append(d); d *= p
        ds = new
    reps = set()
    for s in ds:
        t = 4 * (n // s) - s * s
        if t < 0 or t % 3: continue
        m = t // 3
        if (m & 63) not in SQ64: continue                    # quick square test mod 64
        d = isqrt(m)
        if d * d != m or (s + d) % 2: continue
        x, y = (s + d) // 2, (s - d) // 2
        if y != 0 and gcd(abs(x), abs(y)) == 1 and x**3 + y**3 == n:
            reps.add(tuple(sorted((x, y), reverse=True)))
    return reps

def factor_batch(ns, gp):
    out = []
    for i in range(0, len(ns), 500):
        part = ns[i:i + 500]
        res = subprocess.run([gp, "-q"], input="default(factor_add_primes,0);\n" + "\n".join(f"print(factor({n}));" for n in part),
                             capture_output=True, text=True, check=True).stdout.strip().splitlines()
        for f in res:
            body = re.search(r"\[([^\[\]]*)\]", f.replace("Mat(", "")).group(1)
            out.append([tuple(int(v) for v in r.split(",")) for r in body.replace(" ", "").split(";")])
    return out

def main():
    ap = argparse.ArgumentParser(); ap.add_argument("lines"); ap.add_argument("--gp", default="gp")
    a = ap.parse_args()
    byn = defaultdict(set)
    for l in open(a.lines):
        n, A, B, c, ps = l.strip().split(";")
        byn[int(n)].add(frozenset(tuple(sorted(map(int, q.split(":")), reverse=True)) for q in ps.split(",")))
    multi = sorted(n for n, L in byn.items() if len(L) >= 2)
    print(f"{len(byn)} numbers carry a collinear triple; {len(multi)} carry two or more")
    facs = factor_batch(multi, a.gp)
    for n, fac in zip(multi, facs):
        reps = all_reps(n, fac)
        onlines = set().union(*byn[n])
        assert onlines <= reps, f"line point not found by the exact count at {n}"
        shape = "bowtie" if len(onlines) == 5 else f"{len(byn[n])} lines / {len(onlines)} points"
        flag = "  <<< SIX OR MORE" if len(reps) >= 6 else ""
        print(f"  n = {n}  ({len(str(n))} digits): {len(byn[n])} lines, {len(onlines)} points on lines, "
              f"{len(reps)} coprime reps in total [{shape}]{flag}")

if __name__ == "__main__":
    main()
