#!/usr/bin/env python3
"""filter_measure.py -- how much do the triangle constraints (Theorem 1, Theorem 8 types, Lemmas 17-18) cut?"""
import sys, math, collections, re
from itertools import combinations
sys.path.insert(0, '.'); sys.path.insert(0, 'triangles')
if hasattr(sys, "set_int_max_str_digits"): sys.set_int_max_str_digits(0)
import line_enum as L
from bowtie_mine import lines_of
from near_miss import third

def fac(m):
    m = abs(m); f = {}; p = 2
    while p * p <= m:
        while m % p == 0: f[p] = f.get(p, 0) + 1; m //= p
        p += 1 if p == 2 else 2
    if m > 1: f[m] = f.get(m, 0) + 1
    return f
def nonsplit(m): return math.prod(p**e for p, e in fac(m).items() if p % 3 != 1)
def allowed(a, b):
    if a * b <= 0 or a == b: return False
    return L.allowed_f(fac(a * b))
def tau(P, p):
    x, y = P
    return 1 if x % p == 0 else (-1 if y % p == 0 else 0)

# (A) direction triples of the 150-direction scan
ds = [(a, b) for c, a, b in L.dirs_by_cost(10**7, L.allowed_f) if c > 0][:150]
Dl = ds + [(b, a) for a, b in ds]
grp = collections.Counter(nonsplit(b - a) for a, b in Dl)
tot = math.comb(len(Dl), 3); keep = sum(math.comb(c, 3) for c in grp.values())
print(f"(A) 300 directions: {len(grp)} non-split groups (largest {grp.most_common(3)}); triples {tot:,} -> {keep:,} "
      f"within a group ({keep / tot:.1%})")
hits = [eval(re.match(r'TRI (\[\[.*?\]\]) core', l).group(1)) for l in open('triangles/out150.txt') if l.startswith('TRI')]
ok = sum(len({nonsplit(b - a) for a, b in D}) == 1 for D in hits)
print(f"    the 88 rational triangles of the scan: {ok} have all three sides in one non-split group")

# (B) third sides of bowties: cheap filters first, PARI factoring only for the survivors
import subprocess
def gp_fac(nums):
    src = "\n".join(f"print(factor({abs(v)}));" for v in nums)
    out = subprocess.run(["gp", "-q"], input=src, capture_output=True, text=True, timeout=3600).stdout.strip().splitlines()
    res = []
    for line in out:
        body = re.search(r"\[([^\[\]]*)\]", line.replace("Mat(", ""))
        res.append({} if body is None or not body.group(1).strip() else
                   {int(q.split(",")[0]): int(q.split(",")[1]) for q in body.group(1).replace(" ", "").split(";")})
    return res
C = collections.Counter(); nb = 0; late = []
for l in open('../../results/five_ways_all.txt'):
    if not l[0].isdigit(): continue
    g = l.split(';'); n = int(g[0]); reps = [tuple(map(int, p.split(':'))) for p in g[2].split(',')]
    ls = lines_of(reps)
    if len(ls) < 2: continue
    (d1, T1), (d2, T2) = ls[0], ls[1]
    S = {tuple(sorted(p)) for p in T1} & {tuple(sorted(p)) for p in T2}
    if len(S) != 1: continue
    nb += 1
    ns = nonsplit(d1[1] - d1[0]); types = n % 2 == 1 and n % 9 in (1, 8)
    side1 = [p for p in T1 if tuple(sorted(p)) not in S]; side2 = [p for p in T2 if tuple(sorted(p)) not in S]
    for P in side1:
        for Q0 in side2:
            for Q in (Q0, (Q0[1], Q0[0])):
                C['0 candidate chords'] += 1
                if types and (tau(P, 2) != tau(Q, 2) or tau(P, 3) != tau(Q, 3)): continue
                C['1 orientation (types at 2 and 3)'] += 1
                a, b = Q[1] - P[1], P[0] - Q[0]; gg = math.gcd(a, b); a, b = a // gg, b // gg
                if a < 0 or (a == 0 and b < 0): a, b = -a, -b
                if a * b <= 0 or (a * b) % 4: continue
                C['2 ab > 0 and 4 | ab (Theorem 1)'] += 1
                if n % (a * a + a * b + b * b): continue
                C['3 E_3 | n (Lemma 18)'] += 1
                late.append((n, P, Q, a, b, ns))
fa = gp_fac([a * b for n, P, Q, a, b, ns in late]); fd = gp_fac([b - a for n, P, Q, a, b, ns in late])
for (n, P, Q, a, b, ns), f1, f2 in zip(late, fa, fd):
    if not L.allowed_f(f1): continue
    C['4 ab a norm (Theorem 1)'] += 1
    if math.prod(p**e for p, e in f2.items() if p % 3 != 1) != ns: continue
    C['5 same non-split part (Lemma 18)'] += 1
    R = third(P, Q, n); dR = math.lcm(R[0].denominator, R[1].denominator)
    C['6 survivors with integral third point'] += dR == 1
    C['7 survivors with denominator <= 1000'] += dR <= 1000
print(f"(B) {nb} bowties:")
for k in sorted(C): print(f"    {k:42s} {C[k]:7d}")

# (C) Lemma 17 on four-ways: line + one free representation
def mu(P): t2, t3 = tau(P, 2), tau(P, 3); return t2 * t3 if t2 and t3 else 0
F = collections.Counter()
for l in open('../../results/a047697_catalogue.txt'):
    if not l[0].isdigit(): continue
    g = l.split(';'); n = int(g[0])
    if g[1] != '4' or n % 2 == 0 or n % 9 not in (1, 8): continue
    reps = [tuple(map(int, p.split(':'))) for p in g[2].split(',')]
    ls = lines_of(reps)
    if len(ls) != 1: continue
    on = {tuple(sorted(p)) for p in ls[0][1]}
    free = [r for r in reps if tuple(sorted(r)) not in on]
    if len(free) != 1: continue
    m_line = mu(ls[0][1][0]); m_free = mu(free[0])
    F['same class' if m_line == m_free else 'other class'] += 1
print(f"(C) four-ways 'one line + one free point' (n odd, n = +-1 mod 9): {dict(F)}")
