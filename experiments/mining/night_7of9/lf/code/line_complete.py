#!/usr/bin/env python3
"""line_complete.py -- complete line enumeration: every coprime collinear triple on x^3 + y^3 = n with n <= B in each
given direction (six_way_ideas.md idea 1; no split-prime filter, no height cap).

Per direction (a, b) and the conic point P0 of line_enum.py, slope (s, r) gives raw points (b p_i, T - a p_i), quadratic
forms in (s, r), divided by G = gcd of the six values (line_enum.chord_points). By Theorem 13
    n = E S1 S2 S3 / ((a - b)^2 G^3),  |S1 S2 S3| >= M h^6,  h = max(|r|, s)
(S_i definite, M exact: line_heights.prod_min), so a slope can give n <= B only if h <= H(G) = (B (a-b)^2 G^3 / (E M))^(1/6).
G = content * G', G' | R0' (gcd of pairwise resultants of the primitive forms).
- Tier 1: every coprime slope with h <= H(Glo), Glo = content * (part of G' common to all slopes).
- Tier 2: Glo < G only if some prime p | R0' adds to G beyond Glo; such slopes lie in the projective residue classes
  mod p of the common roots of the forms (divided by the always-present p-part). For each such p and class, the
  progression of slopes is enumerated to H(Gmax) (Gmax: maximum attained, from lifts mod p^e for small p, else the
  R0' bound), keeping each slope with h <= H(its own G). Every slope with G > Glo is in some progression: complete.
Output (same as line_enum): n;a;b;c;x:y,x:y,x:y, one line per coprime triple with n <= B (deduplicated per direction).

Usage: python3 line_complete.py --B 1e19 --cmax 1e7 --out lines.txt [--procs 8] [--dirs-file f] [--only 3,4;12,13]
       python3 line_complete.py --selfcheck            (identical triples to brute force on 6 directions at small B)
"""
import argparse, math, sys, time
from math import gcd, isqrt
from multiprocessing import Pool
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
import line_enum as L
from line_heights import raw_forms, res, prod_min

def cont3(f): return gcd(gcd(f[0], f[1]), f[2])

def proj_points(q):
    """projective points (s : r) mod q as representatives (1, t) and (u, 1) with u = 0 mod p (q a prime power)"""
    p = min(d for d in range(2, q + 1) if q % d == 0)
    return [(1, t) for t in range(q)] + [(u, 1) for u in range(0, q, p)]

