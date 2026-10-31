# Plan: the search for A080642(5), the cubefree taxicab five-way

*29 October 2026. Follows `cubefree.md` (what we know) and `cubefree.txt` (background, 13 October). Discussed with
the user on 29 October; to start after the coprime six-way weekend.*

## The target

A080642(5) is the smallest **cubefree** number that is a sum of two **positive** cubes in five ways. Nobody has
found one. Our lower bound: **A080642(5) > 2.5·10²³** (`cubefree.md` §2, from the exhaustive A047697 search).

## What shapes the plan

- **Cubefree ⇒ coprime.** A cubefree positive five-way is a coprime five-way (A047697 family) whose five
  representations are all sums. Every tool built for the coprime search applies: exact counting from divisors,
  line and D-line enumeration, the catalogue.
- **Lines cannot help.** No line meets x³ + y³ = n in three positive points (convexity, `cubefree.md` §3). The line
  search, our main five-way engine, can never produce an all-positive multi-way. All 82 coprime five-ways found so
  far are line-built, and the best have only 4 positive representations (2724248230569896697541 and
  133258206935285167925449341991); in both the fifth, a difference, is the point the two lines share.
- **What remains: hubs and rank.** Integral points of a multi-way are related only by lines and hubs (FINDINGS F33),
  or not at all, on a curve of high rank. The five known all-positive coprime four-ways (all cubefree) are 4 hubs
  and 1 independent: A080642(4) = 1801049058342701083, rank 4 (`cubefree.md` §4).
- **How rare.** 5 of 8,571 coprime four-ways are all positive (about 1 in 1,700); 0 of 82 five-ways.
- **Where it might be (a guess).** The first cubefree k-ways sit near 10³ (k = 2: 1729), 10¹⁰ (k = 3) and 10¹⁸
  (k = 4): gaps of 7 and 8 decades. A gap of about 9 more puts A080642(5) near **10²⁷**. This is an extrapolation
  from three points, not a model, but it sets the scale: probably beyond any exhaustive search we can afford.
- **Likely shape.** By analogy with the coprime case (line + free point → bowtie → bowtie + free point), the
  likeliest are **hub + free point** (rank 4), two hubs sharing a point, or five independent points (rank ≥ 5).

## Steps, cheapest first

### 1. Literature check (an hour, Mac)
- OEIS A080642: entry, comments, references, b-file; A011541 (taxicab) and A047697 cross-references.
- Bill Butler's pages (`refs/butler_ramanujan.html`, `butler_ramanujans_c.html`): what his exhaustive lists of
  primitive positive five-ways cover, and to which bound.
- Christian Boyer's lists (`refs/boyer_lists/`), and Hollerbach's exhaustive Ta(6) search (2008): did any of these
  list *all* positive five-ways to some bound? If so, the lower bound may already be higher, or a cubefree example
  may be hiding in a published list.
- **Outcome:** the best published lower bound, and any candidate to check.

### 2. Elkies–Rogers curves (an afternoon, Mac)
- Elkies and Rogers (2004, `refs/elkies_rogers_2004_math0403116.pdf`) list values k for which x³ + y³ = k has record
  rank, up to 11. High rank is exactly the "rank route".
- For every k in their tables: is it cubefree, and how many positive representations does it have? Counting is
  instant (`experiments/mining/collisions.py` / `count_all.py`, PARI factorisation + divisor test).
- **Outcome:** a long shot at a direct hit; at least a measurement of how many integral points record-rank curves
  carry.

### 3. Hub search with a positive filter (one 7of9 night)
- `dline_enum.py` with one extra condition: keep only D-lines whose two integer points are both **positive**
  (x, y > 0), plus a cubefree check on n. Report the positive count of every candidate in `count_all.py`.
- Directions and heights from the hub run of 29–30 October (`night_7of9/hubs/`), whose analysis gives first:
  - how many of its 204 hubs are all-positive, and their rate per candidate;
  - which directions and denominators D the positive hubs use.
- **Outcome:** positive hubs in bulk; any hub + free point with all five positive is the answer.

### 4. A sums-only mode for the GPU search (code change, then a background run)
- For positive representations the GPU needs only the sums a³ + b³ (1 ≤ a ≤ b) and can skip the differences:
  about **33 % of the pairs** (sums: 0.44·B^(2/3); all pairs: 1.33·B^(2/3), measured), so about **3× cheaper**.
- **Validation:** recover Ta(6) = 24153319581254312065344 (Hollerbach's exhaustive result), Ta(5), and
  A080642(4) = 1801049058342701083; compare against the full search on 10¹⁵ and 10²¹ windows (sums only).
- **Cost:**
  - 2.5·10²³ → 10²⁴: about 2.7·10¹⁵ pairs, about 5 nights on 7of9 (4 × RTX 2080 Ti);
  - → 10²⁵: about 1.6·10¹⁶ pairs, about 350 GPU-hours on RTX 5090s (too expensive for now).
- **Overlap:** the full A047697 extension to 10²⁴ (`writeup/01_gpu_search.md` §6) covers sums too, so if it runs,
  A080642(5) > 10²⁴ comes free. Sums-only pays beyond 10²⁴, or if the A047697 extension does not run.
- Do this together with the planned sort speed-up (2–2.5×).

### 5. The rank route proper (later, only if 2 or 3 point to it)
- Choose cubefree n with many split primes and a high Mestre–Nagao score (AUC 0.95 for rank ≥ 6, FINDINGS F35) and
  count their positive representations.
- **The catch** (negative result N3): random rich n almost never have any representation. Candidates must come from
  a construction that guarantees some, such as D-lines and hubs (step 3), or from known high-rank families (step 2).

## Status (30 October 2026, FINDINGS F42)

- **Step 1 done.** OEIS A080642 gives no bound for a(5); no published bound found. All 357 five-ways and 24 six-ways
  of Butler's primitive list (to 2.51·10²⁸) checked: none is cubefree (none even has all pairs coprime). Our
  A080642(5) > 2.5·10²³ appears to be the best known.
- **Step 2 done, negative.** The 15 Elkies–Rogers record k have 0 or 1 integer representations.
- **Step 3 prepared.** The positive chords of a direction lie on three slope arcs; `dline_enum.py --positive`
  enumerates only those (validated: same positive D-lines as the full sweep) and makes a hub night about 5× cheaper.
  `night_cpu.sh` switch: `DPOS=1`. Needs fresh direction lists (beyond the 300,000 of the hub run) for one night,
  about 3 million directions.

- **Step 3 run (30–31 October, F43).** 3 million directions in positive mode: **three new all-positive cubefree
  four-ways** (hubs, 1.2·10²⁷, 2.8·10²⁷, 4.2·10²⁹), the first from our searches; 8 now known. At this rate a cubefree
  five-way would take 100–500 such nights: the hub route gives a census, not A080642(5).

## Order and expectations

- **First:** steps 1 and 2 on the Mac (cheap; might settle the question).
- **Then:** analyse the hub run, and make step 3 the first cubefree night on 7of9.
- **Background:** step 4 with the GPU speed-up work.
- **Honest odds:** if A080642(5) is near 10²⁷, the exhaustive route will not reach it on our budget. Steps 2 and 3
  are the realistic routes to an example, and neither is likely to succeed quickly. What we can deliver for certain
  is a higher, self-computed lower bound and a clear account of the structure (convexity, hubs and rank) that makes
  the problem hard.
