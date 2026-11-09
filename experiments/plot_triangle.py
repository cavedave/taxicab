#!/usr/bin/env python3
"""plot_triangle.py -- figure: the smallest coprime four-way n = 16776487 as a rational triangle (FINDINGS F74, F75).
Its four representations are four of the six points of a triangle of three lines; the other two points are rational,
with denominators 37 and 5 -- the closest of all 21,947 'line + free point' four-ways to a triangle six-way.
Drawn in the coordinates (x, y) / n^(1/3) like plot_geometry.py: Tufte style, white background, no title (caption only).
Writes writeup/paper/figs/fig_triangle.pdf and out/paper/fig_triangle.png (figures are not committed)."""
import os
from fractions import Fraction as F
from math import gcd
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

BG, TEXT, TEXT2, AXIS, CURVE, ACCENT = "#ffffff", "#111111", "#666666", "#cccccc", "#999999", "#e41a1c"
N = 16776487

def third(P, Q):
    """third intersection of the chord PQ with x^3 + y^3 = n (Werebrusow-Desboves)"""
    (x, y), (x1, y1) = P, Q; d = x * y - x1 * y1
    return (F(x1 * x1 * y - x * x * y1, d), F(x * y1 * y1 - x1 * y * y, d))

def line_eq(P, Q):
    a, b = Q[1] - P[1], P[0] - Q[0]; g = gcd(int(a), int(b)) if all(F(v).denominator == 1 for v in (a, b)) else 1
    a, b = F(a) / g, F(b) / g
    if a < 0 or (a == 0 and b < 0): a, b = -a, -b
    return a, b, a * P[0] + b * P[1]

# the triangle (found by triangles/tri_decide.gp for the directions (3,4), (3,16), (9,4); triangles/tri_props.out)
A, B, C = (-9, 256), (255, 58), (183, 220)          # corners: three representations of N
D = third(A, C)                                      # side A C: the integer line, third point (-201, 292)
R1 = third(A, B)                                     # side A B: third point with denominator 37
R2 = third(B, C)                                     # side B C: third point with denominator 5
assert D == (F(-201), F(292)) and R1[0].denominator == 37 and R2[0].denominator == 5
for P in (A, B, C, D, R1, R2): assert P[0]**3 + P[1]**3 == N

plt.rcParams.update({"font.family": "serif", "font.serif": ["Palatino", "Book Antiqua", "Georgia", "DejaVu Serif"],
                     "mathtext.fontset": "stix", "axes.edgecolor": AXIS, "xtick.color": TEXT2, "ytick.color": TEXT2,
                     "text.color": TEXT})
fig, ax = plt.subplots(figsize=(6.6, 7.6), dpi=100)
fig.patch.set_facecolor(BG); ax.set_facecolor(BG)
c = N ** (1 / 3)
LIM = 4.3
xs = np.linspace(-LIM, LIM, 3001); ax.plot(xs, np.cbrt(1 - xs**3), color=CURVE, lw=1.3, zorder=1)
ax.plot([-LIM, LIM], [LIM, -LIM], ls=(0, (2, 3)), lw=0.7, color=AXIS, zorder=0)            # asymptote x + y = 0
for s in ("top", "right"): ax.spines[s].set_visible(False)
ax.set_xlim(-LIM, 2.6); ax.set_ylim(-2.4, LIM); ax.set_aspect("equal")
ax.spines["bottom"].set_bounds(-4, 2); ax.spines["left"].set_bounds(-2, 4)
ax.set_xticks([-4, -3, -2, -1, 0, 1, 2]); ax.set_yticks([-2, -1, 0, 1, 2, 3, 4]); ax.tick_params(length=3, labelsize=10)
ax.set_xlabel("$x / n^{1/3}$", fontsize=11, color=TEXT2); ax.set_ylabel("$y / n^{1/3}$", fontsize=11, color=TEXT2)
ax.text(1.75, -1.55, "$x^3 + y^3 = n$", fontsize=10.5, color=TEXT2, rotation=-58)

def seg(pts, lw=0.9, color=TEXT2, ls="-"):
    P = np.array([[float(x) / c, float(y) / c] for x, y in pts])
    i, j = np.argmin(P[:, 0]), np.argmax(P[:, 0]); d = P[j] - P[i]; e = 0.06 * d
    ax.plot([P[i, 0] - e[0], P[j, 0] + e[0]], [P[i, 1] - e[1], P[j, 1] + e[1]], color=color, lw=lw, ls=ls, zorder=1.5)

seg([A, C, D], lw=1.3, color=TEXT)                   # the integer line of the four-way
seg([A, B, R1]); seg([B, C, R2])                     # the two sides that close the triangle

for x, y in (A, B, C, D):                            # every point of the curve with integer coordinates: both orientations
    ax.plot(y / c, x / c, "o", ms=3.2, color=CURVE, zorder=2)
for P in (A, B, C, D): ax.plot(P[0] / c, P[1] / c, "o", ms=6, color=TEXT, zorder=3)
for P in (R1, R2): ax.plot(float(P[0]) / c, float(P[1]) / c, "o", ms=7.5, mfc=BG, mec=ACCENT, mew=1.6, zorder=4)

def num(v): return f"{v:,}".replace("-", "−")
def lab(P, s, dx, dy, color=TEXT):
    ax.annotate(s, xy=(float(P[0]) / c, float(P[1]) / c), xytext=(dx, dy), textcoords="offset points", fontsize=10, color=color)
lab(A, "$P_1$", -6, -17); lab(B, "$P_2$", 7, -3); lab(C, "$P_3$", 6, 4); lab(D, "$P_4$", -20, 4)
lab(R1, "$R_1$", 8, -4, ACCENT); lab(R2, "$R_2$", 8, -2, ACCENT)

e_line = line_eq(A, C); e1 = line_eq(A, B); e2 = line_eq(B, C)
lines = [f"$n$ = {num(N)}, the smallest number with four coprime representations",
         f"$P_1$ = ({num(A[0])}, {num(A[1])}),  $P_2$ = ({num(B[0])}, {num(B[1])}),  "
         f"$P_3$ = ({num(C[0])}, {num(C[1])}),  $P_4$ = ({num(int(D[0]))}, {num(int(D[1]))})",
         f"$R_1$ = ({num(R1[0].numerator)}/37, {num(R1[1].numerator)}/37),   "
         f"$R_2$ = ({num(R2[0].numerator)}/5, {num(R2[1].numerator)}/5)",
         f"lines:  $P_1P_3P_4$:  {e_line[0]}$x$ + {e_line[1]}$y$ = {num(e_line[2])}   (all integer)",
         f"           $P_1P_2R_1$:  {e1[0]}$x$ + {e1[1]}$y$ = {num(e1[2])},     $P_2P_3R_2$:  {e2[0]}$x$ + {e2[1]}$y$ = {num(e2[2])}",
         "four of the six points are integers; the triangle would be a six-way if $R_1$ and $R_2$ were too"]
fig.subplots_adjust(left=0.11, right=0.98, bottom=0.27, top=0.99)
fig.text(0.11, 0.185, "\n".join(lines), fontsize=8.4, color=TEXT2, va="top", linespacing=1.55)
os.makedirs("writeup/paper/figs", exist_ok=True); os.makedirs("out/paper", exist_ok=True)
fig.savefig("writeup/paper/figs/fig_triangle.pdf", facecolor=BG)
fig.savefig("out/paper/fig_triangle.png", facecolor=BG, dpi=150)
print("corners", A, B, C, "| integer third", D, "| R1", R1, "| R2", R2)
