# Upper bounds for Ta(23) – Ta(28)

*20 October 2026. Exact values are in `taxicab_23_28_bounds.txt`, with every representation listed.*

Ta(k) is the smallest positive integer that is a sum of two **positive** cubes in at least k ways.

## Result

| k | our upper bound | previous best published | improvement |
| ---: | --- | --- | ---: |
| 23 | 1.4191 × 10¹⁷³ (174 digits) | 5.0563 × 10¹⁷³ (Su 2014/2016) | 3.56× smaller |
| 24 | 1.5331 × 10¹⁸⁷ (188 digits) | 3.8149 × 10¹⁸⁸ (Su 2014/2016) | 24.9× smaller |
| 25 | 1.1567 × 10²⁰² (203 digits) | none found | — |
| 26 | 2.3713 × 10²¹⁷ (218 digits) | none found | — |
| 27 | 2.5983 × 10²³³ (234 digits) | none found | — |
| 28 | 5.7381 × 10²⁴⁹ (250 digits) | none found | — |

**Previous best:** Su, "More Upper Bounds on Taxicab and Cabtaxi Numbers", JIS 19 (2016) #16.4.3, Theorem 12:
- STa(23) = (97·491)³ · BTa(22)
- STa(24) = (59·1543)³ · STa(23)

Both are also in the OEIS (A011541, October 2014). The paper is in `refs/su_2016_more_upper_bounds_jis19.pdf`.

## Where the numbers come from

Every bound is n = M · L³ on the curve x³ + y³ = M, with M = 3956875867 = 7·31·37·43·73·157 (rank 6). That is
the curve of Boyer–Wroblewski's records for Ta(11)–Ta(22).

**The method:**
1. PARI `ellrank` and `ellsaturation` give generators.
2. `qfminim` lists every point of canonical height ≤ 80: 3,381 positive points.
3. For each k, an **exact integer program** (`experiments/curve_ilp.py`, SciPy/HiGHS) finds the smallest
   L = lcm of the denominators of at least k points.

The same program reproduces every published Ta(11)–Ta(22) bound on this curve as the exact optimum. So our
bounds for k ≥ 23 are *optimal for this curve and height bound*, though not necessarily optimal overall.

**Verification:** every representation was re-checked from the text file alone, with exact integer arithmetic
that shares nothing with PARI or the solver:
- x³ + y³ = n;
- 0 < x < y;
- the pairs are distinct;
- there are at least k of them.

## What has been checked, and what has not

**Literature checked (20 October 2026):**
- Boyer's lists, which stop at Ta(22) for taxicab ([`TaxibigUpdated.txt`](http://www.christianboyer.com/taxicab/TaxibigUpdated.txt), April 2008);
- Boyer's web page;
- MathWorld, which lists only Ta(2)–Ta(6);
- OEIS A011541, which has Su's Ta(23) only;
- Su 2016, which gives Ta(23) and Ta(24).

No bound for Ta(25) or higher was found.

**Not checked:** work after 2016 outside these sources, such as later arXiv papers, Boyer's newer pages, or
private lists. A wider search is advisable before submitting anything to the OEIS.

*Correction (25 October 2026): an earlier version said no bound exists here for k ≥ 29 at height ≤ 80.
That was wrong: the search had been capped at 10²⁶⁰, which is below the true Ta(29) value. See the addendum.*

## Addendum, 24–25 October 2026: Ta(29) and Ta(30)

The same exact program on the same curve also gives Ta(29) and Ta(30). They first came out of a run with
points of height ≤ 110 (26,551 points, denominators factored by trial division to 10⁶). A rerun on
25 October showed that **height 80 gives exactly the same two values**; the earlier "none" at height 80 was
only an artificial cap. Height 80 also continues with Ta(31) (301 digits), and so on.

| k | upper bound | previous best published |
| ---: | --- | --- |
| 29 | 2.19277… × 10²⁶⁶ (267 digits) | none found |
| 30 | 1.81790… × 10²⁸³ (284 digits) | none found |

The exact values and every representation are in `taxicab_29_30_bounds.txt`, re-verified with exact integer
arithmetic.

At height 110 the bounds for Ta(20)–Ta(30) are unchanged: the extra points do not improve them. The
height-110 cabtaxi run was still in progress when this was written; its partial output is in `height110/`.
