#!/usr/bin/env python3
"""Render coprime cabtaxi identities (A047697 five-ways) as PNGs, in the style of
render_equation_png.py: matplotlib mathtext, white background, the full n underneath.

Each number gets one image: its representations stacked one per line, joined by "=",
sums first, then differences written as x^3 - y^3. Every identity and gcd is checked
exactly before anything is drawn.

Usage:  python3 render_cabtaxi_png.py                    # the five known coprime five-ways
        python3 render_cabtaxi_png.py --from a047697/cab_1e19_1e20.txt   # every line of a result file
"""
from __future__ import annotations

import argparse
from math import gcd
from pathlib import Path

import matplotlib.pyplot as plt

KNOWN = {  # n -> (x, y) with n = x^3 + y^3, gcd(x, y) = 1; y < 0 means a difference
    506433677359393: [(28065, 78532), (36489, 77074), (80025, -18218), (95866, -72087), (139264, -129951)],
    137904678696613339: [(310998, 475963), (369286, 444027), (516931, -61128), (539755, -268446),
                         (1365216, -1340093)],
    39673716067958900347: [(418491, 3408526), (1202338, 3360075), (3526755, -1612412), (3819196, -2521629),
                           (14705344, -14643933)],
    95793117931950826933: [(5029461, -3155822), (5073261, -3264272), (5625154, -4348011),
                           (23578300, -23520723), (26192350, -26145723)],
    118371660133721558473: [(752526, 4904113), (1138980, 4889497), (2936497, 4531470), (5004913, -1912674),
                            (5682073, -4022364)],
}
SOURCE = {506433677359393: "Bernstein 1999", 137904678696613339: "Bernstein 1999"}


def term(x: int, y: int) -> str:
    return rf"{x}^{{3}} + {y}^{{3}}" if y > 0 else rf"{x}^{{3}} - {-y}^{{3}}"


def render(n: int, pairs: list[tuple[int, int]], out: Path, dpi: int = 200, note: str | None = None) -> None:
    for x, y in pairs:
        if x**3 + y**3 != n:
            raise ValueError(f"{x}^3 + ({y})^3 != {n}")
        if gcd(abs(x), abs(y)) != 1:
            raise ValueError(f"gcd({x}, {y}) != 1")
    if len(set(pairs)) != len(pairs):
        raise ValueError("duplicate representation")
    pairs = sorted(pairs, key=lambda p: (p[1] < 0, p[0]))       # sums first, then differences
    lines = [rf"${term(*pairs[0])}$"] + [rf"$= {term(x, y)}$" for x, y in pairs[1:]]
    widest = max(len(term(x, y)) for x, y in pairs)
    fig_h = 0.62 * len(lines) + 1.4
    fig, ax = plt.subplots(figsize=(max(9.0, widest * 0.19), fig_h))
    ax.axis("off")
    top, step = 0.93, 0.78 / len(lines)
    for i, line in enumerate(lines):
        ax.text(0.5, top - i * step, line, ha="center", va="top", fontsize=20)
    caption = rf"${n}$"
    ax.text(0.5, 0.06, caption, ha="center", va="center", fontsize=11)
    if note:
        ax.text(0.5, -0.06, note, ha="center", va="center", fontsize=9, color="0.4")
    fig.savefig(out, dpi=dpi, bbox_inches="tight", facecolor="white")
    plt.close(fig)


def read_results(path: Path) -> dict[int, list[tuple[int, int]]]:
    found = {}
    for line in path.read_text().splitlines():
        if not line or line.startswith("#"):
            continue
        n, _k, ps = line.split(";")
        found[int(n)] = [tuple(map(int, p.split(":"))) for p in ps.split(",")]
    return found


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--from", dest="src", type=Path, help="cabtaxi result file (n;k;x:y,...)")
    ap.add_argument("--outdir", type=Path, default=Path(__file__).resolve().parent.parent / "out" / "a047697")
    ap.add_argument("--dpi", type=int, default=200)
    args = ap.parse_args()
    data = read_results(args.src) if args.src else KNOWN
    args.outdir.mkdir(parents=True, exist_ok=True)
    for n, pairs in sorted(data.items()):
        out = args.outdir / f"a047697_{len(pairs)}way_{n}.png"
        render(n, pairs, out, dpi=args.dpi)
        print(out)


if __name__ == "__main__":
    main()
