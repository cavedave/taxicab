#!/usr/bin/env python3
"""height_enum.py -- like generate_multiways.py (F91), but the points are all sum c_k G_k up to a canonical-height bound
(PARI qfminim on the height-pairing matrix) instead of the box |c_1| + ... + |c_r| <= 3. The bound grows in shells
(B0 = smallest generator height, doubled each time) until every point of a shell has n above DIGITS + 20 digits, so every
point with n below the digit limit is reached (assuming digits grow with height, as they do), and the huge points that
timed out in F91 are never computed. At most MAXVEC vectors per curve (rank-5 curves can reach it). Log: shapes/height_enum.jsonl (one line per curve)."""
import sys, json, itertools, time, resource, math
from fractions import Fraction as Fr
from multiprocessing import Pool
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent)); sys.path.insert(0, str(Path(__file__).resolve().parent))
if hasattr(sys, "set_int_max_str_digits"): sys.set_int_max_str_digits(0)
import bowtie_decide as BD
from bowtie_mine import Curve
from bowtie_components2 import seed_of
from generate_multiways import curves_from_file, classify, _cpu, ROOT
DIGITS, SAFETY, MAXVEC = 300, 1.15, 40000

def xpoints(head, x0, combos):
    out = []
    for l in BD.gp(BD.pts_src(head, x0, combos)).splitlines():
        if l.startswith("PT "): out.append((combos[int(l.split()[1]) - 1], Fr(l.split()[2])))
    return out

def rawdigits(C, x):
    """digits of n for the configuration at slope x, scaled to integers (coprime or not)"""
    s, r = x.denominator, x.numerator
    R = C.raw(s, r); G = 0
    for p, q in R: G = math.gcd(G, math.gcd(p, q))
    if G == 0: return 10**9
    p, q = R[0][0] // G, R[0][1] // G
    return len(str(abs(p**3 + q**3)))

def points(C, head, x0, combos):
    out = []
    for l in BD.gp(BD.pts_src(head, x0, combos)).splitlines():
        if l.startswith("PT "):
            j = int(l.split()[1]); x = Fr(l.split()[2]); out.append((combos[j - 1], classify(C, x.denominator, x.numerator)))
    return out

def work(item):
    key, slopes = item; c0 = _cpu(); BD.GPTIME = 900
    try:
        C = Curve(*key); seed = seed_of(C, slopes, 300)
        if seed is None: return dict(key=key, note='no seed', cpu=_cpu() - c0)
        head, x0 = BD.setup(C, seed, [])
        info = BD.gp(head + ['print("RANK ", #G, " ", #Gt); print("HM ", if(#G, ellheightmatrix(E, G), []));'])
        r, ng = [int(v) for v in info.split("RANK")[1].split()[:2]]
        if r == 0: return dict(key=key, note='rank 0', cpu=_cpu() - c0)
        H = [[float(v) for v in row.split(",")] for row in info.split("HM [")[1].split("]")[0].split(";")]
        ht = lambda c: sum(c[i] * H[i][j] * c[j] for i in range(r) for j in range(r))
        # shells: B = B0, 2 B0, 4 B0, ...; stop when every point of a shell has n above DIGITS + 20 digits
        B0 = min(H[i][i] for i in range(r)) * 1.01; B = B0; seen = set(); combos = []; shells = 0; capped = False
        while True:
            src = head + ['HM = ellheightmatrix(E, G); V = qfminim(HM, %.6f, %d, 2); M = V[3];' % (B, MAXVEC),
                          'for(j = 1, #M, print("V ", Vec(M[, j])));']
            vec = [tuple(int(t) for t in l[3:-1].split(",")) for l in BD.gp(src).splitlines() if l.startswith("V [")]
            if len(vec) >= MAXVEC: capped = True
            shell = [tuple(sv * v for v in c) + (0,) * (ng - r) for c in vec if c not in seen for sv in (1, -1)]
            seen |= set(vec); shells += 1
            dg = [rawdigits(C, x) for _, x in xpoints(head, x0, shell)] if shell else []
            combos += shell
            if capped or shells > 12 or (dg and min(dg) > DIGITS + 20): break
            B *= 2
        vec = seen
        five, four = {}, {}
        for c, res in points(C, head, x0, combos):
            if not res: continue
            k, n, allp = res
            if len(str(n)) > DIGITS: continue
            (five if k == 2 else four if k == 1 else {})[n] = allp
        return dict(key=key, note=f'rank {r}, B {B:.1f} after {shells} shells, {len(vec)} vectors{" (capped)" if capped else ""}',
                    cpu=_cpu() - c0, five=[[str(n), p] for n, p in five.items()], four=[[str(n), p] for n, p in four.items()])
    except Exception as e:
        return dict(key=key, note=f'error {e!r}'[:100], cpu=_cpu() - c0)

if __name__ == "__main__":
    curves = curves_from_file(ROOT / 'results/five_ways_all.txt')
    sel = [int(v) for v in sys.argv[1].split(",")] if len(sys.argv) > 1 else None      # pilot: indices into the curve list
    todo = [curves[i] for i in sel] if sel else curves
    LOG = Path(__file__).resolve().parent / ('height_enum_pilot.jsonl' if sel else 'height_enum.jsonl')
    done = {tuple(json.loads(l)['key']) for l in open(LOG)} if LOG.exists() else set()
    todo = [c for c in todo if tuple(c[0]) not in done]
    print(len(curves), "curves,", len(todo), "to do", flush=True); t0 = time.time()
    with Pool(6) as P, open(LOG, 'a') as out:
        for i, d in enumerate(P.imap_unordered(work, todo, chunksize=1)):
            d['key'] = list(d['key']); out.write(json.dumps(d) + "\n"); out.flush()
            print(f"{i + 1}/{len(todo)} {tuple(d['key'])}: {d['note']}; {len(d.get('five', []))} five, {len(d.get('four', []))} four, cpu {d['cpu']:.0f} s [{time.time() - t0:.0f} s]", flush=True)
