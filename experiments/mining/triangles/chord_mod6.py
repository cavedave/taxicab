import sys, math, collections
sys.path.insert(0, '.')
from near_miss import analyse
if hasattr(sys, "set_int_max_str_digits"): sys.set_int_max_str_digits(0)
files, kmin, lim = sys.argv[1:-2], int(sys.argv[-2]), int(sys.argv[-1])
tot = 0; c2 = collections.Counter(); c3 = collections.Counter(); both = 0; neither = []; nums = 0
for fn in files:
    for l in open(fn):
        if not l[0].isdigit(): continue
        g = l.strip().split(';'); reps = [tuple(map(int, p.split(':'))) for p in g[2].split(',')]
        if len(reps) < kmin: continue
        nums += 1
        if nums > lim: break
        n = int(g[0]); nl, ch = analyse(n, reps)
        for d, X, Y, P, Q in ch:
            tot += 1; a, b = d % 2 == 0, d % 3 == 0
            c2[a] += 1; c3[b] += 1
            if not a and not b: neither.append((n, d, P, Q))
print(f'{nums} numbers, {tot} chords: d even {c2[True]}, d divisible by 3 {c3[True]}, neither {len(neither)}')
for x in sorted(neither, key=lambda t: t[1])[:5]: print('   neither:', len(str(x[0])), 'digits, d =', x[1])
