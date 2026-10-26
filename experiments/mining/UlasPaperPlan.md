# Ulas-style plan: infinite families and growth rates for coprime cabtaxi k-ways

Started 25 October 2026. Inspired by:
- M. Ulas, *On the Diophantine equation x³ ± y³ = aᵏ ± bᵏ*, arXiv:2402.06567v2 (`refs/ulas.pdf`);
- D. Curran, *Growth rates of solutions to x³ ± y³ = aᵏ + bᵏ* (`refs/growth.pdf`).

**The problem.** A coprime k-way is an n = x³ + y³ with at least k coprime representations, signs allowed
(A047697 counts them).

**Three goals:**
- **A.** Prove there are infinitely many n with k coprime representations: an Ulas-style theorem, aiming at
  k = 4.
- **B.** Measure how the number of k-ways below N grows with N, compare it with heuristics, and explain the
  gap using the line structure (FINDINGS F17, F18).
- **C.** Construct a six-way directly, as a six-point *structure* (two lines, or a bowtie plus a point, or
  three lines), instead of hoping a five-way picks up a sixth point by chance.

**Ground rule (as in FINDINGS):** stay experimental first. Claims of proof go into `TOPROVE.md` with their
status.

---

## What Ulas does (the template)

1. **Find a family in the data.** A shape repeats in the solution list (for example a = 3(2t+1)²). He fits
   polynomials to it and gets an identity in t.
2. **Reduce the hard part to an elliptic curve.** When no polynomial identity exists, he relaxes one term:
   b⁴ becomes B², so he only needs g₂(x) to be a square. That holds exactly when x is the coordinate of a
   rational point on E: y² = x³ + 62209x.
3. **Rank > 0 plus Hurwitz density.** E has rank 2, so E(Q) is infinite. E(R) is connected, so the rational
   points are dense, and infinitely many of them land in the interval where the signs come out right.
4. **Coprimality by hand.** Write u = pg, v = qg, w = r. Any common prime divisor of the solution divides 6,
   and a case analysis rules out 2 and 3.
