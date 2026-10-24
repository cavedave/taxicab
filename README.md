# Taxicab numbers

Magnification search (`engine_b12` + `seedgen`) and the compact result tables from the earlier `engine_b9` run.

```
N = a³ + b³ = c³ + d³ = …
```

Repo: [github.com/cavedave/taxicab](https://github.com/cavedave/taxicab)

## New results (October 2026)

### Coprime cabtaxi: A047697(6) > 10²³

[OEIS A047697](https://oeis.org/A047697) is the smallest n that is x³ + y³ with gcd(x, y) = 1 in k ways
(negative cubes allowed). The known terms are 1, 91, 3367, 16776487 and 506433677359393. Bernstein (1999)
showed there is no six-way below 2.5 × 10¹⁷.

An exhaustive GPU search (`experiments/cabtaxi_gpu.cu`, checked against brute force, a CPU program and
independent Python recounts) shows **there is no coprime six-way up to 10²³**. Up to 10²³ there are exactly
11 five-ways: Bernstein's two and these **nine new ones**, each recounted independently.

| n | the five representations |
| ---: | --- |
| 39,673,716,067,958,900,347 | 418491³ + 3408526³ = 1202338³ + 3360075³ = 3526755³ − 1612412³ = 3819196³ − 2521629³ = 14705344³ − 14643933³ |
| 95,793,117,931,950,826,933 | 5029461³ − 3155822³ = 5073261³ − 3264272³ = 5625154³ − 4348011³ = 23578300³ − 23520723³ = 26192350³ − 26145723³ |
| 118,371,660,133,721,558,473 | 752526³ + 4904113³ = 1138980³ + 4889497³ = 2936497³ + 4531470³ = 5004913³ − 1912674³ = 5682073³ − 4022364³ |
| 624,256,195,206,357,000,469 | 1807245³ + 8519464³ = 2355597³ + 8486416³ = 3095128³ + 8408973³ = 8884936³ − 4256883³ = 96589720³ − 96567411³ |
| 633,753,337,814,536,954,807 | 1019818³ + 8584815³ = 9764199³ − 6673148³ = 10245412³ − 7615641³ = 10475362³ − 8019441³ = 75791818³ − 75755025³ |
| 921,288,078,249,108,802,505 | 7544409³ + 7893776³ = 9742196³ − 1495911³ = 9846873³ − 3222808³ = 10393689³ − 5862904³ = 22982553³ − 22385788³ |
| 1,038,246,186,276,942,167,105 | 6530217³ + 9124898³ = 10125896³ − 46911³ = 10251009³ − 3390124³ = 11696457³ − 8251942³ = 31043073³ − 30679708³ |
| 2,724,248,230,569,896,697,541 | 3515718³ + 13891669³ = 7975069³ + 13039368³ = 8518752³ + 12818077³ = 10230894³ + 11824693³ = 41571781³ − 41039550³ |
| 5,306,775,242,131,114,520,041 | 9848424³ + 16326073³ = 13667257³ + 14016672³ = 17446393³ − 1518156³ = 18167545³ − 8834844³ = 61604281³ − 61134600³ |

There is no five-way at all between 10²² and 10²³. The details of the runs (hardware, pair counts,
validation) are in [`results/a047697_search.md`](results/a047697_search.md), and images are in `out/a047697/`.

### Upper bounds for Ta(23) – Ta(28)

Published taxicab bounds stop at Ta(22) (Boyer & Wroblewski 2008). The only bounds beyond that are Su's
Ta(23) and Ta(24) (JIS 19, 2016). On the Boyer–Wroblewski record curve x³ + y³ = 3956875867, an exact
integer program over all rational points of height ≤ 80 (`experiments/curve_ilp.py`) gives:

| k | upper bound for Ta(k) | previous best |
| ---: | --- | --- |
| 23 | 1.4191 × 10¹⁷³ (174 digits) | 5.0563 × 10¹⁷³ (Su), **3.6× smaller** |
| 24 | 1.5331 × 10¹⁸⁷ (188 digits) | 3.8149 × 10¹⁸⁸ (Su), **25× smaller** |
| 25 | 1.1567 × 10²⁰² (203 digits) | none found |
| 26 | 2.3713 × 10²¹⁷ (218 digits) | none found |
| 27 | 2.5983 × 10²³³ (234 digits) | none found |
| 28 | 5.7381 × 10²⁴⁹ (250 digits) | none found |

- The same program reproduces every published Ta(11)–Ta(22) bound on that curve as the exact optimum.
- Every representation was re-verified with exact integer arithmetic.
- The full numbers and all their representations are in
  [`results/taxicab_23_28_bounds.txt`](results/taxicab_23_28_bounds.txt). The method and the literature
  checked are described in [`results/taxicab_23_28.md`](results/taxicab_23_28.md).
- The literature search covered Boyer's lists, MathWorld, OEIS A011541 and Su 2016; work after 2016 has not
  been fully checked.

### Cabtaxi upper bounds: Ca(33), Ca(34), Ca(45) – Ca(57) improved, Ca(58) – Ca(70) new

The same exact integer program, allowing negative cubes, runs on the record curve x³ + y³ = 3956875867.

- **Validation:** on their own curves it reproduces every published Cabtaxi bound from Ca(10) to Ca(44).
- **Improvements:** it beats the published bound for:
  - **Ca(33)**, by 1.9×;
  - **Ca(34)**, by 568×;
  - **every k from 45 to 57** (Su 2016): by 12.7× at k = 45, growing to **3 × 10¹⁹ at k = 57**.
- **New bounds** for Ca(58) – Ca(70), where nothing is published.

| k | Ca(k) ≤ | best published |
| ---: | --- | --- |
| 33 | 6.411 × 10¹⁰⁰ | 1.234 × 10¹⁰¹ |
| 34 | 1.564 × 10¹⁰⁵ | 8.874 × 10¹⁰⁷ |
| 45 | 1.894 × 10¹⁸² | 2.396 × 10¹⁸³ |
| 50 | 1.134 × 10²²⁷ | 4.056 × 10²³⁵ |
| 57 | 1.961 × 10²⁹⁶ | 5.954 × 10³¹⁵ |
| 70 | 1.379 × 10⁴³⁵ | none |

The published Ca(31)–Ca(42) come from Boyer and Wroblewski's
[`TaxibigUpdated.txt`](http://www.christianboyer.com/taxicab/TaxibigUpdated.txt) (April 2008). Boyer's PDF paper
only goes up to Ca(30). The full table, method and literature checked are in [`results/cabtaxi_bounds.md`](results/cabtaxi_bounds.md).
Every number and representation is in [`results/cabtaxi_bounds.txt`](results/cabtaxi_bounds.txt).

## Files

| file | what it is |
| --- | --- |
| `engine_b12.cpp` | magnification / splitting engine (`N = seed × m³`), current |
| `seedgen.cpp` | exhaustive root-seed generator (all multi-ways ≤ B) |
| `engine_b9.cpp` | engine that produced `results/` (superseded) |
| `results/seeds.csv` | 8,637 base seeds used by the b9 run (**incomplete**, see below) |
| `results/sixways.csv` | **b12 run**: all 20 six-ways and the 1 seven-way ≤ Boyer's Ta(7) bound from root seeds ≤ 1e15, with every pair |
| `results/k5plus.csv` | b9 run, every **k ≥ 5** hit: 20,908 five-ways, 302 six-ways, 1 seven-way |
| `results/khist.txt` | counts by `k`, including 109,009,103 three-ways and 1,531,440 four-ways |
| `results/found_known.txt` | the one `k = 7` hit: Boyer’s Ta(7) upper bound |
| `results/cf_sf3.csv` | smallest split-prime squarefree 3-way found: `208,438,080,643` |

The full 4-way list (~1.5M rows, ~173 MB) is not stored. GitHub rejects files over 100 MB.

**Known gap in `results/`.** `seeds.csv` had every 3-way ≤ 1e15 but only 4,785 of the
867,008 2-ways, so whole families were never reached. Example: the 2-way root
4,513,486,310,216 generates T(5,6) = 55,634,997,032,869,710,456 (m = 231) and Boyer's
6-way 869,296,828,638,589,225,875,000 (m = 5775), neither of which is in `k5plus.csv`.
Treat `results/` as a partial list until it is regenerated with `seedgen` seeds.

## Known small taxicab numbers

| k | smallest N | notes |
| ---: | ---: | --- |
| 2 | 1729 | Hardy–Ramanujan |
| 3 | 87,539,319 | Ta(3); first line of `seeds.csv` |
| 4 | 6,963,472,309,248 | Ta(4) |
| 5 | 48,988,659,276,962,496 | Ta(5) |
| 6 | 24,153,319,581,254,312,065,344 | Ta(6); first line of `sixways.csv` |
| 7 | ≤ 24,885,189,317,885,898,975,235,988,544 | Boyer upper bound; last line of `sixways.csv` |

`sixways.csv` (`N;k;seed;m;all pairs`) was produced by `engine_b12` on 7of9 (64 threads,
29 min) with UB = Boyer's Ta(7) bound and the 231,842 `seedgen` roots ≤ 1e15. All 20
six-ways are primitive (pairs share no common factor). It contains all 9 of Boyer's
six-ways < 1e26 (JIS 2008, Fig. A4) and all 16 primitive six-ways from `k5plus.csv`, plus
four the b9 run missed: 869,296,828,638,589,225,875,000, 2,750,085,916,337,189,154,400,203,528,
6,226,444,077,409,337,733,141,345,792 and 14,557,204,209,713,206,885,991,784,000. None is new:
all 20 are in Bill Butler's list of 23 primitive six-ways below 2.5e28
([Rama6way](http://www.durangobill.com/RamanujanPics/Rama6way.html), complete to 1e23).

The list is complete for six-ways ≤ the bound that have a multi-way cube-quotient ≤ 1e15.
Butler's other three fall outside that, as expected:

| six-way N | smallest multi-way cube-quotient | reached with seeds to |
| ---: | --- | --- |
| 18,739,897,591,304,984,193,957,312 | N/36³ ≈ 4.0e20 (3-way) | beyond `seedgen`'s 64-bit range |
| 809,496,453,559,886,879,612,245,056 | N/4788³ ≈ 7.4e15 (2-way) | 1e16 |
| 12,045,605,906,025,760,342,134,168,000 | N/4620³ ≈ 1.2e17 (2-way) | 1e18 |

No 7-way below Boyer's bound exists among the reachable families; Butler's exhaustive search
shows Ta(7) > 1e23 (2010).

## Formats

`seeds.csv`:

```
N;k;p:e,p:e,...;a:b,a:b,...
```

`k5plus.csv` (and engine `<out>`):

```
seed;multiplier;N;k;new_a:new_b,...
```

Only **new** (non-scaled) pairs are stored. Scaled seed pairs are `m·(a,b)`.

`cf_sf3.csv`:

```
N;k;squarefree;p:e,...;a:b,...
```

## Engine

This search never produces cubefree hits, because every output is `seed × m³`.

```bash
make                       # builds engine_b12 and seedgen
./engine_b12 --selftest
./seedgen --max 1000000000000000 --out seeds_1e15.csv      # 231,842 roots, ~40 s, 1 GB
./engine_b12 --seeds seeds_1e15.csv --threads 32 --out splits.csv
```

`seedgen` keeps only **roots**: multi-ways with no multi-way cube-quotient `n/g³`. The
engine scans every multiplier of each root, so non-roots add nothing. With roots up
to `B`, one engine pass finds every multi-way `n ≤ UB` that has a multi-way
cube-quotient `≤ B`. No `--rounds`: the engine computes the full pair set of every
`seed × m³` directly. Each number is reported once, by its smallest seed.

Engine outputs (appended, resumable from `<out>.ckpt`):

| file | contents |
| --- | --- |
| `<out>` | `seed;m;N;k;new pairs` for `k ≥ --kmin` (default 4) |
| `<out>.full` | `N;k;seed;m;all pairs` for `k ≥ --fullk` (default 6) |
| `<out>.ckpt` | `seed;multipliers scanned;count k=3,4,...` per finished seed |
| `FOUND7.full` | same as `.full`, for `k ≥ 7` |

## References

- [OEIS A001235](https://oeis.org/A001235) — sums of two positive cubes in at least two ways
- [OEIS A011541](https://oeis.org/A011541) — taxicab numbers Ta(n)
- [OEIS A080642](https://oeis.org/A080642) — cubefree taxicab numbers
- [OEIS A023050](https://oeis.org/A023050) — 3 or more ways, coprime pairs
- [OEIS A047697](https://oeis.org/A047697) — coprime cabtaxi: smallest n = x³ + y³, gcd(x, y) = 1, in k ways
- D. J. Bernstein, *Enumerating solutions to p(a) + q(b) = r(c) + s(d)*, Math. Comp. 70 (2001)
- C. Boyer, *New upper bounds for Taxicab and Cabtaxi numbers*, JIS 11 (2008), Article 08.1.6
- P.-C. Su, *More upper bounds on Taxicab and Cabtaxi numbers*, JIS 19 (2016), Article 16.4.3
