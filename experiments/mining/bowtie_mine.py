#!/usr/bin/env python3
"""bowtie_mine.py -- mine coprime five-ways from the genus-1 bowtie curves (FINDINGS F53), for every known bowtie.

A bowtie = two lines through a shared representation C. Take the cheaper line as the base, direction (a, b) as
line_enum orients it (points swapped if the line came as (b, a)); its triple has a slope (s, r) and C is raw point i.
The second line has direction (a2, b2). Bowties of the same (a, b, i, a2, b2) are the rational points of
    w^2 = Delta(r) = 9 (X v_x^2 + Y v_y^2)^2 - 12 (v_x^3 + v_y^3)(X^2 v_x + Y^2 v_y),  (X, Y) = raw point i at slope (1, r),
v = (b2, -a2): a quartic, generically genus 1.  Steps per curve:
  rank      PARI ellfromeqn + ellrank (time limit)
  generate  group law on w^2 = Delta: the parabola through three points counted with multiplicity (Hermite conditions,
            so one known point suffices: tangent and osculating parabolas) meets the curve in a fourth rational point
  test      each point -> (3,4)-type triple + second line; integral and coprime -> a coprime five-way candidate
  count     exactly, from n = E s1 s2 s3 / (a - b)^2 (Theorem 13): the s_i of the base triple, E and a - b are factored
            (PARI), and every representation is listed (verify_gp/reps.gp: repsf)
Usage: python3 bowtie_mine.py --rounds 2 --out mined.txt [--only-rank]
"""
import argparse, itertools, math, re, subprocess, sys, time
from fractions import Fraction as Fr
from math import gcd, isqrt
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
import line_enum as L
from line_heights import raw_forms
from line_complete import Direction, setup_canon, canon_slope

def lines_of(reps):
    pts = reps + [(y, x) for x, y in reps]; out = {}
    for P, Q, R in itertools.combinations(pts, 3):
        if len({tuple(sorted(p)) for p in (P, Q, R)}) < 3: continue
        (x1, y1), (x2, y2), (x3, y3) = P, Q, R
        if (x2 - x1) * (y3 - y1) != (y2 - y1) * (x3 - x1): continue
        a, b = y2 - y1, x1 - x2; g = gcd(a, b); a, b = a // g, b // g
        if a < 0 or (a == 0 and b < 0): a, b = -a, -b
        out.setdefault(frozenset(tuple(sorted(p)) for p in (P, Q, R)), ((a, b), (P, Q, R)))
    return list(out.values())

# ---------- polynomials in r (lists, constant term first) ----------
def padd(p, q): n = max(len(p), len(q)); return [(p[i] if i < len(p) else 0) + (q[i] if i < len(q) else 0) for i in range(n)]
def pmul(p, q):
    out = [0] * (len(p) + len(q) - 1)
    for i, x in enumerate(p):
        for j, y in enumerate(q): out[i + j] += x * y
    return out
def pscale(p, c): return [c * x for x in p]
def peval(p, x): v = 0; [v := v * x + c for c in reversed(p)]; return v
def pder(p): return [i * p[i] for i in range(1, len(p))]

