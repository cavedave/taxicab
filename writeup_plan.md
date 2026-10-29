# Write-up plan: "An attempt to find a coprime six-way sum of two cubes" (A047697(6))

*Plan of 28 October 2026, for the weekend write-up. Sources are named per section, so each can be drafted from the
repo alone.*

## Working title and claim

**"Searching for the smallest number that is a sum of two coprime cubes in six ways"**, with the subtitle "an
exhaustive bound, 72 coprime five-ways, and what their geometry says".

**Claims, each reproducible from the repo:**
1. A047697(6) > 2.5·10²³ (exhaustive GPU search, validated).
2. Corollary: A080642(5) > 2.5·10²³ (cubefree taxicab), replacing the earlier bound of 10²³, which rested on an
   unpublished list.
3. 72 coprime five-ways are known, most of them new (to be counted against the literature: Bernstein, Butler and Boyer list positive or primitive ones), the largest 3.1·10³⁵. Plus 6,785 coprime four-ways, complete
   for n ≤ 10²² and 10²³–2.5·10²³.
4. The structure of multi-ways: every relation among the integral points is a ±1 line or hub. Multi-ways arise by
   structure or by rank. No line carries three positive points (convexity). Each claim is backed by data and,
   where possible, a proof.
5. A negative result: no six-way so far. Here is what was searched, and what that implies.

## Drafts

- `writeup/01_gpu_search.md`: the exhaustive GPU search (§2 of the outline), draft of 29 October 2026.
- `writeup/02_curve_search.md`: the curve geometry and targeted line/hub search (§3, §4, §6, §7), draft of 29 October 2026.

## Outline

| § | content | sources |
| --- | --- | --- |
| 1 | **The problem.** A047697 and its relatives: A047696 (cabtaxi), A011541 (taxicab), A080642 (cubefree taxicab). Why coprimality makes it hard, since there is no scaling. Known terms; Bernstein's a(5) (1999). | OEIS pages; `cubefree.txt`; refs/INDEX.md |
| 2 | **Exhaustive search.** The GPU method: segments in n^(2/3), 64-bit offsets, radix sort, host verification. The runs 10¹⁹–2.5·10²³, costs, validation (self-tests, the 10¹⁵ benchmark, independent recounts). Result: a(6) > 2.5·10²³. | `results/a047697_search.md`; `experiments/cabtaxi_gpu.cu`; `a047697/` |
| 3 | **Geometry.** x³ + y³ = n as an elliptic curve with a flex at infinity: collinear means P + Q + R = 0, and −P is the swap. Lines, bowties, hubs (two chords meeting at a point R of small denominator, which is a bowtie on D³n), D-lines, stars. Theorems: allowed directions (F10), Theorem 7 (D divides (b − a)E), convexity (no three positive points on a line). | `experiments/mining/THEOREMS.md`; FINDINGS F10, F28–F31, F33; `cubefree.md` §3 |
| 4 | **Targeted search.** Line enumeration via the conic parametrisation; D-lines; the split-prime filter; exact counting of every candidate; costs (the integer rewrite, about 10×). Breadth against depth (F32); the direction-list gap found on 28 October. | FINDINGS F12–F14, F25, F27, F32, F34; `line_enum.py`, `dline_enum.py`, `count_all.py` |
| 5 | **Results.** The 72 five-ways (table: n, factorisation, representations, shape, how found). Their profile: 7 \| n, split primes 8–14, mod-9 classes, off-profile cases. Four-way counts per decade. Recall of the targeted search against exhaustive data, by size. | `results/a047697_catalogue.txt`; FINDINGS F34; images in `out/a047697/` |
| 6 | **Structure.** Relations (F33): only ±1 lines and hubs. Two mechanisms: structure (points spanning rank 3) against rank (independent four-ways on rank-6–8 curves). All-positive multi-ways are hubs or independent. | FINDINGS F33; `curve_relations/`; `cubefree.md` §4 |
| 7 | **Six-way outlook.** The shapes that could give a six-way (3-D-line star, bowtie + D-line, triangle, rank route). Ratios: five-ways per four-way, 1 : 200 exhaustive, 1 : 64 in line search. What a search for a(6) would need. | FINDINGS F29–F31, F33, F34; the weekend's results |
| 8 | **Negative results.** Divisor-richness alone (N3); polynomial families (N4); shared coefficients (N2); multi-way curves for Ta/Ca bounds (N5). | FINDINGS, Negative results |
| A | **Data and code availability.** GitHub repository, catalogue format, how to reproduce each claim. | README |

