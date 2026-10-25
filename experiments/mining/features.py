#!/usr/bin/env python3
"""features.py -- mining stages 1, 2, 5, 7 for coprime cabtaxi data (format n;k;x:y,...).

  stage 1  audit: every pair exact (x^3 + y^3 == n), coprime, distinct, count == k
  stage 2  per representation: s = x + y, t = x^2 - x y + y^2 (so n = s t), sum or difference
  stage 5  factorisation of n (PARI, batched): split primes (p = 1 mod 3), the non-split part, cube-free
  stage 7  residues of n mod 7, 9, 13
  plus the TODO-theorem measurement: does every prime p != 1 (mod 3) dividing n divide every s?

Output: one CSV row per n (header line first). Input files may be search output or control windows;
--tag labels the dataset (e.g. "ctrl_1e15", "a047697").

Usage:  python3 features.py --tag ctrl_1e15 ctrl_1e15.txt --out feat_ctrl_1e15.csv [--gp gp]
"""
from __future__ import annotations

import argparse, csv, re, subprocess
from math import gcd


def read(paths):
    for p in paths:
        for line in open(p):
            if not line[0].isdigit(): continue
            n, k, ps = line.strip().split(";")[:3]
            yield int(n), int(k), [tuple(map(int, q.split(":"))) for q in ps.split(",") if q]


def factor_batch(ns, gp, chunk=2000):
    out = []
    for i in range(0, len(ns), chunk):
        part = ns[i:i + chunk]
        res = subprocess.run([gp, "-q"], input="\n".join(f"print(factor({n}));" for n in part),
                             capture_output=True, text=True, check=True).stdout.strip().splitlines()
        assert len(res) == len(part)
        for f in res:
            body = re.search(r"\[([^\[\]]*)\]", f.replace("Mat(", "")).group(1)   # "[p,e;q,f]" or "Mat([p, e])"
            out.append([tuple(int(v) for v in r.split(",")) for r in body.replace(" ", "").split(";")])
    return out


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("inputs", nargs="+")
    ap.add_argument("--tag", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--gp", default="gp")
    ap.add_argument("--kmin", type=int, default=1)
    a = ap.parse_args()
    rows = [r for r in read(a.inputs) if r[1] >= a.kmin]
    facs = factor_batch([n for n, _, _ in rows], a.gp)
    fields = ["tag", "n", "k", "digits", "mod7", "mod9", "mod13", "r_split", "split_primes", "nonsplit",
              "cubefree", "squarefree", "v3", "has7", "smallest_split", "max_prime_digits",
              "n_sums", "n_diffs", "nonsplit_divides_all_s", "gcd_all_s"]
    with open(a.out, "w", newline="") as fo:
        w = csv.DictWriter(fo, fieldnames=fields); w.writeheader()
        for (n, k, pairs), fac in zip(rows, facs):
            # stage 1: audit
            assert len(pairs) == k and len(set(pairs)) == k, f"count mismatch at {n}"
            assert all(x**3 + y**3 == n and gcd(x, abs(y)) == 1 for x, y in pairs), f"bad pair at {n}"
            # stage 2: s and t for each representation
            ss = [x + y for x, y in pairs]
            assert all((x + y) * (x * x - x * y + y * y) == n for x, y in pairs)
            g = 0
            for s in ss: g = gcd(g, s)
            # stage 5: factorisation
            split = sorted(p for p, e in fac if p % 3 == 1)
            nonsplit = [(p, e) for p, e in fac if p % 3 != 1]
            ns_ok = all(all(s % p == 0 for s in ss) for p, _ in nonsplit)
            w.writerow(dict(
                tag=a.tag, n=n, k=k, digits=len(str(n)), mod7=n % 7, mod9=n % 9, mod13=n % 13,
                r_split=len(split), split_primes=" ".join(map(str, split)),
                nonsplit=" ".join(f"{p}^{e}" if e > 1 else str(p) for p, e in nonsplit),
                cubefree=int(all(e < 3 for _, e in fac)), squarefree=int(all(e < 2 for _, e in fac)),
                v3=sum(e for p, e in fac if p == 3), has7=int(any(p == 7 for p, _ in fac)),
                smallest_split=split[0] if split else "", max_prime_digits=len(str(max(p for p, _ in fac))),
                n_sums=sum(y > 0 for _, y in pairs), n_diffs=sum(y < 0 for _, y in pairs),
                nonsplit_divides_all_s=int(ns_ok), gcd_all_s=g))
    print(f"{a.tag}: {len(rows)} rows audited and featurised -> {a.out}")


if __name__ == "__main__":
    main()
