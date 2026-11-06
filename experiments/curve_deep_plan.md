# Plan: a deeper look at the top 100,000 split-prime curves

*Written 20 October 2026. The pilot results below were run on the Mac with PARI 2.x and SciPy (HiGHS);
nothing here has run on 7of9 yet.*

## Background

- **The sweep so far:** `run_split.sh` searched the top 310,000 of 394,383 curves x³ + y³ = M. Each M is a
  product of 5–8 primes ≡ 1 (mod 3) below 200, with M ≤ 10¹⁸, ranked by Mestre–Nagao score. These are batches
  split1–split1f.
- **Settings used:** height ≤ 80 (`--hmax`), denominators ≤ 10¹² (`--wmax`), beam width 10, effort-1
  `ellrank`, saturation to 1000.
- **Result:** every bound from Ta(6) to Ta(22) equals the published Boyer–Wroblewski value; none was beaten.
- **The record curves:**
  - 82652823799 = 7·13·19·43·73·97·157 (rank 7): Ta(6)–Ta(10)
  - 3956875867 = 7·31·37·43·73·157 (rank 6): Ta(11)–Ta(22)

## Pilot findings (20 October 2026)

Tools: `curve_ilp.py` (an exact integer program for the smallest L divisible by at least k point
denominators), `curve_factor_pts.py` (PARI factorisation of the denominators) and `curve_compare.py` (beam
search against the exact optimum for one curve).

1. **The published records are provably optimal on their own curves**, given all points of height ≤ 80.
   - The exact optimiser reproduces every published bound from Ta(6) to Ta(22) as the true minimum, in under
     5 s per k.
   - The records use exactly k points, all with denominators below 10¹⁰.
   - So no amount of searching *on these two curves* can beat them. Beating them needs other curves.
2. **On the curves tested, beam width 10 already finds the optimum.**
   - On curve 116776387 (rank 6), the beam result equals the exact optimum for every k from 6 to 21.
   - The beam only fails where the 10¹² cap leaves too few points (k = 22 there).
   - Widening the beam would therefore change little. The cap on denominators, not the width, is what limits
     the search.
3. **The 10¹² denominator cap discards about 98% of the points.** For example:

   | curve | points with height ≤ 80 | points kept under the cap |
   | --- | ---: | ---: |
   | 3956875867 | 3,381 | 80 |
   | 82652823799 | 8,176 | 124 |

   This did not matter for the records, but it hides high-k solutions on other curves.
4. **A high Nagao score does not mean good bounds.** Three curves from the score top 10 (116776387,
   89359770409, 452993703751) have ranks 6–7, yet their best bounds are 10¹¹ to 10⁹⁰ times *worse* than
   published.
   - What makes the record curves special is many points whose denominators are **smooth over small primes**
     (2, 3, 5, 7, 13, … up to a few thousand), so that their lcm stays small.
   - Rank is necessary but far from sufficient.
5. **New bounds beyond Ta(22).** On 3956875867 the optimiser gives exactly verified bounds for k = 23 … 28:

   | k | bound |
   | --- | --- |
   | 23 | 1.419 × 10¹⁷³ |
   | 24 | 1.533 × 10¹⁸⁷ |
   | 25 | 1.157 × 10²⁰² |
   | 26 | 2.371 × 10²¹⁷ |
   | 27 | 2.598 × 10²³³ |
   | 28 | 5.738 × 10²⁴⁹ |

   (Correction, 25 October: the bounds continue to Ta(29), Ta(30), Ta(31), … at height ≤ 80; the earlier "none for k ≥ 29" came from a search cap of 10²⁶⁰.) **Whether any Ta(23+) upper bounds are published has not been
   checked** (Su 2014–16? MathWorld? OEIS A011541?). Do that before claiming anything.

## Findings from `split_summary.csv` (all 310,000 hunted curves, 20 October 2026), which REVISE the plan below

- **Few curves produce anything.** Only **1,864** of about 310,000 curves gave any six-way below 10¹⁶⁵ (under
  the old 10¹² cap).
- **The Nagao score is a strong coarse filter**, even though it does not pick the record curves out of its top
  10. Share of curves giving a six-way, by score rank:

  | score rank | share giving a six-way |
  | --- | ---: |
  | 1–1,000 | 40% |
  | 1,001–10,000 | 8.5% |
  | 10,001–50,000 | 1.3% |
  | 50,001–100,000 | 0.23% |
  | 100,001–200,000 | 0.04% |
  | 200,001 and below | 0.005% |

  **The last 84,000 curves are therefore not worth running**, which reverses Q3 step 5. If `split1g` is
  already running, let it finish; it is harmless.
- **Only three curves come within 10⁶ of any record:** the two record curves and **564185788777**
  (= 13·19·43·61·73·79·151, rank 6):

  | k | ratio to published |
  | --- | ---: |
  | 6 | 36× (Ta(6) is exact, so it cannot be beaten) |
  | 7 | 1.7 × 10³ |
  | 8 | 6.3 × 10⁵ |

  Next is 4058099857 at 1.7 × 10⁶ (k = 6). Everything else is 10⁹ or more.
- **Beam search equals the exact optimum** on both of those curves for every k (`curve_compare.py`). Neither
  has a bounded rank.
- **Prime enrichment is a size effect, not a special core.**
  - Smaller primes are smoothly over-represented: 7 at ×1.73, falling steadily to 199 at ×0.51.
  - Fewer primes do better: 1.38% of 5-prime curves give a six-way, against 0.26% of 8-prime curves.
  - 43, 73 and 157 show no special signal. A smaller M simply gives a smaller n = M·L³.

**Revised conclusion.** The existing hunt was already essentially optimal for the split-prime set:
- the records are optimal on their own curves;
- the beam matched the ILP on every curve tested;
- no other curve comes close.

