# Taxicab numbers

Magnification search (`engine_b9`) and the compact result tables it produced.

```
N = a³ + b³ = c³ + d³ = …
```

Repo: [github.com/cavedave/taxicab](https://github.com/cavedave/taxicab)

## Files

| file | what it is |
| --- | --- |
| `engine_b9.cpp` | magnification / splitting engine (`N = seed × m³`) |
| `results/seeds.csv` | 8,637 base seeds, `k ≥ 2`, with factors and pairs |
| `results/k5plus.csv` | every **k ≥ 5** hit: 20,908 five-ways, 302 six-ways, 1 seven-way |
| `results/khist.txt` | counts by `k`, including 109,009,103 three-ways and 1,531,440 four-ways |
| `results/found_known.txt` | the one `k = 7` hit: Boyer’s Ta(7) upper bound |
| `results/cf_sf3.csv` | smallest split-prime squarefree 3-way found: `208,438,080,643` |

The full 4-way list (~1.5M rows, ~173 MB) is not stored. GitHub rejects files over 100 MB.

## Known small taxicab numbers

| k | smallest N | notes |
| ---: | ---: | --- |
| 2 | 1729 | Hardy–Ramanujan |
| 3 | 87,539,319 | Ta(3); first line of `seeds.csv` |
| 4 | 6,963,472,309,248 | Ta(4) |
| 5 | 48,988,659,276,962,496 | Ta(5) |
| 6 | 24,153,319,581,254,312,065,344 | Ta(6); smallest 6-way in `k5plus.csv` |
| 7 | ≤ 24,885,189,317,885,898,975,235,988,544 | Boyer upper bound; `found_known.txt` |

## Formats

`seeds.csv`:

```
N;k;p:e,p:e,...;a:b,a:b,...
```

`k5plus.csv`:

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
make
./engine_b9 --selftest
```

## References

- [OEIS A001235](https://oeis.org/A001235) — sums of two positive cubes in at least two ways
- [OEIS A011541](https://oeis.org/A011541) — taxicab numbers Ta(n)
- [OEIS A080642](https://oeis.org/A080642) — cubefree taxicab numbers
- [OEIS A023050](https://oeis.org/A023050) — 3 or more ways, coprime pairs
