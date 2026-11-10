import subprocess, sys
S = sys.argv[1] if len(sys.argv) > 1 else "shapes/recall12"   # folder holding lines12.txt (line_enum.py output, not committed)
N = [506433677359393,137904678696613339,39673716067958900347,95793117931950826933,118371660133721558473,624256195206357000469,
     633753337814536954807,921288078249108802505,1038246186276942167105,2724248230569896697541,5306775242131114520041,236191447138323830299237]
hits = {}
for l in open(f'{S}/lines12.txt'):
    f = l.split(';'); n = int(f[0])
    if n in N: hits.setdefault(n, set()).add((int(f[1]), int(f[2])))
split = [p for p in range(7, 1000) if p % 3 == 1 and all(p % q for q in range(2, int(p**.5) + 1))]
def filt(n): return sum(n % p == 0 for p in (7, 13, 19, 37)) >= 2 and sum(n % p == 0 for p in split) >= 7
# exact count of coprime representations (x, y) up to swap, signs allowed: x + y = s | n, 3 x y = (s^2 - n/s)... via 4n/s - s^2 = 3 t^2
gp = "cnt(n)=my(c=0);fordiv(n,s,if(s^3>4*n,next);my(q=4*n/s-s^2);if(q%3,next);q/=3;if(!issquare(q,&t),next);my(x=(s+t)/2,y=(s-t)/2);if(denominator(x)>1,next);if(gcd(x,y)==1&&x*y!=0,c++));c\n"
gp += "".join(f"print(cnt({n}))\n" for n in N)
cnts = subprocess.run(["gp", "-q"], input=gp, capture_output=True, text=True).stdout.split("\n")
cnts = [c for c in cnts if c.strip().isdigit()]
found = 0
for n, k in zip(N, cnts):
    h = hits.get(n, set()); found += bool(h)
    print(f"{n:>26}  k={k}  line found: {'yes ' + str(sorted(h)) if h else 'NO'}  filter: {'pass' if filt(n) else 'fail'} (of 7,13,19,37: {sum(n % p == 0 for p in (7,13,19,37))}; split primes < 1000: {sum(n % p == 0 for p in split)})")
print(f"found by the line search: {found} of {len(N)}")
