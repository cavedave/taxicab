# TODO (running list; proofs to do are in experiments/mining/TODO.md)

## Runs
- [x] **lf36_v4 on 7of9** (F64: done and certified 8 Nov, no six-way, 31 new five-ways): complete line search, 23 cheapest directions (cost <= 1e4), n <= 1e36 exactly (~17 h; BOUND=1e35 ~8 h). New bowties -> bowtie_hunt.py curves.
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

## Six-way shapes (9 Nov 2026; FINDINGS F76-F77, paper Table tab:sixshapes)
- [ ] **Genus-1 curves on the two-line surfaces beyond the bowtie curves** (user wants to come back to this). Surface
      X: F_d1(s, r) = c F_d2(s', r') (smooth sextic in P^3, general type). No lines on X among the 23 base directions
      (F77). Next: fix one line's slope as a parameter T and view the other line as a point on an elliptic curve over
      Q(T) -- the method of Ono and Trebat-Leder, *The 1729 K3 surface* (refs/1510.00735v5.pdf).
- [ ] **Pell conics of equal sums (F82).** For Q = P + lambda (b, -a):
      (x + lambda b)^3 + (y - lambda a)^3 - x^3 - y^3 = lambda [3b x^2 - 3a y^2 + 3 lambda (b^2 x + a^2 y) + lambda^2 (b^3 - a^3)],
      so P, Q represent the same n iff P lies on an (indefinite, for ab > 0) Pell conic. Explains why the representations
      of a multi-way are pairwise linked by cheap chords (D-lines); basis for a correct model of free points and of the
      per-number six-way probability (replacing F78's random-square model, off by ~350x, F79).

### Methods to borrow: geometry-based computational searches (9 Nov 2026; PDFs in refs/shape/, see refs/INDEX.md; still missing: Elkies 1988, Swinnerton-Dyer 1968)
- **Elkies, "On A^4 + B^4 + C^4 = D^4", Math. Comp. 51 (1988) 825-835.** Found the counterexample to Euler's
  conjecture by searching an elliptic fibration of the K3 surface, with local conditions to prune. -> two-line
  surfaces (genus-1 curves; fibre the surface by one line's slope).
- **Swinnerton-Dyer, "A^4 + B^4 = C^4 + D^4 revisited", J. London Math. Soc. s1-43 (1968) 155.** Elliptic fibration of a
  quartic surface giving families of solutions. -> same.
- **Elkies, "Three lectures on elliptic surfaces and curves of high rank", arXiv:0709.2908.** Elliptic K3 surfaces,
  Neron-Severi rank, Shioda-Tate, specialisation: the toolkit for "which fibres have points". -> same; also with
  Ono-Trebat-Leder (refs/1510.00735v5.pdf).
- **Elkies, "Rational points near curves and small nonzero |x^3 - y^2| via lattice reduction", ANTS IV (2000).**
  Finds points close to a curve by lattice reduction. -> near-miss searches (near-lines, near-triangles, F67-F75).
- **Cremona, Fisher, Stoll, "Minimisation and reduction of 2-, 3- and 4-coverings of elliptic curves", Algebra &
  Number Theory 4 (2010).** Make quartics small before searching, so large-height points become small. -> the decider's
  seed problem (F65, F71: missed curves with points of height 7,349 and 224,967).
- **Bruin, Stoll, "Two-cover descent on hyperelliptic curves", Math. Comp. 78 (2009).** Prove a curve has no
  rational points. -> turning "no point found" into "no point exists".
- **Booker, "Cracking the problem with 33", Res. Number Theory 5 (2019); Booker, Sutherland, "On a question of
  Mordell", PNAS 118 (2021).** Sums of three cubes: x + y divides z^3 - k, a divisor-driven search. -> our s = x + y
  method (Theorem 5); speed ideas for count_bowties and the GPU search.
- **Elsenhans, Jahnel, "On the smallest point on a diagonal cubic surface", Exp. Math. 19 (2010) 181-193** (and their
  Tamagawa-number estimates). Point counts on diagonal cubic surfaces against Peyre's constant. -> x^3 + y^3 = u^3 + v^3
  is a diagonal cubic surface; our Pell conics (F82-F83) are its accumulating curves; Manin-Peyre counting of the points
  off them might predict the free-point exponent -0.24 (F84).
- **Heath-Brown, Acta Arith. 79 (1997) (refs/aa7913.pdf); Hooley, Math. Z. 82 (1963) (refs/Hooleybf01111429.pdf).**
  Already here: lines and structured families dominate the count of equal sums of two cubes. -> F82.
- **Bremner, "A geometric approach to equal sums of sixth powers", PLMS (1981)** (sixes/). Geometry of the surface
  guiding the search. -> same spirit.
