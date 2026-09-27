# Taxicab numbers

Magnification search (`engine_b9`) and result tables for numbers that are a sum of two positive cubes in several ways:

```
N = a³ + b³ = c³ + d³ = …
```

Repo: [github.com/cavedave/taxicab](https://github.com/cavedave/taxicab)

## Why the 4-way list is not here

The magnification search counted **1,531,440** four-way numbers (`k = 4`). A CSV in the same format as `results/ladder_k5plus.csv` would be about **173 MB**. GitHub rejects files over 100 MB (and warns above 50 MB), so the full Ta(4)-style dump stays off this repo.

What *is* here instead:

| file | what it is | size |
| --- | --- | --- |
| `results/ladder_khist.txt` | counts by `k` (including the 1,531,440 four-ways) | tiny |
| `results/ladder_k5plus.csv` | every **k ≥ 5** hit from the ladder run | 2.3 MB, 21,211 rows |
| `results/main_k5plus.csv` | same class from the main run | 1.9 MB |
| `results/seeds_v3_base.csv` | 8,637 base seeds with `k ≥ 3` | 621 KB |
| `results/cf_sf3.csv` | smallest split-prime **squarefree 3-way** found | 1 row |

`k ≥ 5` is the interesting tail and fits on GitHub easily.

## Known small taxicab numbers

| k | smallest N | notes |
| ---: | ---: | --- |
| 2 | 1729 | Hardy–Ramanujan |
| 3 | 87,539,319 | Ta(3); first line of `seeds_v3_base.csv` |
| 4 | 6,963,472,309,248 | Ta(4); not stored as a full k=4 census |
| 5 | 48,988,659,276,962,496 | Ta(5) |
| 6 | 24,153,319,581,254,312,065,344 | Ta(6) |
| 7 | ≤ 24,885,189,317,885,898,975,235,988,544 | Boyer upper bound; see `results/found_known.txt` |

## Cubefree / squarefree (A080642 and friends)

These cannot come from the magnification engine (`N = seed × m³`).

| N | k | class |
| ---: | ---: | --- |
| 1729 | 2 | squarefree and cubefree |
| 15,170,835,645 | 3 | cubefree, **not** squarefree (A080642(3)) |
| 208,438,080,643 | 3 | squarefree; `13×19×31×37×67×79×139` |
| 1,801,049,058,342,701,083 | 4 | squarefree cubefree (A080642(4)) |
| ? | 5 | A080642(5) unknown |

A local exhaustive split-prime search below 208,438,080,643 found no smaller squarefree 3-way.

Prime taxicab numbers do not exist: `a³ + b³ = (a+b)(a² − ab + b²)` is composite for `a, b ≥ 1`.

## Engine

`engine_b9` is the magnification / splitting search. It never produces cubefree hits (`N = seed × m³`).

```bash
make
./engine_b9 --selftest
```

## Result formats

`seeds_v3_base.csv`:

```
N;k;p:e,p:e,...;a:b,a:b,...
```

`ladder_k5plus.csv` / `main_k5plus.csv`:

```
seed;multiplier;N;k;new_a:new_b,...
```

Only **new** (non-scaled) pairs are stored. Scaled seed pairs are `m·(a,b)`.

## References

- [OEIS A001235](https://oeis.org/A001235) — numbers that are a sum of two positive cubes in at least two ways
- [OEIS A011541](https://oeis.org/A011541) — taxicab numbers Ta(n)
- [OEIS A080642](https://oeis.org/A080642) — cubefree taxicab numbers
- [OEIS A023050](https://oeis.org/A023050) — sums of two positive cubes in 3 or more ways, coprime pairs
