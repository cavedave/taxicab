#!/usr/bin/env python3
"""hard_patterns.py -- universal / absence statements (not averages) in exhaustive k-way data.

1. Absent residues: residues r mod m that occur among the control group (k = 1) but NEVER among
   k-ways, reported only when chance would predict many (expected = share_in_control * count >= MINEXP).
   Also residues that are 100% of the k-ways (a "must" statement).
2. Quantified per-representation statements: for a property P of a pair (x, y), count for every n how
   many of its k representations satisfy P; report statements that hold for EVERY n in the group:
     "all k reps have P", "at least one rep has P", "no rep has P", "exactly j reps have P"
   with the chance expectation computed from the control rate q of P among single representations:
     P(at least one) = 1 - (1 - q)^k, P(all) = q^k, P(none) = (1 - q)^k.
   A statement is interesting when it holds for every n but chance says it should often fail.

Input: files n;k;x:y,...   (--control = k = 1 file(s); targets = files with the k-ways)
Usage: python3 hard_patterns.py --control ctrl.txt --targets cab2_1e15.txt fives.txt --kmin 3
"""
from __future__ import annotations

import argparse
from collections import Counter, defaultdict
from math import gcd

MODULI = list(range(2, 61)) + [64, 81, 121, 125, 169, 243, 343]
PRIMES = [2, 3, 5, 7, 11, 13, 17, 19, 31, 37, 43]
MINEXP = 8.0


def read(paths, kmin=1, kmax=99):
    for p in paths:
        for line in open(p):
            if not line[0].isdigit(): continue
            n, k, ps = line.strip().split(";")[:3]
            k = int(k)
            if kmin <= k <= kmax:
                yield int(n), k, [tuple(map(int, q.split(":"))) for q in ps.split(",") if q]


def rep_props():
    """properties of one representation (x, y), y < 0 for a difference"""
    props = {"sum": lambda x, y: y > 0}
    for p in PRIMES:
        props[f"{p}|x or {p}|y"] = (lambda p: lambda x, y: x % p == 0 or y % p == 0)(p)
        props[f"{p}|s"] = (lambda p: lambda x, y: (x + y) % p == 0)(p)
        props[f"{p}|x-y"] = (lambda p: lambda x, y: (x - y) % p == 0)(p)
    for m in (4, 8, 9):
        props[f"x=y mod {m}"] = (lambda m: lambda x, y: (x - y) % m == 0)(m)
    return props


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--control", nargs="+", required=True)
    ap.add_argument("--targets", nargs="+", required=True)
    ap.add_argument("--kmin", type=int, default=3)
    a = ap.parse_args()
    ctrl = list(read(a.control, 1, 1))
    groups = defaultdict(list)
    for n, k, ps in read(a.targets, a.kmin):
        groups[k].append((n, ps))
    groups = {k: list({n: (n, ps) for n, ps in v}.values()) for k, v in groups.items()}   # dedupe across files
    groups["k>=%d" % a.kmin] = [x for k in sorted(k for k in groups if isinstance(k, int)) for x in groups[k]]
    print(f"control: {len(ctrl)} one-ways; groups: " + ", ".join(f"{k}: {len(v)}" for k, v in groups.items()))

    print("\n== 1. residues of n: absent (expected >= %.0f by chance) or universal ==" % MINEXP)
    for m in MODULI:
        cshare = Counter(n % m for n, _, _ in ctrl); N0 = len(ctrl)
        for gk, g in groups.items():
            gc = Counter(n % m for n, _ in g)
            absent = [(r, cshare[r] / N0 * len(g)) for r in cshare if gc[r] == 0 and cshare[r] / N0 * len(g) >= MINEXP]
            if absent:
                exp = sum(e for _, e in absent)
                print(f"  mod {m:3d}, k={gk}: never r in {sorted(r for r, _ in absent)} "
                      f"(chance expects {exp:.0f} of {len(g)})")

    print("\n== 2. per-representation statements true for EVERY n in the group ==")
    props = rep_props()
    q = {name: sum(f(x, y) for _, _, ps in ctrl for x, y in ps) / sum(len(ps) for _, _, ps in ctrl)
         for name, f in props.items()}
    for gk, g in groups.items():
        if len(g) < 5: continue
        lines = []
        for name, f in props.items():
            cnt = [sum(f(x, y) for x, y in ps) for _, ps in g]
            ks = [len(ps) for _, ps in g]
            stmts = []
            if all(c >= 1 for c in cnt):
                p_chance = 1.0
                for k in ks: p_chance *= 1 - (1 - q[name]) ** k
                stmts.append(("at least one rep", p_chance))
            if all(c == k for c, k in zip(cnt, ks)):
                p_chance = 1.0
                for k in ks: p_chance *= q[name] ** k
                stmts.append(("every rep", p_chance))
            if all(c == 0 for c in cnt):
                p_chance = 1.0
                for k in ks: p_chance *= (1 - q[name]) ** k
                stmts.append(("no rep", p_chance))
            for s, pc in stmts:
                if pc < 0.01:                                     # would be surprising by chance
                    lines.append(f"  k={gk} ({len(g)} n): {s} has [{name}]   (single-rep rate {q[name]:.3f}; "
                                 f"chance of this holding for all: {pc:.1e})")
        print("\n".join(lines) if lines else f"  k={gk}: nothing beyond chance")


if __name__ == "__main__":
    main()
