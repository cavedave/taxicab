#!/usr/bin/env python3
"""sixway.py -- exact count of the coprime representations of one fully factored n with many split primes
(the two 35-prime numbers count_multi.py could not finish, count5/v2/counted_pass2.txt.unk; 20 Nov 2026).

A coprime representation n = x^3 + y^3 is s = x + y with s | n, s^3 <= 4n and (4n/s - s^2)/3 = (x - y)^2 a square.
Here n is coprime to 6 and all its primes are = 1 (mod 3), so each prime power lies wholly in s or in t = n/s
(gcd(s, t) | 3): s is the product of a subset of the prime powers. All 2^k subsets are searched by mitm.c
(two halves, a size bound, and K quadratic-residue tests mod small primes q via discrete logs); the survivors are
checked exactly here. The listed representations must all be found (a check on the search).

Usage: python3 sixway.py N_INDEX [--procs 8] [--K 48]   (N_INDEX 0 or 1: the 'count:' lines of the .unk file)
"""
import argparse, re, subprocess, sys, time
from math import gcd, isqrt, log
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[3]
UNK = HERE.parent / "v2/counted_pass2.txt.unk"

def primroot(q):
    fs = [p for p in range(2, q) if (q - 1) % p == 0 and all(p % r for r in range(2, p))]
    for g in range(2, q):
        if all(pow(g, (q - 1) // p, q) != 1 for p in fs): return g

def main():
    ap = argparse.ArgumentParser(); ap.add_argument("idx", type=int)
    ap.add_argument("--procs", type=int, default=8); ap.add_argument("--K", type=int, default=48)
    A = ap.parse_args(); t0 = time.time()
    L = [l.split(";") for l in open(UNK) if ";count:" in l][A.idx]
    n = int(L[0]); pp = [int(q) ** int(e) for q, e in re.findall(r"(\d+)\^(\d+)", L[2])]
    prod = 1
    for v in pp: prod *= v
    assert prod == n and n % 6 and all(int(q) % 3 == 1 for q, e in re.findall(r"(\d+)\^(\d+)", L[2]))
    known = None
    for l in open(ROOT / "results/five_ways_all.txt"):
        if l.startswith(L[0] + ";"):
            known = {tuple(sorted(map(int, t.split(":")))) for t in l.split(";")[2].split(",")}
    print(f"n = {L[0][:20]}... ({len(L[0])} digits), {len(pp)} prime powers, {len(known)} listed representations", flush=True)
    pp.sort(); half_a = pp[0::2]; half_b = pp[1::2]           # alternate sizes between the halves
    order = half_a + half_b; nA, nB = len(half_a), len(half_b)
    LB = log(4 * n) / 3 + 1e-6
    qs = []; q = 5
    while len(qs) < A.K:
        if all(q % r for r in range(2, isqrt(q) + 1)) and n % q: qs.append(q)
        q += 1
    lines = [f"{nA} {nB} {len(qs)} {LB!r}"]
    dl = []
    for q in qs:
        g = primroot(q); D = {}; x = 1
        for k in range(q - 1): D[x] = k; x = x * g % q
        inv3 = pow(3, -1, q); nq = n % q; t = []
        x = 1
        for k in range(q - 1):
            v = (4 * nq * pow(x, -1, q) - x * x) * inv3 % q
            t.append(1 if v == 0 or pow(v, (q - 1) // 2, q) == 1 else 0); x = x * g % q
        lines.append(f"{q} " + " ".join(map(str, t))); dl.append(D)
    for v in order: lines.append(f"{log(v)!r} " + " ".join(str(dl[k][v % q]) for k, q in enumerate(qs)))
    inp = "\n".join(lines) + "\n"
    NA = 1 << nA; step = (NA + A.procs - 1) // A.procs
    procs = [subprocess.Popen([str(HERE / "mitm"), str(i), str(min(i + step, NA))], stdin=subprocess.PIPE,
                              stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True) for i in range(0, NA, step)]
    for p in procs: p.stdin.write(inp); p.stdin.close()
    surv = []; info = []
    for p in procs:
        out = p.stdout.read(); err = p.stderr.read(); p.wait()
        surv += [tuple(map(int, l.split())) for l in out.split("\n") if l.strip()]; info.append(err.strip())
    pairs = sum(int(re.search(r"(\d+) pairs", e).group(1)) for e in info)
    print(f"search: {pairs:,} subsets under the size bound of 2^{len(pp)} = {2**len(pp):,}; {len(surv)} survive "
          f"{len(qs)} residue tests; {time.time() - t0:.0f} s", flush=True)
    found = set()
    for ma, mb in surv:
        s = 1
        for i in range(nA):
            if ma >> i & 1: s *= half_a[i]
        for i in range(nB):
            if mb >> i & 1: s *= half_b[i]
        if s ** 3 > 4 * n: continue
        Q = 4 * (n // s) - s * s
        if Q % 3: continue
        Q //= 3; m = isqrt(Q)
        if m * m != Q or (s + m) % 2: continue
        x, y = (s + m) // 2, (s - m) // 2
        if gcd(x, y) == 1 and x ** 3 + y ** 3 == n: found.add(tuple(sorted((x, y))))
    print(f"exact check: {len(found)} coprime representations; listed ones all found: {known <= found}")
    for r in sorted(found, key=lambda r: r[0] + r[1]):
        print(f"  {'listed' if r in known else '*** NEW'}  s = x + y = {r[0] + r[1]}")
    if len(found) >= 6: print("*** SIX-WAY OR MORE")
    print(f"total {time.time() - t0:.0f} s")

if __name__ == "__main__":
    main()
