# The exhaustive search (GPU)

*Draft, 29 October 2026, for "An attempt to find a coprime six-way sum of two cubes". Sources: `results/a047697_search.md`
(runs, logs, validation), `experiments/cabtaxi_gpu.cu`, `experiments/cabtaxi.cpp`, `a047697/`.*

## 1. What is searched

A047697(k) is the least positive n with at least k representations n = x³ + y³, gcd(x, y) = 1, where x and y
may be negative. Known: 1, 91, 3367, 16776487 (Rathbun), 506433677359393 (Bernstein, 1999). Bernstein's search
showed that no six-way lies below 2.5·10¹⁷; we know of no later search.

We count, for every n ≤ B, every unordered coprime representation, written in exactly one of two forms:

- **sums** n = a³ + b³ with 1 ≤ a ≤ b;
- **differences** n = (c + d)³ − c³ = d³ + 3dc(c + d) with c, d ≥ 1.

Each representation is produced exactly once. The search is exhaustive: every coprime pair whose value lies in
range is generated, so "no n with six representations up to B" is a proof, not an estimate.

**Cost.** There are about B^(2/3) pairs with value ≤ B. Sums: a, b ≤ B^(1/3). Differences: for each d, c runs to
about (B/3d)^(1/2), and summing over d ≤ B^(1/3) again gives order B^(2/3). So each decade costs 10^(2/3) ≈ 4.64
times the one before; the measured pair counts follow this to three digits. About 6/π² ≈ 60.8 % of pairs are
coprime, as measured (0.60795).

## 2. The algorithm

The problem is to find repeated values in a list of about B^(2/3) numbers (2.4·10¹⁵ raw pairs for
10²³–2.5·10²³) without holding the list. We cut the range of n into **segments**, generate every pair whose value
falls in one segment, sort those values on the GPU, and read off the runs of equal values.

**Segments.** Pair density falls like n^(−1/3), so segment boundaries are spaced equally in n^(2/3); each segment
holds about as many pairs as one GPU can sort at once (about 1.4·10⁹ on a 32 GB card). A segment that turns out too
large is split in half automatically. Segments are independent, so `--part k/N` gives each GPU an equal share of
the *work*, not of n.

**One segment [lo, hi) on the GPU:**
1. **Count.** One thread per *stream* (each a for sums, each d for differences) computes how many of its values lie
   in [lo, hi): exact integer cube roots for sums, an exact quadratic bound for differences.
2. **Scan.** A prefix sum turns the counts into write positions.
3. **Write.** Each thread writes its values in increasing order using additions only:
   (b + 1)³ − b³ = 3b² + 3b + 1 for sums; for differences the steps 3d(2c + d + 1) grow by 6d each time. Each value
   is stored as its offset n − lo, which fits a 64-bit key, so 128-bit values sort as 64-bit integers. Pairs with
   gcd > 1 are discarded with a binary gcd (shifts and subtractions).
4. **Sort.** CUB radix sort of the keys.
5. **Runs.** One thread per sorted entry detects the start of each run of equal keys and keeps runs of length
   ≥ kmin (5 for the main runs; 4 for the runs that also collect four-ways).

**On the CPU, for every value reported:** all representations are re-derived independently by direct search (every
a with 2a³ ≤ n, and every d through the exact quadratic), about n^(1/3) steps; each identity is checked in exact
128-bit arithmetic, and the count must equal the GPU's multiplicity. Any mismatch stops the run. Output is written
in increasing n with a progress file, so an interrupted part resumes (`--resume`).

**Number theory used.** Only to check, never to prune: writing n = s·t with s = x + y, t = x² − xy + y², every prime
factor of t is 3 or ≡ 1 (mod 3), and gcd(s, t) | 3 (THEOREMS 5). This gives the divisor-based recount used in
validation (`experiments/mining/collisions.py`): for each divisor s ≤ (4n)^(1/3) of n, test whether (4n/s − s²)/3 is
a square.

## 3. Validation

Before any result was trusted:
- **Brute force:** every n ≤ 10⁷ with ≥ 2 representations, and the total number of coprime pairs (36,368), match an
  independent brute-force count.
- **Known terms:** 91, 3367, 16776487 and both of Bernstein's five-ways are recovered with their exact
  representation sets.
