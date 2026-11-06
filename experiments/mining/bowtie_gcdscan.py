import subprocess, sys
from fractions import Fraction as Fr
from math import isqrt, gcd
from collections import Counter
from pathlib import Path
sys.path.insert(0, "/Users/davidcurran/Documents/taxicab/experiments/mining")
from bowtie_mine import Curve, peval
from bowtie_hunt import curves_from_catalogue
GPF = "/Users/davidcurran/Documents/taxicab/experiments/mining/verify_gp/quartic2ell.gp"
small = [2, 3, 5, 7, 11, 13, 17, 19, 31, 37, 43]
primes = Counter(); fails = tested = secf = 0
for (a, b, i, a2, b2, slopes) in curves_from_catalogue()[:60]:
    C = Curve(a, b, i, a2, b2); known = []
    for s, r in slopes:
        x = Fr(r, s); v = peval(C.q, x)
        if v > 0 and isqrt(v.numerator)**2 == v.numerator and isqrt(v.denominator)**2 == v.denominator:
            known.append((x, Fr(isqrt(v.numerator), isqrt(v.denominator))))
    if not known: continue
    x0, w0 = known[0]
    qpol = "+".join("(%d)*X^%d" % (c, k) for k, c in enumerate(C.q))
    lines = ["\\r " + GPF,
             "Q = subst(%s, X, %s + u); q0 = %s; E = q2e(Q, q0);" % (qpol, x0, w0),
             'R = iferr(alarm(60, ellrank(E)), e, [0,0,0,[]]); G = vecextract(R[4], Str("1..", min(#R[4], 4)));',
             "forvec(c = vector(#G, k, [-2, 2]), my(P = [0]); for(k = 1, #G, if(c[k], P = elladd(E, P, ellmul(E, G[k], c[k])))); if(#P == 2, my(B = toQ(Q, q0, P)); if(B != 0, print(B[1] + %s))));" % x0]
    out = subprocess.run(["gp", "-q", "-D", "parisizemax=2000000000"], input="\n".join(lines), capture_output=True, text=True)
    for tok in out.stdout.split():
        x = Fr(tok); s, r = x.denominator, x.numerator; tested += 1
        res, why = C.bowtie(s, r)
        if why == "base triple not coprime":
            R = C.raw(s, r); G = 0
            for X, Y in R: G = gcd(G, gcd(X, Y))
            g = 1
            for X, Y in R: g *= gcd(X // G, Y // G)
            fails += 1; rest = g
            for p in small:
                while rest % p == 0: rest //= p
            primes[tuple(p for p in small if g % p == 0) + (("larger",) if rest > 1 else ())] += 1
        elif why == "second line not integral": secf += 1
print("points tested %d; base triple not coprime %d; second line not integral %d" % (tested, fails, secf))
print("primes in the base triple's gcds:", primes.most_common(12))
