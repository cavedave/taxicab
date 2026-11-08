import sys, math
sys.path.insert(0, '.')
from near_miss import analyse
if hasattr(sys, "set_int_max_str_digits"): sys.set_int_max_str_digits(0)
files, kmin = sys.argv[1:-1], int(sys.argv[-1])
ds = []
for fn in files:
    for l in open(fn):
        if not l[0].isdigit(): continue
        g = l.strip().split(';'); reps = [tuple(map(int, p.split(':'))) for p in g[2].split(',')]
        if len(reps) < kmin: continue
        ds += [d for d, X, Y, P, Q in analyse(int(g[0]), reps)[1]]
N = len(ds); print(N, 'chords')
pts = []
for D in [2, 5, 10, 30, 100, 300, 1000, 10**4]:
    c = sum(d <= D for d in ds); pts.append((math.log10(D), math.log10(c) if c else None)); print(f'  d <= {D}: {c}')
xs = [x for x, y in pts if y is not None and x <= 3]; ys = [y for x, y in pts if y is not None and x <= 3]
m = len(xs); sx, sy = sum(xs), sum(ys); sxx = sum(x*x for x in xs); sxy = sum(x*y for x, y in zip(xs, ys))
a = (m*sxy - sx*sy) / (m*sxx - sx*sx); b = (sy - a*sx) / m
print(f'  fit: count(d <= D) ~ {10**b:.1f} * D^{a:.2f}  -> expected chords with d = 1: about {10**b:.2f}')
