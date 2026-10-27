#!/usr/bin/env python3
"""render_fiveway_png.py -- PNG of a coprime k-way n = x^3 + y^3 in the style of out/a047697/a047697_5way_*.png:
one representation per line (sums first, then differences, each by increasing first term), n below.
Representations are recomputed from n (PARI factorisation + exact divisor count, mining/collisions.py) and checked
exactly before drawing.

Usage: python3 render_fiveway_png.py n [n ...] [--gp gp] [--out out/a047697]
"""
import argparse, sys
from pathlib import Path
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

sys.path.insert(0, str(Path(__file__).resolve().parent / "mining"))
from collisions import all_reps, factor_batch

def lines_for(reps):
    rows = []
    for x, y in reps:
        if x > 0 and y > 0:
            a, b = max(x, y), min(x, y); rows.append((0, a, f"{a}^{{3}} + {b}^{{3}}"))
        else:
            p, q = max(x, y), -min(x, y); rows.append((1, p, f"{p}^{{3}} - {q}^{{3}}"))
    rows.sort()
    return [r[2] for r in rows]

def render(n, reps, out):
    eqs = lines_for(reps)
    k = len(eqs)
    H = 0.54 * k + 1.0                                    # inches; k = 5 gives 7.2 x 3.7 in = 1440 x 740 px
    fig = plt.figure(figsize=(7.2, H), dpi=200)
    for i, e in enumerate(eqs):
        y = 1 - (0.45 + 0.54 * i) / H
        fig.text(0.5, y, ("$" if i == 0 else "$= ") + e + "$", ha="center", va="center", fontsize=20)
    fig.text(0.5, 0.35 / H, f"{n}", ha="center", va="center", fontsize=11)
    fig.patch.set_facecolor("white")
    fig.savefig(out, facecolor="white")
    plt.close(fig)

def main():
    ap = argparse.ArgumentParser(); ap.add_argument("n", nargs="+", type=int)
    ap.add_argument("--gp", default="gp"); ap.add_argument("--out", default="out/a047697")
    a = ap.parse_args()
    Path(a.out).mkdir(parents=True, exist_ok=True)
    for n, fac in zip(a.n, factor_batch(a.n, a.gp)):
        reps = sorted(all_reps(n, fac))
        assert all(x**3 + y**3 == n for x, y in reps), n
        out = Path(a.out) / f"a047697_{len(reps)}way_{n}.png"
        render(n, reps, out)
        print(f"{out}  ({len(reps)} representations)")

if __name__ == "__main__":
    main()
