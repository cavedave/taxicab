#!/usr/bin/env python3
"""plot_bowtie.py -- picture of one coprime five-way (a bowtie) on x^3 + y^3 = n, in coordinates (x, y) / n^(1/3):
the curve, its ten points (each representation and its swap, labelled a-j), the two lines and their mirror images,
the shared point, and the two hidden hubs (chord pairs meeting on the curve at R1, R2), with a coordinate table.
Usage: python3 experiments/plot_bowtie.py n [--lim 1.45]   -> out/a047697/bowtie_<n>.png (not committed)"""
import argparse, math, sys
from math import gcd
from fractions import Fraction as F
from itertools import combinations
from pathlib import Path
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

def main():
    ap = argparse.ArgumentParser(); ap.add_argument("n", type=int); ap.add_argument("--lim", type=float, default=1.45)
    A = ap.parse_args(); N = A.n; LIM = A.lim
    row = next((l for l in open("results/a047697_catalogue.txt") if l.startswith(str(N) + ";")), None)
    if row is None: sys.exit("n not in the catalogue")
    reps = [tuple(map(int, p.split(":"))) for p in row.strip().split(";")[2].split(",")]
    assert all(x**3 + y**3 == N for x, y in reps)
    c = N ** (1 / 3); pts = []
    for x, y in sorted(reps, key=lambda p: -(p[0] + p[1])): pts += [(x, y), (y, x)]
    lab = {p: ch for p, ch in zip(pts, "abcdefghijklmnop")}; sw = lambda p: (p[1], p[0])
    def third(P, Q):
        (x, y), (u, v) = P, Q; d = x * y - u * v
        return None if d == 0 else (F(u*u*y - x*x*v, d), F(x*v*v - u*y*y, d))
    lines = [T for T in combinations(pts, 3) if len({tuple(sorted(p)) for p in T}) == 3 and
             (T[1][0] - T[0][0]) * (T[2][1] - T[0][1]) == (T[1][1] - T[0][1]) * (T[2][0] - T[0][0])]
    def dirn(L):
        (x1, y1), (x2, y2) = L[0], L[1]; a, b = y2 - y1, x1 - x2; g = gcd(a, b); a, b = a // g, b // g
        return (-a, -b) if a < 0 else (a, b)
    pair = next(((X, Y) for X, Y in combinations(lines, 2) if set(X) & set(Y)), None)
    if pair is None: sys.exit("no two lines share a point (not a bowtie)")
    L1, L2 = pair; C = (set(L1) & set(L2)).pop()
    M1, M2 = tuple(sw(p) for p in L1), tuple(sw(p) for p in L2)
    P, Q = [p for p in L1 if p != C]; R, T = [p for p in L2 if p != C]
    hubs = [((P1, sw(B)), (Cc, sw(D)), third(P1, sw(B))) for P1, B, Cc, D in ((P, R, T, Q), (P, T, R, Q))]
    BG, TXT, GRAY, RED, BLUE, GREEN = "#ffffff", "#111111", "#888888", "#e41a1c", "#377eb8", "#4daf4a"
    plt.rcParams.update({"font.family": "serif", "font.serif": ["Palatino", "Georgia", "DejaVu Serif"], "mathtext.fontset": "stix"})
    fig = plt.figure(figsize=(10, 11.8), dpi=130); ax = fig.add_axes([0.08, 0.37, 0.86, 0.6]); fig.patch.set_facecolor(BG)
    xs = np.linspace(-LIM, LIM, 3001); ax.plot(xs, np.cbrt(1 - xs**3), color=GRAY, lw=1.3, zorder=1)
    ax.plot([-LIM, LIM], [LIM, -LIM], ls=(0, (2, 3)), color="#cccccc", lw=0.8); ax.plot([-LIM, LIM], [-LIM, LIM], ls=(0, (1, 4)), color="#dddddd", lw=0.8)
    def seg(Ls, color, lw, ls="-", ext=0.25):
        Pt = np.array([[p[0] / c, p[1] / c] for p in Ls]); i, j = np.argmin(Pt[:, 0]), np.argmax(Pt[:, 0]); d = Pt[j] - Pt[i]
        ax.plot([Pt[i, 0] - ext * d[0], Pt[j, 0] + ext * d[0]], [Pt[i, 1] - ext * d[1], Pt[j, 1] + ext * d[1]], color=color, lw=lw, ls=ls, zorder=2)
    seg(L1, RED, 1.7); seg(L2, BLUE, 1.7); seg(M1, RED, 1.0, (0, (4, 3))); seg(M2, BLUE, 1.0, (0, (4, 3)))
    for k, ((A1, B1), (C1, D1), X) in enumerate(hubs, 1):
        mx, my = float(X[0]) / c, float(X[1]) / c
        ax.plot([A1[0] / c, mx], [A1[1] / c, my], color="#bbbbbb", lw=0.8, ls=":"); ax.plot([C1[0] / c, mx], [C1[1] / c, my], color="#bbbbbb", lw=0.8, ls=":")
        ax.plot(mx, my, "o", ms=6.5, mfc=BG, mec=GRAY, mew=1.3, zorder=3)
        ax.annotate(f"$R_{k}$", (mx, my), xytext=(8, -12 if k == 1 else 2), textcoords="offset points", fontsize=11, color="#555555")
    for p in pts:
        sh = p in (C, sw(C))
        ax.plot(p[0] / c, p[1] / c, "o", ms=8.5 if sh else 5.5, color=GREEN if sh else TXT, zorder=4)
        ax.annotate(lab[p], (p[0] / c, p[1] / c), xytext=(6, 5), textcoords="offset points", fontsize=12, color=TXT)
    for s in ("top", "right"): ax.spines[s].set_visible(False)
    ax.set_xlim(-LIM, LIM); ax.set_ylim(-LIM, LIM); ax.set_aspect("equal")
    ax.set_xlabel("$x / n^{1/3}$", fontsize=12, color="#555555"); ax.set_ylabel("$y / n^{1/3}$", fontsize=12, color="#555555")
    nm = lambda L: ", ".join(sorted(lab[p] for p in L))
    def info(L):
        a, b = dirn(L); t = math.degrees(math.atan2(-a, b)); t = t if t > -90 else t + 180
        return a, b, a * L[0][0] + b * L[0][1], t, a*a + a*b + b*b
    a1, b1, c1, t1, E1 = info(L1); a2, b2, c2, t2, E2 = info(L2)
    txt = [f"$n$ = {N:,}: {len(reps)} coprime representations", ""]
    txt += [f"{lab[p]} = ({p[0]:,}, {p[1]:,})" + ("   shared point of the red and blue lines" if p == C else ("   its swap: shared point of the mirror lines" if p == sw(C) else "")) for p in pts]
    txt += ["", f"red line   ({nm(L1)}):  {a1}x + {b1}y = {c1:,},  angle {t1:.1f} deg,  E = {E1:,}",
            f"blue line  ({nm(L2)}):  {a2}x + {b2}y = {c2:,},  angle {t2:.1f} deg,  E = {E2:,}",
            f"dashed: their mirror images in y = x ({nm(M1)} and {nm(M2)}), a second bowtie meeting at {lab[sw(C)]}",
            "dotted: the two hidden hubs.  " + ";  ".join(f"$R_{k}$: chords {lab[h[0][0]]}{lab[h[0][1]]} and {lab[h[1][0]]}{lab[h[1][1]]}, denominator {h[2][0].denominator:,}" for k, h in enumerate(hubs, 1)),
            "grey dotted diagonals: the asymptote x + y = 0 and the symmetry line y = x"]
    fig.text(0.07, 0.32, "\n".join(txt), fontsize=8.6, va="top", color="#333333", linespacing=1.45)
    out = Path("out/a047697") / f"bowtie_{N}.png"; out.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(out, facecolor=BG); print(out)

if __name__ == "__main__":
    main()
