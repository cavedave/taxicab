#!/usr/bin/env python3
"""Independent count of coprime cube-sum pairs in a window lo < n <= hi (exact integers only).

Shares no code with cabtaxi_gpu.cu: cube roots and the difference bound are solved with
math.isqrt / integer Newton steps instead of floating point. Prints, for the window,
  pairs   number of (x, y) with gcd 1 and lo < x^3 + y^3 <= hi (signs allowed, unordered)
  values  number of distinct n hit
  offsum  sum over pairs of (n - lo)
  multi, multioffsum   the same two figures restricted to values hit at least twice
These are the constants hard-coded in cabtaxi_gpu.cu's selftest.

Usage: python3 window_count.py LO HI [LO HI ...]
"""
from __future__ import annotations

import sys
from math import gcd, isqrt
from multiprocessing import Pool


def icbrt(n: int) -> int:                       # floor(cbrt(n)) by integer Newton
    if n <= 0:
        return 0
    x = 1 << ((n.bit_length() + 2) // 3)
    while True:
        y = (2 * x + n // (x * x)) // 3
        if y >= x:
            break
        x = y
    while x ** 3 > n:
        x -= 1
    while (x + 1) ** 3 <= n:
        x += 1
    return x


def cmin(d: int, v: int) -> int:                # smallest c >= 1 with 3dc^2 + 3d^2c + d^3 >= v
    disc = 9 * d ** 4 - 12 * d * (d ** 3 - v)
    c = max(1, (-3 * d * d + isqrt(max(disc, 0))) // (6 * d))
    f = lambda c: d ** 3 + 3 * d * c * (c + d)
    while c > 1 and f(c - 1) >= v:
        c -= 1
    while f(c) < v:
        c += 1
    return c


def chunk(args):
    lo, hi, kind, start, stop = args
    hits = []
    for t in range(start, stop):
        if kind == "sum":                       # n = a^3 + b^3, 1 <= a <= b
            a3 = t ** 3
            b0 = max(t, icbrt(lo - a3) + 1) if lo > a3 else t
            b1 = icbrt(hi - a3)
            for b in range(b0, b1 + 1):
                if gcd(t, b) == 1:
                    hits.append(a3 + b ** 3)
        else:                                   # n = (c+d)^3 - c^3, c, d >= 1
            d = t
            for c in range(cmin(d, lo + 1), cmin(d, hi + 1)):
                if gcd(c, d) == 1:
                    hits.append((c + d) ** 3 - c ** 3)
    return hits


def window(lo: int, hi: int, pool: Pool) -> tuple[int, int, int, int, int]:
    amax = icbrt(hi // 2) + 1                   # 2a^3 <= hi
    dmax = icbrt(hi) + 1                        # d^3 < n <= hi
    jobs = []
    for kind, top in (("sum", amax), ("diff", dmax)):
        step = max(1, top // 256)
        jobs += [(lo, hi, kind, s, min(s + step, top + 1)) for s in range(1, top + 1, step)]
    hits = [n for part in pool.imap_unordered(chunk, jobs) for n in part]
    assert all(lo < n <= hi for n in hits)
    mult = {}
    for n in hits:
        mult[n] = mult.get(n, 0) + 1
    multi = {n: k for n, k in mult.items() if k >= 2}
    return len(hits), len(mult), sum(n - lo for n in hits), len(multi), sum((n - lo) * k for n, k in multi.items())


if __name__ == "__main__":
    a = [int(x) for x in sys.argv[1:]]
    with Pool() as pool:
        for lo, hi in zip(a[::2], a[1::2]):
            pairs, values, offsum, multi, multioffsum = window(lo, hi, pool)
            print(f"lo={lo} hi={hi} pairs={pairs} values={values} offsum={offsum} "
                  f"multi={multi} multioffsum={multioffsum}", flush=True)
