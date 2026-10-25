# Findings: mining coprime cabtaxi k-ways (A047697 family)

Observations only, each with its dataset and coverage. Nothing here is proved; proofs go in `TODO.md`.

## Datasets

| tag | content | coverage |
| --- | --- | --- |
| `cab2_1e15` | every n ≤ 10¹⁵ with k ≥ 2 coprime signed representations (`cabtaxi.cpp`, Mac, 4 threads, about 10 min). Counts: k=2 1,110,305; k=3 12,676; k=4 90; k=5 1 | exhaustive to 10¹⁵ |
| `ctrl_1e15` | every coprime sum in (10¹⁵, 10¹⁵ + 10¹¹]: 538,064 numbers (k=1 538,021, k=2 43) | exhaustive window |
| `fives` | the 11 coprime five-ways ≤ 10²³ | exhaustive to 10²³ |

## F1 (25 October 2026): feature trends by k, band 10¹³–10¹⁵

Groups: 20,000 sampled k=1 (window just above 10¹⁵), 20,000 sampled k=2, all 10,052 k=3, all 65 k=4. The
11 five-ways are shown for reference but cover 10¹⁵–10²².

| k | split primes (mean) | 7 \| n | n ≡ ±2 (mod 9) | 3 \| n | no non-split prime |
| ---: | ---: | ---: | ---: | ---: | ---: |
| 1 | 3.34 | 38% | 25% | 25% | 15% |
| 2 | 5.37 | 59% | 13% | 24% | 41% |
| 3 | 5.91 | 70% | 1% | 32% | 44% |
| 4 | 6.86 | 82% | 0% | 12% | 71% |
| 5 | 8.73 | 91% | 0% | 0% | 82% |

- **Tier A, explained:** 38% of all coprime sums are divisible by 7. Cubes mod 7 are {0, ±1}, and 18 of the 48
  coprime residue pairs give a³ + b³ ≡ 0, which is 37.5%.
- **Tier B, rising with k:** the number of split primes, 7 | n, and the share of n with no non-split prime.
- **Tier B, falling with k:** n ≡ ±2 (mod 9). It vanishes by k = 3.
- **Odd, not yet explained:** 3 | n rises from k = 2 to 3, then falls. The samples for k ≥ 4 are small.
- **TODO theorem measured:** in 100% of about 50,000 numbers, every prime ≢ 1 (mod 3) dividing n divides
  s = x + y in every representation.

**Working explanation (to be tested):** local densities, as in the Hardy–Littlewood singular series.
- A split prime p dividing n gives about 3(p − 1) solutions of a³ + b³ ≡ 0 (mod p), against about p for a
  typical residue: roughly a factor of 3.
- p ≡ 2 (mod 3) gives no factor, because cubing is a bijection mod p.
- n ≡ ±1 (mod 9) has twice the 3-adic density of n ≡ ±2 (mod 9).

**Next:** compute each n's exact local density and test a Poisson model against the exact counts up to 10¹⁵.

## F2 (25 October 2026): "hard" absences and the root number, by k

- **Method:** `hard_patterns.py` lists residues of n that are common among one-ways but never seen among
  k-ways (only when chance predicts at least 8), and per-representation statements ("all", "at least one",
  "no rep") that hold for every n in a group.
- **Steep slopes:**
  - **even n:** 33.5% (k=1) → 15.1% → 0.6% (76 of 12,676 three-ways) → 0/90 → 0/11.
  - **n ≡ 2 (mod 3), split by n mod 9:**

    | k | ≡ 1 | ≡ 8 | ≡ 7 | ≡ 2 |
    | --- | ---: | ---: | ---: | ---: |
    | 1 | 134,381 | 133,826 | 67,509 | 67,569 |
    | 2 | 454,115 | 241,531 | 96,217 | 45,858 |
    | 3 | 5,915 | 2,713 | 92 | **5** |
    | 4+ | 69 | 11 | 0 | 0 |

    From k = 2 on, n ≡ 1 beats n ≡ 2 (mod 3) about 2:1. **Reason:** t ≡ 1 (mod 3) and products of split
    primes are ≡ 1 (mod 3), so n ≡ 2 (mod 3) needs a prime ≡ 2 (mod 3), which gives no local boost.
  - **residues mod 7 and mod 13:** these follow the cubic-residue classes. Residues that are cubes (mod 7:
    1, 6; mod 13: 1, 5, 8, 12) vanish fastest.
- **Root number of x³ + y³ = n:** +1 for 48% (k=1) → 53% → 55% → 78% (k ≥ 4) → 82% (k = 5). It is almost
  entirely fixed by n mod 9 and the parity of the number of primes ≡ 2 (mod 3) dividing n, for example:

  | n mod 9 | odd number of p ≡ 2 (mod 3)? | +1 | −1 |
  | --- | --- | ---: | ---: |
  | 1 | no | 1,047 | 19 |
  | 8 | yes | 13 | 563 |

  The two five-ways containing 5 are exactly the two with −1. This is the Birch–Stephens formula; the few
  exceptions are probably from 3-adic or square factors.

