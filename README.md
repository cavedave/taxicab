# Taxicab numbers

Magnification search (`engine_b12` + `seedgen`) and the compact result tables from the earlier `engine_b9` run.

```
N = a³ + b³ = c³ + d³ = …
```

Repo: [github.com/cavedave/taxicab](https://github.com/cavedave/taxicab)

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
four the b9 run missed: 869,296,828,638,589,225,875,000 (Boyer's), and
2,750,085,916,337,189,154,400,203,528, 6,226,444,077,409,337,733,141,345,792 and
14,557,204,209,713,206,885,991,784,000 (not found in the references checked). The list is
complete for six-ways ≤ the bound that have a multi-way cube-quotient ≤ 1e15. No 7-way
below Boyer's bound exists among those.

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
