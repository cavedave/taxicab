#!/usr/bin/env python3
"""bowtie_components.py -- FINDINGS F57: is the bowtie class of a point on a seeded bowtie curve a function of its
local components (whether it reduces to the singular point mod p, at each prime of bad reduction of the minimal model)?
For every seeded curve: quartic -> Weierstrass (seed = O), ellrank generators, combinations with |c| <= cmax; for each
point the bowtie class (bowtie_mine.Curve.bowtie on its x) and the set of bad primes where it is singular mod p.
Usage: python3 bowtie_components.py [--cmax 2] [--curves 0-20]"""
import argparse, subprocess, sys
from fractions import Fraction as Fr
from math import isqrt
from collections import Counter, defaultdict
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
from bowtie_mine import Curve, peval
from bowtie_hunt import curves_from_catalogue

def analyse(curve, known, cmax, gp="gp"):
    x0, w0 = known[0]
    qpol = "+".join(f"({c})*X^{k}" for k, c in enumerate(curve.q))
    hints = ",".join(f"toE(Q, q0, {x} - ({x0}), {w})" for x, w in known[1:] if x != x0)
    src = f"""\\r {Path(__file__).resolve().parent}/verify_gp/quartic2ell.gp
Q = subst({qpol}, X, {x0} + u); q0 = {w0}; E = q2e(Q, q0);
H = [{hints}]; H = select(P -> #P == 2, H);
R = iferr(alarm(120, ellrank(E, 1, H)), e, [0, 0, 0, H]); G = R[4]; if(#G == 0, G = H); G = vecextract(G, Str("1..", min(#G, 5)));
Em = ellminimalmodel(E, &v); ps = factor(Em.disc)[, 1]~;
print("BAD ", ps, " TAM ", vector(#ps, i, elllocalred(Em, ps[i])[4]), " KOD ", vector(#ps, i, elllocalred(Em, ps[i])[2]));
{{forvec(c = vector(#G, k, [-{cmax}, {cmax}]),
  my(P = [0]); for(k = 1, #G, if(c[k], P = elladd(E, P, ellmul(E, G[k], c[k]))));
  if(#P == 2, my(B = toQ(Q, q0, P)); if(B != 0, print("PT ", B[1] + {x0}, " ", c % 2, " ", comps(Em, ellchangepoint(P, v), ps)))));}}
"""
    out = subprocess.run([gp, "-q", "-D", "parisizemax=4000000000"], input=src, capture_output=True, text=True).stdout
    bad, rows = None, []
    for line in out.splitlines():
        if line.startswith("BAD "): bad = line
        elif line.startswith("PT "):
            x, rest = line[3:].split(" ", 1); x = Fr(x)
            par, comp = rest.strip().split("] ", 1)
            rows.append((curve.bowtie(x.denominator, x.numerator)[1], par + "]"))
    return bad, rows

def main():
    ap = argparse.ArgumentParser(); ap.add_argument("--cmax", type=int, default=2); ap.add_argument("--curves", default="")
    A = ap.parse_args()
    cs = curves_from_catalogue()
    if A.curves: lo, hi = map(int, A.curves.split("-")); cs = cs[lo:hi + 1]
    func_ok = 0; total = 0; pattern = Counter(); prime_role = Counter()
    for (a, b, i, a2, b2, slopes) in cs:
        C = Curve(a, b, i, a2, b2); known = []
        for s, r in slopes:
            x = Fr(r, s); v = peval(C.q, x)
            if v > 0 and isqrt(v.numerator)**2 == v.numerator and isqrt(v.denominator)**2 == v.denominator:
                known += [(x, Fr(isqrt(v.numerator), isqrt(v.denominator))), (x, -Fr(isqrt(v.numerator), isqrt(v.denominator)))]
        if not known: continue
        bad, rows = analyse(C, known, A.cmax)
        if not rows: continue
        by = defaultdict(Counter)
        for cls, comp in rows: by[comp][cls] += 1
        consistent = all(len(v) == 1 for v in by.values())
        bowtie_comps = {c for c, v in by.items() if "BOWTIE" in v}
        total += 1; func_ok += consistent
        pattern[(consistent, "bowtie iff no singular prime" if bowtie_comps == {"[]"} else f"bowtie components {sorted(bowtie_comps)[:3]}")] += 1
        print(f"({a},{b}) pt {i} + ({a2},{b2}): {len(rows)} points; {bad}", flush=True)
        for comp, cls in sorted(by.items(), key=lambda t: -sum(t[1].values()))[:6]: print(f"     singular at {comp:24s} {dict(cls)}")
    print(f"\nclass is a function of the component pattern on {func_ok} of {total} curves"); print(dict(pattern))

if __name__ == "__main__":
    main()