## F3 (25 October 2026): taxicab five-ways against six-ways, at the level of curves (`taxicab_5v6.py`)

- **Data:** `results/k5plus.csv` (b9) and `results/sixways.csv` (b12): 21,215 taxicab (positive) five-,
  six- and seven-ways, each rebuilt in full (the seed pairs × m plus the new pairs) and checked exactly.
- **All 21,215 lie on only 60 curves** x³ + y³ = M (M = the cube-free part of N). Everything else is
  scaling.

| best k on the curve | curves | rank | split primes in M (mean) | M has a prime ≡ 2 (mod 3) |
| --- | ---: | --- | ---: | ---: |
| 5 | 50 | 3–6, mostly 4–5 | 4.5 | 11 / 50 |
| 6 | 9 | 4 4 5 6 6 6 6 6 6 | 5.7 | 1 / 9 |
| 7 | 1 | 7 | 7 | 0 / 1 |

- **The rank tracks k,** but is not a hard rule. Two six-way curves have rank 4 (M = 222859 and 6813163), so
  some of their representations are combinations of others.
- **Denominators** of the points on six-way curves are dominated by 2, 3, 5 and 7, which keeps g (and so N)
  small.
- **Cross-check:** 564185788777, the closest near-miss in the split-prime curve hunt, and 222859, the
  closest in the 25 October scan, are both six-way curves here.
- **Known theory:** Silverman (Invent. Math. 66, 1982, "Integer points and the rank of Thue elliptic curves";
  summarised in `refs/silverman_1993_taxicabs_sums_two_cubes.pdf`) proves N(A) < c^r(A) for cube-free A:
  many integer points force high rank. This applies directly to coprime cabtaxi k-ways, which are k integer
  points on a cube-free curve.
- **Coprime five-ways (A047697):** Bernstein's 506433677359393 has rank exactly 4 (root number +1). The
  other ten are being computed.

## F4 (25 October 2026): the representations come in collinear triples (exact)

On x³ + y³ = n the origin (1 : −1 : 0) is a flex, so P + Q + R = 0 exactly when the three points are
collinear, and −P is P with x and y swapped.

- **Five-ways: exact relations** (`coords5.py`). PARI generators were found, every point was written as an
  exact integer combination of them (verified with exact point arithmetic), and the relations were read off
  as an exact integer kernel. On 10 of the 11 curves (one run did not finish):
  - 9 curves: the 5 points span rank **3**, with **two** relations. The curve ranks are 3, 4 or 6, so the
    points do not use all of the rank.
  - 137904678696613339: span rank **4**, one relation.
  - **Every relation has exactly three nonzero coefficients, each ±1**, for example P₁ + P₂ − P₄ = 0: three
    collinear integer points, allowing swaps.
- **Census by k** (exact 3×3 determinant test over all swap choices):

  | k | numbers with at least one collinear triple | number of triples |
  | --- | --- | --- |
  | 3 | 10,969 / 12,676 (86.5%) | 1 |
  | 4 | 85 / 90 (94%) | 1 |
  | 5 | 11 / 11 | 2 in ten cases, 1 in one |

- **The five-way shape:** in all ten with two triples, the two lines share exactly one point (a "bowtie": 5
  points on 2 lines through a common point).
- **Interpretation:** most multi-representations arise because the line through two integer points meets
  the curve again at an integer point. This is global structure that local densities do not explain.
- **Six-way candidates:** a triangle (3 lines, 6 points, 3 relations), a bowtie plus one point, or three
  concurrent lines (7 points). This suggests a targeted search over line configurations.
- **Open:** the 13.5% of three-ways and 5 four-ways with *no* collinear triple. Are they a separate
  mechanism?

## F5 (25 October 2026): every k ≥ 3 relation up to 10¹⁵ is a line, a hub, or nothing (exact, `relations.py`)

All 1,712 coprime k ≥ 3 numbers ≤ 10¹⁵ without a collinear triple, plus 300 random collinear three-ways,
were run through exact relations (generators, exact coordinates, `matkerint`). All 2,012 were verified.

| group | span | relations | curve rank |
| --- | --- | --- | --- |
| collinear three-ways (300 sampled) | 2 | P + Q + R = 0 (a line), in all 300 | 2: 36%, 3: 43%, 4: 12%, 5–6: 1%, bounded: 8% |
| non-collinear three-ways (all 1,707) | 3 | none | 3: 13%, 4: 60%, 5: 18%, 6: 6%, 7: 12 curves, 8: 2 curves |
| non-collinear four-ways (all 5) | 4 (2 of them), 3 (3 of them) | P₁ ± P₂ ± P₃ ± P₄ = 0 in 3 cases | 4 or 6 |

