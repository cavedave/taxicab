import sys, math, collections
sys.path.insert(0, '.')
from near_miss import analyse
if hasattr(sys, "set_int_max_str_digits"): sys.set_int_max_str_digits(0)
def fac(m):
    f = {}; p = 2
    while p * p <= m and p < 10**6:
        while m % p == 0: f[p] = f.get(p, 0) + 1; m //= p
        p += 1
    if m > 1: f[m] = f.get(m, 0) + 1
    return f
ds = []
for fn in sys.argv[1:]:
    for l in open(fn):
        if not l[0].isdigit(): continue
        g = l.strip().split(';'); reps = [tuple(map(int, p.split(':'))) for p in g[2].split(',')]
        if len(reps) < 5: continue
        ds += [d for d, X, Y, P, Q in analyse(int(g[0]), reps)[1]]
small = [d for d in ds if d <= 10**6]
print('d values <= 100:', sorted(collections.Counter(d for d in small if d <= 100).items()))
cop = [d for d in small if math.gcd(d, 6) == 1]
pr = collections.Counter()
for d in cop:
    for p in fac(d): pr[p % 3] += 1
print('chords with d <= 1e6 coprime to 6:', len(cop), '; their primes by residue mod 3:', dict(pr))
six = [d for d in small if d % 6 == 0]
print('d <= 1e6 divisible by 6:', len(six), '; v2(d), v3(d) for the 10 smallest:', [(d, fac(d).get(2, 0), fac(d).get(3, 0)) for d in sorted(six)[:10]])
