"""bowtie_unseeded.py -- (F58) per-prime pass rates of the bowtie conditions on (3,4)-based curves whose second direction
passes the non-split filter (every prime of b2 - a2 is 1 mod 3); seed from hyperellratpoints(q, 60)."""
import sys, subprocess, re
from fractions import Fraction as Fr
from collections import Counter
sys.path.insert(0, __import__("os").path.dirname(__import__("os").path.abspath(__file__)))
from bowtie_mine import Curve
from bowtie_congruence import points, analyse, pf
from multiprocessing import Pool
def run(key):
    a, b, i, a2, b2 = key; C = Curve(*key)
    out = subprocess.run(["gp", "-q"], input=f"print(hyperellratpoints({C.gp_poly()}, 60));", capture_output=True, text=True).stdout
    pts = [(Fr(x), Fr(y)) for x, y in re.findall(r"\[(-?\d+(?:/\d+)?), (-?\d+(?:/\d+)?)\]", out) if Fr(y) != 0]
    if not pts: return key, None
    xs, rank = points(C, pts[0], 3, 3)
    rows = [o for x in xs if (o := analyse(C, x.denominator, x.numerator))]
    if not rows: return key, (rank, 0, {}, 0)
    rel = sorted(set().union(*(bd[k] for bd, sh in rows for k in bd)))
    frac = {p: sum(1 for bd, sh in rows if not any(p in bd[k] for k in bd)) for p in rel}
    nb = sum(1 for bd, sh in rows if not any(bd.values()))
    return key, (rank, len(rows), frac, nb)
if __name__ == "__main__":
  import line_enum as L
  ok = lambda m: all(q % 3 == 1 for q in (L.factor(abs(m)) if abs(m) > 1 else {}))
  keys = [(3, 4, i, a2, b2) for a2 in range(1, 60) for b2 in range(1, 60) if a2 != b2 and ok(b2 - a2) and __import__("math").gcd(a2, b2) == 1 and {a2, b2} != {3, 4} for i in range(3)]
  with Pool(8) as P:
    for key, r in P.imap_unordered(run, keys):
        if r and r[1]: print(key, "rank", r[0], f"{r[1]} pts, {r[3]} bowties; pass per prime:", {p: f"{v}/{r[1]}" for p, v in r[2].items()}, flush=True)