- **Splitting:** (0, 10¹²] gives exactly the pairs of (0, 10¹¹] and (10¹¹, 10¹²] together (80,226,285 coprime pairs).
- **Above 2⁶⁴:** a window just below 10²¹ gives the 39 coprime pairs of a separate Python count.
- **Against the CPU program** (`cabtaxi.cpp`, itself checked against brute force to 10⁸ and against Bernstein's
  2.5·10¹⁷): identical output at 10¹² (63,974 numbers) and 10¹⁵ (91 numbers).
- **On every GPU before every run:** a self-test (windows up to 10²⁴) and the 10¹⁵ pair counts reproduced exactly.
- **Results recounted independently:** every number reported with k ≥ 4 up to 2.5·10²³ (including all 1,118 numbers
  ≤ 10²² and all 215 in 10²³–2.5·10²³) was refactored with PARI and recounted from its divisors; n, k and the
  representation sets agree.
- **Reproducibility:** the kmin-4 search of 0–10²² was run twice on 7of9 (27–28 and 28–29 October 2026) and gave
  identical output, all 1,118 numbers.

## 4. Runs and cost

| range of n | hardware | raw pairs | time |
| --- | --- | ---: | ---: |
| 0 – 10¹⁹ | Threadripper 3970X, 64 threads (CPU program) | — | ≈ 8 h |
| 10¹⁹ – 10²¹ | 1 × RTX 5090 | 1.26·10¹⁴ | 8.6 h |
| 10²¹ – 10²² | 4 × RTX 5090 | 4.82·10¹⁴ | 26 GPU-h |
| 10²² – 3·10²² | 1 × RTX 5090, v3 code | 6.64·10¹⁴ | 13.9 h |
| 3·10²² – 10²³ | 4 × RTX 5090, v3 | 1.58·10¹⁵ | 36.9 GPU-h |
| 10²³ – 2.5·10²³ | 4 × RTX 5090, v3, kmin 4 | 2.40·10¹⁵ | 54.2 GPU-h |
| 0 – 10²² (kmin 4, four-ways) | 4 × RTX 2080 Ti | 6.15·10¹⁴ | 13.2 h (run twice) |

About 140 GPU-hours on rented RTX 5090s (vast.ai) plus about 9 CPU-hours. The v3 code (interleaved stream layout)
is 2.7× faster than the first version and was validated against it at 10¹⁵ and 10²¹. On 10²³–2.5·10²³ the time
splits: sort 60 %, write 14 %, select 10 %, count 8–10 %.

## 5. Results

- **A047697(6) > 2.5·10²³**, a millionfold beyond Bernstein's 2.5·10¹⁷.
- **Exactly 12 coprime five-ways ≤ 2.5·10²³:** Bernstein's two, nine new ones below 10²³, and
  236191447138323830299237 (which the line method had found first). By decade: 2 below 10¹⁹, 2, 4, 3, **0** in
  10²²–10²³, and 1 in 10²³–2.5·10²³.
- **Four-ways:** complete lists for n ≤ 10²² (1,107) and 10²³ < n ≤ 2.5·10²³ (214); 10²²–10²³ is in progress on 7of9.
- **Corollary for cubefree taxicab numbers (A080642).** A cubefree n has only coprime representations, so a cubefree
  number with five positive representations is a coprime five-way. None of the 12 has five positive representations
  (the best, 2724248230569896697541, has four). Hence **A080642(5) > 2.5·10²³** (`cubefree.md` §2).

## 6. Limits and next steps

- **Range of the code.** Values are 128-bit; the host check is exact to about 10²⁶. The code refuses n > 10²⁴ as a
  guard, so a run to 10²⁴ needs no new validation; beyond it, the self-test windows must be extended.
- **Cost of the next step.** 2.5·10²³ → 10²⁴ is about 8·10¹⁵ raw pairs: about 45 h on 4 × RTX 5090 (180 GPU-h) with
  the present code.
- **Planned speed-up.** The radix sort moves about 51 GB per segment (7 passes over 56-bit keys) at close to memory
  bandwidth. Only values occurring ≥ kmin times are needed, and keys are nearly uniform in a segment, so one scatter
  pass into 65,536 buckets with an exact duplicate count per bucket in shared memory should do the same job with a
  third of the traffic: an estimated 2–2.5× overall.
- **Why the exhaustive search matters for six-ways.** The free-point rate per candidate falls 5–10× per four decades
  of n (FINDINGS F38), so if six-ways exist the region just above 2.5·10²³ is the densest. Every extension raises
  the bounds for A047697(6) and A080642(5) together.
