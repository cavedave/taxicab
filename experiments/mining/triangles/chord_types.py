import sys, math, collections
sys.path.insert(0, '.')
from near_miss import analyse
if hasattr(sys, "set_int_max_str_digits"): sys.set_int_max_str_digits(0)
files, kmin = sys.argv[1:-1], int(sys.argv[-1])
C = collections.Counter(); best = collections.defaultdict(lambda: 10**999)
for fn in files:
    for l in open(fn):
        if not l[0].isdigit(): continue
        g = l.strip().split(';'); reps = [tuple(map(int, p.split(':'))) for p in g[2].split(',')]
        if len(reps) < kmin: continue
        n = int(g[0]); canon = {(max(x, y), min(x, y)) for x, y in reps}
        nl, ch = analyse(n, reps)
        for d, X, Y, P, Q in ch:
            typ = 'same' if ((P in canon) == (Q in canon)) else 'crossed'
            C[(typ, d % 6 == 0, math.gcd(d, 6))] += 1; best[typ] = min(best[typ], d)
for k in sorted(C): print(k, C[k])
print('smallest d by type:', dict(best))
