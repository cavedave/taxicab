# TODO (running list; proofs to do are in experiments/mining/TODO.md)

## Runs
- [x] **lf36_v4 on 7of9** (F64: done 8 Nov, no six-way, 31 new five-ways; certificate needs lf.log + lf_jobs.log): complete line search, 23 cheapest directions (cost <= 1e4), n <= 1e36 exactly (~17 h; BOUND=1e35 ~8 h). New bowties -> bowtie_hunt.py curves.
- [x] line_fast.py: chunks of heavy directions are separate pool tasks (load balance); --B parsed exactly (Decimal). Bundle lf_v3.tar.gz.
- [x] **Complete line search to 1e33 with the C++ version** (F50, F52: done 6 Nov, no six-way, 49 new five-ways): lf_7of9.tar.gz, `nohup bash run_lf.sh > lf.log 2>&1 &` (every direction, ~5-7 h; or CMAX=1e4 first, ~1 h).
- [x] **Complete line search to 1e30 on 7of9** (F47, F48: done 4 Nov, no six-way, 11 new five-ways): copy lc_7of9.tar.gz, `nohup bash run_lc.sh > lc.log 2>&1 &`.
      Then: catalogue merge of lc_1e30_k4.txt, the certificate (lc_1e30_jobs.log), paper statement "no six-way <= 1e30 with a line of cost <= 1.2e12".
- [ ] **Ranks of 7 'independent' four-ways in 1e22 - 2.5e23** (PARI stack overflow at 2 GB on the Mac).
      On 7of9: copy `experiments/mining/curve_relations/rank_7of9/`, then `nohup bash run_ranks.sh > ranks.log 2>&1 &`
      (16 GB stack each, 4 h limit). Add the ranks to FINDINGS F44 (so far 27086411626209197593478 rank 5,
      29439502687316546488027 rank 4; F33's earlier independents: mean 5.8).
- [ ] **Proposition 11 filter in cabtaxi_gpu.cu** (proven, keeps k >= 4 complete with m = 19): table of the non-split
      part f(s) for s <= (4B)^(1/3) (~1e8 at 2.5e23-1e24, 4 bytes each, or 1 byte log2); skip difference rows d with
      19 f(d) > (4 lo)^(1/3) in the count kernel; SENTINEL sum pairs with 19 f(a+b) > (4 lo)^(1/3) in the write kernel.
      Validate: --selftest, and identical output to the unfiltered run on 1e19-1e20 and 1e22-2e22. ~20-25% faster.
- [ ] GPU bucket-count speed-up, then 2.5e23 -> 1e24 on 7of9 (background).
- [ ] Idea (F45): residue-filtered GPU hunt above 2.5e23 (e.g. (7|n or 13|n), n odd, n != +-2 mod 9: 26% of pairs,
      all 82 known five-ways); non-exhaustive. Needs a pair-enumeration change in cabtaxi_gpu.cu. Decide vs the plain 1e24 run.
- [ ] Idea (F45, long term): proven six-way-only bound via a sieve over long y-rows (Theorem 5 subset bound rules out
      ~70% of n); needs a Bernstein-style redesign of the GPU enumeration; payoff at most 2-3x.
- [ ] Optional: code variant for A293647 / A293650 ("primitive" = all summands jointly coprime).

## Paper (writeup/paper/paper.tex; the user writes the prose)
- [ ] Split-prime claim: five-ways have only +0.24 split primes over four-ways of the same size (F44); remove any
      "each extra representation costs 2-3 split primes" wording in sections 6 and 8.
- [ ] Shape table in section 6 -> trend by size (F44 part 2.1: hubs about 11% above 1e17, independents about 1%).
- [ ] Figures still to make: five-ways per decade (exhaustive vs curve search); split primes (size-matched, F44).
- [ ] Captions (user).
- [ ] Before submission: Liu's volume and pages; wording of Hollerbach's post.
- [ ] Literature check by hand for Theorems 9-14 (web search found nothing, which is not evidence of novelty): Dickson
      vol. II ch. XXI (Werebrusow), Silverman 1993 Monthly, Selmer (1950s, ax^3 + by^3 + cz^3 = 0), Mordell
      "Diophantine Equations" (cubic curves), Connell's Elliptic Curve Handbook (Desboves curves), Cassels "Lectures on
      Elliptic Curves" (reduction mod p; Theorem 10's mechanism is standard, the plane-model statement may not be).
- [ ] A mathematician's read of the new proofs: Theorems 10, 13, 14, Lemma 15 (and 8c).
- [x] Independent recount of the whole catalogue in PARI/GP (verify_gp/reps.gp): 18,392 / 18,392 agree.

## OEIS (user submits from their own account; files in results/oeis/)
- [ ] A023050 b-file to 1e19 (310 terms).
- [ ] A293648, A293649, A293651 b-files (A293651: 14 missing terms).
- [ ] New sequences: coprime in >= 4 ways (1,748 terms to 2.5e23), >= 5 ways (12 terms to 2.5e23).
