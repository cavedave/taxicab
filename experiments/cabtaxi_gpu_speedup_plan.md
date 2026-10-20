# Plan: a faster `cabtaxi_gpu.cu`, then 10²²–10²³

*Written 18 October 2026, after the 10²¹–10²² run.*

**Status, 19 October 2026: Steps 1 and 2 are written and pass every test the Mac can run. Step 3 (GPU) is
next: `bash experiments/validate_v2.sh` on one rented 5090.**
- `cabtaxi_gpu_v1.cu` is a frozen copy of the version used for the 10¹⁹–10²² runs (md5 1a29b6f3…).
- `cabtaxi_gpu.cu` is v2:
  - per-phase timing ("time split" lines);
  - `cub::DeviceSelect` drops the non-coprime keys before the sort;
  - the sort uses only `sort_bits(lo, hi)` bits;
  - the limit is 10²⁴.
- New selftest windows below 10²², 10²³ and 10²⁴, with constants from `window_count.py`, an independent
  exact Python counter. That counter was itself checked against the known counts (36,368 pairs up to 10⁷; the
  39-pair window below 10²¹). The 10²⁴ window has 188 pairs and one value with 3 representations.
- **Mac host-only build:** the selftest passes (12/12), and the output at 10¹² is byte-identical to v1
  (63,975 numbers, 80,226,285 coprime pairs).
- **Not testable on the Mac:** the CUB select, the bit-limited GPU sort and the GPU timing. `validate_v2.sh`
  covers them, plus a v1/v2 A/B run around 1.04 × 10²¹ and a speed run at 5 × 10²².
- `run_4x5090.sh` now defaults to 10²² – 10²³ (MIN/MAX/KMIN/TAG can be overridden), and its status shows the
  time split.

## Result of v3 (19 October 2026, one RTX 5090, `validate_v3.sh`: ALL CHECKS PASSED) — GOAL MET

v3 (`cabtaxi_gpu.cu`, md5 26ecf98f…) adds the 32-bit gcd on a running remainder, 64-bit steps and the
warp-interleaved writes.

- **Correctness:** the selftest passed, including the windows up to 10²⁴. Outputs and pair counts are identical
  to v1 and v2 at 10¹⁵ and at 10²¹ (where it finds the known five-way), and identical to v2 at 5 × 10²².
- **Speed:**

  | range | v1 | v2 | v3 | v3 vs v1 |
  | --- | ---: | ---: | ---: | ---: |
  | 10¹⁵ benchmark | 12 s | 11 s | 3 s | 4× |
  | 1.03–1.05 × 10²¹ | 365 s | 304 s | 134 s | **2.72×** |
  | 5–5.01 × 10²² | — (limit) | 301 s | 182 s | 1.65× vs v2, about 2× vs v1 (est.) |

- **Speed per card:** 1.3 × 10¹⁰ raw pairs/s.
- **Padding** of the interleaved layout costs 1–4% extra slots.
- **Time split for v3 at 5 × 10²²:**

  | sort | write | select | count | runs |
  | ---: | ---: | ---: | ---: | ---: |
  | 64% | 13% | 11% | 6% | 4% |

  **The sort is now the bottleneck.** The hashed-counter filter (Step 4) would replace both select and sort,
  which together are 75% of the time.
- **Cost of 10²²–10²³** (about 2.24 × 10¹⁵ raw pairs): **about 47 GPU-hours, roughly 12 h on 4 × 5090**,
  against about 145 GPU-hours with v1.
- **Profiling:** Nsight Compute is blocked in vast.ai containers (ERR_NVGPUCTRPERM), so no profile was taken.

## Result of Step 3 (19 October 2026, one RTX 5090, `validate_v2.sh`: ALL CHECKS PASSED)

- **Correctness:** the v2 GPU selftest passed, including the windows up to 10²⁴. v1 and v2 gave identical
  outputs and pair counts at 10¹⁵ and on 1.03–1.05 × 10²¹.
- **Speed:** only **1.20×** (376 s → 314 s at 10²¹). At 5 × 10²², v2 runs at 7.77 × 10⁹ raw pairs/s.
- **Time split for v2:**

  | scale | write | sort | select | count |
  | --- | ---: | ---: | ---: | ---: |
  | 10²¹ | 65% | 28% | 5% | — |
  | 5 × 10²² | 48% | 39% | 6% | 4% |

- **Lesson:** the assumption that the sort dominates was wrong. On the GPU, the **write kernel** dominates.
  The CPU's 58% sort share did not carry over.

**Why the write kernel is likely slow (hypotheses, to be confirmed with Nsight Compute):**
1. **64-bit binary gcd per pair.** It is emulated with 32-bit instructions and has divergent loops.
2. **Uncoalesced writes.** Each thread writes its own contiguous run, so a warp touches 32 cache lines per step.
3. **Load imbalance.** Stream lengths vary a lot (d = 1 has about 10⁵ pairs per segment). The higher speed at
   5 × 10²², where there are more, shorter streams per segment, fits this.

**Step 2b fixes (v3):**
- **32-bit gcd on a running remainder:** gcd(a, b) = gcd(a, b mod a), keeping r = b mod a by increment-and-wrap,
  with a ≤ 2 × 10⁷ (sums). For differences, gcd(c, d) = gcd(d, c mod d) in the same way.