## Companion results: Ta(k) and Ca(k) upper bounds (notes, 29 October 2026)

Against Boyer–Wroblewski's `TaxibigUpdated.txt` (April 2008; Ta(13)–Ta(22), Ca(23)–Ca(42)) and Su (JIS 19, 2016):

| range | result | source |
| --- | --- | --- |
| Ta(11)–Ta(22) | reproduced exactly as the optimum on the record curve M = 3956875867; **not beaten** (heights 80 and 110) | `results/taxicab_23_28.md` |
| **Ta(23), Ta(24)** | **3.6× and 25× below Su 2016** | `results/taxicab_23_28.md` |
| Ta(25)–Ta(30) | **new** (nothing published found) | `results/taxicab_23_28_bounds.txt`, `taxicab_29_30_bounds.txt` |
| Ca(10)–Ca(44) except 33, 34 | reproduced exactly on the records' own curves; not beaten | `results/cabtaxi_bounds.md` |
| **Ca(33), Ca(34)** | **1.9× and 568× below Boyer–Wroblewski 2008** (the two entries of `TaxibigUpdated.txt` we beat) | `results/cabtaxi_bounds.md` |
| **Ca(45)–Ca(57)** | **12.7× to 3·10¹⁹× below Su 2016** | `results/cabtaxi_bounds.md` |
| Ca(58)–Ca(70) | **new** | `results/cabtaxi_bounds.txt` |

- **Method in one line:** on the record curve x³ + y³ = M, an exact integer program picks the k rational points
  (canonical height ≤ 80) whose denominators have the smallest lcm L; n = M·L³. Boyer–Wroblewski's and Su's records
  are re-found exactly, which validates it; gains come where earlier bounds were built by extending a smaller one
  one cube at a time.
- **Negative result to report with it (FINDINGS N5):** our coprime multi-way curves do not help Ta/Ca bounds;
  small generator heights matter, not rank or n.
- **Can Ta(k ≤ 30) be improved? (checked 29 October 2026)** Not on the known curves: the optimiser is exact for a
  given curve and point set, height 110 changes nothing on the record curve, and the rank-7 Ta(6)–Ta(10) record
  curve 82652823799 is worse for every k from 11 to 30 (Ta(29): 2.8·10²⁸³ against our 2.2·10²⁶⁶). The 310,000-curve
  hunt (`experiments/curve_deep_plan.md`) found no better curve. Untried: curves outside that family (3–4 split
  primes, square factors, primes above 200, Elkies–Rogers high-rank curves).
- **Open before submitting:** the literature search stops at 2016 (Boyer's lists, MathWorld, OEIS A011541 and
  A047696, Su). Check later arXiv work and Boyer's newer pages; then OEIS comments for A011541 and A047696.
- **Venue question:** one paper (bounds + the coprime six-way attempt, sharing the curve geometry) or two short
  notes (bounds: JIS-style, like Boyer and Su; six-way attempt: arXiv note + OEIS b-files).

## Figures and tables
1. Five-ways found per decade, exhaustive against targeted.
2. A bowtie and a hub drawn on the curve, in the (s, v) plane (`render_*` scripts as a starting point).
3. Yield per direction against rank (F32, F34) and against height.
4. Recall by size (F34 table).
5. Table of all 72 five-ways (appendix, generated from the catalogue).

## Checks before publishing
- Re-verify every five-way from the catalogue alone with exact arithmetic (a script that shares no code with the
  search).
- Cross-check the A080642(5) bound against the OEIS entry and its references.
- Confirm Bernstein (1999), Butler's pages and Boyer (2008) citations; list Choudhry and the elliptic-curve
  references (Silverman–Tate; Green–Tao; Burr–Grünbaum–Sloane; Stroeker–Tzanakis).
- Decide the venue: an arXiv note, a JIS article (as Boyer and Su), or OEIS comments plus a b-file.

## Still to produce before the weekend
- The night runs of 28–29 and 29–30 October, and the weekend run. Fold them into §5 and §7.
- The exhaustive four-ways for 10²²–10²³ (GPU, in progress), to make the four-way list complete to 2.5·10²³.
- A one-page summary of the 72 (or more) five-ways for the appendix.
