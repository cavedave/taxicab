"""PARI factor (time limit each, parallel) on every composite part from strip2; writes fac.json {c: [[p,e],...] or null}."""
import sys, json, subprocess, re
from multiprocessing import Pool
if hasattr(sys, "set_int_max_str_digits"): sys.set_int_max_str_digits(0)
T = int(sys.argv[2])
def fac(c):
    src = f'r=alarm({T},factor({c})); if(type(r)=="t_ERROR",print("TIMEOUT"),print([Vec(r[,1]),Vec(r[,2]),apply(x->isprime(x),Vec(r[,1]))]))'
    t = subprocess.run(["gp", "-q", "-D", "parisizemax=2000000000"], input=src, capture_output=True, text=True).stdout.strip()
    if "TIMEOUT" in t or not t: return c, None
    ps, es, pp = eval(t.replace(";", ","))
    assert all(pp), "non-prime factor"
    return c, [[str(p), e] for p, e in zip(ps, es)]
if __name__ == "__main__":
  S = json.load(open(sys.argv[1]))
  cs = sorted({c for r in S for c, e in r["composite"]}, key=lambda c: len(c))
  res = {}
  with Pool(8) as P:
      for c, f in P.imap_unordered(fac, cs):
          res[c] = f; print(len(c), "ok" if f else "TIMEOUT", flush=True)
          json.dump(res, open("fac.json", "w"))
