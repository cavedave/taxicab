#!/usr/bin/env python3
"""gen_pos_dirs.py -- direction lists for the positive hub search (cubefree_plan.md step 3, FINDINGS F42):
the next COUNT D-line directions of a parity in true cost order, skipping every direction already searched
(the legacy 20,000 of 27 October and the 150,000 of the hub run of 29 October).
Usage: python3 gen_pos_dirs.py --parity even --count 1500000 --out night_7of9/dirs/pos_even_1500000.txt"""
import argparse
import line_enum as L, dline_enum as DL
ap = argparse.ArgumentParser()
ap.add_argument("--parity", choices=["even", "odd"], required=True)
ap.add_argument("--count", type=int, required=True); ap.add_argument("--out", required=True)
A = ap.parse_args()
done = set(DL.legacy_norm_directions(20000, A.parity))
done |= {tuple(map(int, l.split(","))) for l in open(f"night_7of9/dirs/hubs_{A.parity}_150000.txt") if l[0] != "#"}
need = A.count + len(done)
cmax = 4 * 10**10
while True:
    Ls = L.dirs_by_cost(cmax, DL.norm_ok(A.parity))
    new = [(a, b) for _, a, b in Ls if (a, b) not in done]
    print(f"cmax {cmax:.2e}: {len(Ls)} directions, {len(new)} new", flush=True)
    if len(new) >= A.count: break
    cmax = int(cmax * 1.6)
new = new[:A.count]
with open(A.out, "w") as f:
    f.write(f"# D-line directions ({A.parity}), true cost order, never searched (not in the legacy 20,000 of 27 Oct "
            f"nor the hub run's 150,000 of 29 Oct): {A.count}; costs {new[0][1]**3 - new[0][0]**3:.3e} .. "
            f"{new[-1][1]**3 - new[-1][0]**3:.3e}\n")
    f.writelines(f"{a},{b}\n" for a, b in new)
print("wrote", A.out)