- **Warp-interleaved, coalesced layout.** At step j, lane l writes to warp_base + 32j + l. The region size is
  32 × the longest stream in the warp. Holes are filled with SENTINEL, which the select step already removes.
  Order does not matter, since the keys are sorted afterwards.
- **Split very long streams** into chunks, each started from an exact recomputed value.
- **Measure first:** `ncu` on one segment of v2, to confirm which of the three causes dominates.

## Where we are

- A047697(6) > 10²² (proved by exhaustive search). There are 11 coprime five-ways up to 10²²: 2 found by
  Bernstein and 9 new ones. Details are in `results/a047697_search.md`.
- The 10²¹–10²² run took 26.0 GPU-hours on 4 × RTX 5090 at about 4.9–5.4 × 10⁹ raw pairs/s per card.
- At today's speed, 10²²–10²³ would cost about 145 GPU-hours (each power of ten costs 4.64× the previous one).
- **Goal: about 2× faster before renting again.** That brings 10²²–10²³ to about 70 GPU-hours, or about 18 h
  on 4 × 5090.

## Known inefficiencies (confirmed in the code)

1. **Non-coprime pairs are sorted.** The write kernel stores gcd > 1 pairs as `SENTINEL`
   (`cabtaxi_gpu.cu:137`, `:144`), and the radix sort then sorts them. That is 39% of all keys sorted for
   nothing.
2. **The sort covers all 64 bits.** `SortKeys` (`:254`) is called without `begin_bit`/`end_bit`. At 10²² a
   segment spans about 2⁵⁵ in n, so 56 bits are enough, which saves one of the eight radix passes.

## Step 1: measure (on the Mac, written but not run)

- Add `cudaEvent` timing per phase (count, scan, write, sort, run detection, host recovery) to the progress
  line and the DONE line.
- Purpose: know the real share of the sort before and after the changes. (The CPU program spent 58% in its
  sort, but the GPU split has never been measured.)

## Step 2: the quick wins (on the Mac)

- **Compact before sorting.** Write only coprime pairs, using warp-aggregated `atomicAdd` to reserve output
  slots. Order does not matter, because the keys are sorted afterwards.
  - The coprime count then comes directly from the counter, so the `atomicMax`/`lower_bound` SENTINEL logic
    (`:172`, `:200`) goes away.
  - The raw-pair count must still be reported (it comes from count/scan, as now).
  - The segment cap can now be measured in coprime pairs, so each segment holds about 1.6× more useful pairs.
- **Sort only the needed bits.** `end_bit = bit length of (hi − lo)`.
- **Raise the 10²² limit** (`LIMIT_STR`) to 10²⁴. The arithmetic is fine up to about 10²⁵–10²⁶, and the host
  check's x³ in 128 bits overflows near 10²⁶.
  - Check the stream buffer memory (`streams_bytes`, `:461`) at 10²⁴.
  - Add selftest windows above 10²² and above 10²³, each checked against an independent Python count, as was
    done for the window below 10²¹.
- **Check the logic on the Mac:**
  - Build with `-DHOST_ONLY`.
  - The result must be byte-for-byte the same at 10¹² and 10¹⁵.
  - The selftest must pass.
- **Expected gain:** about 1.4–1.6×, if the sort dominates.

## Step 3: validate on one rented 5090 (about 1 hour)

1. Run the selftest, including the new windows above 10²².
2. Run the 10¹⁵ benchmark. It must still give `raw pairs=13223067998 coprime pairs=8044700766`.
3. Run a sample range with known results and compare byte for byte with today's output. A good choice is the
   segment containing 1038246186276942167105, for example `--min 1.03e21 --max 1.05e21`.
4. Measure the speed at about 10²² and record the per-phase timing.

## Step 4 (only if Step 3 is short of 2×): hashed-counter filter, which avoids the sort entirely

1. **Pass 1:** generate every coprime pair and increment a counter at `hash(n)`. Store nothing else.
   Use 8-bit counters packed four to a 32-bit word, with about 4 counters per pair.
2. **Pass 2:** regenerate the pairs and keep only those whose counter is ≥ kmin. A true k-way puts all k pairs on
   the same counter, so **no solution can be lost**. With λ ≈ 0.25 pairs per counter, only about 10⁻⁵ of the
   pairs survive.
3. **Pass 3:** sort the survivors exactly, find the runs, and do the same independent host recovery as now.

- **Trade-off:** two cheap generation passes plus random global atomics, instead of eight sort passes over
  stored keys.
- **Risk:** random atomics into a multi-GB array go to DRAM, so their speed is uncertain. Prototype and measure
  before committing to it.
- **Side benefit:** no key buffer, so segments can be much larger. Per-stream setup (about 4 × 10⁷ streams at
  10²²) then becomes a smaller share of the work.

## Also, while the code is open

- Use `--kmin 4` on the next run if output size allows, to get the complete list of coprime four-ways (it
  costs no extra GPU time; until now four-ways were only kept up to 10¹⁵, 90 of them). Estimate the output size
  first.

## Loose ends from the 10²² search (independent of the speed-up)

- Get the pair counts for the 0–10¹⁹ CPU run from `cab2.log` on 7of9; they are the last placeholders in the
  write-up.
- Draft an OEIS comment for A047697: a(6) > 10²², and the 11 five-ways.
- Commit the write-up, scripts, results and images on `engine-b12`.
