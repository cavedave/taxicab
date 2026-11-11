#!/usr/bin/env python3
"""bowtie_decide.py -- (F59) decide whether a direction pair carries bowties and find its smallest ones.

F59: relative to a bowtie, second-line integrality at p | E2 (b2 - a2) is '2P in E_0(Q_p)', a condition on P mod a
finite-index subgroup; for I_n reduction it has period n/2 in the Mordell-Weil coefficients. So:
  1. seed: a rational point of w^2 = q (hyperellratpoints, or a known bowtie); generators G (ellrank) + torsion;
  2. periodic conditions: per prime and kind (second line integral at p, second line coprime at p), tested on the box
     c in [-M, M]^r with M = lcm(n_p / 2) over the I_n primes; kept only if it is a function of c mod M there;
  3. feasible classes mod M = those passing every periodic condition (none: the pair is OBSTRUCTED);
  4. inside the feasible classes, points in order of canonical height c^T H c (H = ellheightmatrix), each tested in full
     (Curve.bowtie); prints the smallest bowties found.
Usage: python3 bowtie_decide.py --pairs a,b,i,a2,b2 ... | --catalogue | --base 3,4 [1,4 ...] --amax 60 [--amin 0] [--npts 3000] [--procs 8]
       [--log run.log --resume]   (--log: per-curve lines also go to this file; --resume skips curves already in it and
       appends to --log and --out.  --base jobs run in order of max(a2, b2), so a stopped run covers every pair below some
       value. --amin skips pairs with max(a2, b2) < amin, i.e. those done by an earlier run with --amax amin.)
"""
import argparse, itertools, math, re, subprocess, sys
from functools import reduce
if hasattr(sys, "set_int_max_str_digits"): sys.set_int_max_str_digits(0)   # Python >= 3.11 only (7of9 has 3.8)
from collections import defaultdict
from fractions import Fraction as Fr
from multiprocessing import Pool
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
import line_enum as L
from bowtie_mine import Curve
from bowtie_hunt import curves_from_catalogue, factor_many, count_reps
from bowtie_congruence import analyse, pf, GPF
from bowtie_components2 import seed_of

GPTIME = 900                                                   # seconds per gp call (--gptime); set in each job
def gp(src):
    return subprocess.run(["gp", "-q", "-D", "parisizemax=4000000000"], input="\n".join(src), capture_output=True, text=True, timeout=GPTIME).stdout

def setup(C, seed, rel):
    x0, w0 = seed
    qpol = "+".join("(%d)*X^%d" % (c, k) for k, c in enumerate(C.q))
    head = ["\\r %s" % GPF, "Q = subst(%s, X, %s + u); q0 = %s; E = q2e(Q, q0); Em = ellminimalmodel(E);" % (qpol, x0, w0),
            'R = iferr(alarm(120, ellrank(E)), e, e); if(type(R) == "t_ERROR", print("RANKTIMEOUT"); R = [0,0,0,[]]);',   # alarm returns its error
            # default effort can find no generators where effort 3 finds them at once ((1,12,2,49,192): rank 4, 3 gens)
            'if(#R[4] < R[2], my(R3 = iferr(alarm(120, ellrank(E, 3)), e, e)); if(type(R3) != "t_ERROR" && #R3[4] > #R[4], R = R3));',
            'G = if(#R[4], vecextract(R[4], Str("1..", min(#R[4], 5))), []); T = elltors(E);',   # Str("1..0") is an error
            "Gt = concat(G, T[3]); ord = concat(vector(#G, k, 0), T[2]);"]
    return head, x0

def pts_src(head, x0, cs):
    body = ["CS = [%s];" % ";".join(",".join(map(str, c)) for c in cs) if cs else "CS = [];",
            "for(j = 1, #CS~, my(c = CS[j,], P = [0]); for(k = 1, #Gt, if(c[k], P = elladd(E, P, ellmul(E, Gt[k], c[k])))); "
            "if(#P == 2, my(B = toQ(Q, q0, P)); if(B != 0, print(\"PT \", j, \" \", B[1] + %s))));" % x0]
    return head + body

def job(args):
    try: return job1(args)
    except Exception as e: return args[0], f"ERROR {e!r}", None

