#!/usr/bin/env python3
"""line_patterns.py -- which patterns of lines can k coprime representations carry?
Every n with a line is odd (Theorem 12), so every coprime representation has a 2-type (Theorem 8). Choose for each
representation the orientation q_i of type +1; by Corollary 8b every line is q_a + q_b + q_c = 0. The group of the curve
is torsion-free here, so a pattern is IMPOSSIBLE iff the linear system forces q_i = 0, q_i = q_j or q_i = -q_j for some
i, j (distinct representations). Decide it with the kernel of the incidence system over Q."""
from fractions import Fraction as Fr
import itertools
def kernel(rows, k):
    M = [[Fr(x) for x in r] for r in rows]; piv = []; R = 0
    for c in range(k):
        p = next((i for i in range(R, len(M)) if M[i][c] != 0), None)
        if p is None: continue
        M[R], M[p] = M[p], M[R]; M[R] = [x / M[R][c] for x in M[R]]
        for i in range(len(M)):
            if i != R and M[i][c] != 0: M[i] = [a - M[i][c] * b for a, b in zip(M[i], M[R])]
        piv.append(c); R += 1
    free = [c for c in range(k) if c not in piv]; basis = []
    for f in free:
        v = [Fr(0)] * k; v[f] = Fr(1)
        for i, c in enumerate(piv): v[c] = -M[i][f]
        basis.append(v)
    return basis                       # columns of the kernel; row i of the kernel matrix = coordinates of q_i
def decide(name, k, lines):
    rows = [[1 if i in L else 0 for i in range(k)] for L in lines]
    K = kernel(rows, k); Q = [tuple(b[i] for b in K) for i in range(k)]      # q_i as vectors in the kernel coordinates
    bad = [f"q{i} = 0" for i in range(k) if all(x == 0 for x in Q[i])]
    for i, j in itertools.combinations(range(k), 2):
        if Q[i] == Q[j]: bad.append(f"q{i} = q{j}")
        if all(a == -b for a, b in zip(Q[i], Q[j])): bad.append(f"q{i} = -q{j}")
    print(f"{name:42s} {k:2d} points {len(lines):2d} lines  rank {len(K):2d}  " + ("IMPOSSIBLE: " + ", ".join(bad[:3]) if bad else "possible (no forced coincidence)"))
def valid(k, lines):
    deg = [sum(i in L for L in lines) for i in range(k)]
    lin = all(len(set(a) & set(b)) <= 1 for a, b in itertools.combinations(lines, 2))
    return lin, deg
def check(name, k, lines, want_deg=None):
    lin, deg = valid(k, lines)
    assert lin, f"{name}: two lines share two points"
    if want_deg: assert all(d == want_deg for d in deg), f"{name}: degrees {deg}"
    decide(name, k, lines)
P = lambda s: [tuple(int(c) for c in t) for t in s.split()]
check("line", 3, P("012"))
check("bowtie", 5, P("012 034"))
check("two disjoint lines", 6, P("012 345"))
check("triangle (corners 0,1,2)", 6, P("013 024 125"))
check("complete quadrilateral (Pasch)", 6, P("012 034 135 245"), 2)
check("three concurrent lines", 7, P("012 034 056"))
check("Fano plane 7_3", 7, P("012 034 056 135 146 236 245"), 3)
check("Moebius-Kantor 8_3", 8, [tuple(sorted(((i) % 8, (i + 1) % 8, (i + 3) % 8))) for i in range(8)], 3)
# Pappus 9_3: two rows of three points, the classical incidences
pap = [(0,1,2),(3,4,5),(6,7,8),(0,4,8),(0,5,7),(1,3,8),(1,5,6),(2,3,7),(2,4,6)]
check("Pappus 9_3", 9, pap, 3)
# Hesse / AG(2,3): points (x, y) in F_3^2, lines = affine lines
pts = [(x, y) for x in range(3) for y in range(3)]; idx = {p: i for i, p in enumerate(pts)}; hes = set()
for p0 in pts:
    for d in [(0, 1), (1, 0), (1, 1), (1, 2)]:
        hes.add(tuple(sorted(idx[((p0[0] + t * d[0]) % 3, (p0[1] + t * d[1]) % 3)] for t in range(3))))
check("Hesse AG(2,3) 9_4 (12 lines)", 9, sorted(hes), 4)
# Desargues 10_3: points = 2-subsets of {0..4}, lines = 3-subsets
two = list(itertools.combinations(range(5), 2)); tid = {t: i for i, t in enumerate(two)}
des = [tuple(sorted(tid[t] for t in itertools.combinations(T, 2))) for T in itertools.combinations(range(5), 3)]
check("Desargues 10_3", 10, des, 3)

# does each impossible pattern contain a complete quadrilateral (4 lines, pairwise meeting in 6 distinct points)?
def has_pasch(lines):
    for Q in itertools.combinations(lines, 4):
        meets = [set(a) & set(b) for a, b in itertools.combinations(Q, 2)]
        if all(len(m) == 1 for m in meets) and len(set().union(*meets)) == 6: return True
    return False
print()
for name, k, L in [("Fano plane", 7, P("012 034 056 135 146 236 245")),
                   ("Moebius-Kantor", 8, [tuple(sorted(((i) % 8, (i + 1) % 8, (i + 3) % 8))) for i in range(8)]),
                   ("Pappus", 9, pap), ("Hesse", 9, sorted(hes)), ("Desargues", 10, des)]:
    print(f"{name:16s} contains a complete quadrilateral: {has_pasch(L)}")
