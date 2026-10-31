#!/usr/bin/env python3
"""plot_a023050.py -- counting function of OEIS A023050 (sums of two coprime positive cubes in >= 3 ways), Tufte style.
Reads results/oeis/b023050_1e17.txt; writes out/oeis/a023050.png and .svg (not committed: no PNGs in git)."""
import os
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

BG, TEXT, TEXT2, AXIS, SERIES, ACCENT = "#fffff8", "#111111", "#666666", "#cccccc", "#666666", "#e41a1c"
OEIS_TERMS = 41                      # the b-file before 31 October 2026 (to 3.75e15)

a = np.array([int(l.split()[1]) for l in open("results/oeis/b023050_1e17.txt")], dtype=float)
n = np.arange(1, len(a) + 1)
theta, c = np.polyfit(np.log10(a[19:]), np.log10(n[19:]), 1)      # N(x) ~ 10^c x^theta, fitted on terms 20+

plt.rcParams.update({"font.family": "serif", "font.serif": ["Palatino", "Book Antiqua", "Georgia", "DejaVu Serif"],
                     "axes.edgecolor": AXIS, "mathtext.fontset": "stix", "xtick.color": TEXT2, "ytick.color": TEXT2, "text.color": TEXT})
fig, ax = plt.subplots(figsize=(9, 6), dpi=100)
fig.patch.set_facecolor(BG); ax.set_facecolor(BG)

# counting function N(x): steps, gray for the terms already in OEIS, accent for the new ones
ax.step(a[:OEIS_TERMS], n[:OEIS_TERMS], where="post", color=SERIES, lw=1.6)
ax.step(a[OEIS_TERMS - 1:], n[OEIS_TERMS - 1:], where="post", color=ACCENT, lw=1.6)
xs = np.logspace(np.log10(a[0]), 17, 50)
ax.plot(xs, 10**c * xs**theta, ls="--", lw=0.9, color=TEXT2)

ax.set_xscale("log"); ax.set_yscale("log")
for s in ("top", "right"): ax.spines[s].set_visible(False)
ax.spines["bottom"].set_bounds(a[0], 1e17); ax.spines["left"].set_bounds(1, n[-1])
ax.set_xlim(a[0] / 2, 3e17); ax.set_ylim(0.8, 160)
ax.set_xticks([1e10, 1e11, 1e12, 1e13, 1e14, 1e15, 1e16, 1e17])
ax.set_xticklabels(["10¹⁰", "10¹¹", "10¹²", "10¹³", "10¹⁴", "10¹⁵", "10¹⁶", "10¹⁷"])
ax.set_yticks([1, 3, 10, 30, 100]); ax.set_yticklabels(["1", "3", "10", "30", "100"])
ax.minorticks_off(); ax.tick_params(length=3, labelsize=11)
ax.set_xlabel("n", fontsize=12, color=TEXT2); ax.set_ylabel("terms ≤ n", fontsize=12, color=TEXT2)

# direct labels and annotations
ax.annotate("41 terms in OEIS\n(to 3.75·10¹⁵)", xy=(a[OEIS_TERMS - 1], OEIS_TERMS), xytext=(1.2e13, 70),
            fontsize=11, color=SERIES, arrowprops=dict(arrowstyle="-", color=AXIS, lw=0.8))
ax.text(1.15e17, n[-1], f"{n[-1]} terms\n(complete to 10¹⁷)", fontsize=11, color=ACCENT, va="center")
ax.annotate("15170835645, the smallest\ncubefree taxicab three-way", xy=(a[0], 1), xytext=(5e11, 1.3),
            fontsize=10, color=TEXT2, va="center", arrowprops=dict(arrowstyle="-", color=AXIS, lw=0.8))
ax.text(2e11, 10**c * 2e11**theta * 1.9, f"fit: $N(n) \\propto n^{{{theta:.2f}}}$", fontsize=10, color=TEXT2, rotation=0)

fig.suptitle("Three-way coprime cube sums: their count grows like $n^{%.2f}$" % theta,
             x=0.08, y=0.965, ha="left", fontsize=15)
ax.set_title("OEIS A023050: n = a³ + b³ in at least three ways with gcd(a, b) = 1 and a, b > 0",
             loc="left", fontsize=11, color=TEXT2, pad=14)
fig.subplots_adjust(left=0.08, right=0.83, bottom=0.11, top=0.86)
os.makedirs("out/oeis", exist_ok=True)
for ext in ("png", "svg"):
    fig.savefig(f"out/oeis/a023050.{ext}", facecolor=BG)
print(f"theta = {theta:.3f}; wrote out/oeis/a023050.png/.svg")
