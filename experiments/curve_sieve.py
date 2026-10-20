#!/usr/bin/env python3
"""curve_sieve.py -- rank curves x^3 + y^3 = M by a Mestre-Nagao sum, keep the best for hunting.

Each seed N (seedgen format N;k;p:e,...;a:b,...) is reduced to its cube-free core M. For every
distinct M we compute  S(M) = - sum_{p <= P, p = 1 mod 3, p not | M} a_p log(p) / p  with PARI's
ellap (a_p = 0 for p = 2 mod 3 on these CM curves). High S predicts high rank: on 602 random
curves from seeds_1e15 the Ta(5) and Boyer-Wroblewski record curves ranked 1st and 2nd, and the
top 20% held 8 of the 9 curves of rank >= 5. Cost ~3.4 ms per curve (ellrank ~1 s).

Outputs:  <ranked>   M;S                 every curve, best first
          <out>      seed lines whose core is among the top --top curves (input for curve_hunt)

Staged use (7of9): the first call scores every curve and saves <ranked>; later calls reuse it
and only cut a new window of ranks.
  python3 curve_sieve.py --gp ~/pari/bin/gp --seeds seeds_1e18.csv extra_seeds.csv \
          --procs 64 --skip 0 --top 10000 --out batch1.csv          # ranks 1..10,000
  python3 curve_sieve.py --seeds seeds_1e18.csv extra_seeds.csv \
          --skip 10000 --top 100000 --out batch2.csv                # ranks 10,001..110,000
"""
import argparse, os, subprocess, tempfile, time
from multiprocessing import Pool

GP = r"""
default(parisizemax, 2*10^9);
V = readvec("%(inp)s");
PR = select(p -> p %% 3 == 1, primes([7, %(P)d]));
nagao(M) = my(E = ellinit([0,0,0,0,-432*M^2]), s = 0.); foreach(PR, p, if(M %% p, s -= ellap(E, p)*log(p)/p)); s;
for(i = 1, #V, printf("%%d %%.4f\n", V[i], nagao(V[i])));
quit;
"""

def core_of(line):
    f = line.split(";")
    M = 1
    for pe in f[2].split(","):
        if pe:
            p, e = pe.split(":"); M *= int(p) ** (int(e) % 3)
    return M

ARGS = None
def init(a):
    global ARGS
    ARGS = a

def score(chunk):
    with tempfile.TemporaryDirectory() as d:
        inp = os.path.join(d, "v.txt"); src = os.path.join(d, "s.gp")
        open(inp, "w").write("\n".join(map(str, chunk)) + "\n")
        open(src, "w").write(GP % dict(inp=inp, P=ARGS.primes))
        out = subprocess.run([ARGS.gp, "-q", src], capture_output=True, text=True, check=True).stdout
    res = []
    for line in out.splitlines():
        parts = line.split()
        if len(parts) == 2 and parts[0].isdigit(): res.append((int(parts[0]), float(parts[1])))
    if len(res) != len(chunk): raise RuntimeError(f"gp returned {len(res)} of {len(chunk)} scores")
    return res

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--gp", default="gp")
    ap.add_argument("--seeds", nargs="+", required=True)
    ap.add_argument("--procs", type=int, default=os.cpu_count())
    ap.add_argument("--top", type=int, default=20000, help="how many curves to select")
    ap.add_argument("--skip", type=int, default=0, help="skip the best SKIP curves (for staged batches)")
    ap.add_argument("--rescore", action="store_true", help="recompute scores even if --ranked exists")
    ap.add_argument("--primes", type=int, default=20000, help="Nagao sum over p <= this")
    ap.add_argument("--chunk", type=int, default=2000)
    ap.add_argument("--ranked", default="ranked_curves.csv")
    ap.add_argument("--out", default="top_seeds.csv")
    a = ap.parse_args()
    t0 = time.time()
    if os.path.exists(a.ranked) and not a.rescore:
        scores = [(int(M), float(S)) for M, S in (l.strip().split(";") for l in open(a.ranked) if l.strip())]
        print(f"reusing {len(scores)} scores from {a.ranked} (--rescore to recompute)", flush=True)
    else:
        cores = set()
        for path in a.seeds:
            for line in open(path):
                if line.count(";") >= 3: cores.add(core_of(line))
        cores = sorted(cores)
        print(f"{len(cores)} distinct curves from {', '.join(a.seeds)} ({time.time()-t0:.0f}s)", flush=True)
        chunks = [cores[i:i + a.chunk] for i in range(0, len(cores), a.chunk)]
        scores = []
        with Pool(a.procs, initializer=init, initargs=(a,)) as pool:
            for i, res in enumerate(pool.imap_unordered(score, chunks), 1):
                scores += res
                if i % 50 == 0 or i == len(chunks):
                    print(f"[{time.time()-t0:6.0f}s] scored {len(scores)}/{len(cores)}", flush=True)
        scores.sort(key=lambda r: (-r[1], r[0]))
        with open(a.ranked, "w") as f:
            for M, S in scores: f.write(f"{M};{S:.4f}\n")
    window = scores[a.skip:a.skip + a.top]
    rank = {M: i for i, (M, _) in enumerate(window)}
    lines = []
    for path in a.seeds:
        for line in open(path):
            if line.count(";") >= 3:
                M = core_of(line)
                if M in rank: lines.append((rank[M], line if line.endswith("\n") else line + "\n"))
    lines.sort(key=lambda r: r[0])                      # best curves first: curve_hunt keeps this order
    with open(a.out, "w") as f:
        for _, line in lines: f.write(line)
    if window:
        print(f"curves ranked {a.skip + 1}..{a.skip + len(window)} of {len(scores)} "
              f"(S from {window[0][1]:.2f} down to {window[-1][1]:.2f}) -> {len(lines)} seed lines in {a.out}")
    print("best 10 overall:", ", ".join(f"{M} ({S:.1f})" for M, S in scores[:10]))

if __name__ == "__main__":
    main()