5. **Counting:**
   - from a polynomial family: C(N) ≫ N^α, via the sum of φ(n) (his Corollary 2.2);
   - from an elliptic curve: only C(N) → ∞, with about (log N)^(r/2) expected (Silverman's height bound).

---

## A. Infinite families of coprime k-ways

### A0. What is already known (literature check, needed first)
- **k = 2:** infinitely many, classical (Euler's parametrisation of x³ + y³ = u³ + v³).
- **k = 3:** infinitely many coprime 3-ways should follow from the chord construction. Our F9 family
  (directions (3k², 3k² + 1)) gives three coprime representations for every k, verified to k = 10⁶ (N4).
  This is probably classical: Werebrusow 1905, Desboves 1879, Dickson vol. 2 ch. XXI.
- **k = 4:** is the infinitude of coprime four-ways known? **Not settled by Silverman 1993 (see below).**
  This decides whether A is a new result.
- **k ≥ 5:** Silverman (1982, Theorem A) bounds k by κ^(R+1) for cube-free n. His question whether
  sup N_f = ∞ is open and tied to unbounded ranks.

### A0b. What Silverman 1993 says (read 25 October 2026, `refs/taxiSilv.pdf`)
J. H. Silverman, *Taxicabs and sums of two cubes*, Amer. Math. Monthly 100 (1993) 331–340.
- **Many representations are easy without coprimality.** Take a rank-1 curve such as x³ + y³ = 7 with
  P = (2, −1). Clear the denominators of P, 2P, …, NP with B = d₁⋯d_N. Then x³ + y³ = 7B³ has at least N
  integer solutions.
  - Quantitatively: N(A) > c·(log A)^(1/3) for infinitely many A (Mahler 1935, exponent improved by
    Silverman 1983).
  - These n are far from cube-free, and the representations share large common factors. **Coprimality is
    the whole difficulty.** It is the same obstacle as Ulas's step 4, and the reason A047697 is hard.
- **Cube-free bound (Silverman 1982, his ref. 8):** N(A) ≤ c^(r(A)) for cube-free A, where r(A) is the rank.
  So many coprime representations force large rank. (This is our Theorem A already; Dem'janenko's
  conjecture.)
- **"Hall of Fame" in 1993:**
  - **"Any integers, 4 representations, cube-free: Unknown!"** Today A047697 and our exhaustive data give
    205 coprime four-ways ≤ 10¹⁷. So even the existence of a cube-free four-way was open in 1993.
  - Smallest positive cube-free three-way: Vojta 1983, 15170835645.
  - Smallest five-way (not cube-free): 1148834232. Added in proof: Rosenstiel, Dardis and Rosenstiel's
    6963472309248, Bull. IMA 27 (1991).
- **Not in the paper:** any infinitude statement for coprime or cube-free three-ways or four-ways. So the
  infinitude of coprime 3-ways (chord families) and 4-ways (A2) must be checked against later literature.
- **Useful exercise:** every solution of x³ + y³ = A has max(|x|, |y|) ≤ 2√(|A|/3). This is the same
  finiteness argument as our divisor count (s·t factorisation).
- **What to chase next for A0:**
  - Silverman 1983, *Integer points on curves of genus 1*, J. London Math. Soc. 28 (Mahler improvement);
  - Silverman 1982, *Integer points and the rank of Thue elliptic curves*, Invent. Math. 66;
  - Lang, *Elliptic Curves: Diophantine Analysis* (1978), p. 140 (Dem'janenko–Lang);
  - the Rosenstiel–Dardis–Rosenstiel paper (Bull. IMA 1991), which may contain parametric families;
  - OEIS A047697 and A080642 references, for post-1993 work on coprime/cube-free four-ways and infinitude.

### A0c. Silverman 1983, Guy D1, Karaatli et al. (read 26 October 2026)
- **Silverman 1983** (`refs/jlms%2Fs2-28.1.1.pdf`):
  - N_f(m) ≫ (log m)^(r/(r+2)) for infinitely many m, using a rank-r curve f = m₀z³;
  - for x³ + y³ this gives (log m)^(3/5) (a rank-3 curve);
  - the method is Mahler's: clear the denominators of rational points, so the representations share large
    factors. **Nothing about coprime solutions.**
- **Guy, UPINT, 3rd ed., D1** (pp. 209–213; djvu in `~/Downloads`):
  - **Coprime (cube-free) bound:** Silverman's N < c^(r(n)).
  - **"It is much harder to find these solutions."**
  - **Records listed:**
    - Vojta's positive cube-free 3-way;
    - Gascoigne and Moore's positive cube-free 4-way 1801049058342701083;
    - Rathbun's signed cube-free 4-way 16776487 (= A047697(4); our selftest value);
    - Bernstein's coprime 5-way 506433677359393.
  - **Bremner:** the ranks of x³ + y³ = Ta(n) are 2, 4, 5, 4 for n = 2…5.
  - **Hardy & Wright Thm 412:** arbitrarily many representations, not coprime.
  - **No statement anywhere that infinitely many coprime 3-ways or 4-ways exist, and no parametric
    family.** That strengthens the case that A (k = 4) is open, but a direct literature search is still
    needed: post-2004 papers; OEIS A047697 and A080642.
- **Karaatli, Keskin, Zhu 2014** (`refs/Karaatli.pdf`): every solution of an indefinite binary quadratic
  x² − 8B_n xy − 2y² = ±2^r, written as recurrence sequences (Pell, Pell–Lucas, balancing numbers).
  - **Relevance to A2/C2:** when the fourth-representation condition d² = P(t) has deg P = 2, the curve
    has genus 0. If P is indefinite, it is a Pell equation, so there are infinitely many t, given by a
    linear recurrence.
  - That would be the *cleanest* possible theorem: an explicit recurrence of four-ways (or six-ways), like
    the balancing-number families here.
  - **Add to the genus survey:** look first for degree-2 cases (s of degree 1 in t).

### A1. Ulas step 1: mine our four-ways for recurring shapes
- **Data:** 205 exhaustive four-ways ≤ 10¹⁷ (`results/fourways.md`, scratchpad `cab2_1e15.txt` and
  `cab4_1e15_1e17.txt`) plus 113 from the hero7 run (`hero7_multi.txt`).
- **Look for** coordinates or line parameters (a, b, c, slope r/s) of the form m·t² or m·t⁴, polynomial in a
  small parameter, repeated across several four-ways. This is like his a = 3(2t+1)² and the m·w⁴ rays in
  `growth.pdf` §5.1.
- **Already tried:** polynomial-family mining of the 204 (F-series), and the F9 family. F9 has three
  representations but never four (N4).

### A2. Ulas step 2: the elliptic-curve route to four-ways
1. **Fix a cheap direction (a, b).** The collinear coprime triples on a·x + b·y = c are rationally
   parametrised (the conic X² + XY + Y² = 3ab³, slope r/s). So n(t) = x(t)³ + y(t)³ is a polynomial with
   three representations built in.
2. **A fourth representation** needs s | n(t) with (4n/s − s²)/3 = d². Take s(t) from the polynomial factors
   of n(t), times constants. The condition becomes **d² = P(t)**, a hyperelliptic curve.
3. **Genus count** (P generic of degree 2·deg s, so genus ≈ deg s − 1):
   - deg s ≤ 2 gives genus ≤ 1: the useful case;
   - higher degree gives genus ≥ 2, which has finitely many points by Faltings: a dead end.
4. **For each genus-1 case:** put it in Weierstrass form, then compute torsion, rank (`ellrank`) and
   generators. Rank > 0 together with density (as in step 3 above) gives infinitely many t, hence
   infinitely many four-ways, **provided** the coprimality argument works.
5. **Two-parameter freedom.** Direction and slope give a surface. Choosing the free point's s as a
   polynomial in both parameters may give a pencil of genus-1 curves, from which we pick one with positive
   rank. This is the analogue of Ulas's E_d: y² = x³ + (243d⁸ + 1)x.
6. **Check for side results:**
   - **F9:** its polynomial s choices give genus 2 and 3, so only finitely many fourth representations
     come from polynomial divisors. A partial explanation of N4, not a proof: non-polynomial divisors
     remain.
   - **The bowtie (five-ways):** two lines sharing a hub. Parametrising both lines and asking for one
     shared n gives a curve; compute its genus too. If it is genus 1 with positive rank, then infinitely
     many coprime five-ways follow. That is a long shot.

### A3. Coprimality and positivity
- Coprimality of each representation: gcd(x, y) = 1, with common prime divisors reduced to 2 and 3 as Ulas
  does.
- The four representations must be distinct and non-trivial (no swaps, no sign-flip duplicates).
- For taxicab-type positive results (cube-free Ta(4), A080642), we also need the real-interval condition.
  This is Ulas's sets A₁ and A₂: Hurwitz density puts infinitely many points in any interval.

### A4. Expected output
- A theorem: "there are infinitely many n with at least four coprime representations", with an explicit
  curve and generator, and an example n produced by the construction (checked with `collisions.all_reps`).
- If it is already known (A0): the method is still useful for k = 5 (A2.6), and for Conjecture C1–C3 in
  `TOPROVE.md`.

---

## B. Growth rates of k-ways

### B1. Data in hand (exhaustive, cumulative counts)

| N | 2-ways | 3-ways | 4-ways |
| --- | ---: | ---: | ---: |
| 10⁹ | 3,208 | 106 | 2 |
| 10¹¹ | 24,100 | 523 | 7 |
| 10¹³ | 168,815 | 2,649 | 25 |
| 10¹⁵ | 1,123,072 | 12,767 | 91 |
| 10¹⁷ | — | — | 205 |
| per decade | ×2.6 | ×2.2 | ×1.5–2 |
| exponent | ≈ 0.41 | ≈ 0.34 | ≈ 0.2 |

Five-ways: 11 up to 10²³ (exhaustive, A047697 runs).

### B2. Heuristics to compare
- **Naive (Wagstaff-style):** there are about N^(2/3) coprime sums below N, so the k-ways number about
  N^((3−k)/3):
  - 2-ways N^(1/3);
  - 3-ways log N;
  - 4-ways **finitely many**;
  - 5-ways finitely many.
- **Observed:** much more for k ≥ 3, so the naive model is wrong there.
- **Geometric reading:**
  - the variety of (k+1)-tuples with equal sums is a complete intersection of k cubics in P^(2k+1), with
    K = (3k − 2k − 2)H = (k − 2)H;
  - k = 1 (two-ways): Fano and rational (Euler);
  - k = 2 (three-ways): Calabi–Yau, the borderline;
  - k = 3 (four-ways): general type.
  - Bombieri–Lang then predicts the points concentrate on special subvarieties. **Conjecture: those are our
    lines** (F17: three-ways 87% collinear, four-ways 90% line + free point).
- **To derive:** a count of collinear coprime triples with n ≤ N (directions × slopes, using the
  line_enum parametrisation). It should predict the three-way exponent (≈ 1/3?) and its constant. The aim
  is a check like `growth.pdf`'s 21,930 predicted against 22,209 found.
- **Four-ways:** about (number of three-ways) × (chance that a free point fits). Predict the exponent ≈ 0.2
  from the local densities (split primes, F1).

### B3. Provable pieces
- **A lower bound** "3-ways ≫ N^c" from a polynomial family, by the sum of φ, as in Ulas Cor. 2.2. Easy.
- **Upper bounds** are hard: probably out of reach, so note them only.

### B4. Work
1. Extend the cumulative counts:
   - 3-ways to 10¹⁷: cheap on 7of9 with `cabtaxi.cpp --kmin 3`;
   - 4-ways to 10¹⁹ or more, from the next GPU run with KMIN=4.
2. Fit local exponents per decade and check whether they settle down (like `growth.pdf` Fig. 2's ratio
   plot).
3. Implement the collinear-triple count model and compare it with the three-way counts.
4. Split the observed k-ways into collinear and non-collinear, and fit growth separately. Does the
   non-collinear part follow the naive heuristic?

---

## C. Constructing a six-way from its structure (added 26 October 2026)

### C0. Why the line search alone is unlikely to reach a six-way
- **The cost of one more representation grows with k.** Ratios of four-ways to five-ways:
  - exhaustive data ≤ 10¹⁷: 205 : 1;
  - directions 501–1000: 280 : 2;
  - hero7 run (F24): 113 : 4.

  Each extra representation costs 2–3 more split primes (F1). The step from five to six is likely at least
  as hard: about 100–300 five-ways per six-way.
- **We have 19 five-ways**, and the yield per tranche is falling (directions 1–200: 9; 201–500: 3; 501–1000:
  2). The cheapest seam is largely mined.
- **Conclusion:** "five-way plus a lucky sixth point" needs roughly 10× more five-ways than we have. That is
  not a Mac-scale task.

### C1. Six-point structures
On x³ + y³ = n, three points are collinear exactly when they sum to zero (flex origin; −P is the swap).
Five-ways are bowties: two lines sharing a hub, 3 + 3 − 1 points (17 of 18). Six-point candidates:

| structure | condition | points |
| --- | --- | ---: |
| two disjoint lines | P₁ + P₂ + P₃ = 0, Q₁ + Q₂ + Q₃ = 0 | 6 |
| bowtie plus a free point | as for a five-way, plus one more | 6 |
| three lines through shared points (a triangle) | three collinear triples pairwise sharing a point | 6 |
| a line plus a "double hub" | two hubs on one line, each with a second line | 7 |

First, measure which of these appear among taxicab and cabtaxi six-ways that are **not** coprime
(`results/sixways.csv`, `k5plus.csv`, curve point sets). There, six-ways exist, so we can see which
structure nature uses.

### C2. Building the structure as a curve problem (the Ulas route again)
- **The obstacle:** the census of 60.9M lines found only one n on two cheap lines (Bernstein's). So a second
  line must be paired with the first *by construction*, not found by coincidence.
- **The method:**
  1. Parametrise line 1 in a cheap direction (a, b), with slope parameter t. Then n = n₁(t) is a polynomial.
  2. Ask that n₁(t) also carry three collinear points in a second direction (a', b'). Equivalently, n₁(t)
     equals n₂(u) for the second direction's parametrisation: one equation in (t, u).
  3. For the bowtie-plus-point and triangle cases, add the shared-point condition. This lowers the degree
     and is where the hub structure helps.
  4. Compute the genus of the resulting curve.
     - **Genus 0 or 1 with positive rank:** a family of n carrying the structure, hence infinitely many
       six-ways (subject to coprimality, as in A3).
     - **Genus ≥ 2:** finitely many points (Faltings), so search it directly but expect little.
- **A cheaper first test:** fix line 1 as a cheap line, and line 2 through a given hub point in every
  direction. For each n from line 1, the second line exists exactly when the exact count finds it. This is
  what the line search already does implicitly. Record which second-line directions occur in the 19
  five-ways, to see whether they concentrate (F20's hub chords).

### C3. Data needed
- The line pairs (directions, slopes) of all 19 five-ways (from `fives_geometry.py`), and of the non-coprime
  six-ways in `results/sixways.csv` (decompose their points into lines the same way).
- PARI `genus` and `ellrank` calls for each candidate curve (Mac).

### C4. Expected output
- Either an explicit curve of genus ≤ 1 and positive rank whose points give six coprime representations (a
  six-way, and possibly infinitely many),
- or a proof-sketch that every six-point structure gives genus ≥ 2 (which would explain why coprime six-ways
  are so rare: a negative result worth a FINDINGS entry).

## What I need from you
- **Papers:**
  - ~~J. H. Silverman, *Taxicabs and sums of two cubes* (1993)~~: received and read (A0b). It does not settle
    infinitude; follow its references above;
  - ~~C. Hooley, *On the representations of a number as the sum of two cubes*, Math. Z. 82 (1963)~~:
    received (`refs/Hooleybf01111429.pdf`), read 26 October 2026.
    - **Theorem 1:** Σ_{n ≤ x} r(n)² = (diagonal term ≍ x^(2/3)) + O(x^(5/9) (log log x)^c / (log x)^c′), for
      **non-negative** cubes.
    - **So:** the number of 2-ways up to x is O(x^(5/9+ε)), and almost all sums of two cubes have a unique
      representation (Theorem 2, N(x) asymptotic).
    - **Method:** the off-diagonal term reduces to representations by binary quadratic forms 3r's² − 3ρ'σ²
      (Gauss's bound on representations), plus a sieve over primes p ≡ 5 (mod 6). The same s·t
      factorisation we use.
    - **For B:** gives the first rigorous upper exponent for 2-ways, 5/9 ≈ 0.556. Our observed signed 2-way
      exponent is ≈ 0.41, the heuristic is 1/3. Check whether later work lowered 5/9.
  - **Received 26 October 2026** (full inventory in `refs/INDEX.md`):
    - D. R. Heath-Brown, Acta Arith. 79 (1997) (`refs/aa7913.pdf`). Corollary: at most O(x^(4/9+ε)) n ≤ x
      with ≥ 2 representations (non-negative cubes). He also quotes Hooley's lower bound ≫ x^(1/3) log x.
      **For B:**
      - the true 2-way exponent lies between 1/3 (with a log factor) and 4/9;
      - x^(1/3) log x has local exponent 1/3 + 1/ln x ≈ 0.37 at x = 10¹³;
      - our signed coprime count shows ≈ 0.41.
      Also: "rational lines dominate the point count" is his starting point. That is the surface-level
      version of our line picture.
    - T. D. Wooley, *Sums of two cubes*, IMRN 1995 (`refs/1995 T3P.pdf`, already in the repo): elementary
      proof of Hooley's bound via 3 coplanar lines.
    - J. H. Silverman, Invent. Math. 66 (1982) (`refs/Thuebf01389220.pdf`, already here): Theorem A.
    - J. H. Silverman, *The Arithmetic of Elliptic Curves*, 2nd ed. (`~/Documents/sixes/Silverman.pdf`, already
      on disk): ch. VII for TOPROVE 11, ch. IX for integer points.
    - Elkies–Rogers, *Elliptic curves x³ + y³ = k of high rank* (`refs/elkies_rogers_2004_math0403116.pdf`):
      relevant to C.
  - **Still wanted:**
    1. Rosenstiel, Dardis, Rosenstiel, Bull. IMA 27 (1991) 155–157 (C).
    2. ~~Silverman 1983~~, ~~Guy D1~~: received, A0c.
    3. Optional: Lang, *Elliptic Curves: Diophantine Analysis* (1978) p. 140; OEIS A047697 and A080642
       references.
- **Already have:** the graph-making code from `growth.pdf` (cumulative count against N, ratio-to-prediction
  plots, as in its Figures 1–2). Reuse it for B, so that both papers have the same look.
- **Compute:** 7of9 time for B4.1 (3-ways to 10¹⁷). The rest runs on the Mac.
- **Decisions:**
  - whether A or B is the paper, or both;
  - whether it extends `growth.pdf` or is a separate note.

## Order of work
**Status: plan only. Nothing run yet (on hold at the user's request, 25 October 2026).**

1. A0 literature check: Silverman 1993 done (A0b). Chase the post-1993 references listed there.
2. B1–B2: fit exponents and build the collinear-count model. Mac, under an hour.
3. A2: genus survey of fourth-representation conditions on cheap directions, then PARI ranks for the
   genus-1 cases.
4. A1: shape mining of the 318 four-ways.
5. C1: classify the line structure of the 19 five-ways and of the non-coprime six-ways.
6. C2: set up the two-line curve for the commonest structure, compute its genus, and run rank checks.
7. Write up: a FINDINGS entry per result; proofs to `TOPROVE.md`.