- **No tangent relations** (no coefficient 2) and no other shapes: only 3-term ±1 (a line through three
  integer points) and 4-term ±1.
- The 4-term relation P₁ + P₂ = −(P₃ + P₄) means lines P₁P₂ and P₃P₄ meet the curve again at the **same
  rational "hub" point**, which is not itself a representation.
- **Mechanisms up to 10¹⁵:**
  1. collinear integer triples (cheap: rank 2 is enough);
  2. two lines through a shared rational hub (rare);
  3. independent points (needs rank ≥ 3, usually 4).
- The five-way bowties (F4) are mechanism 1 twice.

## F6 (25 October 2026): the lines behind collinear triples have small, concentrated directions

- **The lines in the five-ways:** the 22 lines a x + b y = c have |a|, |b| ≤ 3,081, with c large. (3, 4)
  and (16, 21) each appear in two different five-ways.
- **All 10,969 collinear three-ways ≤ 10¹⁵:**
  - direction size max(|a|, |b|): median 36, 90% ≤ 304, 99% ≤ 793, maximum 2,353;
  - most common directions: (3, 4) 1,639; (4, 3) 358; (12, 13) 330; (7, 4) 296; (4, 1) and (1, 4) 272 each;
    (4, 7) 195; (27, 28) 160. Note that 3³ + 4³ = 91 = A047697(2).
  - growth: 894 below 10¹², 2,051 below 10¹³, 4,752 below 10¹⁴, 10,969 below 10¹⁵, about ×2.3 per decade.
    That extrapolates to about 5 × 10⁷ up to 10²⁵.
- **Consequence:** for a fixed direction, the triples on parallel lines a x + b y = c come from the rational
  points of one conic (the first two Vieta sums of the cubic on the line do not depend on n), rescaled by c.
  A line-based search can enumerate collinear triples directly and look for collisions in n:
  - two triples on one n sharing a point give a five-way (bowtie);
  - two disjoint triples, or three lines, give a six-way.
  It reaches n far beyond brute force, but only covers the line mechanism (F5), so it cannot prove absence.

## F7 (25 October 2026): three positive points are never collinear, so sums alone cannot use lines

- **Data (all k ≥ 3 ≤ 10¹⁵):**
  - collinear triples by number of sums among the three points: 0 sums 3,750; 1 sum 3,535; 2 sums 3,771;
    **3 sums: 0**;
  - all 25 coprime three-ways whose representations are all sums are of the independent kind (F5,
    mechanism 3).
- **Reason (easy to prove; TODO 4):** the region x³ + y³ ≤ n with x, y ≥ 0 is convex, so a line meets the
  positive arc at most twice.
- **Consequences:**
  - cubefree taxicab k-ways (A080642, all sums, coprime) need k independent points, so rank of about k.
    That explains why cubefree Ta(4) = 1.8 × 10¹⁸ but A047697(4) = 1.7 × 10⁷.
  - The line-collision search cannot find cubefree records; those need high-rank curves (Elkies–Rogers).
  - For curve bounds, Ca(k) (signed points) can use collinear configurations but Ta(k) (positive points)
    cannot. That plausibly explains why the same record curve reaches Ca(70) but only Ta(31).

## F8 (25 October 2026): a family of line directions (3k² + 1, 3k²) carries a quarter of all collinear triples

- **Counts** over all 11,056 collinear-triple lines in coprime k ≥ 3 numbers ≤ 10¹⁵, with directions folded
  up to sign and mirror:
  - (4, 3): 2,022 (rank 1); (13, 12): 345 (rank 4); (28, 27): 163 (rank 6); (49, 48): 95 (rank 13);
  - (76, 75), (109, 108), (148, 147): 20–29 each (ranks 40–57);
  - k = 8 to 15 are all present, with 1–11 each.
  - **Family total: 2,745 lines (24.8%).**
- **Other near-diagonal directions (m + 1, m)** outside the family: m = 36 (65 lines), 63 (44), 111 (29),
  156 (23), 171 (21), … Possibly a second family.
- **By k:** (3, 4) carries 18% of three-way lines but 24 of 85 (28%) four-way lines, and 2 of 21 five-way
  lines.
- **(16, 21)** appears in 2 of 21 five-way lines but is unremarkable elsewhere: rank 17 among three-ways and
  1 of 85 four-way lines. Possibly chance.
- **Hypothesis:** a polynomial identity in k (and further parameters) produces collinear integer triples on
  lines of direction (3k² + 1, 3k²).
  - Literature to check: Ramanujan's two-cube identities (Hirschhorn, "An amazing identity of Ramanujan",
    Math. Mag. 1995, and related papers); Euler's parametrisation of a³ + b³ = c³ + d³.
  - Experimental route: fit polynomials to the triples on (13, 12) and (28, 27).

