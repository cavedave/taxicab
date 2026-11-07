#!/usr/bin/env python3
"""bowtie_components2.py -- (F59) per prime and per condition: is the bowtie condition at p a function of the Mordell-Weil
coefficients c mod m (smallest m tried), and does it coincide with 'P reduces to the singular point mod p' on the minimal
model? Prints Kodaira symbol and Tamagawa number at every relevant prime.
Usage: python3 bowtie_components2.py [--cmax 3] [--procs 8] [--extra a,b,i,a2,b2 ...]
"""
import argparse, re, subprocess, sys
from collections import Counter, defaultdict
from fractions import Fraction as Fr
from itertools import product
from math import isqrt
from multiprocessing import Pool
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
from bowtie_mine import Curve, peval
from bowtie_hunt import curves_from_catalogue
from bowtie_congruence import analyse, pf, GPF

MS = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 12, 14, 16, 18, 20, 24]

def seed_of(C, slopes):
    for s, r in slopes:
        x = Fr(r, s); v = peval(C.q, x)
        if v > 0 and isqrt(v.numerator)**2 == v.numerator and isqrt(v.denominator)**2 == v.denominator:
            return x, Fr(isqrt(v.numerator), isqrt(v.denominator))
    out = subprocess.run(["gp", "-q"], input=f"print(hyperellratpoints({C.gp_poly()}, 60));", capture_output=True, text=True).stdout
    pts = [(Fr(x), Fr(y)) for x, y in re.findall(r"\[(-?\d+(?:/\d+)?), (-?\d+(?:/\d+)?)\]", out) if Fr(y) != 0]
    return pts[0] if pts else None

def gp_run(C, seed, rel, cmax):
    x0, w0 = seed
    qpol = "+".join("(%d)*X^%d" % (c, k) for k, c in enumerate(C.q))
    ps = "[" + ",".join(map(str, rel)) + "]"
    src = ["\\r %s" % GPF, "Q = subst(%s, X, %s + u); q0 = %s; E = q2e(Q, q0); Em = ellminimalmodel(E, &ch);" % (qpol, x0, w0),
           'R = iferr(alarm(120, ellrank(E)), e, [0,0,0,[]]); G = vecextract(R[4], Str("1..", min(#R[4], 4)));',
           'print("RANK ", R[1], " ", R[2], " ", #G, " TORS ", elltors(E)[2]);',
           "foreach(%s, p, my(L = elllocalred(Em, p)); print(\"RED \", p, \" \", L[2], \" \", L[4]));" % ps,
           "forvec(c = vector(#G, k, [-%d, %d]), my(P = [0]); for(k = 1, #G, if(c[k], P = elladd(E, P, ellmul(E, G[k], c[k])))); if(#P == 2, my(B = toQ(Q, q0, P)); if(B != 0, print(\"PT \", c, \" \", B[1] + %s, \" \", comps(Em, ellchangepoint(P, ch), %s), \" \", comps(Em, ellchangepoint(elladd(E, P, P), ch), %s)))));" % (cmax, cmax, x0, ps, ps)]
    return subprocess.run(["gp", "-q", "-D", "parisizemax=2000000000"], input="\n".join(src), capture_output=True, text=True).stdout

def kod(k):
    k = int(k)
    return {0: "I0", 1: "II", 2: "III", 3: "IV", -1: "I0*", -2: "II*", -3: "III*", -4: "IV*"}.get(k, f"I{k - 4}" if k > 4 else f"I{-k - 4}*")

