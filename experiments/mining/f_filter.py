#!/usr/bin/env python3
"""f_filter.py -- Proposition 11 (THEOREMS.md): a pair (x, y) whose s = x + y has non-split part f with f * m_k > (4n)^(1/3)
belongs to an n with fewer than k coprime representations (m_4, m_5, m_6 = 19, 31, 37). Validates on the catalogue and
measures the share of pairs cut on census windows (argv[1]/ctrl/w_*.txt), overall and by stream (sums / differences)."""
import sys, glob
S = sys.argv[1]
KTH = {4: 19, 5: 31, 6: 37}           # k-th smallest product of distinct split-prime blocks: 1, 7, 13, 19, 31, 37
def fac(m):
    f, p = {}, 2
    while p * p <= m:
        while m % p == 0: f[p] = f.get(p, 0) + 1; m //= p
        p += 1 if p == 2 else 2
    if m > 1: f[m] = f.get(m, 0) + 1
    return f
def fpart(s):
    return eval("*".join(["1"] + [f"{p}**{e}" for p, e in fac(s).items() if p % 3 != 1]))
def icbrt4(n):
    r = int(round((4 * n) ** (1 / 3)))
    while r**3 > 4 * n: r -= 1
    while (r + 1)**3 <= 4 * n: r += 1
    return r                                   # floor((4n)^(1/3)), exact
def cut(x, y, n, k):
    return fpart(x + y) * KTH[k] > icbrt4(n)   # True: provably fewer than k representations
def rows(fn):
    for l in open(fn):
        if l[0].isdigit():
            n, k, r = l.strip().split(";")
            yield int(n), int(k), [tuple(map(int, p.split(":"))) for p in r.split(",")]
# validation: no pair of a known k-way may be cut at level k
bad = 0; checked = 0
for n, k, reps in rows("results/a047697_catalogue.txt"):
    for x, y in reps:
        checked += 1; bad += cut(x, y, n, min(k, 6)) if k >= 4 else 0
print(f"validation: {checked:,} pairs of four- and five-ways, cut at their own level: {bad}")
for w in ("w_1e+12", "w_1e+18", "w_1e+22", "w_2e+23"):
    P = [(x, y, n) for n, k, reps in rows(f"{S}/ctrl/{w}.txt") for x, y in reps]
    print(f"{w}: {len(P):,} pairs; cut for k>=6: {sum(cut(x, y, n, 6) for x, y, n in P)/len(P):.1%}   k>=5: {sum(cut(x, y, n, 5) for x, y, n in P)/len(P):.1%}   k>=4: {sum(cut(x, y, n, 4) for x, y, n in P)/len(P):.1%}")
print("\nby stream (share of all pairs; share of that stream cut for k >= 6 / k >= 4):")
for w in ("w_1e+18", "w_1e+22", "w_2e+23"):
    P = [(x, y, n) for n, k, reps in rows(f"{S}/ctrl/{w}.txt") for x, y in reps]
    su = [p for p in P if p[1] > 0]; di = [p for p in P if p[1] < 0]
    f = lambda G, k: sum(cut(x, y, n, k) for x, y, n in G) / len(G)
    print(f"  {w}: sums {len(su)/len(P):.0%} of pairs, cut {f(su,6):.0%} / {f(su,4):.0%};  differences {len(di)/len(P):.0%}, cut {f(di,6):.0%} / {f(di,4):.0%}"
          f";  rows-only (differences) saves {len(di)/len(P)*f(di,6):.0%} of all pairs")