## F9 (25 October 2026): the identity behind the (3k², 3k² + 1) lines, reverse-engineered and verified

Fitting polynomials in k to the c = D lines (D = a² + ab + b² = 27k⁴ + 9k² + 1) gives, for every integer k:

    (27k⁴ + 6k² + 1)³ − (27k⁴ + 6k²)³
      = (9k³ + 6k² + 1)³ − (9k³ − 3k² + 3k)³
      = (9k³ + 3k² + 3k)³ − (9k³ − 6k² − 1)³
      = (9k² − 3k + 1)(9k² + 3k + 1)(27k⁴ + 9k² + 1)

- All three points lie on the line 3k² x + (3k² + 1) y = 27k⁴ + 9k² + 1 (checked symbolically in PARI).
- k = 1 gives 3367 = A047697(3); k = 2 gives 625177; k = 3 gives 15072967.
- The three norm-form factors are products of split primes, which is consistent with F1.
- **Not yet explained:** the lines of the same direction with c = q·D, where q = 7, 13, 19, 31, 37 are
  Eisenstein norms. They suggest a second parameter (an Eisenstein integer of norm q). Most of them do not
  contain a point of the form (−t, t + 1).
- **Side check (size-confounded):** n = 3t² + 3t + 1 makes up 0.17% (k=1, at 10¹⁵), 0.76% (k=2), 1.2% (k=3),
  1/204 (k=4) and 0/11 (k=5).
- **Literature:** compare with Ramanujan–Mahler (9k⁴)³ + (3k − 9k⁴)³ + (1 − 9k³)³ = 1, Hirschhorn's papers,
  and the Lost Notebook. It may be classical.
- **OEIS (user, 25 October 2026):** t(k) = 27k⁴ + 6k² = 3k²(9k² + 2) = A014820(3k − 1), i.e. A014820's
  m²(m² + 2)/3 at m = 3k (16-cell numbers; 4 × 4 pandiagonal magic squares). Only every third term gives a
  three-way: t = 8 gives n = 217, a two-way only. This matches the derivation (3a must be a square), so the
  link is almost certainly a coincidence of polynomial form.
- **Mahler's identity** (9t⁴)³ + (3t − 9t⁴)³ + (1 − 9t³)³ = 1, his 1936 counterexample to Hypothesis K for
  cubes (J. London Math. Soc. 11), has the same 9t³ and 9t⁴ ingredients. F9 may be a relative. Noted via
  Pliego, arXiv:2010.14536, which is otherwise about Waring's problem for sums of three cubes and does not
  treat these curves.
- **Mahler 1936, read (refs/mahler040.pdf):** his identity comes from the classical parametrisation of
  x³ + y³ + z³ = u³ with ρ = f² + 3g² and ρ′ = f′² + 3g′² (Dickson, *History* vol. 2, p. 555), taking
  f′ = 1, g′ = 0, f = 3g. It shares the norm form w² + 3v² with F10, but has no three-collinear-point
  structure. Each *pair* of F9 representations is a case of Euler's equation, but the line family and the
  direction rule are not in Mahler.
  - Definitive check still to do: Dickson's *History of the Theory of Numbers*, vol. 2, ch. XXI (free on
    archive.org).
- **A399025** (squares on a grid) is A014820 again at even indices: the same polynomial, a coincidence.

## F10 (25 October 2026): which line directions are rich, a predictive rule

**Derivation.** On a x + b y = c, eliminating one root from the two Vieta equations (which do not involve n)
leaves the conic

    w² + 3v² = 12 · a · b³ · c² / (b³ − a³)²

so integer triples need a·b to be a value of w² + 3v² (a norm from Z[ω]).

**Empirical rule** (11,155 lines, 2,605 directions, all coprime k ≥ 3 ≤ 10¹⁷; 0 exceptions):

- a·b > 0, and every prime ≡ 2 (mod 3) in a·b has an even exponent (the norm condition);
- a·b is even. The 2-adic valuations seen are 2, 4, 6, 8 and 10; never 0, and no line has a and b both odd.
  This rules out the cheapest-looking directions (1, 2), (2, 3), (1, 3), (3, 7), …;
- richness falls with the cost |b³ − a³|.

**Predictive check:** of the candidate directions under the rule, ordered by cost, all 23 with cost < 10⁴ and
all 80 with cost < 10⁵ appear in the data, as do 306 of 308 with cost < 10⁶. Observed line counts roughly
follow the cost order:

| direction | (3, 4) | (1, 4) | (4, 7) | (12, 13) | (4, 9) | (7, 12) | … |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | --- |
| lines | 2,046 | 546 | 498 | 348 | 102 | 187 | … |

- **Why 16 recurs:** 2⁴ is the next cheapest way to give a·b the required even power of 2 ≥ 2. Hence (13, 16),
  (9, 16), (7, 16), (3, 16), (1, 16), (16, 19), (16, 21), (16, 25).
