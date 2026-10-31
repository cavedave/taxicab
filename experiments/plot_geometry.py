#!/usr/bin/env python3
"""plot_geometry.py -- paper figure: a bowtie and a hub on the curve x^3 + y^3 = n, drawn in the coordinates
(x, y) / n^(1/3), so every curve is x^3 + y^3 = 1. Examples from results/a047697_catalogue.txt, chosen for compact
and well-separated points: the five-way 36254160765497504708872903 (two lines through a shared point) and the
four-way 215896025011258968012 (two chords meeting at a point of denominator 2). Tufte style, white background, no title.
Writes writeup/paper/figs/fig_geometry.pdf and out/paper/fig_geometry.png (figures are not committed)."""
import os
from fractions import Fraction as F
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

BG, TEXT, TEXT2, AXIS, CURVE, ACCENT = "#ffffff", "#111111", "#666666", "#cccccc", "#999999", "#e41a1c"
BOWTIE, HUB = 36254160765497504708872903, 215896025011258968012

cat = {}
for l in open("results/a047697_catalogue.txt"):
    if l[0].isdigit():
        n, k, r = l.strip().split(";"); cat[int(n)] = [tuple(map(int, p.split(":"))) for p in r.split(",")]

def third(P, Q):
    """third intersection of the chord PQ with x^3 + y^3 = n (Werebrusow-Desboves)"""
    (x, y), (x1, y1) = P, Q; d = x * y - x1 * y1
    return None if d == 0 else (F(x1 * x1 * y - x * x * y1, d), F(x * y1 * y1 - x1 * y * y, d))

def integer_lines(reps):
    pts = sorted({p for x, y in reps for p in ((x, y), (y, x))}); out, seen = [], set()
    for i in range(len(pts)):
        for j in range(i + 1, len(pts)):
            R = third(pts[i], pts[j])
            if R and R[0].denominator == 1 and R[1].denominator == 1 and (int(R[0]), int(R[1])) in pts:
                L = frozenset([pts[i], pts[j], (int(R[0]), int(R[1]))])
                if L not in seen and frozenset((y, x) for x, y in L) not in seen:
                    seen.add(L); out.append(sorted(L))
    return out

def hub(reps):
    for i, j, k, l in ((0, 1, 2, 3), (0, 2, 1, 3), (0, 3, 1, 2)):
        for A in (reps[i], reps[i][::-1]):
            for B in (reps[j], reps[j][::-1]):
                R = third(A, B)
                if R is None or R[0].denominator == 1: continue
                for C in (reps[k], reps[k][::-1]):
                    for D in (reps[l], reps[l][::-1]):
                        if third(C, D) == R: return A, B, C, D, R

plt.rcParams.update({"font.family": "serif", "font.serif": ["Palatino", "Book Antiqua", "Georgia", "DejaVu Serif"],
                     "mathtext.fontset": "stix", "axes.edgecolor": AXIS, "xtick.color": TEXT2, "ytick.color": TEXT2,
                     "text.color": TEXT})
fig, axes = plt.subplots(1, 2, figsize=(9, 6.9), dpi=100, sharey=True)
fig.patch.set_facecolor(BG)
LIM = 2.7
xs = np.linspace(-LIM, LIM, 2001); ys = np.cbrt(1 - xs**3)

def frame(ax, n, label):
    ax.set_facecolor(BG)
    ax.plot(xs, ys, color=CURVE, lw=1.3, zorder=1)
    ax.plot([-LIM, LIM], [LIM, -LIM], ls=(0, (2, 3)), lw=0.7, color=AXIS, zorder=0)      # asymptote x + y = 0
    for s in ("top", "right"): ax.spines[s].set_visible(False)
    ax.set_xlim(-LIM, LIM); ax.set_ylim(-LIM, LIM); ax.set_aspect("equal")
    ax.spines["bottom"].set_bounds(-2, 2); ax.spines["left"].set_bounds(-2, 2)
    ax.set_xticks([-2, -1, 0, 1, 2]); ax.set_yticks([-2, -1, 0, 1, 2]); ax.tick_params(length=3, labelsize=10)
    ax.set_xlabel("$x / n^{1/3}$", fontsize=11, color=TEXT2)
    ax.text(LIM * 0.98, LIM * 0.98, label, fontsize=11.5, va="top", ha="right")
    ax.text(1.35, -1.25, "$x^3 + y^3 = n$", fontsize=10.5, color=TEXT2, rotation=-62)
    c = n ** (1 / 3)
    for x, y in cat[n]:                                 # every point: each representation and its swap
        for p in ((x, y), (y, x)):
            ax.plot(p[0] / c, p[1] / c, "o", ms=3.2, color=CURVE, zorder=2)
    return c

def num(v):
    return f"{v:,}".replace("-", "\u2212")

