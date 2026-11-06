#!/usr/bin/env python3
"""Render the Ta(23)..Ta(28) upper bounds (results/taxicab_23_28_bounds.txt) as PNGs.

One image per k: all k representations x^3 + y^3 stacked and joined by "=", digits aligned in a
monospaced font, and the full n underneath (wrapped). Every identity is checked exactly before
anything is drawn.

Usage:  python3 render_taxicab_bounds_png.py [--src results/taxicab_23_28_bounds.txt] [--outdir out/taxicab_bounds]
"""
from __future__ import annotations

import argparse
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parent.parent


def read(path: Path):
    for line in path.read_text().splitlines():
        if not line or line.startswith("#"):
            continue
        k, n, L, ps = line.split(";")
        pairs = sorted(tuple(map(int, p.split(":"))) for p in ps.split(","))
        yield int(k), int(n), int(L), pairs


def render(k: int, n: int, pairs: list[tuple[int, int]], out: Path, dpi: int) -> None:
    for x, y in pairs:
        if x**3 + y**3 != n or not 0 < x < y:
            raise ValueError(f"bad pair {x}, {y} for k={k}")
    if len(set(pairs)) < k:
        raise ValueError("fewer than k distinct pairs")
    wx = max(len(str(x)) for x, _ in pairs); wy = max(len(str(y)) for _, y in pairs)
    lines = [f"{'  ' if i == 0 else '= '}{x:>{wx}}³ + {y:>{wy}}³" for i, (x, y) in enumerate(pairs)]
    width = len(lines[0])
    digits = str(n)
    nw = width - 4                                          # room for the "n = " prefix
    nlines = [digits[i:i + nw].ljust(nw) for i in range(0, len(digits), nw)]   # padded: centred lines align
    title = f"Smallest Known Taxicab {k} number"
    subtitle = f"Number that can be formed {k} ways from the sum of 2 cubes"
    total = len(lines) + len(nlines) + 5
    fig = plt.figure(figsize=(width * 0.085 + 0.6, total * 0.26 + 0.4))
    ax = fig.add_axes([0, 0, 1, 1]); ax.axis("off")
    step = 1.0 / (total + 1)
    y = 1 - step
    ax.text(0.5, y, title, ha="center", va="center", fontsize=20, fontweight="bold", family="DejaVu Sans")
    y -= 1.3 * step
    ax.text(0.5, y, subtitle, ha="center", va="center", fontsize=13, family="DejaVu Sans", color="0.3")
    y -= 1.7 * step
    for line in lines:
        ax.text(0.5, y, line, ha="center", va="center", fontsize=10, family="DejaVu Sans Mono"); y -= step
    y -= 0.5 * step
    for i, chunk in enumerate(nlines):
        ax.text(0.5, y, ("n = " if i == 0 else "    ") + chunk, ha="center", va="center", fontsize=10,
                family="DejaVu Sans Mono", color="0.25"); y -= step
    fig.savefig(out, dpi=dpi, facecolor="white")
    plt.close(fig)


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--src", type=Path, default=ROOT / "results" / "taxicab_23_28_bounds.txt")
    ap.add_argument("--outdir", type=Path, default=ROOT / "out" / "taxicab_bounds")
    ap.add_argument("--dpi", type=int, default=150)
    a = ap.parse_args()
    a.outdir.mkdir(parents=True, exist_ok=True)
    for k, n, L, pairs in read(a.src):
        out = a.outdir / f"ta{k}_upper_bound.png"
        render(k, n, pairs, out, a.dpi)
        print(out)


if __name__ == "__main__":
    main()
