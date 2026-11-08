#!/usr/bin/env python3
"""coset_test.py -- test the planned proof: with a known bowtie P0 as origin of E (the curve of bowties of one
direction pair), is every point of m E(Q) a coprime integral bowtie for a suitable m?

Usage: python3 coset_test.py a b i a2 b2 [--ms 1,2,3,4,6,12] [--jmax 10]
"""
import argparse, sys, time, collections
from fractions import Fraction as Fr
from pathlib import Path
HERE = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(HERE))
if hasattr(sys, "set_int_max_str_digits"): sys.set_int_max_str_digits(0)
import bowtie_decide as BD
from bowtie_mine import Curve
from bowtie_hunt import curves_from_catalogue
from bowtie_components2 import seed_of

def points(head, x0, cs):
    out = BD.gp(BD.pts_src(head, x0, cs) + ['print("DONE");'])
    xs = {}
    for l in out.splitlines():
        if l.startswith("PT "):
            _, j, x = l.split(); xs[int(j) - 1] = Fr(x)
    return [xs.get(k) for k in range(len(cs))]

def main():
    ap = argparse.ArgumentParser(); ap.add_argument("key", nargs=5, type=int)
    ap.add_argument("--ms", default="1,2,3,4,6,8,12,24"); ap.add_argument("--jmax", type=int, default=10)
    A = ap.parse_args(); key = tuple(A.key); BD.GPTIME = 3600
    C = Curve(*key)
    slopes = next((c[5] for c in curves_from_catalogue() if tuple(c[:5]) == key), [])
    seed = seed_of(C, slopes, 300)
    print("curve", key, "seed (P0 = origin):", seed, "from catalogue bowtie" if slopes else "from point search")
    a, b, i, a2, b2 = key
    rel = sorted(BD.pf(a*a + a*b + b*b) | BD.pf(b - a) | BD.pf(a2*a2 + a2*b2 + b2*b2) | BD.pf(b2 - a2))
    head, x0 = BD.setup(C, seed, rel)
    info = BD.gp(head + ['print("RANK ", R[1], " ", R[2], " ", #G, " ", ord);'])
    print(info.strip(), "| relevant primes", rel)
    r = int(info.split()[3]); ordv = info.split("[")[1].rstrip("]\n ")
    ntor = len([v for v in ordv.split(",") if v.strip()]) - r if ordv.strip() else 0
    dim = r + ntor
    # 1. which m make m * (small combination) a bowtie?
    import itertools
    small = [c for c in itertools.product(range(-1, 2), repeat=r) if any(c)]
    small = [list(c) + [0] * ntor for c in small]
    print(f"{len(small)} small combinations Q = sum c_k G_k, c_k in {{-1, 0, 1}}")
    best = None
    for m in map(int, A.ms.split(",")):
        cs = [[m * v for v in c] for c in small]
        xs = points(head, x0, cs)
        why = collections.Counter()
        for x in xs:
            if x is None: why["no affine point"] += 1; continue
            o, w = C.bowtie(x.denominator, x.numerator); why[w] += 1
        print(f"  m = {m:2d}: {dict(why)}", flush=True)
        if why.get("BOWTIE", 0) == len(cs) and best is None: best = m
    if best is None: print("no tested m makes every point a bowtie"); return
    # 2. the sequence j m Q for a fixed Q = sum of the generators
    Q = [1] * r + [0] * ntor
    cs = [[j * best * v for v in Q] for j in range(1, A.jmax + 1)]
    t = time.time(); xs = points(head, x0, cs)
    print(f"sequence j * {best} * (G_1 + ... + G_{r}), j = 1..{A.jmax}:")
    for j, x in enumerate(xs, 1):
        o, w = C.bowtie(x.denominator, x.numerator) if x is not None else (None, "no affine point")
        print(f"  j = {j:2d}: {w}" + (f", n has {len(str(o[0]))} digits" if o else ""), flush=True)
    print(f"({time.time() - t:.0f} s)")

if __name__ == "__main__":
    main()
