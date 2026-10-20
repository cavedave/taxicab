#!/usr/bin/env python3
"""catalog.py -- turn curve_hunt output into a catalogue of k-way numbers (k >= 6).

For every distinct n in the hunt file(s) (rows k;n;M;L;a:b,...):
  ways_found  pairs we hold (each re-checked: a^3 + b^3 == n)
  ways_exact  the complete number of representations, by window-divisor search over the
              factorisation n = M * L^3 -- only when n has at most --maxdiv divisors, else blank
  primitive   yes if the pairs we hold have gcd 1 (then n is not g^3 times a smaller solution)
  known       where n already appears: Boyer's 6-7-way list (< 5e28), Boyer-Wroblewski bounds
              Ta(7..22), our results/sixways.csv; blank = not in those lists
Writes <out> sorted by ways (desc) then n, and prints the smallest entries per way-count.

Usage:  python3 catalog.py hunt18.csv [more.csv ...] --out catalog.csv
        Known numbers come from known_numbers.csv next to this script (one file, n;source); if it
        is missing they are read from refs/boyer_lists + results/sixways.csv instead.
        Way counts are lower bounds (points we hold) unless ways_exact is filled in.
"""
import argparse, math, os, random, re, sys
from collections import defaultdict

# ---------- factoring (n's factors come from M <= ~4e18 and L, a product of denominators) ----------
def is_prime(n):
    if n < 2: return False
    for p in (2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37):
        if n % p == 0: return n == p
    d, r = n - 1, 0
    while d % 2 == 0: d //= 2; r += 1
    for a in (2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53):
        x = pow(a, d, n)
        if x in (1, n - 1): continue
        for _ in range(r - 1):
            x = x * x % n
            if x == n - 1: break
        else: return False
    return True                        # deterministic below 3.3e24; overwhelmingly reliable above

def rho(n):
    if n % 2 == 0: return 2
    while True:
        y, c, m, g, r, q = random.randrange(1, n), random.randrange(1, n), 128, 1, 1, 1
        while g == 1:
            x = y
            for _ in range(r): y = (y * y + c) % n
            k = 0
            while k < r and g == 1:
                ys = y
                for _ in range(min(m, r - k)):
                    y = (y * y + c) % n; q = q * abs(x - y) % n
                g = math.gcd(q, n); k += m
            r *= 2
        if g == n:
            g = 1
            while g == 1: ys = (ys * ys + c) % n; g = math.gcd(abs(x - ys), n)
        if g != n: return g

