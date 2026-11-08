import sys, math, collections
sys.path.insert(0, '.'); sys.path.insert(0, 'triangles')
from near_miss import analyse
if hasattr(sys, "set_int_max_str_digits"): sys.set_int_max_str_digits(0)
P2 = [p for p in range(5, 2000) if p % 3 == 2 and all(p % q for q in range(2, int(p**.5) + 1))]
P1 = [p for p in range(7, 2000) if p % 3 == 1 and all(p % q for q in range(2, int(p**.5) + 1))]
def v(p, m):
    k = 0
    while m and m % p == 0: m //= p; k += 1
    return k
C = collections.Counter()
kmin = int(sys.argv[1])
for fn in sys.argv[2:]:
    for l in open(fn):
        if not l[0].isdigit(): continue
        g = l.strip().split(';'); reps = [tuple(map(int, p.split(':'))) for p in g[2].split(',')]
        if len(reps) < kmin: continue
        for d, X, Y, P, Q in analyse(int(g[0]), reps)[1]:
            a, b = Q[1] - P[1], P[0] - Q[0]; gg = math.gcd(a, b); a, b = a // gg, b // gg; ab = a * b
            for p in P2:
                e = v(p, ab)
                if e: C[('p=2 mod 3', 'odd' if e % 2 else 'even', 'p|d' if d % p == 0 else 'p not | d')] += 1
            for p in P1[:40]:
                e = v(p, ab)
                if e: C[('p=1 mod 3', 'odd' if e % 2 else 'even', 'p|d' if d % p == 0 else 'p not | d')] += 1
for k in sorted(C): print(k, C[k])
