#!/usr/bin/env python3
"""dline_analyse.py -- join ordinary lines (line_enum.py output) with D-lines (dline_enum.py output) and report
structure, exact counts and yields. Streams the (multi-GB) inputs: compact keys are written to --tmp and sorted
on disk (sort -u), so memory stays small.

  - D histogram per direction, and the Theorem 7 check D | (b - a) E
  - join: n with an ordinary line and a D-line; the D-line shares 0, 1 or 2 points with the n's lines
  - D-line stars: >= 2 distinct D-lines of the same n through the same R (up to swap) = hubs; >= 3: six representations
  - exact counts (collisions.all_reps) for every joined n, every star, and random samples of each candidate set,
    with yields by direction-rank bucket (rank = position in the cost order of its parity)

Usage: python3 dline_analyse.py lines.txt dl1.txt [dl2.txt ...] --out report.txt --tmp DIR [--sample 20000] [--procs 8] [--gp gp]
"""
import argparse, os, random, subprocess, time
from collections import Counter, defaultdict
from fractions import Fraction as F
from multiprocessing import Pool
from collisions import all_reps, factor_batch

def canon(p): return tuple(sorted(p))

def _count(job):
    part, gp = job
    return part, [all_reps(n, f) for n, f in zip(part, factor_batch(part, gp))]

def count(ns, procs, gp="gp"):
    ns = sorted(set(ns)); res = {}
    parts = [ns[i:i + 2000] for i in range(0, len(ns), 2000)]
    with Pool(procs) as pool:
        for part, reps in pool.imap_unordered(_count, [(p, gp) for p in parts]):
            for n, r in zip(part, reps): res[n] = r
    return res

def sort_u(src, dst, tmp):
    subprocess.run(["sort", "-u", "-S", "3G", "-T", tmp, "-o", dst, src], check=True)

def reservoir(path, k, seed):
    rng = random.Random(seed); out = []
    for i, l in enumerate(open(path)):
        if i < k: out.append(l)
        else:
            j = rng.randrange(i + 1)
            if j < k: out[j] = l
    return out

