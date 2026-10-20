# Splitting factors of N from rational points on x^3+y^3=N, via Y^2 = X^3 - 432 N^2.
import sys, itertools
from fractions import Fraction as Fr
from math import lcm

N=48988659276962496
pairs=[(38787,365757),(107839,362753),(205292,342952),(221424,336588),(231518,331954)]
B=-432*N*N
def to_W(x,y): s=x+y; return (Fr(12*N)/s, Fr(36*N)*(x-y)/s)
def to_xy(P):
    X,Y=P; return ((36*N+Y)/(6*X), (36*N-Y)/(6*X))
O=None
def add(P,Q):
    if P is O: return Q
    if Q is O: return P
    (x1,y1),(x2,y2)=P,Q
    if x1==x2:
        if y1==-y2: return O
        l=3*x1*x1/(2*y1)
    else: l=(y2-y1)/(x2-x1)
    x3=l*l-x1-x2; return (x3, l*(x1-x3)-y1)
def neg(P): return O if P is O else (P[0],-P[1])
G=[to_W(Fr(a),Fr(b)) for a,b in pairs]
for (X,Y),(a,b) in zip(G,pairs):
    assert Y*Y==X**3+B and to_xy((X,Y))==(a,b)
C=int(sys.argv[1]) if len(sys.argv)>1 else 3
mult=[]
for P in G:
    t={0:O}; acc=O
    for k in range(1,C+1): acc=add(acc,P); t[k]=acc; t[-k]=neg(acc)
    mult.append(t)
found={}
pts={():O}
for i in range(len(G)):
    new={}
    for key,P in pts.items():
        for c in range(-C,C+1): new[key+(c,)]=add(P,mult[i][c])
    pts=new
for key,P in pts.items():
    if P is O: continue
    x,y=to_xy(P)
    if x>0 and y>0:
        w=lcm(x.denominator,y.denominator)
        if w not in found or sum(map(abs,key))<sum(map(abs,found[w])): found[w]=key
small=sorted(w for w in found if w<=10000)
print('combos with |c_i| <=',C,': positive points',len(found),' denominators <= 10000:',small)
for w in small: print('  w =',w,' combo',found[w])
print('Boyer splitting factors {79,127,139,727,4622} all found:',{79,127,139,727,4622}<=set(found))
