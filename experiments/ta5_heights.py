import math
from fractions import Fraction as Fr
exec(open(__import__('os').path.join(__import__('os').path.dirname(__file__),'ta5_points.py')).read().split('C=int')[0])
def lg(n): # log of big int
    b=n.bit_length(); return math.log(n>>max(0,b-60))+max(0,b-60)*math.log(2) if n>0 else 0
def hnaive(P): X=P[0]; return max(lg(abs(X.numerator)),lg(X.denominator))
K=int(__import__('sys').argv[1])
def hcan(P):
    Q=P
    for _ in range(K): Q=add(Q,Q)
    return hnaive(Q)/4**K
def pair(P,Q): return (hcan(add(P,Q))-hcan(P)-hcan(Q))/2
extra={79:(582162,28906206)}
pts=G+[to_W(Fr(a,79),Fr(b,79)) for a,b in [extra[79]]]
assert all(P[1]**2==P[0]**3+B for P in pts)
n=len(pts); M=[[pair(pts[i],pts[j]) if i!=j else hcan(pts[i]) for j in range(n)] for i in range(n)]
def det(A):
    A=[r[:] for r in A]; d=1.0; m=len(A)
    for c in range(m):
        p=max(range(c,m),key=lambda r:abs(A[r][c])); 
        if abs(A[p][c])<1e-300: return 0.0
        A[c],A[p]=A[p],A[c]; d*=A[c][c]*(1 if p==c else -1)
        for r in range(c+1,m):
            f=A[r][c]/A[c][c]
            for k in range(c,m): A[r][k]-=f*A[c][k]
    return d
print('K=%d heights'%K,[round(M[i][i],4) for i in range(n)])
print('regulator of 5 integral points: %.6g'%det([r[:5] for r in M[:5]]))
print('det with 79-point added:        %.6g'%det(M))
import numpy as np
for k in (5,6):
    pass
ev=np.linalg.eigvalsh(np.array(M)); print('eigenvalues (6 points):',np.round(ev,4))
ev5=np.linalg.eigvalsh(np.array([r[:5] for r in M[:5]])); print('eigenvalues (5 integral):',np.round(ev5,4))
# find integer relation among the 5 integral points: null vector
w,v=np.linalg.eigh(np.array([r[:5] for r in M[:5]])); vec=v[:,0]; print('null vector ~',np.round(vec/vec[np.argmax(abs(vec))],4))
