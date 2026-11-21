"""Combine strip.json + fac.json: fully factored numbers -> ready.unk (sixway.py 'count:' format, product checked);
the rest -> hard.txt (n; composites still to factor)."""
import json, sys
if hasattr(sys, "set_int_max_str_digits"): sys.set_int_max_str_digits(0)
S = json.load(open("strip.json")); FA = json.load(open("fac.json"))
ready = open("ready.unk", "w"); hard = open("hard.txt", "w"); nr = nh = 0
for r in S:
    n = int(r["n"]); F = {int(p): e for p, e in r["F"].items()}; left = []
    for c, e in r["composite"]:
        f = FA.get(c)
        if f is None: left.append(c); continue
        for p, ee in f: F[int(p)] = F.get(int(p), 0) + int(ee) * e
    if left:
        hard.write(f"{n};{r['kind']};{','.join(left)}\n"); nh += 1; continue
    prod = 1
    for p, e in F.items(): prod *= p ** e
    assert prod == n
    fs = "*".join(f"{p}^{e}" for p, e in sorted(F.items()))
    ready.write(f"{n};count:{sum(p % 3 == 1 for p in F)} split primes;{fs};{r['kind']}\n"); nr += 1
print("fully factored", nr, "still hard", nh)
