#!/usr/bin/env python3
"""relations.py -- exact integer relations among the k integer points of n = x^3 + y^3 (coprime reps).

For each n: PARI ellrank (seeded with the k points) + ellsaturation give generators; every point is written
as an exact integer combination of them (verified by exact point arithmetic), and the relations are the
exact integer kernel (matkerint). Output, one line per n:
    n;k;rank_lo;rank_hi;span;ok;relations      relations = space-separated coefficient vectors like 1,1,0,-1
ok = 1 when every coordinate vector was verified exactly. On x^3+y^3=n, P+Q+R=0 <=> collinear, -P = swap.

Usage: python3 relations.py input.txt --out rel.txt [--procs 3]   (input: n;k;x:y,... lines)
"""
import argparse, subprocess
from multiprocessing import Pool

GP = r'''
default(parisizemax,2*10^9); default(realprecision, 150);
n=%(n)s; E=ellinit([0,0,0,0,-432*n^2]); P=[%(pts)s];
R=ellrank(E,1,P); G=ellsaturation(E,R[4],1000); r=#G; ok=1;
if(r==0, print(R[1],";",R[2],";0;1;"); quit);
HG=ellheightmatrix(E,G); C=matrix(#P,r);
for(i=1,#P, my(col=ellheightmatrix(E,concat(G,[P[i]]))[1..r,r+1]); my(c=round(matsolve(HG,col)~)); \
  my(Q=[0]); for(j=1,r, Q=elladd(E,Q,ellmul(E,G[j],c[j]))); if(Q!=P[i], ok=0); C[i,]=c);
K=matkerint(C~); s=""; for(j=1,#K, s=concat(s, concat(" ", strjoin(apply(x->Str(x), Vec(K[,j])), ","))));
print(R[1],";",R[2],";",matrank(C),";",ok,";",s);
'''

def run(line):
    n, k, ps = line.strip().split(";")[:3]
    pts = [tuple(map(int, p.split(":"))) for p in ps.split(",")]
    toW = ",".join(f"[12*n/({x}+({y})), 36*n*({x}-({y}))/({x}+({y}))]" for x, y in pts)
    try:
        out = subprocess.run(["gp", "-q"], input=GP % dict(n=n, pts=toW), capture_output=True, text=True,
                             timeout=600).stdout.strip().splitlines()
        out = out[-1] if out else "err;err;err;0;"
    except subprocess.TimeoutExpired:
        out = "timeout;timeout;timeout;0;"
    return f"{n};{k};{out}"

if __name__ == "__main__":
    ap = argparse.ArgumentParser(); ap.add_argument("input"); ap.add_argument("--out", required=True)
    ap.add_argument("--procs", type=int, default=3); a = ap.parse_args()
    lines = [l for l in open(a.input) if l[0].isdigit()]
    with Pool(a.procs) as pool, open(a.out, "w") as fo:
        for i, res in enumerate(pool.imap_unordered(run, lines), 1):
            fo.write(res + "\n"); fo.flush()
    print(f"{len(lines)} numbers -> {a.out}")