- **Not yet seen** (expensive, probably above 10¹⁷): (4, 79), (100, 121), (36, 121), (16, 121), (4, 121),
  (3, 124), …
- **The (3k², 3k² + 1) family (F8/F9):** it always passes, since a·b = 3k²(1 + 3k²) and 1 + 3k² = 1² + 3k²,
  and it has the smallest cost among near-diagonal directions.
- **Literature checked (25 October 2026):** Hirschhorn 1995 and 1996, Ono & Trebat-Leder 2016 ("The 1729 K3
  surface"), and *Ramanujan's Lost Notebook IV* §8.5. All treat two-way equalities (Euler/Ramanujan
  parametrisations, near-misses a³ + b³ = c³ ± 1). None contains the three-point line family of F9 or this
  rule. Ramanujan's k(T) = 6³(3T² − 3T + 1)(T² + T + 1)(T² − 3T + 3) has the same product-of-norm-forms shape
  as F9's n(k).

## F11 (25 October 2026): lines and n share a divisor; the second parameter is a point on a fixed conic

- **E = a² + ab + b² divides c, and E divides n**, for all 11,176 lines (coprime k ≥ 3 ≤ 10¹⁷ and the
  five-ways). There are no exceptions.
  - **Why:** the root sum is −3a²c/(b³ − a³), with b³ − a³ = (b − a)E, so E | c (up to a factor of 3). The
    root product then gives E | b³n, so E | n. (TODO 8.)
- **q = c/E is not restricted:** only 69% are norms (values such as 23 are common), because c enters the conic
  squared. For a fixed direction the conic w² + 3v² = 12ab·(square) is fixed. Its rational points form a
  one-parameter family r/s, and q only clears denominators. **So the line enumeration is direction (a, b) ×
  coprime (r, s).**
- **Five-way bowties:** 8 of 10 shared points are differences and 2 are sums. The two directions are unrelated
  apart from both E dividing n. gcd(E₁, E₂) = 1 in 7 cases; otherwise 349, 409, 61.
- **A per-n line finder follows:** for a given n, take the divisors E of n that are norms, write each as
  a² + ab + b² (keeping a·b even and a norm), and solve the conic for each direction. That gives all collinear
  triples of n without enumerating its representations.

## Literature status after Dickson vol. 2 (25 October 2026; refs/historyoftheoryo02dickuoft.pdf, ch. XXI p. 562)

- **The chord (line) construction is classical.** Werebrusow (L'intermédiaire des math. 1905; Matem. Sbornik
  27, 1909) gives the third representation from two: x₂ = (x₁²y − x²y₁)/(xy − x₁y₁),
  y₂ = (xy₁² − x₁y²)/(xy − x₁y₁). On 3367, (15, −2) and (−9, 16) give (−33, 34), our collinear triple.
  Fauquembergue: it follows from an identity of Desboves (Nouv. Ann. Math. 1879).
- **Werebrusow's general solution** of x³ + y³ = x₁³ + y₁³ = x₂³ + y₂³ is parametrised with
  M² + MN + N² = 3ω²φψ, the same norm form as F10. So the F10 norm condition is probably implicit there.
- **Attribution:**
  - **classical:** the line mechanism and the norm-form parametrisation;
  - **apparently not in the literature:**
    - the quantitative census (F4/F5: 87% of coprime three-ways collinear, five-ways = bowties, only lines,
      hubs or independent points, no tangents);
    - the evenness condition and the predictive cost ordering of directions (F10);
    - E | n and the per-n line finder (F11);
    - the explicit k-family F9 (probably a special case of Werebrusow).
- Also in Dickson p. 562: Gérardin's "least" three-sum solution 560, 70 / 552, 198 / 525, 315 (not coprime),
  and Fauquembergue's multiple representations of 19 × 363510³ via Cauchy's formulas.

## F12 (25 October 2026): the line enumerator works, and finds a new coprime five-way beyond 10²³

- **Tool:** `line_enum.py`. For each allowed direction (a, b), in F10 cost order, take one rational point of the
  conic X² + XY + Y² = 3ab³ (PARI `qfsolve`), sweep the lines through it with slopes r/s (|r|, s ≤ H), turn
  each point into a primitive collinear triple, and keep the coprime ones.
  - Every output triple is checked exactly: x³ + y³ = n and a x + b y = c for all three points.
- **Tool:** `collisions.py`. For every n on two or more lines, count all coprime representations exactly from
  the divisors of n (s = x + y | n, s ≤ (4n)^(1/3), (4n/s − s²)/3 a square). This is exhaustive for one n.
- **Validation:** 20 cheapest directions, H = 250, n ≤ 10¹⁷: all 4,984 known lines in those directions were
  recovered (100%). The 17,920 extra triples all have n > 10¹⁵, exactly where our three-way data stops.