class Curve:
    def __init__(self, a, b, i, a2, b2):
        self.a, self.b, self.i, self.a2, self.b2 = a, b, i, a2, b2
        self.P0 = L.conic_points([(a, b)])[0]
        self.raw, coord, _ = raw_forms(a, b, self.P0)
        X = [coord[2 * i][0], coord[2 * i][1], coord[2 * i][2]]          # A + B r + C r^2  (s = 1)
        Y = [coord[2 * i + 1][0], coord[2 * i + 1][1], coord[2 * i + 1][2]]
        vx, vy = b2, -a2
        t1 = padd(pscale(X, vx * vx), pscale(Y, vy * vy))
        t2 = padd(pscale(pmul(X, X), vx), pscale(pmul(Y, Y), vy))
        self.q = padd(pscale(pmul(t1, t1), 9), pscale(t2, -12 * (vx**3 + vy**3)))
        while self.q and self.q[-1] == 0: self.q.pop()
        self.E = a*a + a*b + b*b

    def gp_poly(self, var="x"):
        return "+".join(f"({c})*{var}^{k}" for k, c in enumerate(self.q) if c) or "0"

    def bowtie(self, s, r):
        """five integral coprime points (n > 0) or a reason"""
        if s < 0: s, r = -s, -r
        if gcd(s, r) != 1: return None, "slope not reduced"
        R = self.raw(s, r); G = 0
        for x, y in R: G = gcd(G, gcd(x, y))
        if G == 0: return None, "degenerate"
        pts = [(x // G, y // G) for x, y in R]
        if any(p == 0 or q == 0 or gcd(p, q) != 1 for p, q in pts): return None, "base triple not coprime"
        x, y = pts[self.i]; vx, vy = self.b2, -self.a2
        A = vx**3 + vy**3; Bq = 3 * (x * vx * vx + y * vy * vy); Cq = 3 * (x * x * vx + y * y * vy); D = Bq * Bq - 4 * A * Cq
        w = isqrt(D) if D >= 0 else -1
        if w < 0 or w * w != D: return None, "not on the curve"
        out = []
        for e in (1, -1):
            t = Fr(-Bq + e * w, 2 * A); X, Y = x + t * vx, y + t * vy
            if X.denominator != 1 or Y.denominator != 1: return None, "second line not integral"
            out.append((int(X), int(Y)))
        if any(p == 0 or q == 0 or gcd(p, q) != 1 for p, q in out): return None, "second line not coprime"
        allp = pts + out
        if len({tuple(sorted(p)) for p in allp}) < 5: return None, "repeated point"
        n = allp[0][0]**3 + allp[0][1]**3
        if n < 0: allp = [(-p, -q) for p, q in allp]; n = -n
        return (n, allp, [x + y for x, y in allp[:3]]), "BOWTIE"

    def fourth(self, pts):
        """the parabola through three points with multiplicity ([(x, w)], repeats = tangency) meets w^2 = q again"""
        xs = [p[0] for p in pts]
        # Hermite interpolation of w(x) along the curve: derivatives from w^2 = q
        conds = []
        for x0, w0 in set(pts):
            m = xs.count(x0)
            if w0 == 0: return None
            q0, q1, q2 = peval(self.q, x0), peval(pder(self.q), x0), peval(pder(pder(self.q)), x0)
            d1 = q1 / (2 * w0); d2 = (q2 - 2 * d1 * d1) / (2 * w0)
            conds.append((x0, [w0, d1, d2][:m]))
        # solve for y = a x^2 + b x + c: rows for value, first and second derivative conditions
        rows, rhs = [], []
        for x0, ds in conds:
            for k, v in enumerate(ds):
                rows.append([x0 * x0, x0, 1] if k == 0 else ([2 * x0, 1, 0] if k == 1 else [2, 0, 0])); rhs.append(v)
        if len(rows) != 3: return None
        M = [r + [v] for r, v in zip(rows, rhs)]
        for c in range(3):
            piv = next((k for k in range(c, 3) if M[k][c] != 0), None)
            if piv is None: return None
            M[c], M[piv] = M[piv], M[c]
            for k in range(3):
                if k != c and M[k][c] != 0:
                    f = M[k][c] / M[c][c]; M[k] = [u - f * v for u, v in zip(M[k], M[c])]
        a_, b_, c_ = (M[k][3] / M[k][k] for k in range(3))
        lead = self.q[4] - a_ * a_ if len(self.q) == 5 else None
        if lead is None or lead == 0: return None
        c3 = self.q[3] - 2 * a_ * b_
        x4 = -c3 / lead - sum(xs)
        w4 = a_ * x4 * x4 + b_ * x4 + c_
        if peval(self.q, x4) != w4 * w4: return None
        return (x4, w4)

class Group:
    """the group law on w^2 = q(r) from the fourth-point map F (the four points on a parabola sum to a fixed class):
    with O as zero, K = F(O,O,O), -P = F(P,O,K), P + Q = F(F(P,Q,O),O,O)"""
    def __init__(self, curve, O):
        self.C, self.O = curve, O; self.K = curve.fourth([O, O, O])
    def F(self, P, Q, R):
        if None in (P, Q, R): return None
        try: return self.C.fourth([P, Q, R])
        except ZeroDivisionError: return None
    def neg(self, P): return self.F(P, self.O, self.K)
    def add(self, P, Q):
        if P == self.O: return Q
        if Q == self.O: return P
        return self.F(self.F(P, Q, self.O), self.O, self.O)
    def mul(self, P, k):
        if k < 0: P, k = self.neg(P), -k
        R, A = self.O, P
        while k and A is not None and R is not None:
            if k & 1: R = self.add(R, A)
            A = self.add(A, A); k >>= 1
        return R

def height(P):
    return max(abs(P[0].numerator), P[0].denominator).bit_length() if P is not None else 10**9

def lattice_points(curve, known, cmax, hbits):
    """small integer combinations of the known points (relative to O = known[0]), height <= hbits"""
    known = sorted(set(known), key=height)
    if not known: return set()
    G = Group(curve, known[0])
    if G.K is None: return set(known)
    basis = [P for P in known[1:5] if P != G.O]
    basis = basis[:4]
    out = set(known)
    for cs in itertools.product(range(-cmax, cmax + 1), repeat=len(basis)):
        if not any(cs): continue
        R = G.O
        for c, P in zip(cs, basis):
            if c == 0: continue
            T = G.mul(P, c)
            R = G.add(R, T) if T is not None else None
            if R is None or height(R) > hbits: R = None; break
        if R is not None and R[1] != 0: out.add(R); out.add((R[0], -R[1]))
    return out

def rank_of(curve, gp, tlim):
    src = f'iferr(my(e = ellinit(ellfromeqn(y^2 - ({curve.gp_poly()}))), R = alarm({tlim}, ellrank(e))); print(R[1], " ", R[2]), err, print("-1 -1"))'
    out = subprocess.run([gp, "-q", "-D", "parisizemax=2000000000"], input=src, capture_output=True, text=True).stdout.split()
    try: return int(out[0]), int(out[1])
    except Exception: return -1, -1

def count_exact(curve, n, s3, gp):
    """exact representation count of n = E s1 s2 s3 / (a - b)^2 from the factorisations of the pieces"""
    a, b = curve.a, curve.b
    parts = " ; ".join(f"factor({abs(v)})" for v in [curve.E] + list(s3))
    # factoring the s_i (about n^(1/3)) is the cost; PARI's factor uses ECM / MPQS
    src = (f'\\r {Path(__file__).resolve().parent}/verify_gp/reps.gp\n'
           f'my(f = matreduce(matconcat([{parts}])), d = factor({abs(a - b)})); '
           f'f = matreduce(matconcat([f; matrix(#d~, 2, i, j, if(j == 1, d[i, 1], -2 * d[i, 2]))])); '
           f'f = matreduce(f); '
           f'if(factorback(f) != {n}, print("MISMATCH"), print(iferr(my(r = alarm(900, repsf({n}, f))); if(type(r) == "t_ERROR", "?", #r), e, "?")));')   # alarm returns, not raises
    out = subprocess.run([gp, "-q", "-D", "parisizemax=4000000000"], input=src, capture_output=True, text=True).stdout.split()
    return out[-1] if out else "?"

def main():
    ap = argparse.ArgumentParser(); ap.add_argument("--rounds", type=int, default=2); ap.add_argument("--out", required=True)
    ap.add_argument("--gp", default="gp"); ap.add_argument("--rank-time", type=int, default=120); ap.add_argument("--only-rank", action="store_true")
    ap.add_argument("--frontier", type=int, default=10); ap.add_argument("--nmax-exp", type=int, default=130); ap.add_argument("--cmax", type=int, default=0)
    ap.add_argument("--basis", type=int, default=6); ap.add_argument("--hbits", type=int, default=80)
    A = ap.parse_args(); t0 = time.time()
    curves = {}
    for l in open(Path(__file__).resolve().parents[2] / "results/a047697_catalogue.txt"):
        if not l[0].isdigit(): continue
        n, k, r = l.strip().split(";")
        if int(k) < 5: continue
        reps = [tuple(map(int, p.split(":"))) for p in r.split(",")]
        ls = lines_of(reps)
        if len(ls) < 2: continue
        (d1, T1), (d2, T2) = sorted(ls[:2], key=lambda t: abs(t[0][1]**3 - t[0][0]**3))
        inter = set(T1) & set(T2)                                   # the geometrically shared point (ordered)
        if not inter:                                               # the lines meet only up to swap: use the mirror line
            T2 = tuple((y, x) for x, y in T2); d2 = (d2[1], d2[0]); inter = set(T1) & set(T2)
        if not inter: continue
        if d1[0] > d1[1]:                                          # orient the base as line_enum: (a, b) with a < b
            T1 = tuple((y, x) for x, y in T1); T2 = tuple((y, x) for x, y in T2); d1 = (d1[1], d1[0]); d2 = (d2[1], d2[0])
            inter = set(T1) & set(T2)
        cs = next(iter(inter))
        key0 = (d1, d2, cs)
        curves.setdefault((d1[0], d1[1], d2[0], d2[1]), []).append((int(n), T1, T2, cs))
    print(f"{sum(len(v) for v in curves.values())} bowties on {len(curves)} (base, second direction) pairs", flush=True)
    out = open(A.out, "w"); tot5 = 0
    for (a, b, a2, b2), bts in sorted(curves.items(), key=lambda kv: -len(kv[1])):
        P0 = L.conic_points([(a, b)])[0]; d = Direction(a, b, P0, 10**60); setup_canon(d, P0)
        byi = {}
        for n, T1, T2, cs in bts:
            h, s, r = canon_slope(d, list(T1))
            R = d.raw(s, r); G = 0
            for x, y in R: G = gcd(G, gcd(x, y))
            red = [(x // G, y // G) for x, y in R]
            idx = [k for k, p in enumerate(red) if p == cs or (-p[0], -p[1]) == cs]          # exact point, up to overall sign
            if idx: byi.setdefault(idx[0], []).append((s, r, n))
        for i, seeds in byi.items():
            C = Curve(a, b, i, a2, b2)
            rk = rank_of(C, A.gp, A.rank_time)
            line = f"curve ({a},{b}) point {i} + ({a2},{b2}): {len(seeds)} known bowtie(s), rank {rk}"
            if A.only_rank: print(line, flush=True); out.write(line + "\n"); continue
            pts = set()
            for s, r, n in seeds:
                x = Fr(r, s); v = peval(C.q, x)
                if v < 0: continue
                wn, wd = isqrt(v.numerator), isqrt(v.denominator)
                if wn * wn == v.numerator and wd * wd == v.denominator: pts |= {(x, Fr(wn, wd)), (x, -Fr(wn, wd))}
            for _ in range(A.rounds):
                fr = sorted(pts, key=lambda p: max(abs(p[0].numerator), p[0].denominator))[:A.frontier]; new = set()
                for combo in itertools.combinations_with_replacement(fr, 3):
                    F4 = C.fourth(list(combo))
                    if F4: new.add(F4); new.add((F4[0], -F4[1]))
                pts |= new
            if A.cmax: pts |= lattice_points(C, sorted(pts, key=height)[:A.basis], A.cmax, A.hbits)
            five = {}
            reasons = {}
            for x, w in pts:
                res, why = C.bowtie(x.denominator, x.numerator); reasons[why] = reasons.get(why, 0) + 1
                if res: five[res[0]] = res
            line += f"; {len(pts)} points, " + ", ".join(f"{k} {v}" for k, v in sorted(reasons.items()))
            print(line, flush=True); out.write(line + "\n")
            for n in sorted(five):
                if n >= 10**A.nmax_exp: continue
                k = count_exact(C, n, five[n][2], A.gp)
                tot5 += 1
                out.write(f"FIVE {n};{k};" + ",".join(f"{x}:{y}" for x, y in five[n][1]) + "\n"); out.flush()
    print(f"done: {tot5} bowtie numbers written, {time.time() - t0:.0f} s", flush=True)

if __name__ == "__main__":
    main()