**A careful rerun of the top 100,000 is low value.** The remaining opportunities are:
1. **Ta(23)–Ta(28):** do the literature check (finding 5). This is the only potential new result in hand.
2. **Smaller curves outside the current set:**
   - products of 3–4 primes ≡ 1 (mod 3) (`split_curves.py --rmin 3 --rmax 4`), which is cheap;
   - small squared factors (7², 13², 19²);
   - primes 200–400 only in short products.
   Rank them by score, hunt the top few thousand with no denominator cap, and check the best with the ILP.
3. **The same summary for the seed-based hunt (`hunt18.csv`),** to see whether a different curve family
   behaves differently.
4. **Rank-bounded curves:** check only the curves among the 1,864 productive ones, logging `M` with the
   warning. Expect nothing to change.

The sections below are kept for reference; where they conflict, this section wins.

## Q1: how wide and deep

| setting | before | new | why |
| --- | --- | --- | --- |
| height bound `hmax` | 80 | 80 (try 100 on near misses) | height 80 already reaches denominators of about 10⁴⁸; the records use ≤ 10¹⁰ |
| denominator cap `wmax` | 10¹² | **none (10⁶⁰)** | the cap, not the width, was the binding limit |
| subset search | beam width 10 | beam for screening, **exact ILP** for every curve within 10⁶ × a record at any k | ILP gives a proven optimum, in seconds |
| k range | 6–22 | **6–30** | for k > 22, see finding 5 |
| `qfminim` vector cap | 500,000 (silent truncation) | log `#VECTORS` and flag hitting the cap | rank-8+ curves could silently lose points |

**Cost:** about the same as the original batches, roughly 2–3 s of CPU per curve, or about 3.5 h for 100,000
curves on 7of9's 64 threads. The ILP adds seconds per selected curve.

## Q2: rank only bounded

- **The problem:** about 3% of curves printed `rank only bounded: lo ≤ r ≤ hi`, but the logs **do not say
  which curve**, so the affected curves must be recomputed.
- **Instrumentation (do first):** `curve_hunt.py` writes `<out>.meta`, one line per curve:
  `M;rank_lo;rank_hi;generators;vectors;vector_cap_hit;points;seconds`.
- **For each bounded curve in the top 100,000:**
  1. **Root number.** Run `ellrootno(E)`, which gives the parity of the rank (assuming the parity conjecture).
     If `rank_lo` has the wrong parity, at least one generator is missing.
  2. **Rerun `ellrank` with more effort** (effort 3, then 5), passing the points already known.
  3. **Search for points directly** with `ellratpoints` on the curve at a moderate height bound, then saturate
     again.
  4. **If new generators turn up,** recompute the points and the ILP for that curve.
  5. **If it stays unresolved,** record the curve with its current best ratio.
- **How much this matters:** the points that matter have small denominators, hence small height, and those
  are exactly the points `ellrank`'s own search finds first. A missing generator is likely to have large
  height, so it adds few useful points. Expect little change; the cost is small, about 3,000 curves at a few
  seconds each.
- **Priority:** bounded curves whose current best ratio is closest to a record go first.

## Q3: curves worth more analysis

The data for this already exists on 7of9. `hunt_split.csv` holds every curve's best n for each k ≥ 6, and
`ranked_split.csv` holds every curve's score.

1. **Find the near misses.** Run `near_misses.py` on `hunt_split.csv` (and `hunt18.csv`): every curve's best
   ratio to the published value, for each k.
   - **Deep treatment** for curves within 10³ of a record at any k: ILP over k = 6–30, height up to 100, and
     the Q2 rank checks.
2. **Look for curves that beat their score.** Join the near-miss ratios with the Nagao scores, and list the
   curves that did much better than their score predicts. That is direct evidence of what the score misses.
3. **Look for prime-factor enrichment.** Both records contain **7·43·73·157 = 3,449,761**.
   - Count which primes, and which pairs and triples of primes, are over-represented among the best 1% of
     curves compared with all curves.
   - Use the enriched cores to **build new curves outside the current set**: those cores times 1–3 further
     primes ≡ 1 (mod 3) up to 1000, plus variants with a squared prime (M is cube-free, so p² is allowed).
     The current set stops at p < 200 and squarefree M.
4. **A better ranking score**, to test against the records:
   - **"smooth-point score"**: the number of points of height ≤ 40 whose denominator is 1000-smooth, which is
     cheap after `ellrank`;
   - or simply the beam ratio itself.
   - **Validation:** a good score must put both record curves at the very top, and it must predict the
     near-miss ratios better than the Nagao sum.
5. **Finish the last 84,000 curves of the sweep (cheap, about 3 h).** This revises the earlier advice that
   they weren't worth running. Since the Nagao score turns out to predict bound quality poorly, a low score is
   no longer a good reason to skip a curve.

## Order of work

1. **Literature check** for published Ta(23)–Ta(28) bounds (finding 5). This decides whether k > 22 is a
   result or a curiosity.
2. **Analysis on 7of9 with the existing files:**
   - near misses;
   - score against outcome;
   - prime enrichment (Q3, steps 1–3).
3. **Instrumentation in `curve_hunt.py`:**
   - the `.meta` line;
   - the vector-cap flag;
   - optional ILP mode (`--ilp-within 1e6`);
   - k up to 30;
   - no `wmax` cap.

   Validate on the two record curves: the ILP must reproduce the published values.
4. **Re-run the top 100,000** with the new settings (about 3.5 h), and also the last 84,000 (about 3 h).
5. **Rank-bounded follow-up** (Q2).
6. **New prime families** from step 2, ranked by the better score (Q3, step 4).
