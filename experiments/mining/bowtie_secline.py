import subprocess, sys
from fractions import Fraction as Fr
from math import isqrt, gcd
from collections import Counter, defaultdict
sys.path.insert(0, "/Users/davidcurran/Documents/taxicab/experiments/mining")
from bowtie_mine import Curve, peval
import line_enum as L
GPF = "/Users/davidcurran/Documents/taxicab/experiments/mining/verify_gp/quartic2ell.gp"
def proj(s, r, q, p):
    if s % p: return ("t", r * pow(s, -1, q) % q)
    return ("u", s * pow(r, -1, q) % q)
def points(C, seed, cmax):
    x0, w0 = seed
    qpol = "+".join("(%d)*X^%d" % (c, k) for k, c in enumerate(C.q))
    lines = ["\\r " + GPF, "Q = subst(%s, X, %s + u); q0 = %s; E = q2e(Q, q0);" % (qpol, x0, w0),
             'R = iferr(alarm(60, ellrank(E)), e, [0,0,0,[]]); G = vecextract(R[4], Str("1..", min(#R[4], 4)));',
             "forvec(c = vector(#G, k, [-%d, %d]), my(P = [0]); for(k = 1, #G, if(c[k], P = elladd(E, P, ellmul(E, G[k], c[k])))); if(#P == 2, my(B = toQ(Q, q0, P)); if(B != 0, print(B[1] + %s))));" % (cmax, cmax, x0)]
    out = subprocess.run(["gp", "-q", "-D", "parisizemax=2000000000"], input="\n".join(lines), capture_output=True, text=True).stdout
    return [Fr(t) for t in out.split()]
def second_line(C, s, r):
    R = C.raw(s, r); G = 0
    for X, Y in R: G = gcd(G, gcd(X, Y))
    pts = [(X // G, Y // G) for X, Y in R]
    x, y = pts[C.i]; vx, vy = C.b2, -C.a2
    A = vx**3 + vy**3; Bq = 3 * (x * vx * vx + y * vy * vy); Cq = 3 * (x * x * vx + y * y * vy); D = Bq * Bq - 4 * A * Cq
    w = isqrt(D)
    if w * w != D: return None
    dens = 1
    for e in (1, -1):
        t = Fr(-Bq + e * w, 2 * A); dens = dens * (x + t * vx).denominator // gcd(dens, (x + t * vx).denominator); dens = dens * (y + t * vy).denominator // gcd(dens, (y + t * vy).denominator)
    return dens
for (i, a2, b2, seed_sr) in [(0, 9, 52, (30, 47)), (1, 27, 28, (2357, 6579))]:
    C = Curve(3, 4, i, a2, b2)
    x = Fr(seed_sr[1], seed_sr[0]); v = peval(C.q, x); seed = (x, Fr(isqrt(v.numerator), isqrt(v.denominator)))
    xs = points(C, seed, 3)
    dens = [(xx.denominator, xx.numerator, second_line(C, xx.denominator, xx.numerator)) for xx in xs]
    dens = [d for d in dens if d[2] is not None]
    allp = Counter()
    for s, r, d in dens:
        for p, e in L.factor(d).items(): allp[p] += 1
    print(f"(3,4) pt {i} + ({a2},{b2}): {len(dens)} points, second line non-integral in {sum(d > 1 for *_, d in dens)}; primes in denominators: {dict(allp)}")
    for p in sorted(allp):
        for k in (1, 2, 3):
            q = p**k; cls = defaultdict(set)
            for s, r, d in dens: cls[proj(s, r, q, p)].add(d % p == 0)
            if all(len(v) == 1 for v in cls.values()):
                print(f"    p = {p}: decided by (s : r) mod {p}^{k} ({sum(1 for v in cls.values() if True in v)} bad of {len(cls)} classes seen)"); break
        else: print(f"    p = {p}: NOT decided by (s : r) mod p^3 on these points")