- **Run 1:** 150 directions, H = 300, n ≤ 10³⁰. 4,229,001 triples. One collision: 506433677359393 (Bernstein).
- **Run 2:** 5,200 directions, H = 100, n ≤ 10³⁰, 9.7 min on 6 cores. 16,701,979 triples. Five collisions,
  all bowties, each with exactly 5 coprime representations:
  - 506433677359393, 95793117931950826933, 624256195206357000469, 5306775242131114520041 (known);
  - **581834611748164220101952821 (5.8 × 10²⁶): NEW.**
    - n = 7·19·37·73·79·97·211·277·463·823·2221·4273: twelve split primes, n ≡ 1 (mod 9), 7 | n.
    - Representations: 879096213³ − 460320926³ = 914740341³ − 568334390³ = 1378449904³ − 1267724307³ =
      1443979966³ − 1344232635³ = 1749407062³ − 1683590043³.
    - Lines: 603x + 676y = 167394377983 and 579x + 676y = 197819761351, through (1378449904, −1267724307).
- **Completeness:** H = 100 is not enough for expensive directions. 39673716067958900347 and
  921288078249108802505 were missed although both their directions are within the 5,200. The line search is
  not exhaustive and cannot prove that no six-way exists.
- **Rarity:** 2 collisions in 4.2 million triples (run 1), 5 in 16.7 million (run 2). Bowties need two
  directions, and the expensive one usually has cost rank in the thousands.

## F13 (25 October 2026): cheap line + exact count, a second new five-way

- **Design** (`cheap_search.py`):
  1. enumerate collinear triples only on the cheapest directions, deeply;
  2. keep n with at least 4 distinct split primes below 200 (every known five-way passes; the strictest is
     624256195206357000469, with exactly 4);
  3. factor the survivors (PARI) and count all coprime representations exactly (divisor method).

  This finds every number that has at least one cheap line, however its other representations arise.
- **Validation** on the 150-direction file (H = 300, n ≤ 10³⁰): 1.61 million candidates. It found 5 known
  five-ways, including 633753337814536954807, whose second line has cost rank 80,112, and the two the bowtie
  method missed.
- **Deep run** (`line_enum.py`, 200 directions, H = 600, n ≤ 10³², 14.5 min on 6 cores): 22,900,972 triples,
  9,034,986 candidates. **Stopped at 3,980,000 of them (sorted order); resume with --start 3980000.**
  - So far: 8 five-ways (7 of the 11 known, i.e. all those with a line in these 200 directions), 636
    four-ways, no six-way.
  - **NEW: 867568642528959824806171 (8.7 × 10²³)** = 79186278³ + 71857339³ = 82498848³ + 67392259³ =
    97363267³ − 38120748³ = 98534347³ − 44664678³ = 100778875³ − 53829834³.
    - n = 7²·13·31·37·43·241·691·907·1399·130681: all primes ≡ 1 (mod 3), proven prime; n ≡ 1 (mod 9).
    - Exactly 5 coprime representations (exhaustive divisor count).
- **Completed (resumed with --start 3980000):** all 9,034,986 candidates counted. Totals: 9 five-ways (7 known
  and 2 new), 713 four-ways, **no six-way**. Four-ways thin out sharply with size: 636 in the first 3.98 million
  candidates (sorted by n), 77 in the remaining 5.05 million.
  - **NEW: 1441335932043659816048279479 (1.4 × 10²⁷)** = 1110168886³ + 418087647³ = 1129711558³ − 76993377³ =
    1134621759³ − 268413890³ = 1140344500³ − 346361241³ = 16593139390³ − 16591394241³.
    - n = 7·31·37·61²·67·73·79·271·859·1153·465187: all primes ≡ 1 (mod 3), proven prime; n ≡ 1 (mod 9).
    - Exactly 5 coprime representations. The last is a near-diagonal difference (the cubes differ by about
      1.7 × 10⁶).
- **The 4 known five-ways missed** all lack a line in the 200 cheapest directions.
- **Total from the line methods so far: 3 new coprime five-ways beyond 10²³** (5.8 × 10²⁶, 8.7 × 10²³,
  1.4 × 10²⁷), and no six-way.

## F14 (25 October 2026): directions 201–500, two more new five-ways

- **Run:** `line_enum.py --skip 200 --dirs 300 --height 600 --nmax 1e32 --rmin 4` (the split-prime filter
  applied while enumerating: 34,663,721 triples generated, 14,637,249 written), then `cheap_search.py --procs 6`
  (parallel PARI counting, about 7,800 numbers per second; 31 min).
