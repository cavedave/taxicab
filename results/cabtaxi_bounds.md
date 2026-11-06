# Cabtaxi upper bounds: Ca(33), Ca(34), Ca(45) – Ca(57) improved, Ca(58) – Ca(70) new

*24 October 2026. Exact values are in `cabtaxi_bounds.txt`, with every representation listed.*

Cabtaxi(k), written Ca(k), is the smallest positive integer that is a³ + b³ with integers of either sign in
at least k ways ([OEIS A047696](https://oeis.org/A047696)).

## Result

| k | our upper bound | best published | factor smaller |
| ---: | --- | --- | ---: |
| 33 | 6.411 × 10¹⁰⁰ | 1.234 × 10¹⁰¹ (Boyer–Wroblewski 2008) | 1.9 |
| 34 | 1.564 × 10¹⁰⁵ | 8.874 × 10¹⁰⁷ (Boyer–Wroblewski 2008) | 568 |
| 45 | 1.894 × 10¹⁸² | 2.396 × 10¹⁸³ (Su 2016) | 12.7 |
| 46 | 5.774 × 10¹⁹⁰ | 5.350 × 10¹⁹² (Su) | 93 |
| 47 | 5.366 × 10¹⁹⁹ | 1.742 × 10²⁰³ (Su) | 3.2 × 10³ |
| 48 | 1.636 × 10²⁰⁸ | 7.852 × 10²¹³ (Su) | 4.8 × 10⁵ |
| 49 | 3.652 × 10²¹⁷ | 5.243 × 10²²⁴ (Su) | 1.4 × 10⁷ |
| 50 | 1.134 × 10²²⁷ | 4.056 × 10²³⁵ (Su) | 3.6 × 10⁸ |
| 51 | 3.203 × 10²³⁶ | 3.313 × 10²⁴⁶ (Su) | 1.0 × 10¹⁰ |
| 52 | 7.150 × 10²⁴⁵ | 4.036 × 10²⁵⁷ (Su) | 5.6 × 10¹¹ |
| 53 | 2.221 × 10²⁵⁵ | 1.113 × 10²⁶⁹ (Su) | 5.0 × 10¹³ |
| 54 | 1.445 × 10²⁶⁵ | 3.289 × 10²⁸⁰ (Su) | 2.3 × 10¹⁵ |
| 55 | 2.365 × 10²⁷⁵ | 1.382 × 10²⁹² (Su) | 5.8 × 10¹⁶ |
| 56 | 7.700 × 10²⁸⁵ | 8.052 × 10³⁰³ (Su) | 1.0 × 10¹⁸ |
| 57 | 1.961 × 10²⁹⁶ | 5.954 × 10³¹⁵ (Su) | 3.0 × 10¹⁹ |
| 58 – 70 | 1.456 × 10³⁰⁶ … 1.379 × 10⁴³⁵ | none found | new |

For every other k from 10 to 44, the exact optimum on the record curves **equals** the published bound.

## How

- **The curve:** every bound is n = M · L³ on x³ + y³ = M, with M = 3956875867 = 7·31·37·43·73·157 (rank 6).
  That is the curve behind the Boyer–Wroblewski taxicab and cabtaxi records.
- **The points:** every rational point of height ≤ 80, with either sign: 10,191 points.
- **The optimiser:** for each k, the exact integer program (`experiments/curve_ilp.py`) finds the smallest
  L that is a multiple of at least k point denominators. It ran via `experiments/curve_cabtaxi.py`.
- **Validation:** the same program, run on the curve of each published record, reproduces every published
  bound exactly on its own curve. That covers Ca(10); Ca(11), Ca(12) and Ca(14) (M = 1423214); Ca(13),
  Ca(15)–Ca(18) and Ca(20) (M = 116776387); and Ca(19) and Ca(21)–Ca(44) (M = 3956875867), excluding
  Ca(33) and Ca(34), which it improves.
- **Why the gains grow with k:** Su's bounds extend Boyer's Ca(42) by multiplying by one more cube per step.
  The optimiser instead re-chooses the whole set of points for each k.
- **Verification:** every representation was re-checked from the text file alone, using exact integer
  arithmetic shared with neither PARI nor the solver: x³ + y³ = n, all pairs distinct, at least k of them.
- **Literature checked:**
  - Boyer, [`CabtaxiUpdated.txt`](http://www.christianboyer.com/taxicab/CabtaxiUpdated.txt): Ca(10)–Ca(22),
    18 April 2008, with all representations;
  - Boyer and Wroblewski, [`TaxibigUpdated.txt`](http://www.christianboyer.com/taxicab/TaxibigUpdated.txt),
    section "Big Cabtaxi Upper Bounds": Ca(23)–Ca(42), 18 April 2008. This is the source of the Ca(33) and
    Ca(34) bounds improved here;
  - Su, JIS 19 (2016), Theorem 11 (Ca(43)–Ca(57));
  - OEIS A047696, whose bound comments stop at a(44), 2014.
- **Published table:** the values compared against are in `experiments/cabtaxi_known.csv`. Copies of both
  Boyer text files are in `refs/boyer_lists/`.

**A note on Boyer's PDF.** Boyer's journal paper ([JIS 11 (2008), Article 08.1.6](http://www.christianboyer.com/taxicab/TaxicabUpperBounds.pdf),
dated March 2008) only gives Cabtaxi bounds up to **Ca(30)**. The bounds for Ca(31)–Ca(42), including the
Ca(33) and Ca(34) compared here, appear only in the later `TaxibigUpdated.txt` on the same site. Su (2016)
uses those same values, calling them BCa(n).