def factor(n, F=None):
    F = {} if F is None else F
    for p in range(2, 20000):
        while n % p == 0: F[p] = F.get(p, 0) + 1; n //= p
        if n == 1: return F
    stack = [n]
    while stack:
        m = stack.pop()
        if m == 1: continue
        if is_prime(m): F[m] = F.get(m, 0) + 1; continue
        d = rho(m); stack += [d, m // d]
    return F

def icbrt(n):
    r = int(round(n ** (1 / 3))) if n < 1 << 900 else 1 << (n.bit_length() // 3)
    while r ** 3 > n: r -= 1
    while (r + 1) ** 3 <= n: r += 1
    return r

def exact_reps(n, F, maxdiv):
    """all (a,b), a<=b, a^3+b^3=n; None if n has more than maxdiv divisors"""
    if math.prod(e + 1 for e in F.values()) > maxdiv: return None
    lo, hi = icbrt(n) + 1, icbrt(4 * n)
    divs = [1]
    for p, e in F.items():
        divs = [d * p ** i for d in divs for i in range(e + 1) if d * p ** i <= hi]
    out = []
    for s in divs:
        if s < lo: continue
        v = 4 * (n // s) - s * s
        if v <= 0 or v % 3: continue
        r = math.isqrt(v // 3)
        if r * r * 3 == v and (s - r) % 2 == 0 and r < s: out.append(((s - r) // 2, (s + r) // 2))
    return sorted(set(out))

# ---------- known lists ----------
def known_numbers(refs, repo):
    known = {}
    def grab(path, label, mindig=20):
        if not os.path.exists(path): print(f"  (missing {path})"); return
        for m in re.findall(r"\d{%d,}" % mindig, open(path, errors="ignore").read()):
            known.setdefault(int(m), label)
    grab(os.path.join(refs, "ListTaxicab6_7.txt"), "Boyer 6-7-way list")
    grab(os.path.join(refs, "TaxicabUpdated.txt"), "Boyer-Wroblewski bound")
    grab(os.path.join(refs, "TaxibigUpdated.txt"), "Boyer-Wroblewski bound")
    sw = next((p for p in (os.path.join(repo, "results", "sixways.csv"), os.path.join(repo, "sixways.csv"))
               if os.path.exists(p)), "")
    if os.path.exists(sw):
        for line in open(sw): known.setdefault(int(line.split(";")[0]), "our sixways.csv")
    return known

def main():
    here = os.path.dirname(os.path.abspath(__file__))
    ap = argparse.ArgumentParser()
    ap.add_argument("hunt", nargs="+")
    ap.add_argument("--out", default="catalog.csv")
    # repo layout (experiments/../refs/boyer_lists) or flat (everything copied into one folder)
    flat = not os.path.isdir(os.path.join(here, "..", "refs", "boyer_lists"))
    ap.add_argument("--refs", default=os.path.join(here, "boyer_lists") if flat
                    else os.path.join(here, "..", "refs", "boyer_lists"))
    ap.add_argument("--repo", default=here if flat else os.path.join(here, ".."))
    ap.add_argument("--known", default=os.path.join(here, "known_numbers.csv"),
                    help="n;source file of known numbers (default: next to this script)")
    ap.add_argument("--maxdiv", type=int, default=200_000, help="skip the exact count above this many divisors")
    ap.add_argument("--show", type=int, default=5)
    a = ap.parse_args()
    random.seed(1)

    nums = {}                                            # n -> [M, L, set(pairs)]
    for path in a.hunt:
        for line in open(path):
            f = line.strip().split(";")
            if len(f) < 5: continue
            n, M, L = int(f[1]), int(f[2]), int(f[3])
            pairs = {tuple(map(int, p.split(":"))) for p in f[4].split(",") if p}
            for x, y in pairs:
                if x ** 3 + y ** 3 != n: sys.exit(f"FATAL: bad pair {x}:{y} for {n}")
            if n not in nums: nums[n] = [M, L, set()]
            nums[n][2] |= pairs
    print(f"{len(nums)} distinct numbers from {', '.join(a.hunt)}", flush=True)
    if os.path.exists(a.known):                         # one-file form (preferred)
        known = {}
        for line in open(a.known):
            if line[:1].isdigit():
                n, label = line.rstrip("\n").split(";", 1); known[int(n)] = label
    else:
        known = known_numbers(a.refs, a.repo)
    print(f"{len(known)} known numbers loaded for the novelty check", flush=True)

    rows = []
    for i, (n, (M, L, pairs)) in enumerate(sorted(nums.items()), 1):
        F = factor(M)
        # L = lcm of the point denominators w = L / gcd(a, b, L), each small (<= --wmax of the
        # hunt): factor those instead of L itself
        FL = {}
        for x, y in pairs:
            for p, e in factor(L // math.gcd(math.gcd(x, y), L)).items(): FL[p] = max(FL.get(p, 0), e)
        if math.prod(p ** e for p, e in FL.items()) != L:          # fallback: factor L directly
            FL = factor(L)
        for p, e in FL.items(): F[p] = F.get(p, 0) + 3 * e
        assert math.prod(p ** e for p, e in F.items()) == n
        ex = exact_reps(n, F, a.maxdiv)
        if ex is not None and not set(pairs) <= set(ex): sys.exit(f"FATAL: exact count misses a held pair for {n}")
        g = 0
        for x, y in (ex or pairs): g = math.gcd(g, math.gcd(x, y))
        rows.append(dict(n=n, found=len(pairs), exact=len(ex) if ex is not None else None,
                         prim=(g == 1), M=M, L=L, known=known.get(n, ""), pairs=sorted(ex or pairs)))
        if i % 1000 == 0: print(f"  {i}/{len(nums)}", flush=True)

    ways = lambda r: r["exact"] if r["exact"] is not None else r["found"]
    rows.sort(key=lambda r: (-ways(r), r["n"]))
    with open(a.out, "w") as f:
        f.write("n;ways_found;ways_exact;primitive;known;curve_M;L;pairs\n")
        for r in rows:
            f.write(f"{r['n']};{r['found']};{'' if r['exact'] is None else r['exact']};"
                    f"{'yes' if r['prim'] else 'no'};{r['known']};{r['M']};{r['L']};"
                    + ",".join(f"{x}:{y}" for x, y in r["pairs"]) + "\n")
    print(f"wrote {len(rows)} rows to {a.out}\n")
    by = defaultdict(list)
    for r in rows: by[ways(r)].append(r)
    print(f"{'ways':>4} {'numbers':>8} {'primitive':>9} {'new':>6}  smallest (P = primitive, * = not in known lists)")
    for k in sorted(by, reverse=True):
        rs = by[k]
        small = ", ".join(f"{r['n']:.4g}{'P' if r['prim'] else ''}{'*' if not r['known'] else ''}"
                          for r in sorted(rs, key=lambda r: r["n"])[:a.show])
        print(f"{k:>4} {len(rs):>8} {sum(r['prim'] for r in rs):>9} {sum(not r['known'] for r in rs):>6}  {small}")
    # the one novelty test that means something: Boyer's list claims every primitive 6- and 7-way
    # below 5e28, so a primitive 6/7-way below 5e28 that is missing from it is genuinely new
    gaps = [r for r in rows if ways(r) in (6, 7) and r["n"] < 5 * 10**28 and r["prim"] and not r["known"]]
    print(f"\nprimitive 6/7-ways below 5e28 missing from Boyer's list: {len(gaps)}")
    for r in gaps[:20]: print(f"   {r['n']}  ({ways(r)} ways, curve {r['M']})")
    exact_n = sum(r["exact"] is not None for r in rows)
    print(f"\nexact way counts for {exact_n}/{len(rows)} numbers (others: ways_found is a lower bound)")

if __name__ == "__main__":
    main()
