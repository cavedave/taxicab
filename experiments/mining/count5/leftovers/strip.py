"""Hard cofactors of the 'factor:' leftovers, via a coprime basis (gcds) of n and the pieces (s = x + y, E of each line),
then primes < 1e7 removed and each remaining base element tested: prime (isprime, proved), or composite (needs ECM/NFS).
Output JSON: n, kind, F = proved prime factorisation part, composite = elements still to factor (with exponent)."""
import sys, subprocess, json
from math import gcd
sys.path.insert(0, "/Users/davidcurran/Documents/taxicab/experiments/mining")
if hasattr(sys, "set_int_max_str_digits"): sys.set_int_max_str_digits(0)
from bowtie_mine import lines_of
R = "/Users/davidcurran/Documents/taxicab/"
reps = {}
for fn in ("results/five_ways_all.txt", "results/four_ways_generated.txt"):
    for l in open(R + fn):
        f = l.split(";")
        if f[0].isdigit(): reps[int(f[0])] = [tuple(map(int, p.split(":"))) for p in f[2].split(",")]
def refine(B):                      # coprime basis of a list of integers > 1
    B = [b for b in B if b > 1]
    changed = True
    while changed:
        changed = False
        for i in range(len(B)):
            for j in range(i + 1, len(B)):
                g = gcd(B[i], B[j])
                if g > 1 and not (B[i] == B[j] == g):
                    a, b = B[i], B[j]; B = [x for k, x in enumerate(B) if k not in (i, j)] + [g, a // g, b // g]
                    B = [x for x in B if x > 1]; B = list(dict.fromkeys(B)); changed = True; break
                if g > 1: B.pop(j); changed = True; break
            if changed: break
    return B
def gp(src): return subprocess.run(["gp", "-q", "-D", "parisizemax=2000000000"], input=src, capture_output=True, text=True).stdout.strip()
out = []
for l in open(R + "experiments/mining/count5/v2/counted_pass2.txt.unk"):
    f = l.rstrip("\n").split(";")
    if not f[0].isdigit() or not f[1].startswith("factor:"): continue
    n = int(f[0]); five = reps[n]
    pieces = {abs(x + y) for x, y in five} | {a*a + a*b + b*b for (a, b), T in lines_of(five)}
    B = refine([gcd(q, n) for q in pieces])
    m = n
    for b in B:
        while m % b == 0: m //= b
    if m > 1: B = refine(B + [m])
    F = {}; comp = []
    for b in B:
        e = 0; t = n
        while t % b == 0: t //= b; e += 1
        if e == 0: continue
        txt = gp(f"v=factor({b},10^7); print([Vec(v[,1]),Vec(v[,2]),apply(x->isprime(x),Vec(v[,1]))])")
        ps, es, pp = eval(txt.replace(";", ","))
        for p, ee, isp in zip(ps, es, pp):
            if isp: F[p] = F.get(p, 0) + ee * e
            else: comp.append((p, ee * e))
    # sanity: product of everything equals n
    prod = 1
    for p, e in F.items(): prod *= p ** e
    for c, e in comp: prod *= c ** e
    assert prod == n, "product mismatch"
    out.append({"n": str(n), "kind": f[2][0], "F": {str(p): e for p, e in F.items()}, "composite": [[str(c), e] for c, e in comp]})
    print(len(str(n)), f[2][0], "hard:", [len(str(c)) for c, e in comp], flush=True)
json.dump(out, open(sys.argv[1], "w"))