- **Results:** 3 five-ways, 325 four-ways, **no six-way**.
  - **137904678696613339**: Bernstein's second five-way. Its only line, direction (12, 109), is beyond rank 200.
  - **NEW: 36382243612093946470090369 (3.6 × 10²⁵)** = 327379905³ + 108983764³ = 331356993³ + 4456108³ =
    331560514³ − 40613655³ = 340899562³ − 147889719³ = 742131514³ − 719424375³.
    - n = 7²·13·43·157·181·193·829·1789·3319·49201: all primes ≡ 1 (mod 3); n ≡ 1 (mod 9).
  - **NEW: 4006751594615544419200755017 (4.0 × 10²⁷)** = 1310961369³ + 1205921552³ = 1498106073³ + 863797640³ =
    1588105089³ + 112584722³ = 2031165105³ − 1635294802³ = 4259754201³ − 4184840344³.
    - n = 7·13·53·61·103·109²·127·199·571·13723·56197; n ≡ 8 (mod 9).
    - **Off-profile:** contains 53 ≡ 2 (mod 3), so 53 divides every s (TOPROVE item 1). Three of its five
      representations are sums.
  - Both have exactly 5 coprime representations (exhaustive divisor count), proven-prime factorisations, and
    every identity exact.
- **Running total from the line methods:** 5 new coprime five-ways beyond 10²³ (8.7 × 10²³, 3.6 × 10²⁵,
  5.8 × 10²⁶, 1.4 × 10²⁷, 4.0 × 10²⁷). Of the 11 known five-ways ≤ 10²³, all but 3 (11837…, 27242…, 53067…, whose
  cheapest lines rank 61,599, 2,683 and 1,838) have now been rediscovered.

## F14b (25 October 2026): directions 501–1000, two more new five-ways

- **Run:** `line_enum.py --skip 500 --dirs 500 --height 600 --nmax 1e32 --rmin 4` (55,788,955 triples,
  23,386,963 candidates), then `cheap_search.py --procs 6` (76 min, about 5,100 per second).
- **Results:** 2 five-ways, 280 four-ways, no six-way. k ≥ 4 saved in `multi_501_1000.txt`.
- **Predictions made before the run:** user 2 new five-ways (**correct**); Claude 3.
- **NEW: 15442272835364300840226739 (1.5 × 10²⁵)** = 208066083³ + 185999278³ = 229129762³ + 150558771³ =
  997367115³ − 992165396³ = 1359827104³ − 1357037685³ = 3716031604³ − 3715658805³.
  - n = 7·19·37·109·157·163·421·2803·6781·140587: all ≡ 1 (mod 3); n ≡ 1 (mod 9).
  - Three of its representations are near-diagonal differences.
- **NEW: 34501269164386329986697851653 (3.5 × 10²⁸)** = 3112812834³ + 1631078149³ = 3180904861³ + 1323131988³ =
  4220557686³ − 3439222187³ = 4654339933³ − 4047865344³ = 32212272037³ − 32201184870³.
  - n = 7·13·19·43·73·151·163·199·1669·2131·2671·136621: all ≡ 1 (mod 3); n ≡ 1 (mod 9).
- **Running total:** 7 new coprime five-ways beyond 10²³ from the 1,000 cheapest directions. No six-way.

## F15 (25 October 2026): divisors (user's question): many split-prime divisors are needed, more as n grows

Every representation has s = x + y dividing n with s³ ≤ 4n, so the divisors s ≤ (4n)^(1/3) are the "candidates".

- **Same size (10¹³–10¹⁵, medians):**

  | k | divisors τ(n) | split-prime divisors | candidate divisors | k / candidates |
  | ---: | ---: | ---: | ---: | ---: |
  | 1 | 32 | 8 | 13 | 0.109 |
  | 2 | 96 | 48 | 25 | 0.113 |
  | 3 | 128 | 64 | 31 | 0.122 |
  | 4 | 128 | 128 | 33 | 0.123 |

  At fixed size each candidate succeeds about 11–12% of the time whatever k is: multi-way numbers simply have
  more candidates.
- **The 18 five-ways (all sizes):** τ(n) = 256 to 4,096, always a power of 2: 8–12 distinct primes, almost all
  ≡ 1 (mod 3), almost all to the first power. Candidate divisors and success rate by size:

  | size | candidates | success per candidate |
  | --- | ---: | ---: |
  | 10¹⁵ | 55–58 | ≈ 0.09 |
  | 10²⁰ to 10²² | 102–191 | 0.03–0.05 |
  | 10²⁴ to 10²⁸ | 279–692 | 0.007–0.018 |

  **Larger n needs many more divisors for the same k.** A six-way near 10²⁵–10³⁰ probably needs ≥ 13 split
  primes.

## F16 (25 October 2026): more about the four-way n values (user's question)

**Four-ways ≤ 10¹⁵ (90) against size-matched three-ways (1,672):**

| feature | four-ways | three-ways |
| --- | ---: | ---: |
| squarefree | 74% | 58% |
| distinct primes (median) | 7 | 6 |
| largest prime as a power of n (median) | 0.24 | 0.27 |
| smallest s / n^(1/3) (median) | 0.065 | 0.076 |