def job(args):
    (a, b, i, a2, b2, slopes), cmax = args
    C = Curve(a, b, i, a2, b2); seed = seed_of(C, slopes)
    if seed is None: return (a, b, i, a2, b2), None
    rel = sorted(pf(a*a + a*b + b*b) | pf(b - a) | pf(a2*a2 + a2*b2 + b2*b2) | pf(b2 - a2))
    out = gp_run(C, seed, rel, cmax)
    red, rows, rank = {}, [], "?"
    for l in out.splitlines():
        if l.startswith("RANK"): rank = l[5:]
        elif l.startswith("RED"): _, p, k, c = l.split(); red[int(p)] = (kod(k), int(c))
        elif l.startswith("PT"):
            m = re.match(r"PT \[(.*?)\] (\S+) \[(.*?)\] \[(.*)\]", l)
            c = tuple(int(v) for v in m.group(1).split(",")); x = Fr(m.group(2))
            s1 = {int(v) for v in m.group(3).split(",") if v.strip()}; s2 = {int(v) for v in m.group(4).split(",") if v.strip()}
            sing = {p: ("odd" if p in s2 else "2" if p in s1 else "0") for p in rel}
            o = analyse(C, x.denominator, x.numerator)
            if o: rows.append((c, o[0], sing))
    return (a, b, i, a2, b2), (rank, red, rows, rel)

def min_mod(rows, f, cmax=3):
    for m in [m for m in MS if m <= 2 * cmax]:
        by = defaultdict(set)
        for c, bd, sg in rows: by[tuple(v % m for v in c)].add(f(bd, sg))
        if all(len(v) == 1 for v in by.values()): return m
    return None

def main():
    ap = argparse.ArgumentParser(); ap.add_argument("--cmax", type=int, default=3); ap.add_argument("--procs", type=int, default=8)
    ap.add_argument("--extra", nargs="*", default=[]); ap.add_argument("--only-extra", action="store_true"); A = ap.parse_args()
    cs = [] if A.only_extra else curves_from_catalogue()
    cs += [tuple(map(int, e.split(","))) + ([],) for e in A.extra]
    T = Counter()
    with Pool(A.procs) as pool:
        for key, res in pool.imap_unordered(job, [(c, A.cmax) for c in cs]):
            if res is None or not res[2]: print(key, "no points"); continue
            rank, red, rows, rel = res
            a, b, i, a2, b2 = key
            where = lambda p: "+".join(nm for nm, m in (("E1", a*a + a*b + b*b), ("b-a", b - a), ("E2", a2*a2 + a2*b2 + b2*b2), ("b2-a2", b2 - a2)) if m % p == 0)
            nb = sum(1 for c, bd, sg in rows if not any(bd.values()))
            print(f"{key} rank {rank}: {len(rows)} pts, {nb} bowties", flush=True)
            for p in rel:
                for kind in ("base", "den", "sec"):
                    if not any(p in bd[kind] for c, bd, sg in rows): continue
                    m = min_mod(rows, lambda bd, sg: p in bd[kind])
                    byc = defaultdict(set)
                    for c, bd, sg in rows: byc[sg[p]].add(p in bd[kind])
                    rel_s = ("fails on components " + ",".join(sorted(k for k, v in byc.items() if v == {True})) + " passes on " + ",".join(sorted(k for k, v in byc.items() if v == {False}))) if all(len(v) == 1 for v in byc.values()) else "not a function of the component (" + ", ".join(f"{k}: {sorted(v)}" for k, v in sorted(byc.items())) + ")"
                    k, cp = red.get(p, ("?", 0))
                    print(f"   p={p} [{where(p)}] {kind}: fails {sum(1 for c, bd, sg in rows if p in bd[kind])}/{len(rows)}; function of c mod {m}; {k} c_p={cp}; vs singular reduction: {rel_s}", flush=True)
                    T[(kind, where(p), "mod m found" if m else "no m <= 24", rel_s)] += 1
            mall = min_mod(rows, lambda bd, sg: any(bd.values()))
            T[("joint", "mod m found" if mall else "no m <= 24")] += 1
            print(f"   joint: function of c mod {mall}", flush=True)
    print("\nSUMMARY"); [print(f"  {k}: {v}") for k, v in sorted(T.items(), key=str)]

if __name__ == "__main__":
    main()
