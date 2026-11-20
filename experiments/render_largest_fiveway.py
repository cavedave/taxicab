import textwrap, math, matplotlib
matplotlib.use("Agg"); import matplotlib.pyplot as plt
L=[l.strip().split(';') for l in open('results/five_ways_all.txt') if l[0]!='#']
r=max(L,key=lambda r:int(r[0])); n=int(r[0])
reps=[tuple(map(int,p.split(':'))) for p in r[2].split(',')]
assert len(set(reps))==5
for x,y in reps: assert x**3+y**3==n and math.gcd(x,y)==1
rows=[]
for x,y in reps:
    if x>0 and y>0: a,b=max(x,y),min(x,y); rows.append((0,a,a,"+",b))
    else: P,q=max(x,y),-min(x,y); rows.append((1,P,P,"−",q))
rows.sort()
W=102
def wrapc(v): ch=textwrap.wrap(str(v),W); ch[-1]+="³"; return ch
blocks=[("n =",textwrap.wrap(str(n),W),"")]
for _,_,a,op,b in rows: blocks.append(("=",wrapc(a),"")); blocks.append((op,wrapc(b),"gap"))
nl=sum(len(bl[1]) for bl in blocks)
H=0.2*nl+0.12*len(blocks)+1.1
fig=plt.figure(figsize=(11,H),dpi=200); fig.patch.set_facecolor("white")
y=H-0.4
for lab,ls,g in blocks:
    for i,t in enumerate(ls):
        if i==0: fig.text(0.04,y/H,lab,fontsize=9,family="monospace",va="center")
        fig.text(0.08,y/H,t,fontsize=9,family="monospace",va="center"); y-=0.2
    y-=0.22 if (g or lab=="n =") else 0.04
fig.text(0.04,0.35/H,f"Largest five-way in our list (capped at 300 digits): {len(str(n))} digits, exactly five representations x³ + y³, coprime, all checked exactly.",fontsize=9,family="serif",color="#666666",va="center")
out="out/a047697/a047697_5way_largest_300digits.png"
fig.savefig(out,facecolor="white"); print(out, len(str(n)), r[1], r[3], [len(str(max(abs(x),abs(y)))) for x,y in reps])
