"""bowtie_parity.py -- (F58) is each bowtie condition, and their conjunction, a function of the Mordell-Weil coefficients mod 2?"""
import sys, subprocess, re
from fractions import Fraction as Fr
from collections import defaultdict
sys.path.insert(0, __import__("os").path.dirname(__import__("os").path.abspath(__file__)))
from bowtie_mine import Curve
from bowtie_congruence import analyse, GPF
for key in [(3, 4, 0, 3, 16), (3, 4, 0, 27, 28), (3, 4, 0, 9, 52)]:
    C = Curve(*key)
    out = subprocess.run(["gp", "-q"], input=f"print(hyperellratpoints({C.gp_poly()}, 60));", capture_output=True, text=True).stdout
    x0, w0 = [(Fr(x), Fr(y)) for x, y in re.findall(r"\[(-?\d+(?:/\d+)?), (-?\d+(?:/\d+)?)\]", out) if Fr(y) != 0][0]
    qpol = "+".join("(%d)*X^%d" % (c, k) for k, c in enumerate(C.q))
    src = ["\\r %s" % GPF, "Q = subst(%s, X, %s + u); q0 = %s; E = q2e(Q, q0);" % (qpol, x0, w0),
           'R = ellrank(E); G = vecextract(R[4], Str("1..", min(#R[4], 4)));',
           "forvec(c = vector(#G, k, [-3, 3]), my(P = [0]); for(k = 1, #G, if(c[k], P = elladd(E, P, ellmul(E, G[k], c[k])))); if(#P == 2, my(B = toQ(Q, q0, P)); if(B != 0, print(c, \" \", B[1] + %s))));" % x0]
    rows = []
    for l in subprocess.run(["gp", "-q", "-D", "parisizemax=2000000000"], input="\n".join(src), capture_output=True, text=True).stdout.splitlines():
        m = re.match(r"\[(.*)\] (\S+)", l)
        if not m: continue
        c = tuple(int(v) for v in m.group(1).split(",")); x = Fr(m.group(2))
        o = analyse(C, x.denominator, x.numerator)
        if o: rows.append((c, o[0]))
    ps = sorted(set().union(*(bd[k] for c, bd in rows for k in bd)))
    print(key, len(rows), "points; primes", ps, "bowties", sum(1 for c, bd in rows if not any(bd.values())))
    for p in ps + ["all"]:
        by = defaultdict(set)
        for c, bd in rows:
            ok = not any(bd.values()) if p == "all" else not any(p in bd[k] for k in bd)
            by[tuple(v % 2 for v in c)].add(ok)
        dec = all(len(v) == 1 for v in by.values())
        print(f"   p={p}: pass a function of c mod 2: {dec}; classes mod 2 passing {sum(1 for v in by.values() if True in v)} / {len(by)}"
              + ("" if dec else f" (mixed {sum(1 for v in by.values() if len(v) > 1)})"))