def main():
    ap = argparse.ArgumentParser(); ap.add_argument("lines"); ap.add_argument("dls", nargs="+")
    ap.add_argument("--out", required=True); ap.add_argument("--tmp", required=True)
    ap.add_argument("--sample", type=int, default=20000); ap.add_argument("--procs", type=int, default=8)
    ap.add_argument("--gp", default="gp")
    A = ap.parse_args(); t0 = time.time(); rep = open(A.out, "w"); os.makedirs(A.tmp, exist_ok=True)
    def say(*x):
        s = " ".join(map(str, x)); print(s, flush=True); rep.write(s + "\n"); rep.flush()
    import dline_enum as DL
    rk = {}
    for par in ("even", "odd"):
        for i, d in enumerate(DL.norm_directions(5000, par)): rk[d] = i + 1
    def bucket(r): return next(f"rank<={x}" for x in (8, 50, 200, 1000, 5000, 10**9) if r <= x)
    T = lambda f: os.path.join(A.tmp, f)

    # pass 1: lines -> "n;rank" keys
    ntrip = 0; ldirs = Counter()
    with open(T("l_raw"), "w") as g:
        for l in open(A.lines):
            n, a, b, _ = l.split(";", 3); ntrip += 1; ldirs[(int(a), int(b))] += 1
            g.write(f"{n};{rk.get((int(a), int(b)), 10**9)}\n")
    sort_u(T("l_raw"), T("l_sorted"), A.tmp); os.remove(T("l_raw"))
    lrank = {}; nl = 0
    with open(T("l_n"), "w") as g:
        prev = None
        for l in open(T("l_sorted")):
            n, r = l.strip().split(";")
            if n != prev: g.write(n + "\n"); nl += 1; prev = n
    say(f"lines: {ntrip} triples in {len(ldirs)} directions, {nl} distinct n  [{time.time()-t0:.0f}s]")

    # pass 2: D-lines -> "n;R;pair;d;a;b"
    nd = 0; bad = 0; dhist = defaultdict(Counter)
    with open(T("d_raw"), "w") as g:
        for fn in A.dls:
            for l in open(fn):
                n, d, a, b, c, ps, R = l.strip().split(";"); d, a, b = int(d), int(a), int(b); nd += 1
                P1, P2 = sorted(canon(tuple(map(int, q.split(":")))) for q in ps.split(","))
                X, Y = map(int, R.split(":")); Rc = canon((F(X, d), F(Y, d)))
                g.write(f"{n};{Rc[0]}:{Rc[1]};{P1[0]}:{P1[1]},{P2[0]}:{P2[1]};{d};{a};{b}\n")
                dhist[(a, b)][d] += 1
                if ((b - a) * (a*a + a*b + b*b)) % d: bad += 1
    sort_u(T("d_raw"), T("d_sorted"), A.tmp); os.remove(T("d_raw"))
    say(f"D-lines: {nd} written (with repeats); Theorem 7 (D | (b-a)E) violations: {bad}")
    for (a, b), c in sorted(dhist.items(), key=lambda kv: rk.get(kv[0], 10**9))[:40]:
        say(f"  ({a},{b}) rank {rk.get((a, b))} b-a={b-a} E={a*a+a*b+b*b}: " + ", ".join(f"D={d}:{k}" for d, k in sorted(c.items())))
    if len(dhist) > 40: say(f"  ... {len(dhist)} directions in all")

    # scan sorted D-lines: distinct lines, distinct n, stars (same n and R, distinct pairs)
    stars = {}; ndl = 0; nn = 0; prevn = None; prevkey = None; group = set(); grp_key = None
    with open(T("d_n"), "w") as g:
        for l in open(T("d_sorted")):
            n, R, pair, d, a, b = l.strip().split(";")
            if (n, R, pair) == prevkey: continue
            prevkey = (n, R, pair); ndl += 1
            if n != prevn: g.write(n + "\n"); nn += 1; prevn = n
            if (n, R) != grp_key:
                if len(group) >= 2: stars[grp_key] = group
                grp_key = (n, R); group = set()
            group.add((pair, d, a, b))
        if len(group) >= 2: stars[grp_key] = group
    say(f"D-lines: {ndl} distinct, {nn} distinct n; stars (>= 2 D-lines through one R): sizes "
        f"{dict(Counter(len(v) for v in stars.values()))}  [{time.time()-t0:.0f}s]")

    # join (both n files are sorted the same way)
    J = set(subprocess.run(["comm", "-12", T("l_n"), T("d_n")], capture_output=True, text=True, check=True).stdout.split())
    Jint = {int(n) for n in J}
    linepts = defaultdict(set); dpairs = defaultdict(list)
    for l in open(A.lines):
        n = l.split(";", 1)[0]
        if n in J:
            for q in l.strip().split(";")[4].split(","): linepts[n].add(canon(tuple(map(int, q.split(":")))))
    for l in open(T("d_sorted")):
        n = l.split(";", 1)[0]
        if n in J:
            pair = [tuple(map(int, q.split(":"))) for q in l.split(";")[2].split(",")]
            dpairs[n].append(frozenset(pair))
    shape = Counter(); guaranteed = {}
    for n in J:
        best = 0
        for pair in set(dpairs[n]):
            new = len(pair - linepts[n]); best = max(best, new); shape[f"D-line shares {2 - new} point(s) with the lines"] += 1
        guaranteed[int(n)] = len(linepts[n]) + best
    say(f"join: {len(J)} n with a line and a D-line; per D-line: {dict(shape)}; guaranteed: {dict(Counter(guaranteed.values()))}")

    # exact counts: joined, stars, samples
    sL = [int(l) for l in reservoir(T("l_n"), A.sample, 1)]
    sD = [int(l) for l in reservoir(T("d_n"), A.sample, 2)]
    starn = {int(n) for n, R in stars}
    todo = Jint | starn | set(sL) | set(sD)
    say(f"counting {len(todo)} n exactly ...")
    t1 = time.time(); K = count(todo, A.procs, A.gp); dt = time.time() - t1
    say(f"  {len(todo)} counted in {dt:.0f}s ({1000*dt/max(1,len(todo)):.1f} ms each, {A.procs} processes)")
    def hist(ns): return dict(sorted(Counter(len(K[n]) for n in ns).items()))
    say(f"  sample of line candidates: {hist(sL)}")
    say(f"  sample of D-line candidates: {hist(sD)}")
    say(f"  joined n: {hist(Jint)}")
    say(f"  star n: {hist(starn)}")
    # rank buckets for the samples (min rank over all lines of n)
    need = {str(n) for n in sL}; lr = {}
    for l in open(T("l_sorted")):
        n, r = l.strip().split(";")
        if n in need: lr[n] = min(lr.get(n, 10**9), int(r))
    need = {str(n) for n in sD}; dr = {}
    for l in open(T("d_sorted")):
        p = l.strip().split(";")
        if p[0] in need: dr[p[0]] = min(dr.get(p[0], 10**9), rk.get((int(p[4]), int(p[5])), 10**9))
    for name, smp, rr in (("line", sL, lr), ("D-line", sD, dr)):
        by = defaultdict(list)
        for n in smp: by[bucket(rr[str(n)])].append(n)
        for b in sorted(by, key=lambda x: int(x.split("<=")[1])):
            h = Counter(len(K[n]) for n in by[b]); m = len(by[b]); k4 = sum(v for k, v in h.items() if k >= 4)
            say(f"  {name:6s} sample {b:11s}: {m:6d} n; >=4: {k4} ({1e3*k4/max(1,m):.2f} per 1000); >=5: {sum(v for k, v in h.items() if k >= 5)}")
    for n in sorted(n for n in todo if len(K[n]) >= 5):
        tags = (["join(guaranteed %d)" % guaranteed[n]] if n in Jint else []) + \
               [f"star{len(v)}" for (m, R), v in stars.items() if int(m) == n]
        say(f"  *** n = {n}: {len(K[n])} representations  {' '.join(tags)}")
    with open(A.out + ".multi", "w") as f:
        for n in sorted(n for n in todo if len(K[n]) >= 4):
            f.write(f"{n};{len(K[n])};" + ",".join(f"{x}:{y}" for x, y in sorted(K[n])) + "\n")
    with open(A.out + ".stars", "w") as f:
        for (n, R), v in stars.items():
            f.write(f"{n};{R};{len(K.get(int(n), []))};" + "|".join(f"{p}/D{d}/({a},{b})" for p, d, a, b in sorted(v)) + "\n")
    say(f"done [{time.time()-t0:.0f}s]")

if __name__ == "__main__":
    main()
