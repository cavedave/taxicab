# TODO (running list; proofs to do are in experiments/mining/TODO.md)

## Runs
- [ ] **Ranks of 7 'independent' four-ways in 1e22 - 2.5e23** (PARI stack overflow at 2 GB on the Mac).
      On 7of9: copy `experiments/mining/curve_relations/rank_7of9/`, then `nohup bash run_ranks.sh > ranks.log 2>&1 &`
      (16 GB stack each, 4 h limit). Add the ranks to FINDINGS F44 (so far 27086411626209197593478 rank 5,
      29439502687316546488027 rank 4; F33's earlier independents: mean 5.8).
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

## OEIS (user submits from their own account; files in results/oeis/)
- [ ] A023050 b-file to 1e19 (310 terms).
- [ ] A293648, A293649, A293651 b-files (A293651: 14 missing terms).
- [ ] New sequences: coprime in >= 4 ways (1,748 terms to 2.5e23), >= 5 ways (12 terms to 2.5e23).