- **Squarefree and smoother** both maximise the number of divisors for a given size (F15).
- **Sign patterns:** four-ways with 3 of their 4 representations as sums are relatively common: 3 of 90, and 11
  of all 204 four-ways ≤ 10¹⁷, against 3 of 1,672 three-ways. These are near-misses for the cubefree four-way
  (A080642(4) ≈ 1.8 × 10¹⁸, beyond 10¹⁷).
- **Near-diagonal differences** (|x + y| < 1% of x): about 10–12% in both groups. Not special.
- **Small-prime cores** (10¹²–10¹⁵: k = 4: 79, k = 3: 11,480, k = 2: 30,000 sampled):

  | core | k = 4 | k = 3 | k = 2 |
  | --- | ---: | ---: | ---: |
  | 7·13 | 53% | 33% | 25% |
  | 7·19 | 46% | 25% | 19% |
  | 7·37 | 42% | 24% | 11% |
  | **7·13·19 = 1729** | **32%** | **12%** | **8%** |
  | 7·67 | 25% | 11% | 6% |

  Cores are typically 1.6–2.7 times more frequent at k = 4 than at k = 3.
- **The enriched cores are the fingerprints of the cheap line directions** (F11: E = a² + ab + b² divides n):

  | direction | E | core |
  | --- | --- | --- |
  | (3, 4) | 37 | 37 |
  | (4, 9) | 133 = 7·19 | 7·19 |
  | (12, 13) | 469 = 7·67 | 7·67 |
  | (1, 4) | 21 = 3·7 | 7 |
  | (4, 7) | 93 = 3·31 | 31 |

  A four-way with a (3, 4) line is automatically divisible by 37, and so on. This links F1 (prime enrichment)
  to F11 (E | n).

**Four-ways against ordinary integers of the same size** (all 204 four-ways ≤ 10¹⁷; 4,080 random integers with
matching digit counts; 4,000 coprime sums at 10¹⁵):

| property | integers | coprime sums | four-ways |
| --- | ---: | ---: | ---: |
| even | 50% | 33% | 0.5% |
| 3 \| n | 33% | 26% | 18% |
| n ≡ 1 (mod 3) | 34% | 37% | 71% |
| 7 \| n | 15% | 37.5% | 84% |
| squarefree | 61% | 54% | 72% |
| no prime ≡ 2 (mod 3) | 9% | 19% | 88% |
| distinct primes (median) | 4 | 5 | 8 |
| primes ≡ 1 (mod 3) (median) | 1 | 3 | 7 |
| divisors (median) | 16 | 32 | 256 |
| largest prime, as a power of n | 0.61 | 0.47 | 0.22 |

**Coprime four-ways are highly composite, smooth numbers built almost entirely from primes ≡ 1 (mod 3).**
- The only even four-way is 89369647088939126 = 2·7·13·19·43·103·1171·1549·3217. It contains 1729 = 7·13·19,
  and 2 divides every s (all four representations have x and y odd), as TOPROVE item 1 requires.

## Negative results

- **N3 (25 October 2026): divisor-richness alone does not make multi-way numbers.** Of 20,000 random products
  of 12 of the 20 smallest split primes (20–30 digits): 19,861 have no coprime representation, 136 have one,
  3 have two, none has ≥ 3.
  - Reasons: the square condition (4n/s − s²)/3 = d² almost never holds by chance; and there are local
    obstructions (for example, n ≡ 4 or 5 (mod 9) is never a sum of two cubes).
  - The line method works because it guarantees three representations by construction and then uses
    divisor-richness (the split-prime filter) to pick candidates. Structure first, divisors second.

- **N2 (25 October 2026): shared coefficient 676 is not a rich vein.** The new five-way's lines share b = 676
  (= 2²·13²), and 95793117931950826933 has a (633, 676) line. The full family (a, 676), 124 allowed
  directions, H = 200, n ≤ 10³⁰, gave 844,440 triples and only the one known collision. The control family
  (a, 1444), 253 directions, gave 651,583 triples and none. There is no evidence that shared-b directions pair
  into bowties much more than chance (`fixed_b.py`).

- **N1 (25 October 2026):** in exhaustive data to 10¹⁵ (12,676 three-ways, 90 four-ways) plus the 11
  five-ways, **no residue of n is absent for k ≥ 3 beyond what local densities predict.**
  - Every apparent "never" is a steep slope. Examples: 5 three-ways with n ≡ 2 (mod 9), 76 even three-ways.
  - The k ≥ 4 "never" cases rest on 90 numbers, too few to separate a wall from a slope.
  - **Conclusion:** first-order structure is local (the singular series). New structure, if any, must be
    global: rank, relations between the k points, or deviations from a local-density model.
