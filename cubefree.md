# Cubefree taxicab numbers (A080642): what the coprime search tells us

*28 October 2026 (updated after the night's runs). Follows `cubefree.txt` (background and search plan, 13 October). Data:
`results/a047697_catalogue.txt`; method notes: `experiments/mining/FINDINGS.md` F28–F33.*

## The question

A080642(n) is the smallest **cubefree** number that is a sum of two **positive** cubes in n ways.

| n | A080642(n) | found by |
| --: | --- | --- |
| 1 | 2 | trivial |
| 2 | 1,729 = 7·13·19 | Hardy–Ramanujan |
| 3 | 15,170,835,645 = 3²·5·7·31·37·199·211 | Vojta, 1981 |
| 4 | 1,801,049,058,342,701,083 = 7·31·37·43·163·193·9151·18121 | Gascoigne; Moore, 2003 |
| 5 | **unknown**: no published upper bound that we could find | |

## 1. A cubefree n-way is a coprime n-way

If n = x³ + y³ and g = gcd(x, y), then g³ divides n. So a cubefree n has **only coprime representations**.

A cubefree number with five positive representations therefore has at least five coprime representations. It is a
coprime five-way in the sense of A047697 (coprime cubes, either sign), the family our GPU and line searches find.
Everything we learn about coprime five-ways applies, restricted to those whose representations are all positive
sums.

## 2. New lower bound: A080642(5) > 2.5 × 10²³

**Proof.**
1. Our GPU search (`experiments/cabtaxi_gpu.cu`; runs and validation in `results/a047697_search.md`) is
   exhaustive. It lists every n ≤ 2.5 × 10²³ with at least five coprime representations, signs allowed.
2. There are 12. All were refactored and recounted independently (PARI factorisation + divisor test).
3. None has five positive representations:

| n | positive representations (of 5) |
| --- | :-: |
| 506,433,677,359,393 | 2 |
| 137,904,678,696,613,339 | 2 |
| 39,673,716,067,958,900,347 | 2 |
| 95,793,117,931,950,826,933 | 0 |
| 118,371,660,133,721,558,473 | 3 |
| 624,256,195,206,357,000,469 | 3 |
| 633,753,337,814,536,954,807 | 1 |
| 921,288,078,249,108,802,505 | 1 |
| 1,038,246,186,276,942,167,105 | 1 |
| **2,724,248,230,569,896,697,541** | **4** |
| 5,306,775,242,131,114,520,041 | 2 |
| 236,191,447,138,323,830,299,237 | 1 |

By section 1, a cubefree positive five-way ≤ 2.5 × 10²³ would be in this table. Hence **A080642(5) > 2.5 × 10²³.** ∎

- **Before:** `cubefree.txt` (13 October) gave A080642(5) > 10²³. That bound rested on Bill Butler's exhaustive
  list of primitive five-ways, which we checked but did not compute.
- **Now:** the bound is 2.5 times higher and rests on our own validated search.
- **Before submitting** to the OEIS, check the A080642 entry and its references once more for any published bound.

## 3. Lines can never carry three positive representations

**Theorem.** No line meets the curve x³ + y³ = n in three points with positive coordinates.

**Proof.** In the positive quadrant the curve is part of the boundary of {x³ + y³ ≤ n}, the ball of the ℓ³ norm,
which is strictly convex. A line meets a strictly convex curve in at most two points. ∎

**Data:** across all 4,076 collinear triples in the catalogue, the number of positive points on a line is 0
(1,740 lines), 1 (1,206) or 2 (1,130). It is never 3.

**Why this matters.** Our line searches find multi-ways through lines: three representations on a line, and
bowties made of two such lines. Ninety per cent of the coprime four-ways, and 40 of the 43 five-ways known before
27 October, are built that way.
- **Every line contains at least one difference.** So the line mechanism can never produce an all-positive
  multi-way.
- **The near-misses show it.** The best five-way, 2,724,248,230,569,896,697,541, has four positive
  representations and one difference. It is a bowtie, and the difference is the point the two lines share.

## 4. The two routes that remain: hubs and rank

In the language of `FINDINGS.md` F33, the integral points of x³ + y³ = n form part of an elliptic curve's
Mordell–Weil group. A multi-way arises either:
- **by structure:** relations among the points, as lines (3-term) or hubs (4-term, two chords meeting at a point R
  of small denominator); or
- **by rank:** no relations, on a curve of unusually high rank.

Lines are ruled out for all-positive sets (section 3), so only hubs and rank remain. Our only two coprime
four-ways with all four representations positive are one of each:

| n | cubefree | shape | curve rank |
| --- | :-: | --- | --- |
| 1,801,049,058,342,701,083 = A080642(4) | yes | **independent** (no relations) | **4** (exact, PARI `ellrank`) |
| 682,238,339,160,892,906,483 = 7·13·37·67·223·307·937·1693·27847 | yes | **hub** | not yet computed |

- **The record A080642(4) is a pure "rank" example:** four independent points on a rank-4 curve. This matches
  the OEIS note on A080642 that the rank must grow with n.
- **The second is a hub.** A chord through two positive points always has its third point off the positive arc.
  Two such chords meeting at the same rational point R give four positive integral points, with no line needed.

**Update, 28 October: five all-positive four-ways, and the shapes the theory predicts.** The night's D-line runs found
three more, all above 10²². All five are cubefree:

| n | shape |
| --- | --- |
| 1,801,049,058,342,701,083 = A080642(4) | independent (rank 4) |
| 682,238,339,160,892,906,483 | hub |
| 24,603,921,410,355,704,710,055,618,765 | hub |
| 14,551,560,408,872,015,690,484,403,997,371 | hub |
| 66,634,432,188,724,490,089,709,387,904,499 | hub |

Four of the five are hubs and the other is independent. None is a line, as section 3 requires. The D-line search
(hubs) is the right tool for positive cubefree multi-ways; the line search is not.

## 5. How rare the positive cases are

All 6,785 coprime four-ways and 72 five-ways we know (catalogue of 28 October), by number of positive representations:

| positive representations | 0 | 1 | 2 | 3 | 4 | 5 |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| four-ways | 1,649 | 2,411 | 2,123 | 597 | **5** | — |
| five-ways | 10 | 15 | 34 | 12 | **1** | **0** |

- **Cubefree:** 3,906 of the four-ways and 50 of the five-ways are cubefree. The exceptions carry 3³, 5³ or
  similar. One of the new five-ways, 1.78 × 10³¹, is divisible by 27.
- **"All positive" costs about a factor of 2,000 among four-ways** (5 of 6,785, about 1 in 1,400). If that holds for five-ways, a
  cubefree positive five-way is roughly as rare as, or rarer than, a coprime six-way.

## 6. What this means for searching

1. **The exhaustive GPU search proves bounds for both problems at once.** Every extension raises the lower bounds
   for A047697(6) and A080642(5) together.
   - From 2.5 × 10²³ to 1.25 × 10²⁴ (5×): about 57 h on 4× RTX 5090, or about 15 days on 7of9's 4× RTX 2080 Ti.
   - To 2.5 × 10²⁴ (10×): about 108 h, or 29 days.
   - The planned sort and per-stream speed-ups should roughly halve both.
   - The code's 10²⁴ cap is a guard, not a limit: the 128-bit arithmetic and the host check hold to about 10²⁶,
     but they need re-validating past 10²⁴.
2. **Reporting is free.**
   - The exact counter (`experiments/mining/count_all.py`) already has every representation and the factorisation
     of n. It can report the positive count and whether n is cubefree at no cost.
   - The GPU output needs no change: a cubefree positive five-way is a coprime five-way, so it is already caught.
3. **The structural route is the D-line search,** restricted to chords through two *positive* integral points,
   looking for hubs and stars of such chords. This is a filter in `dline_enum.py`, costing almost nothing.
4. **The line searches cannot find an all-positive five-way** (section 3). They remain the main source of coprime
   five-ways and six-way candidates, not of cubefree taxicab numbers.
5. **The rank route needs curves of high rank and the right size.** It is an Elkies-style search, not yet started.

## Open questions

- **Answered 28 October:** the GPU re-find of all coprime four-ways up to 10²² contains exactly three numbers with
  ≥ 4 positive representations, all cubefree: 1,801,049,058,342,701,083, 682,238,339,160,892,906,483 and
  2,724,248,230,569,896,697,541 (a five-way, 4 of whose representations are positive). This confirms
  independently that **A080642(4) = 1,801,049,058,342,701,083**, and that 682,238,339,160,892,906,483 is the
  second cubefree positive four-way.
- **The 29 new coprime five-ways of 27–28 October** (`experiments/mining/FINDINGS.md` F34) have at most 3 positive
  representations each, so none is a candidate for A080642(5). All are bowties, as section 3 predicts for
  line-found five-ways.
- Do all-positive multi-ways need *only* hubs and rank, or can larger relations (five or more terms) appear when
  no line is available? F33 found only ±1 lines and hubs among 1,765 coprime multi-ways, but almost none of them
  were all-positive.
- What rank does a cubefree positive five-way need? With one hub its five points span rank 4; with no relations,
  rank 5 or more. Measuring the ranks of the all-positive four-ways as more are found would calibrate this.