def job1(args):
    global GPTIME
    key, slopes, npts, cmaxh, seedh, count, GPTIME = args
    a, b, i, a2, b2 = key; C = Curve(*key)
    seed = seed_of(C, slopes, seedh)
    if seed is None: return key, "no point found", None
    rel = sorted(pf(a*a + a*b + b*b) | pf(b - a) | pf(a2*a2 + a2*b2 + b2*b2) | pf(b2 - a2))
    head, x0 = setup(C, seed, rel)
    info = gp(head + ['print("RANK ", R[1], " ", R[2], " ", #G, " ", ord);',
                      'foreach([%s], p, my(L = elllocalred(Em, p)); print("RED ", p, " ", L[2]));' % ",".join(map(str, rel)),
                      'print("HM ", if(#G, ellheightmatrix(E, G), []));'])
    rank, ordv, red, HM = None, None, {}, None
    for l in info.splitlines():
        if l.startswith("RANK"):
            m = re.match(r"RANK (\S+) (\S+) (\d+) \[(.*)\]", l); rank = (m.group(1), m.group(2)); ordv = [int(v) for v in m.group(4).split(",")]
        elif l.startswith("RED"): _, p, k = l.split(); red[int(p)] = int(k)
        elif l.startswith("HM"):
            rows = l[3:].strip().replace("Mat(", "").rstrip(")").strip("[]").split(";")
            HM = [[float(v.replace(" ", "")) for v in r.split(",")] for r in rows] if rows[0].strip() else []
    if "RANKTIMEOUT" in info: return key, "RANKTIMEOUT: ellrank over 120 s, curve not decided", None
    if ordv is None or not HM: return key, f"rank {rank}: no generators", None
    r = len(HM); M = 1
    for p in rel:
        k = red.get(p, 0)
        if k > 4 and (k - 4) % 2 == 0: M = M * ((k - 4) // 2) // math.gcd(M, (k - 4) // 2)   # lcm (math.lcm is 3.9+)
    # 2. box covering every class mod M (torsion coordinates over their order)
    box = [c for c in itertools.product(*([range(-M, M + 1)] * r + [range(o) for o in ordv[r:]]))]
    out = gp(pts_src(head, x0, box))
    st = {}
    for l in out.splitlines():
        if l.startswith("PT "):
            _, j, x = l.split(); x = Fr(x); o = analyse(C, x.denominator, x.numerator)
            if o: st[box[int(j) - 1]] = o[0]
    cls = lambda c: tuple(v % M for v in c[:r]) + tuple(c[r:])
    periodic = []
    for p in rel:
        for kind in ("den", "sec"):
            by = defaultdict(set)
            for c, bd in st.items(): by[cls(c)].add(p in bd[kind])
            if any(True in v for v in by.values()) and all(len(v) == 1 for v in by.values()): periodic.append((p, kind))
    by = defaultdict(set)
    for c, bd in st.items(): by[cls(c)].add(all(p not in bd[kind] for p, kind in periodic))
    feas = sorted(k for k, v in by.items() if True in v)
    if not feas: return key, f"rank {rank}, M {M}: OBSTRUCTED by {periodic}", None
    # 4. height-ordered points in the feasible classes
    cand = []
    for c in itertools.product(*([range(-cmaxh, cmaxh + 1)] * r + [range(o) for o in ordv[r:]])):
        if cls(c) in set(feas):
            h = sum(HM[u][v] * c[u] * c[v] for u in range(r) for v in range(r)); cand.append((h, c))
    cand = [c for h, c in sorted(cand)[:npts]]
    out = gp(pts_src(head, x0, cand))
    found = {}
    for l in out.splitlines():
        if l.startswith("PT "):
            _, j, x = l.split(); x = Fr(x)
            o, why = C.bowtie(x.denominator, x.numerator)
            if o and o[0] < 10**300: found[o[0]] = o
            elif o: found.setdefault("big", 0); found["big"] += 1
    big = found.pop("big", 0); ns = sorted(found)
    if not count: return key, f"rank {rank}, M {M}, periodic {len(periodic)}, feasible {len(feas)}/{len(by)} classes, {len(cand)} points tested", dict({n: (None, found[n][1]) for n in ns}, big=big)
    pieces = []
    for n in ns: pieces += [C.E, abs(a - b) or 1] + [abs(v) for v in found[n][2]]
    facs = factor_many(pieces, "gp", 300) if pieces else []
    res = {"big": big}
    for j, n in enumerate(ns):
        fs = facs[5 * j: 5 * j + 5]
        if None in fs: res[n] = (None, found[n][1]); continue
        F = {}
        for fac, sg in zip(fs, (1, -2, 1, 1, 1)):
            for p, e in fac: F[p] = F.get(p, 0) + sg * e
        F = sorted((p, e) for p, e in F.items() if e)
        assert all(e > 0 for p, e in F) and math.prod(p**e for p, e in F) == n
        reps = count_reps(n, F); assert len(reps) >= 5
        res[n] = (reps, found[n][1])
    return key, f"rank {rank}, M {M}, periodic {len(periodic)}, feasible {len(feas)}/{len(by)} classes, {len(cand)} points tested", res

def main():
    ap = argparse.ArgumentParser(); ap.add_argument("--pairs", nargs="*", default=[]); ap.add_argument("--catalogue", action="store_true")
    ap.add_argument("--base", nargs="*", default=[]); ap.add_argument("--amin", type=int, default=0); ap.add_argument("--amax", type=int, default=60); ap.add_argument("--npts", type=int, default=3000)
    ap.add_argument("--cmaxh", type=int, default=6); ap.add_argument("--procs", type=int, default=8); ap.add_argument("--out", default="")
    ap.add_argument("--seedh", type=int, default=60); ap.add_argument("--count", action="store_true")
    ap.add_argument("--alli", action="store_true", help="all three shared points (F61: they give the same bowties)")
    ap.add_argument("--log", default=""); ap.add_argument("--resume", action="store_true")
    ap.add_argument("--gap", type=int, default=0, help="only second directions (a2, a2 + GAP), a2 in [amin, amax) (F93: gap 1 is ~15x richer)")
    ap.add_argument("--gptime", type=int, default=900, help="seconds per gp call (the periodicity box (2M+1)^r can take minutes)")
    A = ap.parse_args()
    jobs = [(tuple(map(int, s.split(","))), []) for s in A.pairs]
    if A.catalogue: jobs += [(c[:5], c[5]) for c in curves_from_catalogue()]
    ns = lambda m: {q for q in (L.factor(abs(m)) if abs(m) > 1 else {}) if q % 3 != 1}
    bj = []
    for base in A.base:
        a, b = map(int, base.split(","))
        for a2 in range(1, A.amax):
            for b2 in ((a2 + A.gap,) if A.gap else range(1, A.amax)):
                if max(a2, b2) < A.amin: continue
                if a2 != b2 and math.gcd(a2, b2) == 1 and {a2, b2} != {a, b} and ns(b2 - a2) <= ns(b - a) and ns(b - a) <= ns(b2 - a2) | {3}:
                    bj += [((a, b, i, a2, b2), []) for i in (range(3) if A.alli else (0,))]
    jobs += sorted(bj, key=lambda j: (max(j[0][3], j[0][4]), j[0]))
    done = set()
    if A.resume and A.log and Path(A.log).exists():
        for l in open(A.log):
            m = re.match(r"^\((\d+), (\d+), (\d+), (\d+), (\d+)\): ", l)
            if m and "ERROR" not in l: done.add(tuple(map(int, m.groups())))
    todo = [j for j in jobs if j[0] not in done]
    print(f"{len(jobs):,} curves, {len(done):,} already logged, {len(todo):,} to run", flush=True)
    cat = {int(l.split(";")[0]) for l in open(Path(__file__).resolve().parents[2] / "results/a047697_catalogue.txt") if l[0].isdigit()}
    mode = "a" if A.resume else "w"
    f = open(A.out, mode) if A.out else None
    lg = open(A.log, mode) if A.log else None
    def say(line):
        print(line, flush=True)
        if lg: lg.write(line + "\n"); lg.flush()
    with Pool(A.procs) as pool:
        for key, note, found in pool.imap_unordered(job, [(k, s, A.npts, A.cmaxh, A.seedh, A.count, A.gptime) for k, s in todo]):
            if found is None: say(f"{key}: {note}"); continue
            big = found.pop("big", 0); ns = sorted(found); kmax = max((len(found[n][0]) for n in ns if found[n][0]), default=0)
            say(f"{key}: {note}; {len(ns)} bowties < 1e300 (+{big} larger), largest k {kmax}, k unknown {sum(1 for n in ns if found[n][0] is None)}" + (f", smallest {ns[0]:.3e} ({len(str(ns[0]))} digits, {'known' if ns[0] in cat else 'NEW'})" if ns else ""))
            if f:
                for n in ns:
                    reps, five = found[n]
                    f.write(f"{n};{len(reps) if reps else '?'};" + ",".join(f"{x}:{y}" for x, y in sorted(reps or five, reverse=True)) + f";{'known' if n in cat else 'new'};{key}\n")
                    if reps and len(reps) >= 6: print(f"*** SIX-WAY OR MORE: k = {len(reps)}, n = {n}", flush=True)
                f.flush()

if __name__ == "__main__":
    main()
