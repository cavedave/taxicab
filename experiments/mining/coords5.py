import subprocess, sys
from multiprocessing import Pool
GP = r'''
default(parisizemax,4*10^9); default(realprecision, 150);
n=%(n)s; E=ellinit([0,0,0,0,-432*n^2]);
P=[%(pts)s];
R=ellrank(E,1,P); G=ellsaturation(E,R[4],1000); r=#G;
print("rank ",R[1],"..",R[2],"  generators ",r, "  torsion ", elltors(E)[1]);
HG=ellheightmatrix(E,G); C=matrix(#P,r); ok=1;
for(i=1,#P, my(col=ellheightmatrix(E,concat(G,[P[i]]))[1..r,r+1]); my(c=round(matsolve(HG,col)~)); \
  my(Q=[0]); for(j=1,r, Q=elladd(E,Q,ellmul(E,G[j],c[j]))); \
  if(Q!=P[i] && elladd(E,Q,ellneg(E,P[i]))!=[0], ok=0); C[i,]=c);
print("exact coordinates verified: ", ok);
print("rank of span of the ", #P, " points (exact): ", matrank(C));
K=matkerint(C~); for(j=1,#K, print("relation (exact): ", K[,j]~));
'''
def run(line):
    n, k, ps = line.strip().split(";")
    pts = [tuple(map(int, p.split(":"))) for p in ps.split(",")]
    toW = ",".join(f"[12*n/({x}+({y})), 36*n*({x}-({y}))/({x}+({y}))]" for x, y in pts)
    try:
        out = subprocess.run(["/opt/homebrew/bin/gp", "-q"], input=GP % dict(n=n, pts=toW), capture_output=True, text=True, timeout=1500).stdout.strip()
    except subprocess.TimeoutExpired:
        out = "TIMEOUT"
    return n, out.replace("\n", "\n   ")
if __name__ == "__main__":
    lines = [l for l in open(sys.argv[1]) if l[0].isdigit()]
    with Pool(4) as p:
        for n, r in p.imap_unordered(run, lines): print(f"{n}\n   {r}", flush=True)
