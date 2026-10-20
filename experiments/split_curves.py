#!/usr/bin/env python3
"""split_curves.py -- build curves x^3 + y^3 = M directly, M a product of small primes = 1 (mod 3).

Both record curves and every near miss from the 1e18 hunt have this shape:
    82652823799 = 7.13.19.43.73.97.157      (Ta(6)..Ta(10) bounds)
    3956875867  = 7.31.37.43.73.157         (Ta(11)..Ta(22) bounds)
so instead of hoping seeds lead to such curves, list them all: every product of RMIN..RMAX
distinct primes p = 1 (mod 3) with p < PMAX (and M <= MMAX), optionally times one extra small
factor (--extra 2,3 for example).

Output is seedgen format with no pairs ("M;0;p:1,...;"), so it feeds straight into
curve_sieve.py (scoring) and curve_hunt.py (which then finds all points with PARI).

Usage:  python3 split_curves.py --pmax 200 --rmin 5 --rmax 8 --out split_curves.csv
"""
import argparse, itertools, math

def primes_1mod3(pmax):
    sieve = bytearray([1]) * pmax; sieve[:2] = b"\0\0"
    for i in range(2, int(pmax ** 0.5) + 1):
        if sieve[i]: sieve[i*i::i] = bytearray(len(sieve[i*i::i]))
    return [p for p in range(7, pmax) if sieve[p] and p % 3 == 1]

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--pmax", type=int, default=200)
    ap.add_argument("--rmin", type=int, default=5)
    ap.add_argument("--rmax", type=int, default=8)
    ap.add_argument("--mmax", type=float, default=1e18)
    ap.add_argument("--extra", default="", help="comma list of extra single factors, e.g. 2,3")
    ap.add_argument("--out", default="split_curves.csv")
    a = ap.parse_args()
    P = primes_1mod3(a.pmax)
    extras = [1] + [int(x) for x in a.extra.split(",") if x]
    n = 0
    with open(a.out, "w") as f:
        for r in range(a.rmin, a.rmax + 1):
            for combo in itertools.combinations(P, r):
                base = math.prod(combo)
                for e in extras:
                    M = base * e
                    if M > a.mmax: continue
                    fac = sorted(combo + ((e,) if e > 1 else ()))
                    f.write(f"{M};0;" + ",".join(f"{p}:1" for p in fac) + ";\n"); n += 1
    print(f"{len(P)} primes = 1 mod 3 below {a.pmax}: {P}")
    print(f"{n} curves (products of {a.rmin}..{a.rmax} of them{', times ' + a.extra if a.extra else ''}) -> {a.out}")

if __name__ == "__main__":
    main()