def line_eq(P, Q):
    """a x + b y = c through two integer points, gcd(a, b) = 1, a > 0"""
    from math import gcd
    a, b = Q[1] - P[1], P[0] - Q[0]; g = gcd(a, b); a, b = a // g, b // g
    if a < 0 or (a == 0 and b < 0): a, b = -a, -b
    return a, b, a * P[0] + b * P[1]

BLOCKS = []
def legend_block(ax, lines):
    BLOCKS.append((ax, lines))                                    # drawn under the panel once the layout is fixed

def tag(ax, P, c, name, dx=6, dy=6, color=TEXT):
    ax.annotate(name, xy=(P[0] / c, P[1] / c), xytext=(dx, dy), textcoords="offset points", fontsize=10, color=color)

def segment(ax, pts, c, color=TEXT2):
    P = np.array([[float(x) / c, float(y) / c] for x, y in pts])
    i, j = np.argmin(P[:, 0]), np.argmax(P[:, 0])
    d = P[j] - P[i]; e = 0.08 * d
    ax.plot([P[i, 0] - e[0], P[j, 0] + e[0]], [P[i, 1] - e[1], P[j, 1] + e[1]], color=color, lw=0.9, zorder=1.5)

# (a) bowtie: two lines with three integer points each, sharing one point
ax = axes[0]; c = frame(ax, BOWTIE, "(a) a bowtie: five representations")
L1, L2 = integer_lines(cat[BOWTIE])[:2]
for L in (L1, L2):
    segment(ax, L, c)
    for x, y in L: ax.plot(x / c, y / c, "o", ms=4.5, color=TEXT, zorder=3)
shared = (set(L1) & set(L2)).pop()
ax.plot(shared[0] / c, shared[1] / c, "o", ms=6, color=ACCENT, zorder=4)
pts = sorted(set(L1) | set(L2))                                   # P1..P5 from left to right
names = {P: f"$P_{i}$" for i, P in enumerate(pts, 1)}
for P in pts:
    tag(ax, P, c, names[P], *((-16, 6) if P == shared else (4, 6)), color=ACCENT if P == shared else TEXT)
e1, e2 = line_eq(*L1[:2]), line_eq(*L2[:2])
legend_block(ax, [f"$n$ = {num(BOWTIE)}"] +
             [f"{names[P]} = ({num(P[0])}, {num(P[1])})" for P in pts] +
             [f"lines: {e1[0]:,}$x$ + {e1[1]:,}$y$ = {num(e1[2])}", f"           {e2[0]:,}$x$ + {e2[1]:,}$y$ = {num(e2[2])}",
              f"{names[shared]} is on both lines"])
ax.set_ylabel("$y / n^{1/3}$", fontsize=11, color=TEXT2)

# (b) hub: two chords through integer points meeting at the same non-integral point R
ax = axes[1]; c = frame(ax, HUB, "(b) a hub: four representations")
A, B, C, D, R = hub(cat[HUB])
for P, Q in ((A, B), (C, D)):
    segment(ax, [P, Q, R], c)
    for x, y in (P, Q): ax.plot(x / c, y / c, "o", ms=4.5, color=TEXT, zorder=3)
ax.plot(float(R[0]) / c, float(R[1]) / c, "o", ms=6.5, mfc=BG, mec=ACCENT, mew=1.4, zorder=4)
ax.annotate("$R$", xy=(float(R[0]) / c, float(R[1]) / c), xytext=(-12, -12),
            textcoords="offset points", fontsize=10, color=ACCENT)
for P, name, off in ((A, "$P_1$", (4, 6)), (B, "$P_2$", (4, 6)), (C, "$P_3$", (5, -2)), (D, "$P_4$", (6, 2))):
    tag(ax, P, c, name, *off)
D_ = R[0].denominator
legend_block(ax, [f"$n$ = {num(HUB)}",
                  f"$P_1$ = ({num(A[0])}, {num(A[1])})", f"$P_2$ = ({num(B[0])}, {num(B[1])})",
                  f"$P_3$ = ({num(C[0])}, {num(C[1])})", f"$P_4$ = ({num(D[0])}, {num(D[1])})",
                  f"$R$ = ({num(R[0].numerator)}/{D_}, {num(R[1].numerator)}/{D_})",
                  "chords $P_1P_2$ and $P_3P_4$ both pass through $R$:", "$P_1 + P_2 = P_3 + P_4$"])

fig.subplots_adjust(left=0.08, right=0.98, bottom=0.37, top=0.98, wspace=0.12)
for ax, lines in BLOCKS:
    fig.text(ax.get_position().x0 + 0.01, 0.275, "\n".join(lines), fontsize=8.6, color=TEXT2, va="top", linespacing=1.5)
os.makedirs("writeup/paper/figs", exist_ok=True); os.makedirs("out/paper", exist_ok=True)
fig.savefig("writeup/paper/figs/fig_geometry.pdf", facecolor=BG)
fig.savefig("out/paper/fig_geometry.png", facecolor=BG)
print("bowtie lines:", L1, L2, "\nhub:", A, B, C, D, "R =", R)
