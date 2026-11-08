import sys, math, collections
sys.path.insert(0, '.'); sys.path.insert(0, 'triangles')
import line_enum as L
from near_miss import analyse
if hasattr(sys, "set_int_max_str_digits"): sys.set_int_max_str_digits(0)
def direction(P, Q):
    a, b = Q[1] - P[1], P[0] - Q[0]; g = math.gcd(a, b); a, b = a // g, b // g
    if a < 0 or (a == 0 and b < 0): a, b = -a, -b
    return a, b
allowed = {(a, b) for c, a, b in L.dirs_by_cost(10**7, L.allowed_f)}
rows = []
for fn in sys.argv[1:]:
    for l in open(fn):
        if not l[0].isdigit(): continue
        g = l.strip().split(';'); reps = [tuple(map(int, p.split(':'))) for p in g[2].split(',')]
        if len(reps) < 5: continue
        for d, X, Y, P, Q in analyse(int(g[0]), reps)[1]:
            a, b = direction(P, Q); rows.append((d, abs(b**3 - a**3), (a, b) in allowed or (b, a) in allowed or (abs(a), abs(b)) in allowed))
def band(c): return 0 if c == 0 else int(math.log10(c))
for lab, sel in [('all chords', rows), ('chords with d <= 1000', [r for r in rows if r[0] <= 1000]), ('chords with d <= 100', [r for r in rows if r[0] <= 100])]:
    c = collections.Counter(min(band(r[1]), 40) for r in sel)
    print(f'{lab}: {len(sel)}; direction cost log10 quantiles:', [sorted(band(r[1]) for r in sel)[int(q * (len(sel) - 1))] for q in (0, .1, .5, .9)],
          '; in allowed list (cost <= 1e7):', sum(r[2] for r in sel))
