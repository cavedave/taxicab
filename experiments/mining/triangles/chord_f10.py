import sys, math, collections
sys.path.insert(0, '.'); sys.path.insert(0, 'triangles')
from near_miss import analyse
if hasattr(sys, "set_int_max_str_digits"): sys.set_int_max_str_digits(0)
def v(p, m):
    k = 0
    while m and m % p == 0: m //= p; k += 1
    return k
C = collections.Counter()
for fn in sys.argv[2:]:
    kmin = int(sys.argv[1])
    for l in open(fn):
        if not l[0].isdigit(): continue
        g = l.strip().split(';'); reps = [tuple(map(int, p.split(':'))) for p in g[2].split(',')]
        if len(reps) < kmin: continue
        for d, X, Y, P, Q in analyse(int(g[0]), reps)[1]:
            a, b = Q[1] - P[1], P[0] - Q[0]; gg = math.gcd(a, b); a, b = a // gg, b // gg
            C[('4|ab' if v(2, a * b) >= 2 else 'not 4|ab', '2|d' if d % 2 == 0 else 'd odd', '3|d' if d % 3 == 0 else '3 not | d')] += 1
for k in sorted(C): print(k, C[k])
