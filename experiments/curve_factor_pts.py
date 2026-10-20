import sys, pickle, subprocess, tempfile, os
M, r, pts = pickle.load(open(sys.argv[1], "rb"))
ws = sorted({w for w,_,_ in pts})
with tempfile.TemporaryDirectory() as d:
    open(f"{d}/w.txt","w").write("\n".join(map(str, ws))+"\n")
    open(f"{d}/f.gp","w").write(f'V=readvec("{d}/w.txt"); for(i=1,#V, my(F=factor(V[i])); print(V[i],";",Vec(F[,1]),";",Vec(F[,2]))); quit;')
    out = subprocess.run(["/opt/homebrew/bin/gp","-q",f"{d}/f.gp"],capture_output=True,text=True,check=True).stdout
fac = {}
for line in out.splitlines():
    w, ps, es = line.replace(" ", "").split(";")
    fac[int(w)] = list(zip(eval(ps), eval(es)))
assert len(fac) == len(ws)
pickle.dump((M, r, pts, fac), open(sys.argv[2], "wb"))
print(M, "factored", len(fac), "denominators")