def sqrt_mod(a, p):
    """square roots of a mod an odd prime p (Tonelli-Shanks); [] if none"""
    a %= p
    if a == 0: return [0]
    if pow(a, (p - 1) // 2, p) != 1: return []
    q, s = p - 1, 0
    while q % 2 == 0: q //= 2; s += 1
    z = 2
    while pow(z, (p - 1) // 2, p) != p - 1: z += 1
    m, c, t, r = s, pow(z, q, p), pow(a, q, p), pow(a, (q + 1) // 2, p)
    while t != 1:
        i, tt = 0, t
        while tt != 1: tt = tt * tt % p; i += 1
        b = pow(c, 1 << (m - i - 1), p); m, c, t, r = i, b * b % p, t * b * b % p, r * b % p
    return sorted({r, p - r})

def form_roots_mod_p(f, p):
    """projective roots (s : r) mod p of A s^2 + B s r + C r^2, a form not identically 0 mod p"""
    A, B, C = (x % p for x in f)
    if p < 50:
        return [(s, r) for s, r in proj_points(p) if (A*s*s + B*s*r + C*r*r) % p == 0]
    out = []
    if C == 0:                                       # (0 : 1) is a root; finite roots solve A + B t = 0
        out.append((0, 1))
        if B: out.append((1, (-A * pow(B, -1, p)) % p))
    else:                                            # A + B t + C t^2 = 0, p odd
        inv = pow(2 * C, -1, p)
        for d in sqrt_mod((B*B - 4*A*C) % p, p): out.append((1, (-B + d) * inv % p))
    return sorted(set(out))

def class_lattice(combo):
    """reduced basis of {(s, r) : cr s - cs r = 0 mod q for each (q, cs, cr)} (q prime powers), Gauss-reduced"""
    b1, b2 = (1, 0), (0, 1)
    for q, cs, cr in combo:
        f1, f2 = (cr * b1[0] - cs * b1[1]) % q, (cr * b2[0] - cs * b2[1]) % q
        g = gcd(gcd(f1, f2), q)
        if g == q: continue                                         # condition already holds on the lattice
        q, f1, f2 = q // g, f1 // g, f2 // g                       # now f1 or f2 is a unit mod q (q a prime power)
        if gcd(f1, q) == 1:
            c = (-f2 * pow(f1, -1, q)) % q
            b1, b2 = (q * b1[0], q * b1[1]), (b2[0] + c * b1[0], b2[1] + c * b1[1])
        else:
            c = (-f1 * pow(f2, -1, q)) % q
            b1, b2 = (b1[0] + c * b2[0], b1[1] + c * b2[1]), (q * b2[0], q * b2[1])
    n2 = lambda w: w[0] * w[0] + w[1] * w[1]
    while True:                                                    # Gauss reduction
        if n2(b1) > n2(b2): b1, b2 = b2, b1
        m = round((b1[0] * b2[0] + b1[1] * b2[1]) / n2(b1))
        if m == 0: return b1, b2
        b2 = (b2[0] - m * b1[0], b2[1] - m * b1[1])

def box_points(u, v, S0, S1, R0, R1):
    """every lattice point i u + j v with S0 <= s <= S1, R0 <= r <= R1"""
    from math import floor, ceil
    det = u[0] * v[1] - u[1] * v[0]
    js = [(u[0] * r - u[1] * s) / det for s in (S0, S1) for r in (R0, R1)]
    for j in range(floor(min(js)) - 1, ceil(max(js)) + 2):
        lo, hi = -10**30, 10**30
        for (c, off, A, Bd) in ((u[0], j * v[0], S0, S1), (u[1], j * v[1], R0, R1)):
            if c == 0:
                if not (A <= off <= Bd): lo, hi = 1, 0
                continue
            x1, x2 = (A - off) / c, (Bd - off) / c
            lo, hi = max(lo, ceil(min(x1, x2) - 1e-9)), min(hi, floor(max(x1, x2) + 1e-9))
        for i in range(lo, hi + 1):
            s, r = i * u[0] + j * v[0], i * u[1] + j * v[1]
            if S0 <= s <= S1 and R0 <= r <= R1: yield s, r

class Direction:
    def __init__(self, a, b, P0, B):
        self.a, self.b, self.B = a, b, B
        self.raw, coord, S = raw_forms(a, b, P0)
        self.E = a*a + a*b + b*b
        self.M = prod_min(S)
        self.content = 0
        for f in coord: self.content = gcd(self.content, cont3(f))
        prim = [tuple(x // self.content for x in f) for f in coord]
        R0 = 0
        for i in range(6):
            for j in range(i + 1, 6): R0 = gcd(R0, res(prim[i], prim[j]))
        self.prim = prim
        self.always = 1; self.extra = []                         # [(p, lo, hi, levels)], levels[j] = classes mod p^j
        for p, e in L.factor(R0).items():
            lo, hi, levels = self._prime(p, e)
            self.always *= p**lo
            if hi > lo: self.extra.append((p, lo, hi, levels))
        self.Glo = self.content * self.always
        self.Gmax = self.Glo * math.prod(p**(hi - lo) for p, lo, hi, _ in self.extra)

    def G(self, s, r):
        g = 0
        for x, y in self.raw(s, r): g = gcd(g, gcd(x, y))
        return g

    def vp_at(self, s, r, p, cap):
        """v_p(G'(s, r)), capped at cap (G' = gcd of the primitive coordinate forms)"""
        q = p**cap; g = q
        for A, B_, C in self.prim:
            g = gcd(g, (A*s*s + B_*s*r + C*r*r) % q)
            if g == 1: return 0
        v = 0
        while g % p == 0: g //= p; v += 1
        return v

    def _prime(self, p, e):
        """(lo, hi, levels): v_p(G') >= lo for every slope; levels[j] (lo < j <= hi) = projective classes mod p^j whose
        slopes have v_p(G') >= j, found by lifting level by level (p children per class per level)"""
        children = lambda c, q: [(1, c[1] + k * q) for k in range(p)] if c[0] % p else [(c[0] + k * q, 1) for k in range(p)]
        # level 1 candidates: all projective points mod p (small p) or the common roots of the forms (large p)
        if p < 1000: C = [c for c in proj_points(p) if self.vp_at(c[0], c[1], p, 1) >= 1]
        else:
            roots = None
            for f in self.prim:
                if all(x % p == 0 for x in f): continue
                rs = set(form_roots_mod_p(f, p)); roots = rs if roots is None else roots & rs
            C = sorted(roots or [])
        levels = {}; lo = 0; j = 1; npts = p + 1
        while C and j <= e:
            if len(C) == npts and lo == j - 1: lo = j                  # every class mod p^j has v >= j: always present
            else: levels[j] = C
            if j == e: break
            C = [d for c in C for d in children(c, p**j) if self.vp_at(d[0], d[1], p, j + 1) >= j + 1]
            j += 1; npts *= p
        levels = {k: v for k, v in levels.items() if k > lo}
        hi = max(levels) if levels else lo
        return lo, hi, levels

    def H(self, g):
        return (self.B * (self.a - self.b)**2 * g**3 / (self.E * self.M)) ** (1 / 6)

    def slopes(self, s_lo=0, s_hi=None):
        """yield every coprime slope (s, r) that can give n <= B (repeats possible; triples are deduplicated later).
        Tier 1: all slopes to H(Glo). Tier 2: for each nonempty set T of extra primes, the slopes whose (s : r) is in an
        extra class mod every p in T (CRT progression mod prod T), to H(Glo * prod_{p in T} p^(hi - lo)). A slope whose
        set of primes adding to G is exactly T lies in T's progression and needs h <= H(G) <= that height: complete."""
        from itertools import combinations, product
        H1 = int(self.H(self.Glo)) + 1
        top = lambda H: H if s_hi is None else min(H, s_hi)
        for s in range(s_lo, top(H1) + 1):
            for r in range(-H1, H1 + 1):
                if (s == 0 and r != 1) or gcd(r, s) != 1: continue
                yield s, r
        ex = self.extra
        for k in range(1, len(ex) + 1):
            for T in combinations(ex, k):
                for lv in product(*[sorted(levels) for p, lo, hi, levels in T]):
                    want = tuple(sorted((p, jj) for (p, *_), jj in zip(T, lv)))
                    Hx = int(self.H(self.Glo * math.prod(p**(jj - lo) for (p, lo, hi, _), jj in zip(T, lv)))) + 1
                    S0, S1 = s_lo, top(Hx)
                    if S0 > S1: continue
                    for combo in product(*[[(p**jj, cs, cr) for cs, cr in levels[jj]] for (p, lo, hi, levels), jj in zip(T, lv)]):
                        u, v = class_lattice(combo)
                        for s, r in box_points(u, v, S0, S1, -Hx, Hx):
                            if (s == 0 and r != 1) or gcd(r, s) != 1: continue
                            if max(abs(r), s) > H1 and self.member(s, r) == want: yield s, r

    def member(self, s, r):
        """exact (p, v_p(G')) for the extra primes with v_p(G') above their floor: each slope is yielded once, for exactly
        this assignment, whose height H(Glo * prod p^(v - lo)) is the slope's own bound"""
        out = []
        for p, lo, hi, levels in self.extra:
            v = self.vp_at(s, r, p, hi)
            if v > lo: out.append((p, v))
        return tuple(sorted(out))

    def hmax(self):
        """largest height any slope can need (for splitting into s-chunks)"""
        return int(self.H(self.Gmax)) + 1

def setup_canon(d, P0):
    from fractions import Fraction as Fr
    d.X0, d.Y0 = Fr(P0[0]), Fr(P0[1]); d.Dc = d.b**3 - d.a**3

def canon_slope(d, pts):
    """the reduced slope of every ordering (i, j) of the triple (Theorem 4 (ii): X = D u_i + a^2, Y = D u_j + a^2,
    u = x / c), as (h, s, r); orderings whose point is P0 itself have no slope and are skipped"""
    from fractions import Fraction as Fr
    c = d.a * pts[0][0] + d.b * pts[0][1]
    u = [Fr(x, c) for x, y in pts]; out = []
    for i in range(3):
        for j in range(3):
            if i == j: continue
            dx = d.Dc * u[i] + d.a * d.a - d.X0; dy = d.Dc * u[j] + d.a * d.a - d.Y0
            if dx == 0 and dy == 0: continue
            den = dx.denominator * dy.denominator // gcd(dx.denominator, dy.denominator)
            S_, R_ = int(dx * den), int(dy * den); g = gcd(S_, R_); S_, R_ = S_ // g, R_ // g
            if S_ < 0 or (S_ == 0 and R_ < 0): S_, R_ = -S_, -R_
            out.append((max(abs(R_), S_), S_, R_))
    return min(out)

def count_batch(ns, gp, chunk=20000):
    """exact coprime representation lists for many n (PARI factorisation, collisions.all_reps)"""
    import subprocess, re
    from collisions import all_reps
    res = []
    for i in range(0, len(ns), chunk):
        part = ns[i:i + chunk]
        txt = subprocess.run([gp, "-q", "-D", "parisizemax=2000000000"], input="default(factor_add_primes,0);\n" +
                             "\n".join(f"print(factor({n}));" for n in part), capture_output=True, text=True, check=True).stdout
        facs = []
        for f in txt.strip().splitlines():
            body = re.search(r"\[([^\[\]]*)\]", f.replace("Mat(", "")).group(1)
            facs.append([tuple(int(v) for v in r.split(",")) for r in body.replace(" ", "").split(";")])
        res += [(n, all_reps(n, f)) for n, f in zip(part, facs)]
    return res

def run_dir(job):
    """job = (a, b, P0, B, s_lo, s_hi, gp): canonical triples (each unordered triple once, at its least-height ordering)
    of the s-chunk; with gp, every n is counted exactly and only k >= 4 are returned"""
    a, b, P0, B, s_lo, s_hi, gp = job
    d = Direction(a, b, P0, B); setup_canon(d, P0); out = []; tried = 0; ns = []
    for s, r in d.slopes(s_lo, s_hi):
        tried += 1
        pts = d.raw(s, r); G = 0
        for x, y in pts: G = gcd(G, gcd(x, y))
        if max(abs(r), s) > d.H(G): continue
        pts = [(x // G, y // G) for x, y in pts]
        n = pts[0][0]**3 + pts[0][1]**3
        if n == 0 or abs(n) > B: continue
        if any(x == 0 or y == 0 or gcd(x, y) != 1 for x, y in pts): continue
        if len({tuple(sorted(p)) for p in pts}) < 3: continue
        if canon_slope(d, pts)[1:] != (s, r): continue          # not the least-height ordering: counted there
        if n < 0: pts = [(-x, -y) for x, y in pts]; n = -n
        out.append((n, a * pts[0][0] + b * pts[0][1], pts)); ns.append(n)
    if gp is None: return (a, b, s_lo, s_hi, tried, len(out), 0), out
    counted = count_batch(ns, gp); kmax = max((len(r) for n, r in counted), default=0)
    return (a, b, s_lo, s_hi, tried, len(out), kmax), [(n, reps) for n, reps in counted if len(reps) >= 4]

def brute(a, b, P0, B, hmax):
    pts_of = L.chord_points(a, b, P0); found = set()
    for s in range(0, hmax + 1):
        for r in range(-hmax, hmax + 1):
            if (s == 0 and r != 1) or gcd(r, s) != 1: continue
            pts, c = pts_of(s, r); n = pts[0][0]**3 + pts[0][1]**3
            if n < 0: pts = [(-x, -y) for x, y in pts]; n = -n
            if n == 0 or n > B or any(x == 0 or y == 0 or gcd(x, y) != 1 for x, y in pts): continue
            if len({tuple(sorted(p)) for p in pts}) < 3: continue
            found.add((n, frozenset(tuple(sorted(p)) for p in pts)))
    return found

def selfcheck(gp="gp"):
    dirs = [(3, 4), (12, 13), (3, 16), (16, 21), (27, 28), (4, 7)]; B = 10**14
    ok = True
    for (a, b), P0 in zip(dirs, L.conic_points(dirs, gp)):
        d = Direction(a, b, P0, B)
        (_, _, _, _, tried, ntrip, _), out = run_dir((a, b, P0, B, 0, None, None)); Glo, Gmax = d.Glo, d.Gmax
        mine = {(n, frozenset(tuple(sorted(p)) for p in pts)) for n, c, pts in out}
        assert len(mine) == len(out), 'duplicate triple'
        ref = brute(a, b, P0, B, int(2 * d.H(d.Gmax)) + 2)
        print(f"  ({a},{b}) Glo {Glo} Gmax {Gmax} H {d.H(Glo):.0f}-{d.H(Gmax):.0f}: complete {len(mine)} triples, brute (2x Hmax) {len(ref)}, "
              f"identical {mine == ref}, no duplicates; slopes tried {tried:,}")
        ok &= mine == ref
    print("SELFCHECK", "PASS" if ok else "FAIL"); return ok

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--B", default="1e19"); ap.add_argument("--cmax", type=float, default=1e6)
    ap.add_argument("--cmin", type=float, default=0); ap.add_argument("--only", default="")
    ap.add_argument("--out", default="lines_complete.txt"); ap.add_argument("--log", default="")
    ap.add_argument("--procs", type=int, default=8); ap.add_argument("--gp", default="gp")
    ap.add_argument("--count", action="store_true", help="count every n exactly (PARI); write only k >= 4 as n;k;x:y,...")
    ap.add_argument("--chunk", type=float, default=2e7, help="slopes per job for cheap directions (split by s)")
    ap.add_argument("--selfcheck", action="store_true")
    ap.add_argument("--resume", action="store_true", help="skip jobs already in --log; append to --out and --log")
    A = ap.parse_args()
    if A.selfcheck: sys.exit(0 if selfcheck(A.gp) else 1)
    from decimal import Decimal
    B = int(Decimal(A.B))                                              # exact: "1e33" is 10^33
    if A.only: dirs = [tuple(map(int, d.split(","))) for d in A.only.split(";")]
    else: dirs = [(a, b) for c, a, b in L.dirs_by_cost(int(A.cmax), L.allowed_f) if c > A.cmin]
    t0 = time.time(); P = L.conic_points(dirs, A.gp)
    jobs = []
    for (a, b), P0 in zip(dirs, P):
        k = 1
        if b**3 - a**3 <= 10**6:                                    # cheap: split the s-range into ~equal-slope chunks
            d = Direction(a, b, P0, B); est = 2.5 * d.H(d.Glo)**2 + sum(2.5 * d.H(d.Glo * p**(jj - lo))**2 * len(lv[jj]) / p**jj for p, lo, hi, lv in d.extra for jj in lv)
            k = max(1, int(est / A.chunk)); hm = d.hmax()
        if k == 1: jobs.append((a, b, P0, B, 0, None, A.gp if A.count else None))
        else:
            cuts = [round(hm * i / k) for i in range(k + 1)]
            jobs += [(a, b, P0, B, cuts[i] + (i > 0), cuts[i + 1], A.gp if A.count else None) for i in range(k)]
    jobs.sort(key=lambda j: j[1]**3 - j[0]**3)                       # cheapest (largest) first
    if A.resume and A.log and Path(A.log).exists():
        done = {tuple(l.split(";")[:4]) for l in open(A.log) if l.strip()}
        key = lambda j: (str(j[0]), str(j[1]), str(j[4]), str(j[5]))
        jobs = [j for j in jobs if key(j) not in done]
        print(f"resume: {len(done):,} jobs already done", flush=True)
    print(f"{len(dirs):,} directions, {len(jobs):,} jobs, setup {time.time() - t0:.0f} s", flush=True)
    tot = slopes = hits = 0; kmax = 0
    mode = "a" if A.resume else "w"
    log = open(A.log, mode) if A.log else None
    with open(A.out, mode) as f, Pool(A.procs) as pool:
        if not A.resume: f.write(f"# line_complete.py: every coprime collinear triple with n <= {B} in {len(dirs)} directions "
                f"(cost {A.cmin:.3g} < c <= {A.cmax:.3g}{', only ' + A.only if A.only else ''})"
                f"{'; every n counted exactly, k >= 4 listed as n;k;x:y,...' if A.count else ''}\n")
        for (a, b, lo, hi, tried, ntrip, km), out in pool.imap_unordered(run_dir, jobs, chunksize=1):
            slopes += tried; tot += ntrip; kmax = max(kmax, km)
            if log: log.write(f"{a};{b};{lo};{hi};{tried};{ntrip};{km}\n"); log.flush()
            if A.count:
                for n, reps in out:
                    hits += 1; f.write(f"{n};{len(reps)};" + ",".join(f"{x}:{y}" for x, y in sorted(reps, reverse=True)) + "\n")
            else:
                for n, c, pts in out: f.write(f"{n};{a};{b};{c};" + ",".join(f"{x}:{y}" for x, y in pts) + "\n")
            f.flush()
    print(f"done: {tot:,} triples, {slopes:,} slopes" + (f", {hits:,} with k >= 4, largest k {kmax}" if A.count else "") +
          f", {time.time() - t0:.0f} s", flush=True)

if __name__ == "__main__":
    main()
