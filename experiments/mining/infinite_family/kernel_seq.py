#!/usr/bin/env python3
"""kernel_test.py -- step 3 of the proof plan, explicitly. With P0 (a bowtie) as origin: points P = 2 * sum c_k G_k
that also reduce to the identity mod p (on the minimal model) for each p in PRIMES should all be bowties.
Prints, for c in a box, whether P is in that kernel K and whether P is a bowtie."""
import sys, itertools, collections, subprocess
from fractions import Fraction as Fr
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
if hasattr(sys, "set_int_max_str_digits"): sys.set_int_max_str_digits(0)
import bowtie_decide as BD
from bowtie_mine import Curve
from bowtie_hunt import curves_from_catalogue
from bowtie_components2 import seed_of

key = tuple(map(int, sys.argv[1:6])); PRIMES = list(map(int, sys.argv[6].split(","))); B = int(sys.argv[7])
C = Curve(*key); slopes = next((c[5] for c in curves_from_catalogue() if tuple(c[:5]) == key), [])
seed = seed_of(C, slopes, 300)
head, x0 = BD.setup(C, seed, [])
r = 5
box = [c for c in itertools.product(range(-B, B + 1), repeat=r) if any(c)] if B > 0 else [tuple(j * v for v in (0, 1, 1, -2, -2)) for j in range(1, 11)]
src = head + ["Em = ellminimalmodel(E, &chg); H = vector(#G, k, ellmul(E, G[k], 2));",
              "CS = [%s];" % ";".join(",".join(map(str, c)) for c in box),
              "for(j = 1, #CS~, my(c = CS[j,], P = [0], Pm, d, ink = 1); for(k = 1, #H, if(c[k], P = elladd(E, P, ellmul(E, H[k], c[k])))); "
              "if(#P == 2, Pm = ellchangepoint(P, chg); d = denominator(Pm[1]); "
              "foreach([%s], p, if(d %% p, ink = 0)); my(B0 = toQ(Q, q0, P)); if(B0 != 0, print(\"PT \", j, \" \", ink, \" \", B0[1] + %s))));" % (",".join(map(str, PRIMES)), x0)]
out = subprocess.run(["gp", "-q", "-D", "parisizemax=4000000000"], input="\n".join(src), capture_output=True, text=True).stdout
tally = collections.Counter(); kern = []
for l in out.splitlines():
    if not l.startswith("PT "): continue
    _, j, ink, x = l.split(); x = Fr(x); o, w = C.bowtie(x.denominator, x.numerator)
    tally[("in K" if ink == "1" else "not in K", "BOWTIE" if o else w)] += 1
    if ink == "1": kern.append((box[int(j) - 1], o is not None))
    if B == 0: print(" j =", int(j), "in K" if ink == "1" else "NOT in K", w, f"(n has {len(str(o[0]))} digits)" if o else "")
for k in sorted(tally): print(k, tally[k])
print("kernel vectors (c with 2 sum c_k G_k reducing to O mod", PRIMES, "):", len(kern))
print("  first few:", [c for c, ok in kern[:8]])
print("  all bowties:", all(ok for c, ok in kern))
