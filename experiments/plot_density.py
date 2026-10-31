#!/usr/bin/env python3
"""plot_density.py -- Figure 2 of the paper: N_k(x) = #{n <= x : n = x^3 + y^3 with gcd(x, y) = 1 in >= k ways},
k = 2..5, from the exhaustive searches (k >= 2 to 1e13 and k >= 3 to 1e17 by cabtaxi.cpp, results/counts/;
k >= 4 to 1e22 and k >= 5 to 2.5e23 from the GPU-complete part of results/a047697_catalogue.txt). Tufte style.
Writes writeup/paper/figs/fig_density.pdf and out/paper/fig_density.png (figures are not committed)."""
import gzip, os
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

BG, TEXT, TEXT2, AXIS, ACCENT = "#fffff8", "#111111", "#666666", "#cccccc", "#e41a1c"
GRAYS = {2: "#b0b0b0", 3: "#888888", 4: "#555555", 5: ACCENT}

def values(path, k, B):
    f = gzip.open(path, "rt") if path.endswith(".gz") else open(path)
    v = [int(p[0]) for p in (l.strip().split(";") for l in f if l[0].isdigit()) if int(p[1]) >= k and int(p[0]) <= B]
    return np.array(sorted(v), dtype=float)

DATA = {2: values("results/counts/coprime_k2_1e13.txt.gz", 2, 1e13),
        3: values("results/counts/coprime_k3_1e17.txt.gz", 3, 1e17),
        4: values("results/a047697_catalogue.txt", 4, 1e22),
        5: values("results/a047697_catalogue.txt", 5, 2.5e23)}
FIRST = {2: "91", 3: "3367", 4: "16776487", 5: "506433677359393"}

plt.rcParams.update({"font.family": "serif", "font.serif": ["Palatino", "Book Antiqua", "Georgia", "DejaVu Serif"],
                     "mathtext.fontset": "stix", "axes.edgecolor": AXIS, "xtick.color": TEXT2, "ytick.color": TEXT2,
                     "text.color": TEXT})
fig, ax = plt.subplots(figsize=(9, 6), dpi=100)
fig.patch.set_facecolor(BG); ax.set_facecolor(BG)

for k, a in DATA.items():
    N = np.arange(1, len(a) + 1)
    ax.step(np.append(a, a[-1]), np.append(N, N[-1]), where="post", color=GRAYS[k], lw=1.7)
    m = len(a) // 4                                   # local growth exponent over the upper three quarters
    th = np.polyfit(np.log10(a[m:]), np.log10(N[m:]), 1)[0]
    ax.plot(a[0], 1, "o", ms=4, color=GRAYS[k])
    ax.annotate(FIRST[k], xy=(a[0], 1), xytext=(0, -14), textcoords="offset points", ha="center",
                fontsize=9, color=GRAYS[k] if k < 5 else ACCENT)
    ax.text(a[-1] * 1.6, len(a), f"$k \\geq {k}$: {len(a):,}\n" + f"slope {th:.2f}", fontsize=10.5,
            color=GRAYS[k] if k < 5 else ACCENT, va="center")

ax.axvline(2.5e23, ymin=0.02, ymax=0.25, color=ACCENT, lw=0.8, ls=":")
ax.text(2.5e23, 2.2, "no six-way\nbelow $2.5\\cdot10^{23}$", fontsize=10, color=ACCENT, ha="center")

ax.set_xscale("log"); ax.set_yscale("log")
for s in ("top", "right"): ax.spines[s].set_visible(False)
ax.spines["bottom"].set_bounds(DATA[2][0], 2.5e23); ax.spines["left"].set_bounds(1, len(DATA[2]))
ax.set_xlim(20, 1e26); ax.set_ylim(0.45, 6e5)
xt = [10.0**e for e in range(2, 25, 2)]
ax.set_xticks(xt); ax.set_xticklabels([f"$10^{{{e}}}$" for e in range(2, 25, 2)])
yt = [1, 10, 100, 1000, 10**4, 10**5]
ax.set_yticks(yt); ax.set_yticklabels(["1", "10", "100", "1,000", "10,000", "100,000"])
ax.minorticks_off(); ax.tick_params(length=3, labelsize=10.5)
ax.set_xlabel("$x$", fontsize=12, color=TEXT2)
ax.set_ylabel("numbers $n \\leq x$ with at least $k$ representations", fontsize=11, color=TEXT2)

fig.suptitle("Each extra representation makes coprime multi-ways far rarer", x=0.08, y=0.965, ha="left", fontsize=15)
ax.set_title("$n = x^3 + y^3$, $\\gcd(x, y) = 1$, signs allowed; exhaustive counts. The first point of each curve is "
             "A047697$(k)$", loc="left", fontsize=10.5, color=TEXT2, pad=14)
fig.subplots_adjust(left=0.1, right=0.86, bottom=0.11, top=0.86)
os.makedirs("writeup/paper/figs", exist_ok=True); os.makedirs("out/paper", exist_ok=True)
fig.savefig("writeup/paper/figs/fig_density.pdf", facecolor=BG)
fig.savefig("out/paper/fig_density.png", facecolor=BG)
print({k: len(a) for k, a in DATA.items()})
