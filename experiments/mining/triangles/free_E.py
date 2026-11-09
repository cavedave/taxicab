import sys, math, collections, statistics
sys.path.insert(0, '.')
if hasattr(sys, "set_int_max_str_digits"): sys.set_int_max_str_digits(0)
from bowtie_mine import lines_of
def fac(m):
    m = abs(m); f = {}; p = 2
    while p * p <= m:
        while m % p == 0: f[p] = f.get(p, 0) + 1; m //= p
        p += 1 if p == 2 else 2
    if m > 1: f[m] = f.get(m, 0) + 1
    return f
def v(p, m):
    k = 0
    while m and m % p == 0: m //= p; k += 1
    return k
C = collections.Counter(); share = {'free': [], 'line': []}
for l in open('../../results/a047697_catalogue.txt'):
    if not l[0].isdigit(): continue
    g = l.split(';'); n = int(g[0]); reps = [tuple(map(int, p.split(':'))) for p in g[2].split(',')]
    if len(reps) != 4: continue
    ls = lines_of(reps)
    if len(ls) != 1: continue
    (a, b), T = ls[0]; E = a*a + a*b + b*b; Ef = {p: e for p, e in fac(E).items() if p != 3}
    if not Ef: continue
    on = {tuple(sorted(p)) for p in T}; F = [r for r in reps if tuple(sorted(r)) not in on][0]
    for tag, pts in (('line', list(T)), ('free', [F])):
        for x, y in pts:
            s = x + y
            # for each split prime p of E: does s take the FULL power of p that n has, none of it, or part?
            for p, e in Ef.items():
                vn, vs = v(p, n), v(p, s)
                C[(tag, 'none' if vs == 0 else ('all of n' if vs == vn else 'part'))] += 1
            # share of the E-primes' power of n inside s
            num = sum(min(v(p, s), v(p, n)) * math.log(p) for p in Ef); den = sum(v(p, n) * math.log(p) for p in Ef)
            share[tag].append(num / den if den else 0)
for tag in ('line', 'free'):
    tot = sum(C[(tag, k)] for k in ('none', 'part', 'all of n'))
    print(f"{tag}: E-prime power of n inside s -- none {C[(tag, 'none')] / tot:.1%}, part {C[(tag, 'part')] / tot:.1%}, all of n {C[(tag, 'all of n')] / tot:.1%} | mean share {statistics.mean(share[tag]):.3f}")
