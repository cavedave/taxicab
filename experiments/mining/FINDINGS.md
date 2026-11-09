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

## F17 (25 October 2026): every four-way ≤ 10¹⁷ is a line + free point, a hub, or independent (exact)

All 204 exhaustive four-ways (`results/fourways.md`) were run through `relations.py`: exact generators,
coordinates and `matkerint`; 204 of 204 verified (`fourways_relations.txt`).

| shape | count | relation |
| --- | ---: | --- |
| line + free point | 184 (90%) | one 3-term ±1 relation; span 3 |
| hub | 11 (5%) | one 4-term ±1 relation P₁ ± P₂ ± P₃ ± P₄ = 0; span 3 |
| independent | 9 (4%) | no relation; span 4 |

- Curve ranks: 3 (22), 4 (136), 5 (30), 6 (11), 7 (3), 3–5 (2).
- **Geometry:** a line meets the cubic in at most 3 points, and two lines share at most one point. So a
  four-way has at most one line, and two lines need at least 5 points (the five-way bowtie).
- **The fourth point is never tied to the line triple by any further relation.**
- **Line directions** among the 184: (3, 4) 48; (12, 13) 9; (4, 7) 7; (12, 31), (9, 16), (12, 19), (27, 28) 4
  each. 62 (34%) are in the (3k², 3k² + 1) family.
- **The hierarchy:** line (3) → line + free point (4) → second line through a shared point (5, bowtie).
  Six-way candidates: a bowtie + free point, two disjoint lines, a triangle of three lines, or a hub + line.

## F18 (25 October 2026): geometry of the 18 five-ways, and a mod-3 law for same-line chords

**Tool:** `fives_geometry.py`, rank-free with exact rationals. It finds lines, hubs and chord third points using
Werebrusow's chord formula (PARI ranks fail on the larger five-ways).

**Five-ways (11 known ≤ 10²³ + 7 new):**
- 17 of 18 are **bowties** (two lines sharing a point). The exception is 137904678696613339 (Bernstein): one
  line + two free points.
- The two "hubs" in each bowtie are consequences of the two line relations (A + B = C + D), not new structure.
- The shared point is a difference in 14 of 18. Its position on the two lines (middle or end) shows no pattern:
  end/end 7, end/middle 7, middle/middle 3.
- The smallest denominator of a non-representation chord point ranges from 12 to 44,226. **All 18 are divisible
  by 3.**

**The law behind it (exact, no exceptions):**
- **Chords between two points on the same line** (third point = Q − P, which is not a representation): 33,168
  cases (all k ≥ 3 ≤ 10¹⁵), **100.00%** with denominator divisible by 3.
- **Chords between points not on a common line:** 10,820 cases, 52.7%, close to the 51–64% seen for chords in
  general.
- **Consequence:** a same-line "swapped chord" can never produce a new representation. A sixth representation
  of a five-way would have to come from a cross-line chord or a new point. Near-miss hunting should look only
  at cross-line chords.
- **Correction (F20 below):** the five-ways' smallest chord denominators are not same-line chords but the
  cross-line "hub" chords (differences), which are also always divisible by 3.
- **Proposed reason** (TOPROVE item 11): x³ ≡ x (mod 3) gives x + y ≡ n (mod 3) for every representation. The
  curve reduces mod 3 to (x + y)³ = n, which is additive and degenerate, so differences of collinear points
  land in the kernel of reduction mod 3.

## F19 (25 October 2026): the free point in "line + free point" four-ways (user's question)

**184 four-ways ≤ 10¹⁷ with a line:** the free point against the three line points.
- **Essentially ordinary:** sum 36% against 30%; largest s of the four 32% against 23%; x prime 10% against 11%;
  near-diagonal 11% against 11%; s / n^(1/3) median 0.61 against 0.52; max(|x|, |y|) / n^(1/3) about 1.0 for
  both.
- **The one strong difference, the line's E = a² + ab + b²:**

  | | free point | line points |
  | --- | ---: | ---: |
  | gcd(s, E) > 1 | 64.7% | 19.0% |
  | E \| s | 26% (48) | 0% (0 of 552) |
  | s = E exactly | 9 (5%) | 0 |

  - When E | s, the multiplier s/E is 1, 7, 9, 13, 19, 21, 31, 43, 67, 79, 103, 109, 111, 163, 199, …
    (3s and split primes).
  - Example: A047697(4) = 16776487 has line direction (3, 16), E = 313, and free point s = 313. Also
    265370336497: E = s = 7333.
- **Exact law behind it (PROVED, given TOPROVE item 8):** every point on a line has E | t = x² − xy + y²
  (33,465 of 33,465).
  - **Proof:** E | c gives a·x ≡ −b·y (mod E), so a²·t ≡ y²(b² + ab + a²) = E·y² ≡ 0 (mod E), and gcd(a, E) = 1.
  - Since gcd(s, t) | 3, E never divides a line point's s, apart from a factor of 3.
- **Interpretation:** E | n, and each representation places E's primes in s or in t. Line points must put
  them in t. The free point can put them in s, and in about a quarter of cases puts all of E there.

## F20 (25 October 2026): cross-line chords in the 17 bowties: no near-misses for a sixth representation

For a bowtie with lines A + S + B = 0 and C + S + D = 0, take the 8 chords between {A, B} and {C, D} (both
orientations).
- **4 are "hub" chords** (differences, e.g. A − C = D − B). Their denominators are always divisible by 3, and
  they include every small one: 12, 30, 90, 114, 156, 180, 366, 618, 1308, 1488, 1830, 2286, 3288, 10758, 44226.
- **4 are "live" chords** (A + C, A + D, B + C, B + D). Their smallest denominators range from 368,771 to about
  10¹³, so nowhere near an integer point.
- **Conclusion:** bowties are not near-misses for a six-way via chords. Likelier six-way shapes are a bowtie
  plus a free point, or two disjoint lines (A + B + C = 0, D + E + F = 0). The cheap-line search catches
  either, provided one line is cheap.
- **E in five-ways:** points off a line have E | s in 11 of 68 cases (16%). The free point of a four-way: 26%.

## F21 (25 October 2026): census of all enumerated lines: two cheap lines almost never share an n

- **Method:** the n values of all 60.9 million collinear triples from directions 1–1000 (n ≤ 10³²), sorted
  externally to find repeats (`cut | sort | uniq -d`).
- **Result:** exactly one n lies on two enumerated lines, 506433677359393 (Bernstein's bowtie, directions
  (3, 4) and (9, 52)). There are **no disjoint pairs**, so no "two opposite lines" six-way with both lines among
  the 1,000 cheapest directions, up to 10³².
- **Meaning:** the other five-ways found pair a cheap line with an expensive one (e.g. (3, 4) with (273, 304),
  rank 1,042), and the exact count catches the expensive line's points for free. A disjoint-line six-way would
  most likely also be cheap + expensive. `cheap_search.py` already tests that shape; extending directions and
  slopes is the way to test it further.

## F22 (25 October 2026): mining the 204 four-ways for polynomial families: none visible, two cheap hints

| idea | result |
| --- | --- |
| line-parameter clustering, direction (3, 4), 48 four-ways | none; the conic-slope heights, denominators and residues mod 3 match three-way lines |
| free points with small s = x + y (quadratic families n = s(3x² − 3sx + s²)) | no enrichment: s ≤ 1000 for 10% of free points, 6% of line points, 9% of three-way representations |
| free point's s = E × (small norm) | yes, 26% (F19); multipliers 1, 7, 9, 13, 19, 31, 43, …, 1729 |
| the line's multiplier q = c/E is a norm | 88% of four-way lines, against 68% of three-way lines (10,075 lines, n > 10¹²); prime 39% against 29%. About 3.5× in odds |

- **No explicit polynomial family of four-ways** is visible in 204 examples spread over dozens of directions.
  A complete list up to 10²³ (a GPU `--kmin 4` run) would be needed for a proper family search.
- **Usable without the GPU** (ordering only, results unchanged):
  1. prioritise lines whose q is a norm;
  2. test s = E·m with small norm m first for extra representations.

## Six-way profile (25 October 2026): bets, not proofs; factors overlap, so the odds do not multiply

| # | trait | evidence | rough effect |
| --- | --- | --- | --- |
| 1 | at least one cheap line (top ~1,000; the (3k², 3k² + 1) family, (3, 4) richest), likely paired with an expensive second line | 7 of 11 known five-ways have a top-200 line; bowties are cheap + expensive | strong; also what makes it findable |
| 2 | very many divisors: five-ways have τ = 256–4,096 (8–12 distinct primes); at 10²⁵–10³⁰ a six-way likely needs ≥ 13 primes (τ ≳ 8,000) | F15 | strong (~10×+) |
| 3 | primes almost all ≡ 1 (mod 3), none ≡ 2 (mod 3) | four-ways 88%, five-ways 16/18; integers 9% | strong (~5–10×) |
| 4 | odd | 203/204 four-ways, 18/18 five-ways | ~2× |
| 5 | n ≡ 1 (mod 9) (never ±2) | five-ways: 14 ≡ 1, 4 ≡ 8 | ~2–3× |
| 6 | 7 \| n, often 1729 = 7·13·19 \| n | four-ways: 7 in 84%; 1729 in 32% against 12% of three-ways | ~2× each |
| 7 | squarefree and smooth (largest prime ≈ n^0.2) | 72% against 54–61%; 0.22 against 0.61 | ~1.5× |
| 8 | the cheap line's q = c/E is a norm | 88% against 68% (F22) | ~1.5–3× |
| 9 | the extra point's s is a multiple of E (×1, ×7, ×13, …, ×1729) | 26% of four-way free points, 16% of five-way off-line points | weak |
| — | small s = x + y (quadratic families) | no enrichment (F22) | dropped |

- **Likely shapes, most believed first:** bowtie + free point; two disjoint lines (cheap + expensive); line +
  three free points (high rank); hub mixtures. Not chord completion of a bowtie (F20).
- **No edge:** position of the shared point, near-diagonal points, prime coordinates, root number (implied by
  #3 and #5).
- **Suggested change for six-way hunting:** tighten the `cheap_search.py` filter from "≥ 4 split primes below
  200" towards "≥ 8 split primes overall". That needs a cheap partial factorisation first.

## F23 (25 October 2026): "hero" search on the six-way profile: four-ways enriched about 12×, no five- or six-way

- **Run** (about 13 min on the Mac): `line_enum.py --dirs 120 --height 800 --nmax 1e40 --old-height 600
  --old-nmax 1e32 --hero 6`, i.e. only new territory (slopes > 600 or n > 10³²), keeping only n with:
  - 1729 | n, n odd, n ≡ 1 (mod 9);
  - no prime ≡ 2 (mod 3) below 200;
  - ≥ 6 split primes below 200.

  Then `cheap_search.py --rmin 6` for the exact count. Files: `hero_120.log`, `hero_search.log`,
  `hero_multi.txt`.
- **Result:** 161,740 candidates; 24 four-ways, **no five-way, no six-way**.
- **The profile works:**

  | candidates | four-way rate |
  | --- | ---: |
  | hero (profile) | 24 / 161,740 = 1.5 × 10⁻⁴ |
  | tranche 501–1000 (only ≥ 4 split primes) | 280 / 23.4 M = 1.2 × 10⁻⁵ |

  That is about 12× enrichment, although hero candidates are larger (up to 10⁴⁰).
- **Expected five-ways** at that enrichment: about 0.2, so none is unsurprising. A hero search expecting a
  five-way or six-way needs 10–100× more profile candidates (more directions and/or larger slopes): hours,
  better on 7of9.

## F24 (25 October 2026): hero search with 7 | n instead of 1729 | n finds a new five-way

- **Run** (about 19 min on the Mac): the same territory as F23 (`--dirs 120 --height 800 --nmax 1e40
  --old-height 600 --old-nmax 1e32`), with the looser profile `--core 7 --hero 4`:
  - 7 | n (84% of four-ways, against 32% for 1729), n odd, n ≡ 1 (mod 9);
  - no prime ≡ 2 (mod 3) below 200;
  - ≥ 4 split primes below 200.

  Enumeration about 12 min (as in F23: the filter does not change it); exact counting of 1,740,042
  candidates 6.5 min. Files: `hero7_120.log`, `hero7_search.log`, `hero7_multi.txt`.
- **Result:** 113 four-ways and **4 five-ways**, no six-way:
  - 39673716067958900347 and 624256195206357000469 (known, exhaustive range);
  - 867568642528959824806171 (our F14 line-method five-way);
  - **357308079971019656068684549 (new)**, on the line 36x + 37y = 3086151649 (direction (36, 37), slope
    height > 600, which is why the H = 600 sweep missed it).
    n = 7 · 13² · 43 · 61 · 79 · 151 · 277 · 571 · 631 · 2251 · 42967: all eleven primes ≡ 1 (mod 3). Not
    divisible by 19 (so not by 1729) and not squarefree.
- **Recall against cost:**

  | filter | candidates | four-ways | five-ways | four-way rate |
  | --- | ---: | ---: | ---: | ---: |
  | 1729, ≥ 6 split (F23) | 161,740 | 24 | 0 | 1.5 × 10⁻⁴ |
  | 7, ≥ 4 split (F24) | 1,740,042 | 113 | 4 | 6.5 × 10⁻⁵ |

  The 1729 filter is denser per candidate but loses most hits; since enumeration dominates the time, the
  looser filter is the better use of a run. Two of the four five-ways are not divisible by 1729, and a third
  (624256195206357000469, divisible by 1729) failed F23's ≥ 6 split-prime threshold.
- **Lesson for the six-way profile:** 1729 | n should be a preference, not a requirement. Keep 7 | n as the
  hard filter.

## F25 (26 October 2026): directions 1001–1400 are thin: 148 four-ways, no new five-way

- **Run:** `line_enum.py --skip 1000 --dirs 400 --height 600 --nmax 1e32 --hero 4 --core 0`. The F24
  profile: at least two of {7, 13, 19, 37} divide n, and ≥ 4 split primes below 200 (no mod-9 or
  p ≡ 2 (mod 3) rule). Then `cheap_search.py --rmin 4`. About 1 h on the Mac, paused overnight.
  Files: `lines_1001_1400.log`, `search_1001_1400.log`, `multi_1001_1400.txt`.
- **Result:** 14,457,800 candidates; 148 four-ways (124 of them above 10²³) and one five-way, the known
  39673716067958900347 (also on a cheap direction, F24: the second line of its bowtie). No six-way.
- **Yield per direction is tiny:** the best direction has 7 four-ways (`rank_dirs.py`), against 48 for
  (3, 4) in F24.
- **Five-ways per tranche keep falling:**

  | directions | five-ways |
  | --- | --- |
  | 1–200 | 9 |
  | 201–500 | 3 |
  | 501–1000 | 2 |
  | 1001–1400 | 0 new |

- **Lesson:** more expensive directions are not worth it on the Mac. Better uses of time:
  - deeper slopes on the few productive cheap directions;
  - the structural route (UlasPaperPlan goal C).

## F26 (26 October 2026): deep search of 8 cheap directions to slope height 4,000: five new five-ways

- **Run:** `line_enum.py --only "3,4;12,13;12,19;3,16;36,37;12,49;57,64;48,49" --chunks 6 --height 4000
  --nmax 1e40 --old-height 600 --old-nmax 1e32 --hero 4 --core 0`, then `cheap_search.py --rmin 4`.
  - The directions are the most productive ones from F24.
  - New `line_enum.py` options: `--only` (an explicit list of directions) and `--chunks` (split each
    direction's slope range across processes).
  - Time: about 28 min enumeration plus 21 min counting, on the Mac.
  - Files: `deep8.log`, `deep8_search.log`, `deep8_multi.txt`.
- **Result:** 30.6 M triples, 15,315,926 distinct n. **500 four-ways, 9 five-ways, no six-way.**
- **The five new five-ways** (each verified by the exact divisor count; all prime factors ≡ 1 (mod 3)):

  | n | direction | slope height | factorisation |
  | --- | --- | ---: | --- |
  | 236191447138323830299237 (2.36 × 10²³) | (3, 4) | 1,750 | 7² · 13 · 19 · 37 · 97 · 349 · 787 · 1447 · 3607 · 3793 |
  | 459803710089257980965337 (4.60 × 10²³) | (12, 13) | 1,192 | 7 · 13 · 31 · 67 · 181 · 241 · 4273 · 24007 · 543661 |
  | 2851826724766078018833601 (2.85 × 10²⁴) | (3, 4) | 3,459 | 7 · 13 · 37 · 61 · 229 · 751 · 6997 · 24733 · 466537 |
  | 153461072317103291251148239 (1.53 × 10²⁶) | (12, 19) | 1,487 | 7 · 19 · 37 · 43 · 97 · 307 · 577 · 733 · 853 · 2251 · 29989 |
  | 889713631299214636707596167 (8.90 × 10²⁶) | (3, 16) | 1,459 | 7 · 13 · 19 · 31 · 79 · 97 · 103 · 151 · 163 · 313 · 24571 · 111103 |

  The other four were known: 39673716067958900347, 624256195206357000469, 867568642528959824806171 and
  357308079971019656068684549.
- **Per direction** (`rank_dirs.py`, deduplicated):

  | direction | distinct n | four-ways | five-ways |
  | --- | ---: | ---: | ---: |
  | (3, 4) | 3,332,066 | 291 | 3 |
  | (12, 13) | 2,201,302 | 61 | 1 |
  | (12, 19) | 1,404,092 | 38 | 1 |
  | (3, 16) | 2,275,606 | 45 | 1 |
  | (36, 37) | 1,567,680 | 24 | 1 |
  | (12, 49) | 2,431,360 | 18 | 1 |
  | (57, 64) | 1,408,379 | 10 | 1 |
  | (48, 49) | 695,441 | 13 | 0 |

- **A rich seam:**
  - Five-ways per candidate are about 5–10× those of the broad sweeps (F25: 0 new in 14.5 M).
  - The new five-ways sit at slope heights 1,192–3,459, across the whole new range, so the seam very likely
    continues above 4,000.
  - The cheapest direction, (3, 4), carries 58% of the four-ways and 3 of the 9 five-ways.
- **Consequences:**
  1. **Depth beats breadth.** Higher slopes on cheap directions are far better than more expensive
     directions.
  2. **The 10²²–10²³ gap was a fluctuation:** three five-ways are now known in 10²³–10²⁴ (2.36, 4.60 and
     8.68 × 10²³).
  3. **A pool of 50–100 five-ways looks reachable** (the top ~25 directions to height 10,000 on 7of9). That
     revises the pessimism of UlasPaperPlan C0.
  4. **A test of recall:** 2.36 × 10²³ lies in the planned GPU window 10²³–2.5 × 10²³. That run would show
     what the line method misses in an exhaustive range.
- **Caution:** 9 five-ways is a small sample, so the 5–10× figure is rough.

## F27 (26 October 2026): line search on the rental's spare CPUs: 19 new five-ways; recall measured against the 10²³–2.5 × 10²³ exhaustive run

- **Setting:** the 4 × RTX 5090 vast.ai machine (96 threads, 80 used at nice 19) while its GPUs ran the exhaustive
  10²³–2.5 × 10²³ search. Results copied to `linesearch_4x5090/`.
- **Run 1, `deep_cpu.sh`** (09:36–15:58 UTC): the 30 cheapest directions plus (12, 49) and (57, 64), slope height
  15,000, n ≤ 10⁴⁰, `--hero 4 --core 0`. Skipped: slopes already searched (height 4,000 for the F26 directions,
  600 for the rest).
  - 760 M triples counted exactly. **1,996 distinct four-ways, 21 five-way hits, no six-way.**
  - Five-ways by direction: (3,4) 7 hits; (12,13), (27,28), (12,19) 2 each; (1,4), (1,12), (16,19), (9,16), (36,37),
    (16,25), (63,64), (12,49) 1 each. **14 of them are new.**
- **Run 2, `solo_band.sh`** (direction (3, 4) only, height 50,000, slopes above 15,000, in bands of 2,500 in s):
  13 of 20 bands done (s ≤ 32,499) before the GPU run ended. 735 M triples counted.
  **927 distinct four-ways, 9 distinct five-ways, no six-way.** 5 of the 9 are new; 4 were also found by run 1
  (other orderings of the same triples).
  - Most five-way "hits" per band are re-finds: one triple has 6 orderings, hence 6 slopes, often in different bands.
- **The 19 new five-ways** (all verified on the Mac: exact divisor count = 5, every prime factor proven):

  | n | found in |
  | --- | --- |
  | 36254160765497504708872903 (3.6 × 10²⁵) | (3,4) |
  | 182392325742867193833098401 (1.8 × 10²⁶) | (3,4), solo |
  | 201297892510496465061972139 (2.0 × 10²⁶) | (3,4), solo |
  | 1875257556360663546196170409 (1.9 × 10²⁷) | (3,4), solo |
  | 9027370398769170672971729619 (9.0 × 10²⁷, 3² ‖ n) | (16,19) |
  | 34547209243400012474421281413 (3.5 × 10²⁸) | (12,13) |
  | 104153248919447127324401999977 (1.0 × 10²⁹) | solo |
  | 278052073362590568252158271051 (2.8 × 10²⁹, 3² ‖ n) | (1,4) |
  | 498424028328865332465535957193 (5.0 × 10²⁹, 11 \| n) | (1,12) |
  | 650942832109065456723121976491 (6.5 × 10²⁹) | (27,28), solo |
  | 2575932492706922775209751529471 (2.6 × 10³⁰) | solo |
  | 3598085549085232075646572993861 (3.6 × 10³⁰) | solo |
  | 5155590025407314470961337159897 (5.2 × 10³⁰, 3³ ‖ n) | (16,25) |
  | 7016830156515525773263162950169 (7.0 × 10³⁰) | solo |
  | 7621954168931821961653299403879 (7.6 × 10³⁰) | solo |
  | 12134354169911534158461101130403 (1.2 × 10³¹) | (12,19) |
  | 19008553084548906511372979784727 (1.9 × 10³¹) | (63,64) |
  | 241472402714194053046481660069701 (2.4 × 10³²) | (9,16) |
  | 378855256022502299689661564666966839 (3.8 × 10³⁵, 7 ∤ n) | (12,49) |

  Representations are in `results/a047697_search.md`; images in `out/a047697/`.
- **Pool of coprime five-ways now 43:** Bernstein 2 + 9 exhaustive (≤ 10²³) + 32 from the line method (> 10²³).
- **Exceptions to earlier "rules" of the five-way profile:** 11 | n (498…193), 3² and 3³ ‖ n (three cases), 7 ∤ n
  (3.8 × 10³⁵), and prime factors up to 3.84 × 10⁶ (so a smoothness filter would need a bound of at least 10⁷).
  The `--core 0` filter (≥ 2 of {7, 13, 19, 37}, ≥ 4 split primes below 200) is the only one consistent with all 43.
- **Recall, measured against the exhaustive GPU run 10²³ < n ≤ 2.5 × 10²³** (`a047697/cab_1e23_2.5e23_part*.txt`,
  kmin 4: 214 four-ways, 1 five-way, verified independently on the Mac):
  - **five-ways: 1 of 1.** 236191447138323830299237 had been found by F26 and again by run 1.
  - **four-ways: 49 of 214 (23%)**, combining every line-search file in `experiments/mining/`.
    159 of the 214 (74%) pass the `--core 0` filter; the searches found 48 of those (30%) and 1 of the 55 that fail it.
  - So the filter keeps about 3/4 of four-ways, and the directions and heights searched so far catch about 1/3 of
    those. For five-ways (two lines through a hub) the catch rate should be higher, since either line suffices;
    1 of 1 is consistent with that but is no measurement.
- **Six-way chance:** none found among about 2,600 four-ways and 26 distinct five-way n from this day's runs.

## F28 (27 October 2026): line structure of the exhaustive four-ways at 10²³ and of all 43 five-ways

**Tool:** `line_structure.py` (exact). For each n it finds every collinear triple among the representations and
their swaps, the direction's cost rank (among all allowed directions, ordered by D = b³ − a³), and the smallest
slope height at which `line_enum.py` produces the triple; also hubs and the `--core 0` filter verdict.
It reproduces F17 exactly on the 204 four-ways ≤ 10¹⁷ (184 line + free, 11 hub, 9 independent), and the
slope height 1,750 of 236191447138323830299237 on (3, 4) (F26).

**Shapes:**

| set | line + free point | hub | independent |
| --- | ---: | ---: | ---: |
| 204 four-ways ≤ 10¹⁷ | 184 (90%) | 11 (5%) | 9 (4%) |
| 214 four-ways 10²³ – 2.5 × 10²³ | 188 (88%) | 24 (11%) | 2 (1%) |

Five-ways (all 43): 40 bowties, 3 one line + two free points (137904678696613339, 236191447138323830299237 and
153461072317103291251148239). No five-way has two disjoint lines or a third line.

**The lines move to expensive directions as n grows:**

| direction rank | ≤ 10¹⁷ (184 lines) | 10²³ (188 lines) | five-ways (83 lines) |
| --- | ---: | ---: | ---: |
| 1, i.e. (3, 4) | 48 (26%) | 26 (14%) | 15 |
| 2–32 | 53 | 27 | 16 |
| 33–1400 | 53 | 43 | 15 |
| > 1400 | 30 (16%) | **92 (49%)** | 37 |

**Slope height grows like n^(1/6):**
- Median line height: 13 (≤ 10¹⁷) → 75 (10²³). On (3, 4): 5–181 at ≤ 10¹⁷, but **1,196–2,495** for every
  (3, 4) four-way in 10²³ – 2.5 × 10²³.
- On (3, 4), log n against log h has slope 5.86, and n / h⁶ lies in 938 – 7.8 × 10⁴ (89 lines). Other cheap
  directions behave the same, with larger constants.
- Reason: the triple's common denominator c grows like Q = s² + sr + r² ≈ h², and n ≈ c³.
- **Consequence:** each n range lives in a band of heights in each direction, and enumerating a direction to
  height H costs about H² ∝ N^(1/3) slopes. An exhaustive search costs N^(2/3). (Heuristic, not a bound: n / h⁶
  can be small when one point is near the asymptote x + y = 0.)
- By this rule, (3, 4) to height 15,000 covers its lines to about 5 × 10²⁷, and to about 32,500 roughly 10³⁰.

**Why the line method misses four-ways in 10²³ – 2.5 × 10²³** (214 four-ways):

| reason | count | |
| --- | ---: | --- |
| no line at all (24 hubs, 2 independent) | 26 (12%) | out of reach of any line search |
| line, but n fails the `--core 0` filter | 50 (23%) | 1 found anyway, by an earlier, looser sweep |
| line direction ranked > 1400 (not searched) | 73 (34%) | |
| line inside a searched region | 65 (30%) | 48 found; the other 17 lie in directions ranked ≤ 500, whose sweeps (F13, F14) kept only five-ways. Re-running 3 of them generates the triples. |

- **So within the region searched the line method missed nothing.** Its recall is set by three choices: the
  filter (−23%), the number of directions (−34%) and the shapes without a line (−12%).
- For five-ways a bowtie has two lines and either suffices, so the direction limit hurts less: of the 43, 38 have
  a line inside the searched region; the other 5 were found by the exhaustive search.

**Pointers:**
- Hubs doubled their share (5% → 11%). A hub is two chords P₁P₂ and P₃P₄ meeting the curve at the same
  non-integral point R: a "rational bowtie". A search over small-height R would reach them; not tried.
- A six-way that is a bowtie + free point or two disjoint lines needs at least one line, so the gaps that matter
  most are the filter and the direction count, not the hubs.

## F29 (27 October 2026): hubs, first look: two chords with the same b − a

A hub is a four-way with P₁ + P₂ = P₃ + P₄: the chords P₁P₂ and P₃P₄ meet the curve again at the same
non-integral point R (a "rational bowtie"). 35 hubs (11 ≤ 10¹⁷, 24 in 10²³ – 2.5 × 10²³), 105 chord-pair views.

- **R's denominator** ranges from 2 to 2.8 × 10⁷; 18 of the 105 views have a denominator ≤ 12.
- **Chord directions are mostly not "allowed" directions** (Theorem 1 is about lines with three integer points,
  and these lines have only two).
- **Pattern:** in **24 of the 35 hubs (69%)** the two chords through R have directions (a, b) and (a′, b′) with
  |b − a| = |b′ − a′| (or a + b = a′ + b′). Examples: (171, 193) and (417, 439); (31, 37) and (463, 469);
  (259, 403) and (6349, 6493); (4, 39) and (796, 831). Often R's denominator equals that common difference.
- **Control:** among the 383 non-hub four-ways, only 12 (3%) have any pairing of their points with this property.
- **Not in bowties:** only 4 of the 40 bowtie five-ways (two lines through an integer point) have equal b − a or
  a + b, three of them with b − a = 1, which is common among cheap directions anyway. So the pattern belongs to
  the non-integral hub point R.
- Since b − a = s_Q − s_P for a chord PQ (s = x + y), up to the gcd, this says that the two chords change
  s = x + y by the same amount. Not explained yet; a lead for a constructive hub search.

## F30 (27 October 2026): hubs explained: two lines through a point of small denominator, i.e. a bowtie on D³n

**Tool:** `hub_geometry.py` (coordinates s = x + y, v = x − y, where the curve is s(s² + 3v²) = 4n). 35 hubs
(11 ≤ 10¹⁷, 24 in 10²³ – 2.5 × 10²³). Each hub P₁ + P₂ = P₃ + P₄ has 3 meeting points R (the 3 ways to pair the
points); in 11 hubs the two lines meet the curve at R and its mirror (s_R, −v_R) rather than at R itself.

**1. The F29 pattern (equal b − a) is a side effect.**
- For a line PQ, b − a = Δs and a + b = Δv: (b − a, a + b) is the line's direction in the (s, v) plane.
- If R has integer s_R = S and v_R = w/d, then each line from R to an integer point has direction
  (d(S − sᵢ), w − d·vᵢ), so its b − a is a **multiple of d** (checked: all 57 cases). Equal b − a = the case where
  both multiples are 1 (18 of 57).
- **Integer s_R** happens in 33 of 35 hubs. Write R = (X/D, Y/D) in lowest terms, so X³ + Y³ = D³ n =
  (X + Y)(X² − XY + Y²). Primes ≡ 2 (mod 3), and 3, cannot sit in the second factor, so they force D | X + Y,
  i.e. integer s. Primes ≡ 1 (mod 3) can go either way: the 8 non-integer cases have s-denominators 7, 43, 103,
  229, 1171, all ≡ 1 (mod 3). Matched by denominator size, random chords have integer s just as often
  (D ≤ 12: 94% random vs 100% hubs; D ≤ 1000: 41% vs 62%).

**2. The real property: a meeting point of small denominator.**

| smallest denominator D | hubs (35) | non-hub four-ways (383; smallest of all 12 chord points) |
| --- | ---: | ---: |
| ≤ 2 | 4 | 15 |
| ≤ 6 | **20 (57%)** | 54 (14%) |
| ≤ 12 | 23 (66%) | 71 (19%) |
| ≤ 100 | 31 (89%) | 147 (38%) |
| ≤ 1000 | 35 (100%) | 233 (61%) |

Typical smallest denominators: 2, 3, 5, 6, 12, 15.

**3. Unification: a hub of n is a bowtie of D³n.**
- Multiply all coordinates by D. P₁, …, P₄ become integer points divisible by D, and R becomes an integer
  point (X, Y) of x³ + y³ = D³n. The two chords become two lines, each with three integer points, through the
  shared point (X, Y): a bowtie on D³n, whose four outer points are multiples of D.
- Bowtie five-ways are the case D = 1. The hierarchy line → line + point → bowtie extends to "D-lines" (two
  integer points and one point of denominator D) and hubs (two D-lines sharing that point).
- `line_enum.py` already generates such triples (on D³n), but drops them because two points are not coprime.

**Consequences:**
- **A hub search is a line search that keeps D-lines for small D** (2, 3, 4, 5, 6, …), indexed by (n, R).
  Two D-lines with the same n and R give a hub; a D-line plus an ordinary line through the same n gives more.
- **Direction rule for D-lines (21 cases with D ≤ 6, no exception):** a·b > 0 and every prime ≡ 2 (mod 3) divides
  a·b to an even power, as in Theorem 1(a). Parity depends on D: **D odd (3, 5): a·b even**, the usual allowed
  directions, e.g. (1, 4), (4, 7), (37, 76), (12, 67); **D even (2, 4, 6): a·b odd**, e.g. (1, 3), (7, 9), (1, 7),
  (31, 37), (1, 13). Conjecture, to prove alongside Theorem 1. Cost scaling not measured yet.
- **Six-way shapes this adds:** hub + line (6 points), hub + bowtie pieces, two hubs sharing points.

## F31 (27 October 2026): D-line search (`dline_enum.py`): validated; the line ∩ D-line join; a five-way of shape line + D-line

**Tool:** `dline_enum.py` enumerates D-lines (two coprime integer points of n, one point R of denominator
2 ≤ D ≤ --dmax) with the conic of `line_enum.py`, on the F30 directions (`--parity even` for odd D, `odd` for even
D). Output `n;D;a;b;c;x1:y1,x2:y2;X:Y` with R = (X/D, Y/D).

- **Validation:** every hub line with D ≤ 6 has a computed direction and slope height. Typically one line is in
  a cheap direction at large height and the other in an expensive direction at small height. Running
  (4,7), (1,4), (7,9), (1,3), (1,7) to height 300–400 re-finds all 6 hubs aimed at, each through 2–3 D-lines
  (≈ 3 s).
- **Calibration ≤ 10¹⁷** (30 cheapest directions of each parity, height 600, D ≤ 12; 3 min): 561,055 D-lines,
  237,148 distinct n. Exact count of all: **33 four-ways (7 of the 11 hubs, 26 line + free), all in the exhaustive
  list of 204**, no false hits. But 236,394 of the n are two-ways: as a candidate source D-lines are weak
  (4-way rate 1.4 × 10⁻⁴, against 4 × 10⁻³ for ordinary lines on the same directions: 102 four-ways and 1 five-way
  among 25,027 n).
- **The join:** n carrying both an ordinary line and a D-line. ≤ 10¹⁷: 8 such n, **all 8 four-ways** (the D-line
  shares one point with the line). If the D-line is disjoint from the line, n has ≥ 5 representations.
- **Five-ways of that shape exist:**
  - 236191447138323830299237: the (3, 4) line + the line through its two free points, which meets the curve at
    a point of denominator **24**: a line + disjoint D-line (D = 24).
  - 137904678696613339 (Bernstein): line + free pair whose chord point has denominator 129.
  - 153461072317103291251148239: no small D (smallest 194,271,019).
- **The star picture** (lines through one point C):

  | centre C | 2 lines | 3 lines |
  | --- | --- | --- |
  | integer point (D = 1) | bowtie, 5 points (40 of 43 five-ways) | 7 points |
  | point of small denominator D | hub, 4 points | **6 points** |

  Six-way shapes with three relations on six points: a 3-line star around a small-D point; a bowtie + a D-line
  to a sixth point; a line + a hub sharing a point; a triangle of three lines. With two relations: bowtie + free
  point, two disjoint lines, line + disjoint D-line + free point.

## F32 (27 October 2026): Mac test, deep against wide. Breadth wins; exact counting of every candidate is cheap

**Setup.** M3, 8 cores. Filters `--hero 4 --core 0`, n ≤ 10⁴⁰. Every candidate n was counted exactly
(`count_all.py`, about 10,000 n/s), not sampled. Results are in `linesearch_mac/` (`union_4plus.txt`: all 1,108 four- and five-ways; reports, stars, run scripts; `mac1` is the deep run, `mac2` the
wide run). The bulky triple files were not kept.

| | deep: 8 directions per parity, height 3,000 | wide: 1,000 directions per parity, height 200 |
| --- | --- | --- |
| line stage | 14.3M triples, 6.7M n; 4,888 CPU-s; 2.3 GB | 4.5M triples and n; 2,795 CPU-s; 50 MB |
| line hits | 503 four-ways, 4 five-ways | 559 four-ways, 7 five-ways |
| line four-ways > 10²³ | 230 (0.047 per CPU-s) | 192 (0.069 per CPU-s) |
| D-line stages (even + odd) | 11.1M n; 9,323 CPU-s | 7.1M n; 5,537 CPU-s |
| D-line hits | 84 four-ways, 2,664 three-ways | 144 four-ways, 3,636 three-ways |
| joins (line ∩ D-line) | 7 | 57 (50 four-ways, the five-way 3.6e25) |
| stars (hubs found directly) | 0 | 4 (D = 3, 6, 6, 2) |

- **Union:** 1,098 four-ways and 10 five-ways, all ten already known; no six-way.
  - The run found **130 of the 204 exhaustive four-ways ≤ 10¹⁷**, and 51 of the 214 at 10²³–2.5·10²³.
  - 917 of the four-ways lie in ranges we have not covered exhaustively (10¹⁷–10²³ and above 2.5·10²³, up to
    10²⁹).
- **Yield per direction falls slowly with rank.** At height ≤ 200, four- and five-ways per direction:
  - rank 1–10: 9.5;
  - rank 11–30: 2.75;
  - rank 31–100: 1.3;
  - rank 101–300: 0.62;
  - rank 301–1000: 0.29.

  That is roughly rank^−0.7. Cumulative yield over R directions grows like R^0.3.
- **Depth: hits per height band in the 8 deep directions.** The bands are 0–100, 100–200, …, 1600–3000, each
  about double the last. They gave 51, 36, 54, 78, 122 and 166 hits, about ×1.5 per doubling of height for
  ×4 the slopes. Cumulative yield grows like h^0.6, that is about cost^0.3. The cost per slope also grows with
  height: 56 µs per slope at h ≤ 3,000 against 19 µs at h ≤ 300.
- **Breadth reaches large n too.** Expensive directions (large b³ − a³) give large n at small height.
  - The wide run's four-ways > 10²³ came at 1.5× the deep run's rate per CPU-second.
  - Its five-ways reach 3.6·10²⁵.
- **D-lines are a complementary source, not a better one.**
  - 122 of the four-ways were found only by the D-line search: 57 hubs, 59 line + free whose line lies
    outside the line-searched region, and **6 "independent" four-ways** (no line, no hub). The six are
    955453440097, 13427849422198295, 266890627295626663, 925841207022664807, 3550033331173949893 and
    46124514427057530170833.
  - **Every hub came from the D-line search.**
  - Stars need two D-lines in *different* directions, for example (4,7) with (316,337), or (1,7) with
    (67,109). So stars are a breadth-only phenomenon; the deep run found none.
- **Infrastructure:**
  - exact counting at about 0.1 ms per n means every candidate can be counted, so sampling is not needed;
  - the deep odd-parity stage ran at about 30 % idle at the end of each direction; use more chunks;
  - peak memory in the deep line stage was 2.3 GB, from holding one direction's triples per chunk.

**Conclusion.** For the six-way hunt, spend on breadth (thousands of directions, small to moderate height)
rather than depth. Always run the D-line enumeration alongside, because it alone finds hubs and stars. The
six-way most expected from the star picture (F31) is a 3-D-line star, and those can only come from a wide
search.

## F33 (27 October 2026): every relation among the integral points is a line or a hub; "independent" four-ways sit on high-rank curves

**Language.** x³ + y³ = n is an elliptic curve, and the point at infinity (1 : −1 : 0) is a flex. Taking it as zero:
- three points are collinear exactly when P + Q + R = 0;
- −(x, y) = (y, x), which is why the line finder must include swaps, and why "mirror" hubs exist.

So a line is a 3-term relation among the integral points, a hub a 4-term relation P₁ + P₂ = P₃ + P₄, and a D-line
point R = −(P₁ + P₂) is a rational point of small height. This is the chord-and-tangent law of the Ta(k) upper
bound literature (Boyer, Su) and of Choudhry's constructions. Bowties and stars are small "orchard" configurations
(Sylvester; Burr–Grünbaum–Sloane; Green–Tao: extremal 3-point-line configurations lie on cubics).

**Method** (`curve_relations/`):
- **Data:** 1,378 coprime k ≥ 4 numbers: the exhaustive four-ways ≤ 10¹⁷ and at 10²³–2.5·10²³, the 43 five-ways,
  and the Mac line-search union.
- **Relations:** for each, the height-pairing matrix of the k integral points. LLL on [identity; 10²⁰·H] gives
  candidate integer relations with |cᵢ| ≤ 1,000, and each is checked *exactly* with the group law (`elladd`).
  This takes under a second for all 1,378.
- **Ranks:** the curve rank by PARI `ellrank`, with the points as hints, for the 453 smallest curves. 358 are exact;
  the screen was stopped before the large n.

**Results:**

| shape (`line_structure.py`) | curves | rank of the integral points | relations found |
| --- | ---: | ---: | --- |
| line + free (k = 4) | 1,233 | 3 | one 3-term, coefficients ±1 |
| hub (k = 4) | 87 | 3 | one 4-term, coefficients ±1 |
| independent (k = 4) | 15 | **4** | **none** |
| bowtie (k = 5) | 40 | 3 | two (a 3-term and a 3- or 4-term; the basis choice varies) |
| line + 2 free (k = 5) | 3 | 4 | one 3-term |

- **Lines and hubs are the only relations.** All 1,403 relations found have every coefficient ±1 and 3 or 4
  terms. There is no 2P = Q + R (a tangent through an integral point), and no 5-term relation. The geometric
  search (lines + D-lines) therefore sees *all* the structure there is.
- **The "independent" four-ways are a different mechanism: rank.** Twelve of the 15 have an exact curve rank:

  | group | curves | mean rank | rank ≥ 6 |
  | --- | ---: | ---: | ---: |
  | independent | 12 | **5.83** (4, 4, 4, 5, 6, 6, 6, 6, 7, 7, 7, 8) | 8 of 12 |
  | line + free, size-matched (10¹¹–4·10¹⁸) | 235 | 4.12 | 10 of 235 |
  | hub, size-matched | 16 | 3.88 | 0 |

  So four integral points arise either from **structure** (one relation, so the points span rank 3, on curves
  of typical rank 4) or from **rank** (no relation, on curves of rank about 6–8). These are the "1 % with no
  pattern". 266890627295626663 has rank 8.
- **Six-way consequence (a guess, not a theorem).** On this evidence, a six-way comes either:
  - by structure: three relations, so the points span rank 3, as in a star of three D-lines or two bowtie lines
    plus a hub; any curve of rank ≥ 3 can carry it, which is the geometric search;
  - or by rank: few relations, needing rank around 8–10 or more, which the line searches cannot target.

  A rank-targeted search would mean high-rank curves of the right size, Elkies-style, where the integral points
  are then counted directly.

## F34 (28 October 2026): night of 27–28 October: 29 new coprime five-ways; exhaustive four-ways to 10²²; line-method recall by size

**Runs** (scripts in `night_7of9/`; outputs in `night_7of9/results_27oct/` and `a047697/cab_*_k4_part*.txt`):

| machine | job | candidates counted exactly | four-ways | five-ways (new) | time |
| --- | --- | ---: | ---: | ---: | ---: |
| 7of9, 4× RTX 2080 Ti | exhaustive, k ≥ 4, 0 < n ≤ 10²² | all n | 1,107 | 11 (0) | 13.2 h |
| 7of9 CPU | D-lines, 20,000 directions, height 200 | 158.1 M | 385 | 2 (0) | 1.0 h |
| 7of9 CPU | D-lines, 20,000 directions, height 550 | 1,189 M | 731 | 7 (**2**) | 9.4 h |
| worf CPU | lines, ranks 1,401–20,000, height 800 | 1,436 M | 2,188 | 34 (**27**) | 10.6 h |

**Verification:**
- **GPU output:** all 1,118 numbers it reports were recounted on the Mac (PARI factorisation + divisor test), and n,
  k and every representation agree, as sets.
- **GPU against earlier lists:** it reproduces exactly the 11 known five-ways ≤ 10²² and the 204 four-ways ≤ 10¹⁷
  from the earlier CPU run.
- **Catalogue against GPU:** every catalogue four-way ≤ 10²² is in the GPU list, which has 1,107; no targeted
  search had found one the GPU misses.
- **The 29 new five-ways** were recounted independently from n alone.

**Catalogue** (`results/a047697_catalogue.txt`): **6,785 four-ways and 72 five-ways**. Four-ways are now complete
for n ≤ 10²² and 10²³–2.5·10²³.

**Predictions** (made the evening before): user 10 new five-ways (3 on 7of9, 7 on worf); Claude 5 (range 2–9).
**Actual 29** (2 on 7of9, 27 on worf). Breadth over ranks 1,401–20,000 was far richer than either estimate.

**The 29 new five-ways:**
- **Size:** 7.5·10²³ to 3.1·10³⁵. The smallest, **751273218784283299882407**, is the first known five-way above
  the exhaustive bound of 2.5·10²³.
- **Divisibility:** 28 of 29 are divisible by 7.
- **n mod 9:** 1 for 17, **0 for 6, 8 for 6**. Before this, almost every five-way was ±1 (mod 9).
- **Split primes:** 11–14 (11: 10, 12: 11, 13: 7, 14: 1), up from 8–10 below 10²³: larger n needs more divisors.
- **Off-profile:** 8 contain a prime ≡ 2 (mod 3) (5, 23, 29, 113, 173, 293, 953); 3 are not cubefree.
- **Positive representations:** at most 3 (14 have 2), so none is a candidate for A080642(5).
- **Shape:** all 29 are bowties (two lines through a shared point), including the two found by D-lines.

**Line-method recall by size.** Fraction of the exhaustive four-ways found by the night's targeted runs. These are
four-ways in general, not only those of the shapes the searches target.

| decade | four-ways | worf lines | D-lines h200 | D-lines h550 | any |
| --- | ---: | ---: | ---: | ---: | ---: |
| 10¹²–10¹³ | 14 | 0 | 7 | 7 | 50 % |
| 10¹³ | 26 | 0 | 12 | 15 | 58 % |
| 10¹⁴ | 39 | 3 | 22 | 24 | 64 % |
| 10¹⁵ | 48 | 9 | 26 | 32 | 69 % |
| 10¹⁶ | 66 | 11 | 21 | 33 | 52 % |
| 10¹⁷ | 77 | 15 | 20 | 33 | 51 % |
| 10¹⁸ | 127 | 17 | 36 | 48 | 46 % |
| 10¹⁹ | 167 | 7 | 42 | 59 | 37 % |
| 10²⁰ | 216 | 20 | 29 | 48 | 29 % |
| 10²¹ | 316 | 31 | 40 | 58 | 27 % |

- **The D-line runs alone find 50–70 % of all four-ways up to 10¹⁶.** They cover all 20,000 cheapest directions,
  including the cheap ones the worf run skipped.
- **Recall falls with n,** as the heights needed grow like n^(1/6).
- **worf's lines (ranks > 1,400 only) find few small four-ways but most of the large five-ways:** expensive
  directions reach large n even at modest height (F32).

**A080642 (cubefree taxicab).**
- **All-positive numbers up to 10²²:** the exhaustive list contains exactly three coprime numbers with ≥ 4 positive
  representations, all cubefree: 1801049058342701083, 682238339160892906483 and 2724248230569896697541 (the last a
  five-way with 4 positive).
- **This independently confirms A080642(4) = 1801049058342701083**, and that 682238339160892906483 is the second
  cubefree positive four-way.
- **A080642(5) > 2.5·10²³** (see `cubefree.md`).

**Yields per CPU-hour** (one worf hour is about 22 threads; one 7of9 hour is about 56 threads):
- worf lines: 207 four-ways and 3.2 five-ways per hour;
- D-lines at height 550: 78 four-ways (26 of them hubs) and 0.7 five-ways per hour.

Lines over expensive directions are the five-way engine; D-lines are the hub and small-n engine.

## F35 (28 October 2026): rank predictors, the height shell, and why bowties do not complete

Three tests of "blue-sky" ideas on data in hand.

**1. A Mestre–Nagao score predicts rank** (the 358 curves with exact rank, from `curve_relations/ranks.txt`). The
score is S(P) = Σ_{p ≤ P, p ∤ 6n} −a_p·log p / p on Y² = X³ − 432n² (PARI `ellap`; about 0.2 s per curve for
P = 10⁶).

| predictor | AUC, rank ≥ 6 vs ≤ 4 | Spearman ρ with rank |
| --- | ---: | ---: |
| S(10⁶) | **0.95** | +0.35 |
| S(10⁵) | 0.93 | +0.28 |
| number of split primes | 0.57 | +0.38 |
| log n | 0.36 | +0.35 |

- **The mean score rises with rank:** 26, 29, 36, 44, 51, 66 for ranks 3–8. It is nearly independent of size
  (slope −0.08 per unit of log n).
- **Root number:** it matched rank parity in 358 of 358 cases.
- **Independent four-ways against line + free:** AUC 0.83 (mean score 44 against 30).
- **As a filter for multiplicity it is only moderate.** Size-matched AUC is 0.72 for four-ways, and also for
  five-ways, against random 3-way line candidates. Five-ways against four-ways gives 0.46: our five-ways are
  bowties, made by structure, not rank. S(2000) keeps most of the signal (0.68–0.70).
- **Use:** the rank route (independent multi-ways; cubefree all-positive candidates), not the line search.

**Addendum (28 October, unbiased sample).** Exhaustive four-ways ≤ 10²² contain 26 independent ones (2.3 %). Ranks of
the 14 not ranked before plus size-matched controls (`curve_relations/ranks_indep_1e22.txt`; PARI `ellrank` needs
`gp -D nbthreads=1` at this size, 1–3 min per curve):

| group | exact ranks | mean |
| --- | --- | ---: |
| independent | 4, 4, 4, 4, 4, 5, 6, 7, 7, 8 (plus 4 with bounds 4–6) | 5.3 |
| line + free controls | 3, 3, 3, 4, 4, 4, 4, 4, 4, 5 | 3.8 |
| hub controls | 3, 3, 4, 4, 4, 4, 4, 4, 4, 4, 5, 7 | 4.2 |

Independent four-ways sit about 1.1–1.5 ranks higher (two rank 7 and one rank 8; 58350391018399258021 has rank
8), but one hub control also has rank 7, and half the independent ones have rank exactly 4: a tendency, not a
rule.

**2. The integral points of a multi-way lie on a thin shell, at least 60° apart** (72 five-ways and 800 four-ways;
canonical height Gram matrices).
- **Heights:** the relative spread (max − min)/mean has median 4.5 % (90th percentile 10.8 %).
- **Points on a common line:** |cos| has median 0.502, as P + Q + R = 0 with equal heights forces.
- **Pairs with no common line (2,832):** |cos| ≤ 0.5 in every case, mostly 0.1–0.3. Random directions in dimension
  3 or 4 exceed 0.5 about half the time.
- **This is the gap principle for integral points** (Mumford, Silverman; Helfgott–Venkatesh, JAMS 2006, who bound
  integral points by sphere packing in the Mordell–Weil lattice).
- **Heuristic consequence:** six representations are 12 shell vectors at least about 60° apart. Rank 2 holds at
  most 3, the hexagon. Rank 3 holds at most 6, essentially only as the A3 (face-centred cubic) minimal vectors:
  6 points with 4 three-term relations, the **complete quadrilateral**. Removing one point leaves two lines
  through a common point: a **bowtie**.

**3. No bowtie completes to a complete quadrilateral: denominators always divisible by 6 (now Theorem 8).**
- **The two candidates:** a bowtie A + B + C = 0, A + D + E = 0 implies B + C = D + E. Its two possible sixth
  points are ±(B − E) = ±(D − C) and ±(B − D) = ±(E − C), each the third point of two chords (one through a
  non-shared point of each line).
- **The data:** for all 69 bowtie five-ways, all 138 candidates are rational, non-integral, with denominator
  divisible by **both 2 and 3**. The smallest is 6 (6 bowties); 2-adic valuations run 1–8, 3-adic 1–5.
- **Explained and proved: THEOREMS.md Theorem 8.** Give each integral point a p-type (which coordinate p
  divides; defined for p = 2 when n is odd, for p = 3 when n ≡ ±1 mod 9). A chord between points of opposite type
  has a third point that is not p-integral (Lemma 8a; a two-line valuation argument). So every line keeps its
  type (8b). The bowtie completions join a point to the *swap* of a point on the other line, so they have
  opposite type at both primes, and their denominators are divisible by 2 and 3.
  - **Theorem 8c:** for n odd or n ≡ ±1 (mod 9), no six coprime representations form a complete quadrilateral.
  - **Coverage:** all 72 five-ways have n odd; 8 of the 6,785 four-ways are outside the theorem.
  - The earlier component-group observation at 3 (c₃ = 3, integral points off the identity component) is the
    same phenomenon seen through the Néron model.
- **Consequence (gap principle heuristic + 8c):** a coprime six-way needs its six points to span rank ≥ 4, for
  example a bowtie plus a free point, or to arise by rank. Line searches with exact counting still catch the
  former.
- **Next:** use the types elsewhere: which hub meeting points R can have small D; whether a bowtie + free point is
  constrained by types too.

## F36 (28 October 2026): how much rarer six-ways are, and a split-prime filter for six-way hunting

**Transition rates** (line_structure shapes of the whole catalogue; exact counting means every representation of
a line-found n is known, so these are unbiased given the line):

| n range | line + free four-ways | → bowtie (second line) | → line + 2 free (extra free point) |
| --- | ---: | ---: | ---: |
| ≤ 10²² | 955 | 10 (1.0·10⁻²) | 1 (1.0·10⁻³) |
| 10²²–10²⁷ | 1,647 | 17 (1.0·10⁻²) | 2 (1.2·10⁻³) |
| 10²⁷–10³¹ | 2,491 | 24 (9.6·10⁻³) | 0 |
| ≥ 10³¹ | 1,358 | 18 (1.3·10⁻²) | 0 |

- **A second line is common and steady:** about 1 in 100 at every size. That is the five-way : four-way ratio.
- **An extra free point is about 10× rarer,** and rarer at large n (0 of 3,849 above 10²⁷).
- **By Theorem 8 a bowtie cannot be completed,** so a six-way from a bowtie needs a free point.
- **Richness:** the free-point rate roughly doubles per extra small split prime (next table), and five-way n are
  richer than four-way n.
- **Estimate:** six-ways about 1 : 300 to 1 : 1,500 of five-ways at our sizes, central about 1 : 500, not 1 : 100.

**The free-point rate rises steeply with split primes.** Line candidates of the Mac test (11.2 M, line + free
four-ways among them); s = number of split primes below 1,000:

| s | 4 | 5 | 6 | 7 | 8 | 9 | 10 | 11 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| share of candidates | 21 % | 32 % | 25 % | 14 % | 5.8 % | 1.9 % | 0.5 % | 0.1 % |
| four-way rate | 1.7e-5 | 3.7e-5 | 7.8e-5 | 1.6e-4 | 2.7e-4 | 5.2e-4 | 6.8e-4 | 1.2e-3 |
| share of the 72 five-ways | 1 % | 8 % | 14 % | 15 % | 25 % | 19 % | 11 % | 6 % |

**Filter benchmark** (`line_enum.py --hero R --hero-pmax 1000 --core 0`; 300 unsearched directions, height 300; Mac):

| filter | candidates | enumerate + count | four-ways | five-ways kept (of 72) | ground per CPU-hour |
| --- | ---: | ---: | ---: | ---: | ---: |
| hero 4, primes < 200 (used so far) | 3.29 M | 30 + 331 s | 14 | 72 | 1× |
| hero 7, primes < 1,000 | 0.77 M | 49 + 115 s | 12 | 55 | 2.2× |
| hero 8, primes < 1,000 | 0.29 M | 50 + 56 s | 5 | 44 | 3.4× |

- **For six-way hunting** (which needs a rich n), hero 8 / 1,000 gives about 2–2.5× the six-way yield per CPU-hour.
  Hero 7 / 1,000 is the compromise if five-way counts also matter (about 1.7× the five-way yield per CPU-hour).
- **Enumeration now costs more** (the filter tests 160 primes per triple); an early-exit or gcd-based test would
  recover part of it.

## F37 (28 October 2026): choose directions by the richness of E = a² + ab + b²

Every n on direction (a, b) is divisible by E (Theorem 2), so a direction whose E carries many small split primes
gives every candidate that richness for free. worf's line run of 27–28 October (ranks 1,401–20,000, height 800;
per-direction candidate counts from its log; four- and five-ways by their line's direction):

| split primes < 1,000 in E | directions | four-ways per 1,000 directions | five-ways per 1,000 directions |
| ---: | ---: | ---: | ---: |
| 0 | 5,443 | 42 | 0.18 |
| 1 | 8,151 | 113 | 1.96 |
| 2 | 2,531 | 154 | 2.77 |
| 3 | 2,118 | 269 | 6.14 |
| ≥ 4 | 357 | 213 | 5.60 |

**Within cost bands** (E rich = ≥ 2 split primes in E, five-ways per 1,000 directions):

| cost band | E poor | E rich |
| --- | ---: | ---: |
| 10⁷–10⁸ | 3.48 | 6.49 |
| 10⁸–5·10⁸ | 0.98 | 4.93 |
| 5·10⁸–1.4·10⁹ | 0.65 | 3.10 |

- **The effect is not a cost artefact:** it is 2–5× within every band.
- **E-rich yield decays slowly with cost** (about cost^−0.17), so going further out in E-rich directions beats
  taking every direction in cost order.
- **Night 2 list:** `night_7of9/dirs/rich_E2_60000.txt` holds the 60,000 cheapest never-searched directions with
  ≥ 2 split primes in E. They have true ranks 1,376–214,614 and cost up to 4.9·10¹⁰; 18,292 of them have ≥ 3.
  That is 93,721 E-rich among the first 300,000 unsearched.

## F38 (28 October 2026): size matters at fixed richness; prime weights do not; faster filter; which six-way shapes survive

**1. The free-point rate falls steeply with n at fixed richness** (Mac line candidates; rate of line + free
four-ways per candidate; s = split primes < 1,000):

| s | n < 10²² | 10²²–10²⁶ | 10²⁶–10³⁰ |
| --- | ---: | ---: | ---: |
| ≤ 6 | 3.8e-4 | 3.5e-5 | 7.8e-6 |
| 7–8 | 1.5e-3 | 1.8e-4 | 3.8e-5 |
| ≥ 9 | 4.0e-3 | 6.6e-4 | 1.3e-4 |

- **The rate falls about 5–10× per four decades of n.** A six-way (a bowtie plus a free point) is therefore most
  likely just above the exhaustive bound, at 2.5·10²³–10²⁷, and much less likely above 10³⁰.
- **In worf's output** 18 of 34 five-ways and 1,040 of 2,188 four-ways are above 10³⁰, but they carry only about
  5 % of the expected six-way chance.
- **`night_cpu.sh` now takes NMAX** (e.g. 1e30) for six-way hunting.
- **Corollary:** extending the exhaustive GPU search just above 2.5·10²³ searches the densest region for six-ways.

**2. Individual primes carry no weight beyond the count.** At equal s, the enrichment of each split prime < 160 in
four-ways against candidates is 0.95–1.27 (37: 1.27, the largest). The count of small split primes is the
signal; a weighted score adds little.

**3. Faster filter.** Testing only the split primes, with early exit both ways, gives identical output and
enumeration 1.46× faster at hero 8 (1.94× at hero 4).

**4. Six-way shapes after Theorem 8 (types).**
- **Complete quadrilateral** (rank 3, 4 lines): impossible for n odd or n ≡ ±1 (mod 9) (Theorem 8c).
- **Triangle** (rank 3; lines v₁v₂p₁, v₂v₃p₂, v₃v₁p₃ with orientation signs σᵢ): ruled out heuristically, not
  proved.
  - Types force σ₁σ₂σ₃ = +1.
  - With equal heights h₀, each line forces cos = −½ between its points. The Gram determinant of v₁, v₂, v₃ is then
    h₀³(¼ − σ₁σ₂σ₃/4) = 0, so ĥ(v₁ + v₂ + v₃) ≈ 0.
  - That needs a rational point of height far below the integral points'. With heights equal only to within about
    5 %, this is not a proof.
- **Rank-4 shapes are unconstrained by types:** two disjoint lines; a bowtie + a free point; a line + a hub sharing
  one point. They contain no cycle of lines.
- **These are what remains, and line searches with exact counting catch all three.**

## F39 (28 October 2026): n ≈ cost²·h⁶, per-direction heights, and why E-rich directions work

**1. Size of n against direction cost and slope height** (60 directions across the night lists; 60 random slopes at
each of 8 heights; chord formula):

  median log₁₀ n = −0.06 + 2.05·log₁₀ cost + 6.00·log₁₀ h   (rms 1.2 decades);
  10th percentile: −1.60 + 2.00·log₁₀ cost + 5.96·log₁₀ h.

So **n ≈ cost²·h⁶**. With the cap n ≤ 10³⁰ (F38), expensive directions stop being useful at low heights: the
median passes 10³⁰ at h ≈ 415 for cost 10⁷, 86 for 10⁹, 39 for 10¹⁰. At fixed height 800, most slopes of such
directions are wasted.

**2. `line_enum.py --auto-height --auto-margin M`.** Each direction stops at the height where the 10th-percentile n
passes NMAX·10^M, capped at --height. 300 directions spread over the E-rich list, cap 10³⁰, hero 8 / 1,000:

| margin M | candidates kept | enumeration time | speed-up |
| ---: | ---: | ---: | ---: |
| 0.5 | 59 % | 2.7 s | 34× |
| 2.5 | 77 % | 8.8 s | 10.5× |
| 3.5 | 87 % | 17.5 s | 5.3× |
| 4.5 | 94 % | 33.6 s | 2.75× |
| fixed h 800 | 100 % | 92.5 s | 1× |

The lost candidates sit in the low tail of n at large height (slopes with cancellation).
`night_7of9/dirs/rich_E2_400000.txt`: 400,000 unsearched E-rich directions, cost 1.3·10⁷–8.5·10¹¹ (from a pool of
1,563,877 directions up to cost 1.2·10¹²).

**3. E-rich directions work only by enriching n.** Four-way rate per candidate by s(n) (split primes < 1,000 in n)
and by split primes in E (Mac line files): at fixed s(n) the E count adds nothing (rates within noise, if anything
lower). E divides n (Theorem 2), so E-rich directions produce more candidates that pass the hero filter. The
filter on n is the right test; E only decides which directions to search.

**4. The other six-way shapes need three structured new representations beyond a line.**
- Per line candidate, adding one free point costs about 1.5·10⁻⁶ (worf: 2,188 four-ways in 1.44·10⁹ candidates);
  a second line through a point (2 new) costs about 2.4·10⁻⁸ (34 bowties).
- Two disjoint lines and line + hub need 3 structured new points. None has been seen: there is one bowtie and no
  disjoint pair among 11 M Mac candidates, and no 6-point configuration in the catalogue.
- **So "bowtie + free point" is the dominant six-way route** and F36's estimate (about 1 : 500 of five-ways) stands.

## F40 (29 October 2026): night 1 of the six-way hunt: ordinary lines below 10³⁰ are nearly exhausted

**Runs** (all n ≤ 10³⁰, split-prime filter with primes < 1,000, `--auto-height --auto-margin 4.5`; every candidate
counted exactly; files in `night_7of9/results_28oct/`):

| run | machine, threads | directions | filter | time | five-ways | new five-ways | new four-ways |
| --- | --- | --- | ---: | --- | ---: | ---: | ---: |
| n1 E-rich | worf, 22 | `rich_E2_400000` (cost 1.3·10⁷–8.5·10¹¹) | 8 | 32 min | 7 | 3 | 515 |
| n1 cheap, deep | 7of9, 56 | legacy ranks 31–1,400, heights 600 → 5,000 | 8 | 74 min | 6 | 1 | 401 |
| n2 deep | 7of9, 56 | legacy ranks 1,401–20,000, heights 800 → ≤ 5,000 | 7 | 2 h 06 | 7 | 0 | 88 |
| n2 rest | worf, 22 | `rest_1143877`: every other direction with cost ≤ 1.2·10¹² | 7 | 1 h 13 | 12 | 3 | 425 |
| n2 E-rich again | worf, 22 | `rich_E2_400000` | 7 | 35 min | 9 | 2 | 174 |
| n2 cheap again | worf, 22 | legacy ranks 31–1,400 to 5,000 | 7 | 48 min | 9 | 1 | 187 |
| **total** | | | | | **50 finds** | **10** | **1,786** |

No six-way. Catalogue: 8,571 four-ways and 82 five-ways (`results/a047697_catalogue.txt`).

**The 10 new five-ways** (all bowties):

| n | split primes < 1,000 | positive representations | note |
| --- | ---: | ---: | --- |
| 4,036,309,295,411,263,159,329,229 | 7 | 2 | |
| 42,260,261,086,176,943,302,212,239 | 7 | 2 | |
| 1,296,617,553,500,637,759,962,705,407 | 8 | 2 | |
| 3,657,763,792,654,176,108,524,148,073 | 9 | 2 | |
| 49,198,477,403,551,015,172,965,003,217 | 8 | 0 | |
| 82,027,323,974,760,829,384,613,994,009 | 7 | 2 | a prime cube divides n |
| 133,258,206,935,285,167,925,449,341,991 | 8 | **4** | cubefree; the second coprime five-way with 4 positive representations |
| 439,021,230,838,628,776,223,053,710,815 | 10 | 3 | |
| 604,435,071,167,779,766,756,548,521,087 | 7 | 0 | |
| 941,032,349,986,372,040,878,880,684,077 | 10 | 2 | direction (9, 28), slope height 2,435: reachable only by the deep run |

**What the night shows:**
1. **Saturation.** 40 of the 50 five-way finds were already known (found from other lines of the same bowtie, or
   by earlier runs). Below 10³⁰ the line method has found most of the five-ways it can reach.
   - Every allowed direction with cost ≤ 1.2·10¹² is now searched at filter 7. Beyond that cost, n ≈ cost²·h⁶
     (F39) leaves almost no slopes below 10³⁰.
   - Deeper slopes on cheap directions are exhausted too: the deep run on ranks 1,401–20,000 gave 7 five-ways, all
     known.
2. **Filter 7 against 8.** 4 of the 6 new five-ways from the filter-7 runs have exactly 7 split primes, so filter 8
   would have missed them. This matches F36 (filter 8 keeps 44 of 72 five-ways, filter 7 keeps 55).
3. **Speed.** worf's E-rich run found 28 new five-ways per 100 thread-hours, about 4× last night's rate for
   n ≤ 10³⁰. The 10× in raw speed (F36, F38, F39) partly went into the filter rejecting more candidates, as
   designed.
4. **The six-way odds were small.** 10 new five-ways (23 over two nights) at 1 : 300–1,500 (F36) means about
   0.01–0.08 expected six-ways, so finding none says nothing against the estimate.
5. **GPU reproducibility.** By mistake (an old `night_gpu.sh` that ignores GMIN/GMAX was left in the run folder),
   7of9's GPUs repeated the 0–10²² search at kmin 4. All 1,118 numbers (1,107 four-ways, 11 five-ways) match the
   run of 27–28 October exactly. Lesson: unpack every run into a fresh folder, and check the range in the first
   output.

**Strategy after night 1** (user and Claude, 29 October):
- **Ordinary lines below 10³⁰ are done** as a six-way route. What remains: filter 6, hubs (D-lines), and n above
  10³⁰, where the free-point rate per candidate is 5–10× lower per four decades (F38).
- **A hunt above 10³⁰ is only worth it with a new signal** that raises the six-way chance per candidate by about
  10×. Even 24 hours of worf with the present signals is unlikely to find one. Tonight's hub run (n3: 2 × 100,000
  never-searched D-line directions, filter 7, n ≤ 10³⁰) is as much to learn where hubs live and what predicts them
  as to find five-ways.
- **The GPU extension 2.5·10²³ → 10²⁴** (about 180 GPU-hours on RTX 5090 now, about 100 after the planned
  speed-ups) is not worth about €100 for its six-way chance alone. Plan: make the GPU code faster, then run it in the
  background on GPUs available occasionally. It would raise both bounds, A047697(6) and A080642(5), to 10²⁴.

## F41 (30 October 2026): the hub run: hubs are where the new four-ways are, but no 10× signal, and no all-positive hub

**Run** (7of9, 56 threads, 29 October 16:02 – 22:39; `night_7of9/hubs/`, results in `night_7of9/results_29oct_hubs/`):
D-lines on 150,000 never-searched directions of each parity, height 550, D ≤ 10⁹, filter 7 split primes < 1,000,
n ≤ 10³⁰. Enumeration 2 h 08 (even) and 2 h 14 (odd); exact counting of 276 M candidates, 2 h 20.

| parity | candidates | four-ways: hub / independent / line + free | five-ways |
| --- | ---: | --- | ---: |
| even (odd D) | 128.0 M | 70 / 5 / 135 | 1 |
| odd (even D) | 148.0 M | 134 / 5 / 124 | 3 |

458 distinct numbers (some found by both parities): 199 hubs, 10 independent, 246 line + free, 3 bowties.
**New: 172 four-ways (142 hubs, 29 line + free, 1 independent), no new five-way.** Catalogue: 8,743 four-ways,
82 five-ways.

**What the run shows:**
1. **Hubs are the unexplored territory.** 142 of 199 hubs were new, against 29 of 246 line + free (the line
   searches have covered those). 153 of the hubs are above 2.5·10²³.
2. **But D-lines are a poor six-way engine.** Four-ways per candidate: 1.7·10⁻⁶, against 7.2·10⁻⁵ for ordinary lines
   (worf, F40), about 40× less. The four five-ways were all known bowties. Even D (odd-parity directions) gives
   twice the hubs of odd D.
3. **Hub denominators are small**, as in F30: smallest meeting-point denominator D ≤ 6 for 93 of 199 (47 %), ≤ 12
   for 61 %, ≤ 100 for 96 %. Most common: 6 (30), 3 (26), 2 (23), 12 (12), 4 (11), 18, 24, 9.
4. **Chord costs.** One chord of each hub is cheap (median cost 6.5·10¹⁰, the searched directions); the other is
   typically expensive (median 2·10²²). Only one D-line needs to be enumerated: exact counting finds the rest. This
   is the same "one cheap line suffices" effect as for bowties.
5. **No all-positive hub.** Split of the two chords by number of positive endpoints: (1,1) 60, (0,1) 48, (0,0) 43,
   (0,2) 40, (1,2) 8, **(2,2) 0**. 12 % of chords have both endpoints positive; if the two chords were independent,
   about 3 all-positive hubs would be expected (Poisson probability of none 5.5 %). A mild deficit, worth
   rechecking with the 4 known all-positive hubs and more data.

**For the cubefree plan (`cubefree_plan.md`, step 3).** All-positive hubs per candidate here: 0 of 276 M (at most
about 10⁻⁸). With a five-to-four ratio of 1 : 100–500, a cubefree positive five-way from hubs would need of order
10¹⁰ candidates, about 40 nights of 7of9 at this rate. A positive filter that only *discards* candidates after
enumeration saves counting time, not enumeration time.
- **Idea (not tested):** for a direction (a, b), the chords whose two integer points are both positive form a
  sub-interval of slopes of the conic parametrisation (the positive arc is convex). Enumerating only that interval
  could cut enumeration by the same factor as the filter, about 8×. Measure before planning a cubefree night on
  hubs.

**For the six-way hunt.** Hubs do not give the 10× signal asked for in F40. The line + hub six-way shape remains
possible, but the candidate rate is 40× lower than for lines, and no five-way came from a hub.

## F42 (30 October 2026): cubefree plan steps 1–3 on the Mac: positive slopes lie on 3 arcs, a 5× cheaper hub search

**Positive arcs (step 3, the F41 idea).** For a direction (a, b), let the slope (s, r) of the conic parametrisation
run round the half circle. The lines with two positive points (never three, by convexity) fill **three arcs**, one
per choice of the negative point, not one interval (`pos_slopes.py`, 20,000-angle scan; a fourth piece appears when
an arc wraps round ±π/2). On 80 directions from the hub lists, height 400:

| parity | lattice slopes in the arcs | D-lines with both integer points positive | same, after filter 7 (height 550) |
| --- | ---: | ---: | ---: |
| even | 23.2 % | 9.7 % | 11.4 % |
| odd | 19.1 % | 9.4 % | 9.1 % |

The D-line share is about a third of the arc share, as expected: inside an arc, the denominator point R must also be
the negative one.

**`dline_enum.py --positive`** enumerates, for each s, only the r of the (padded) arcs, and keeps D-lines with both
integer points positive. **Validated:** on the same 80 directions it finds exactly the 67,299 positive D-lines of
the full sweep (0 mismatches); enumeration is 3.6× (even) and 4.3× (odd) faster. In the hub run enumeration was
71 % of the time and counting 29 %, so a positive hub run costs about 0.71/4 + 0.29/10 ≈ 0.21 of a full one:
**about 5× cheaper** per direction, for the hubs that matter to A080642. `night_cpu.sh`: `DPOS=1`.

**Elkies–Rogers curves (step 2): negative.** The 15 record k of Elkies–Rogers 2004 (minimal k for ranks 1–11, and
minimal conductor for ranks 4–8) are all cubefree, but have 0 or 1 integer representations (19 = 3³ − 2³,
657 = 10³ − 7³, 763002 = 85³ + 53³). High rank with small k gives rational points of large height, not integral ones:
the same lesson as N3 and N5.

**Literature (step 1).**
- OEIS A080642 (checked 30 October 2026): four terms, keywords hard, more; no bound or search limit for a(5).
  A web search found no published bound either.
- Butler's primitive five-way list (`Rama5way.html`; complete to 10²³, "nearly complete" to 2.51·10²⁸, built from
  known four-ways above 10²³): all **357** five-ways and all **24** six-ways (`Rama6way.html`) parsed and checked
  (every representation verified). **None has all its pairs coprime, so none is cubefree.** This extends the
  check of the 27 below 10²³ (`cubefree.txt`) but gives no new bound, since the list is not complete above 10²³.
- So our A080642(5) > 2.5·10²³ (from the exhaustive A047697 search) appears to be the best known bound.

**Cost of a positive hub night (estimate).** 7of9 did 300,000 directions in 6.6 h; in positive mode a 15 h night
covers about 3 million fresh directions. If yields per direction stay at the hub run's level, with 12 % of chords
positive on each side, that is of order 10 all-positive hubs (fewer if the (2,2) deficit of F41 is real), and a
cubefree five-way only with luck (a five-to-four ratio of 1 : 100–500). Its main value: the first census of
all-positive hubs, and a test of the F41 deficit.

**The night prepared (`night_7of9/pos/run_pos.sh`, `gen_pos_dirs.py`).** 1,500,000 never-searched directions per
parity (`dirs/pos_even_1500000.txt`, `pos_odd_1500000.txt`; costs 2.3·10¹⁰–8.6·10¹¹, skipping the legacy 20,000 and
the hub run's 150,000), in 12 chunks of 250,000, cheapest first, even and odd alternating. Positive filter-7
candidates per direction (n ≤ 10³⁰, height 550) fall with cost: 343 at cost 2·10⁹, 163–203 at 2–3·10¹⁰, 46 at
8·10¹¹; their slope heights stay spread over the whole range (median s 100–200, 99 % below 540), so a fixed height
550 is right and an auto-height cut would not help. Mac test: 0.42 CPU-s per direction, so 3 million directions
take about 6 h on 56 threads at Mac speed, 10–13 h on 7of9.

**Butler's method (checked 30 October).** `ramanujans.c` cuts the range of n into bands, generates every I³ + J³
in the band (about 2.4 million values), and inserts them in a 2²²-entry hash table (index from bits 8–29 of the low
part); only chains with enough entries are checked for real duplicates. This is our segment scheme with a hash in
place of the sort, and it is the planned GPU speed-up (bucket counts, then check only crowded buckets;
`writeup/01_gpu_search.md` §6). His list above 10²³ was "calculated using known 4-way solutions": multiples of
known primitive solutions with an extra point, which is why none of the 357 is coprime. Nothing there for the
coprime or cubefree search beyond confirming the hash idea.

## F43 (31 October 2026): the positive hub run: three new all-positive cubefree four-ways

**Run** (7of9, 22 threads, 30 October 14:08 – 31 October 09:49, 19 h 41; `night_7of9/pos/run_pos.sh`, results in
`night_7of9/results_31oct_pos/`): `dline_enum.py --positive` on 3,000,000 never-searched directions (12 chunks of
250,000, even and odd alternating, cheapest first), height 550, filter 7 split primes < 1,000, n ≤ 10³⁰. Each chunk
took about 1 h 35 to enumerate and 2–8 min to count; 55.2 M candidates in all (8.8–10.1 M in the first chunks, 2.3–2.6 M
in the last).

**Found:** 107 distinct k ≥ 4 numbers: 56 hubs, 48 line + free, 2 independent, and one five-way
(137904678696613339, line + two free points, known: one of the 12 exhaustive five-ways). **New: 45 four-ways**
(34 hubs, 10 line + free, 1 independent), all above 2.5·10²³. Catalogue: 8,788 four-ways, 82 five-ways.
Four-ways per chunk fell with cost, 19 and 27 in the first two chunks to 2–8 in the last.

**Three all-positive coprime four-ways, all new, all cubefree, all hubs** (recounted independently, every
representation exact):

| n | factorisation | representations | meeting-point D |
| --- | --- | --- | ---: |
| 1227282646644292205096095057 (1.2·10²⁷) | 7·13·19·31·43·103·109·181·331·487·811·1201·1669 | 854522762³ + 844977209³ = 878256377³ + 819248474³ = 1069350416³ + 164721521³ = 1070260544³ + 110371697³ | 48 |
| 2839283598503402079742309051 (2.8·10²⁷) | 7·13·19·31·199·397·829·15439·140281·373453 | 1251355555³ + 958210476³ = 1297603107³ + 868195252³ = 1365353238³ + 664944859³ = 1415863851³ + 98069050³ | 16,606,389 |
| 424174357271163809860926173135 (4.2·10²⁹) | 5·13·37·43·73·109·127·181·397·439·463·1999·139021 | 6359417472³ + 5506719983³ = 6970662063³ + 4404901292³ = 7206319502³ + 3682623303³ = 7507456482³ + 1013102423³ | 432,820 |

Before this run, 5 all-positive coprime four-ways were known (all in the catalogue, the smallest A080642(4)); now 8.
These three are cubefree numbers with four positive representations, i.e. cubefree "taxicab four-ways" beyond
A080642(4).

**What the run shows:**
1. **The positive mode works:** 3 all-positive hubs from 55 M candidates, against 0 from 276 M in the full hub run
   (F41). All three came from odd-parity directions (even D) in late chunks (o5, o5, o6).
2. **Positive endpoints.** Of the 107 numbers, 58 have 2 positive representations, 46 have 3 and 3 have 4. Hub chord
   split: (0,2) 37, (1,2) 16, **(2,2) 3**. If the second chord were positive as often as chords in general (12 %,
   F41), about 7 would be expected; 3 is low again (Poisson probability of ≤ 3 about 11 %). The F41 deficit is
   mild but persists.
3. **Positive hubs meet at larger denominators:** median D 84, D ≤ 100 for 54 % (F41, all hubs: 96 %); the three
   all-positive ones at 48, 4.3·10⁵ and 1.7·10⁷. A large dmax matters for this search.
4. **Cost of a cubefree five-way by this route.** About 3 all-positive hubs per 3 million directions (20 h on 22
   threads, about 8 h on 56). A five-way needs a fifth, positive, representation on top: at a five-to-four ratio of
   1 : 100–500, of order 300–1,500 all-positive hubs, i.e. 100–500 nights like this one. Not feasible by this route
   alone; the positive hubs are a census, not a path to A080642(5).

## Predictions for the night of 27–28 October 2026 (to check in the morning)

Number of **new** coprime five-ways found by the night's runs:
- 7of9 GPUs (exhaustive four-ways 0–10²²): 11 rediscovered, 0 new (certain unless a run was wrong);
- 7of9 D-lines at height 550; worf lines, ranks 1,401–20,000 at height 800; worf deep, ranks 31–1,400 at heights
  600–2,500.

| | 7of9 | worf | total new |
| --- | ---: | ---: | ---: |
| user | 3 | 7 | **10** |
| Claude | 0–1 | 2–8 | **5** (range 2–9) |

All known coprime k ≥ 4 numbers are now in one file, `results/a047697_catalogue.txt` (4,169 four-ways, 43 five-ways,
recounted exactly, 27 October). Exhaustive ratios of five-ways to four-ways: 1 : 203 for n ≤ 10¹⁷, and 1 : 214 at
10²³–2.5·10²³. In the targeted searches it is about 1 : 100.

## F44 (3 November 2026): the checks rerun on all the data, and the statistics redone on the exhaustive data only

**Why:** the catalogue is now complete for every k ≥ 4 to 2.5·10²³ (1,736 four-ways, 12 five-ways), and
cabtaxi.cpp gives every three-way to 10¹⁹ with its representations. Earlier statistics used 90 four-ways
(F1/F2) or a mix of exhaustive and line-search data (F33/F36), where the search method biases what is seen.

**Part 1 — exact checks on everything** (9,010 catalogue numbers, plus the 244,909 numbers with k ≥ 3 in
10¹⁷–10¹⁹; `recheck_all.py`, 6 s; mutated claims are caught, so the checks bite):

| check | tests (catalogue + worf) | failures |
| --- | ---: | ---: |
| T1–T3 on every collinear triple (`verify_theorems.py --reps`) | 492,028 triples, 70,916 directions | 0 |
| Theorem 5 (primes ≢ 1 mod 3 divide s fully; v₃) | 253,919 numbers | 0 |
| Lemma 6 (xy mod 3 shared) | 253,919 | 0 |
| Theorem 7 (D divides (b − a)E), every chord | 3.16 M | 0 |
| Theorem 8 (types at 2 and 3; opposite types ⇒ non-integral third point; lines keep type) | 3.89 M | 0 |
| open: a, b odd and D > 1 ⇒ D even | 1.58 M | 0 |
| open (item 11): same-line pairs keep the 3 in the chord's denominator | 2.95 M | 0 |

- **Relations (F33 on all 9,010, `curve_relations/relations_9010.txt`):** 9,051 relations, every one a 3-term
  (8,543) or 4-term (508) relation with coefficients ±1. Still no tangent relation, no 5-term relation.
- **Shapes (`all_ls_9010.csv`):** 8,393 line + free, 497 hub, 38 independent, 79 bowtie, 3 line + 2 free;
  the shapes and the relations agree on every number.

**Part 2 — statistics on exhaustive data only** (`exhaustive_mining.py`; controls are exact census windows,
`control_windows.py`, about 6,000 numbers at each of 10⁸, 10¹⁰, …, 10²², 2·10²³, and 2.4 M at 3·10¹⁷):

1. **Shape mix of the four-ways by size:**

   | band | four-ways | hub | independent |
   | --- | ---: | ---: | ---: |
   | ≤ 10¹⁵ | 90 | 3.3% | 2.2% |
   | 10¹⁵–10¹⁷ | 114 | 7.0% | 6.1% |
   | 10¹⁷–10¹⁹ | 204 | 13.2% | 2.9% |
   | 10¹⁹–10²¹ | 383 | 11.2% | 2.3% |
   | 10²¹–10²² | 316 | 14.2% | 0.6% |
   | 10²²–10²³ | 415 | 10.1% | 1.7% |
   | 10²³–2.5·10²³ | 214 | 11.2% | 0.9% |

   Hubs rise to about 11–14% by 10¹⁷ and then stay flat; independent four-ways fall to about 1%. Line + free
   stays the large majority (85–94%).

2. **Five-ways (exhaustive):** 10 bowties and 2 line + 2 free. Rates per line + free four-way: bowtie 6.6·10⁻³,
   extra free point 1.3·10⁻³, close to F36's line-search rates (1.0·10⁻², 1.0·10⁻³). Five : four is 1 : 145
   overall; by band 1 : 204, 3 : 371, 7 : 532, 1 : 629 (the last is 7% likely under a constant rate).

3. **Features by k, every n in 10¹⁷–10¹⁹:**

   | k | N | split primes | 7 \| n | 3 \| n | even | n ≡ ±2 (9) | all split | cubefree |
   | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
   | 1 | 20,000 | 3.54 | 37% | 25% | 33% | 26% | 13% | 83% |
   | 2 | 45 | 5.98 | 76% | 33% | 13% | 9% | 40% | 87% |
   | 3 | 244,704 (40,000 sampled) | 6.61 | 69% | 33% | 0.2% | 0.2% | 39% | 89% |
   | 4 | 204 | 8.15 | 81% | 25% | 0% | 1% | 60% | 89% |
   | 5 (all 12, other sizes) | 12 | 8.83 | 92% | **0%** | 0% | 0% | 83% | 100% |

   F1's trends hold at 10¹⁸ with far larger groups. Even three-ways: 492 of 244,704; n ≡ ±2 (mod 9): 474.

4. **Split primes grow with size, and the excess over k = 1 grows too:**

   | band | four-ways: mean split | k = 1 census | excess |
   | --- | ---: | ---: | ---: |
   | ≤ 10¹⁵ | 6.64 | 2.87 | +3.77 |
   | 10¹⁵–10¹⁷ | 7.60 | 3.40 | +4.19 |
   | 10¹⁷–10¹⁹ | 8.15 | 3.61 | +4.54 |
   | 10¹⁹–10²¹ | 8.67 | 3.74 | +4.93 |
   | 10²¹–10²² | 8.92 | 3.85 | +5.07 |
   | 10²²–10²³ | 9.23 | 3.93 | +5.30 |
   | 10²³–2.5·10²³ | 9.30 | 3.93 | +5.37 |

**What changed:**
- **Five-ways are not much richer than four-ways of the same size.** Against the four-ways within a factor 3 of
  each five-way, the 12 five-ways have +0.24 split primes on average (range −0.87 to +1.29). The earlier
  claim ("each extra representation costs about 2–3 more split primes", from 90 four-ways ≤ 10¹⁵ against
  five-ways ≤ 10²³) was mostly a size effect: four-ways themselves gain about 2.7 split primes from 10¹⁵ to 10²³.
  The split-prime filter for six-way hunting (F36, F38) still holds as a filter, but the step from four to five
  representations is mainly a second line, not more divisors.
- **Hubs are a steady ~11% share above 10¹⁷,** not a share that keeps growing; F41's "hubs are where the new
  four-ways are" was about what the line search misses, not about the population.
- **No five-way is divisible by 3** (0 of 12, against 23% of four-ways at the same sizes: 4% by chance alone,
  and one of many features looked at, so only a hint).
- **Ranks of the 9 new independent four-ways (10²²–2.5·10²³):** 27086411626209197593478 has rank 5,
  29439502687316546488027 rank 4; the other 7 stopped with a PARI error after 1–5 minutes (not the 2-hour time
  limit; probably the stack), to rerun with a larger parisizemax. So far consistent with F33's "independent ⇒ rank ≥ 4".
- **3 | n among five-ways, on all 82:** 11 of the 70 five-ways above 2.5·10²³ (line-search data) are divisible by 3,
  against 15.4 expected from four-ways of the same size found by the same searches. The 0 of 12 below 2.5·10²³
  is chance; at most a mild deficit.
- **Hubs as objects** (every pair of chords on four different representations meeting at the same non-integral
  R = (X/D, Y/D), all 9,010 numbers: 1,649 hubs in 576 numbers):
  - **every hub relation P₁ + P₂ = P₃ + P₄ appears as exactly 3 hubs,** one per pairing of the four points
    (−P = swap P turns P₁ − P₃ = P₄ − P₂ into another hub): 1,491 hubs in the 497 hub four-ways; 2 per bowtie (158 in 79).
  - **always:** gcd(X, Y) = 1 (R is a primitive representation of D³n); D | (b − a)E for both chords (Theorem 7);
    D even ⟺ both chords have a, b odd (1,181 / 1,181 and 0 / 468; Theorem 7 plus the open half), so the two
    chords of a hub always share their parity class; and X + Y ≡ 0 (mod D) ⟺ D | b − a (1,649 / 1,649; then proved for every chord: THEOREMS.md, Theorem 9).
  - gcd(X, Y) = 1 also holds for all 166,228 non-integral chords of the catalogue, not only hubs; it fails for
    non-coprime points, and is now proved: THEOREMS.md, Theorem 10 (a chord through two coprime points meets
    the curve again in a primitive point).
  - **often, not always:** 3 | D 71% (every hub with n ≡ 2 or 7 mod 9); D ∈ {6, 3, 2, 12} the commonest;
    gcd(D, n) = 1 62%; n odd 95%.
- **Unchanged:** every exact theorem and both open observations, on 25× more data; the relation structure
  (lines and hubs only); the bowtie and free-point rates, and so F36's six-way estimate.

## F45 (3 November 2026): conditions on n: no residue walls, but residue filters for a cheaper non-exhaustive GPU hunt

**Question (user):** is there a condition on n itself that every multi-way satisfies and most n fail? To prune the
exhaustive GPU search it must be (a) proven and (b) readable from a pair (x, y): in practice n mod small m.

**Search** (`residue_walls.py`; every class r mod m, m < 400; k = 1 census windows 1e8 – 2e23, all 244,704
three-ways in 1e17 – 1e19, the 1,736 exhaustive four-ways):
- 3,393 classes are empty among four-ways although ordinary sums put ≥ 8 there. Almost all are classes of **even n**
  (12 of 1,736 four-ways are even: a slope, not a wall) or **n ≡ ±2 (mod 9)** (F2).
- **Slopes, not walls:** predicting each class's k = 4 share from its own k = 1 → 3 decline (geometric in k) fits the
  single primes: mod 7 (0: 1,388 predicted / 1,412 seen; 1: 20/10; 6: 28/31), mod 13, mod 19. The classes that empty
  fastest are those with few local solutions: the nonzero cubes mod p (mod 13, x³ + y³ = ±1 or ±5 has 6 solutions
  against 9–36 for the rest). n ≡ ±1 (mod 13): 2 predicted each, 0 seen; ±5: 2 each, 3 seen.
- The strongest leftovers (n ≡ 134 mod 387: 14 predicted, 0 seen; 5 mod 129; 15 mod 56; …) are nested composite
  classes where the crude slope model overpredicts (it is 27% high for n ≡ 8 mod 9 alone); among 69,526 tests they
  are not evidence of a wall.
- **Why no wall can be proved this way:** every class with local solutions has a positive local density, so only a
  global argument (like Theorem 8 for configurations) could exclude it.

**Proven conditions that do exist are not usable:** k(n) ≤ #{subsets S of the split primes of n : f·∏_{p∈S} p^{v_p(n)}
≤ (4n)^{1/3}} (Theorem 5: s carries every non-split prime power, f; each s gives at most one representation). It needs
the factorisation of n, which the pair-sorting GPU never has. (Corrected, measured: it rules out k ≥ 6 for **67–70%**
of ordinary n at 10²² and 2·10²³, not a third; every five-way passes it easily, the smallest bound being 49.)
- **Computing it per pair does not pay.** Only primes ≤ (4n)^{1/3} matter, so trial division to P gives a proven upper
  bound, but at 2·10²³ it rules out 4% (P = 10³), 15% (10⁴), 42% (10⁵), 52% (10⁶), 68% (10⁸) of n, while the GPU spends
  about 0.3 ns per pair (sort-bound). Even P = 10⁴ costs ~100× that per pair to save 15%. A sieve (p | x³ + y³ along y
  for fixed x is an arithmetic progression) would make it cheap per pair, but the GPU walks rows of only ~10 pairs per
  x inside a segment, so per-row overhead dominates; it would need a long-row (Bernstein-style) redesign, for at most
  2–3× on a k ≥ 6 bound only.
- **Source bias in the five-way pass rate:** line/hub-search four-ways pass the residue filter below at 97.7%
  (exhaustive four-ways 90.8%), so 70/70 search five-ways passing has probability 0.20 and 12/12 exhaustive ones 0.31.

**Even n (user's question: are the even four-ways few and small?):** 12 of 1,736 four-ways below 2.5e23 (0.7%,
against 33% of ordinary sums), spread from 8.9e16 to 2.0e23 (none below 1e17), v₂(n) = 1–3; 31 in the whole catalogue,
**every one a hub (29) or independent (2), never a line**. Proved: THEOREMS.md, Theorem 12 (even n has no collinear
triple of coprime points; 0 of 524 even n with k ≥ 3 have one, against 97% of odd n). It explains the "even" slope of
F2: the commonest mechanism, lines, is closed to even n.

**A cheap PROVEN filter does exist (user: "mod 2 is cheap, does it buy anything?"): THEOREMS.md, Proposition 11.**
The non-split part f of n is read off the pair: by Theorem 5 it is the non-split part of s = x + y, and s ≤ (4n)^{1/3}
(about 10⁸ at 10²³), so f comes from a small precomputed table. k representations need k distinct s_i = f·m_i ≤
(4n)^{1/3}, so pairs with 37 f > (4n)^{1/3} (six-ways) or 19 f > (4n)^{1/3} (four-ways) can be dropped, exhaustively.

| n near | pairs cut, k ≥ 6 | k ≥ 4 (keeps the complete four-way lists) |
| --- | ---: | ---: |
| 10¹² | 39% | 34% |
| 10¹⁸ | 30% | 27% |
| 10²² | 28% | 25% |
| 2·10²³ | 27% | 24% |

- In `cabtaxi_gpu.cu` differences are rows of fixed d = s (n = (c + d)³ − c³), two thirds of all pairs: a failing row
  is skipped before counting, writing or sorting (16% of all pairs, free). Sums are rows of fixed a with s = a + b
  stepping by 1: a sequential table read marks failing pairs as SENTINEL like non-coprime ones (about 11% more).
- Estimated wall-time gain about 20–25% (the sort is 50–60% of the time), with every claim of the run kept.

**What the slopes do give: a cheaper non-exhaustive GPU hunt above 2.5e23.** Every condition below is a congruence
on (x, y) (e.g. 7 | n ⟺ y ≡ −x, −2x, −4x mod 7; n odd ⟺ x + y odd), so the GPU can enumerate only those pairs:

| filter | pairs kept | four-ways kept | five-ways ≤ 2.5e23 | all 82 five-ways | five-way yield per pair |
| --- | ---: | ---: | ---: | ---: | ---: |
| 7 \| n | 37% | 81% | 11/12 | 94% | 2.5× |
| 7 \| n, n odd | 25% | 81% | 11/12 | 94% | 3.7× |
| (7 \| n or 13 \| n), n odd, n ≢ ±2 (mod 9) | 26% | 91% | 12/12 | 100% | 3.9× |
| 7 \| n, n odd, n ≡ ±1 (mod 9) | 13% | 62% | 11/12 | 80% | 6.3× |

Such a run proves no bound, but it searches the region where every known five-way lives at a quarter of the cost,
and unlike the line/hub searches it is blind to geometry, so it would also catch "rank" six-ways.

## F46 (3 November 2026): other primes (user: "does Theorem 12 have siblings?"): a line's direction fixes the non-split part of n

**Data** (`primes_lines.py`; 253,919 numbers with k ≥ 3: the catalogue and every three-way 1e17 – 1e19):

| p | n with p \| n | carry a line | lines on those n: p divides … |
| --- | ---: | ---: | --- |
| 2 | 524 | **0%** | (none) |
| 3 | 82,326 | 98% | b − a and c always; a, b, a + b never |
| 5, 11, 17, 23, 29, 41, 47, 53 | 2,564 – 28,437 | 98% | b − a and c always (100%); a, b, a + b, E never |
| 7, 13, 19, 31, 37, 43 (split) | 45,896 – 176,575 | 95–97% | no rule (b − a 5–9%, E 17–55%) |

**Proved (THEOREMS.md, Theorem 13):** the values sᵢ = xᵢ + yᵢ of three collinear points are the roots of
E z³ − 3c(a + b) z² + 3c² z − (a − b)²n. With Theorem 5 this gives, for every p ≢ 1 (mod 3), v_p(b − a) = v_p(s)
exactly and p^{v_p(s)} | c: **the non-split part of b − a is the non-split part of n** (3: one less), checked on all
492,028 lines. p = 2 is the case where this is impossible (b − a is odd by Theorem 1(b)), which re-proves Theorem 12.

**Hubs and every other chord (THEOREMS.md, Theorem 14).** The s-cubic identities hold for a chord with a rational third
point R as well (166,228 chords): the denominator of x_R + y_R divides E, and the two chords of a hub satisfy
(a − b)² E′ s₃ s₄ = (a′ − b′)² E s₁ s₂ (3,298 pairs). On such chords v_p(b − a) − v_p(s) was never negative (75,208
tests; offsets 0–8, and ≥ 1 at p = 2), and it is a theorem: **for every pair of representations, the non-split part
of n divides b − a of their chord** (3,158,936 pairs; proof from one exact identity of the curve). Lines are the
equality case.

**Meaning:** primes ≡ 2 (mod 3) and 3 are not "random" in a line's n; the direction chooses them. A line search over
directions with b − a built from split primes only produces n whose non-split part is 1 (or 3^1), the "all split"
profile that 60% of four-ways and 83% of five-ways have (F44).

## F47 (3 November 2026): a complete line search (`line_complete.py`), validated against the exhaustive data

**What it does.** For each allowed direction, every coprime collinear triple with n <= B, with no height cap and no
filter (six_way_ideas.md idea 1). Rigorous per-direction heights from n = E S1 S2 S3 / ((a - b)^2 G^3) (Theorem 13):
the S_i are definite (|S1 S2 S3| >= M h^6, M exact) and G | content * R0' (resultants). Tier 1 enumerates every slope
to H(Glo); tier 2, for each set T of primes that can enlarge G, enumerates the lattice of slopes in T's residue
classes (Gauss-reduced basis, points in the box) to H(Glo * prod_T p^(hi - lo)). Each unordered triple is kept once,
at its least-height ordering (Theorem 4 (ii) gives every ordering's slope), so no set is needed and directions split
into s-chunks. With --count every n is counted exactly (PARI + collisions.all_reps) and only k >= 4 is written, with a
certificate line per job (slopes, triples, largest k); --resume skips logged jobs.

**Validation:**
- `--selfcheck`: on 6 directions at B = 1e14, the triple sets equal brute force over every slope to 2x the largest
  bound, with no duplicates.
- B = 1e19, all 1,197 allowed directions of cost <= 1e7 (10.7 M slopes, 196,358 triples, 30 s on the Mac):
  **all 153,916 lines of the exhaustive data in those directions produced, none missing**; every one of the 196,357
  numbers produced is in the exhaustive k >= 3 lists; with counting, all 263 catalogue numbers <= 1e19 having such a
  line are found with the catalogue's k, and nothing else. These directions carry 64% of all k >= 3 numbers <= 1e19.
- Bound sharpness: worst slope reaches 0.999 of its bound (line_heights.py brute checks to 1e16).

**What the bounds showed:** the earlier "deep" runs stopped cheap directions at height <= 5,000; complete coverage to
1e30 needs 43,000 - 75,000 for (3,4) and up to 147,000 for (12,13). The cheap directions were complete only to about
1e25.

**The 1e30 run** (`night_7of9/lc/run_lc.sh`, 7of9): every allowed direction of cost <= 1.2e12 (1,563,877 directions),
B = 1e30, every n counted. Estimate: 5e10 - 8e10 slopes at ~4.5 us, ~1e9 exact counts; 2-4 h on 60 processes.

## F48 (4 November 2026): the complete line search to 1e30: no six-way; 11 new five-ways; yield by direction

**Run** (7of9, 60 processes, 3 Nov 19:14 - 4 Nov 21:14; the last 3 directions on the Mac with the level-lifted code,
`line_complete.py` dd80ac2): every allowed direction with cost <= 1.2e12 (1,563,877), every coprime collinear triple
with n <= 1e30, every n counted exactly. Files: `night_7of9/results_lc_1e30/` (k >= 4 list, gzipped job log).

**Certificate:** 1,567,014 jobs, each logged once; all 1,563,877 directions present; the 3,450 s-chunks of the 313
cheap directions tile [0, H_max] exactly; 1.845e11 slopes, 1.592e9 triples counted; **largest k = 5**.
So: **no n <= 1e30 with a line in a direction of cost <= 1.2e12 has six coprime representations.**

**Results:** 8,962 numbers with k >= 4 (8,898 four-ways, 64 five-ways); new to the catalogue: 2,596 four-ways and
**11 five-ways** (two near 1e25 and one near 1e26, in the range the earlier cheap-direction runs had capped at
height 5,000). All new ones verified by independent recount; no disagreement with the catalogue.
- **Coverage of the class:** 64 of the 66 known five-ways <= 1e30 (97%) have a line of cost <= 1.2e12; the other two
  (98066148860955562962446737, 162898846056046374394270913) have lines only of cost 8e12 - 1.3e13. Four-ways: 93.8%
  (8,898 of 9,489 known <= 1e30).
- **Slowest directions:** three near-diagonal directions with 3^11 or 3^10 in a or b ran for days under a crude bound
  (v_3(G) up to 13 when 3^e > 2e5); lifting classes level by level shows v_3 <= 1 there, and they took 2 s.

**Yield by cost band (lines of four- and five-ways found per slope):**

| cost band | directions | slopes | four-way lines | five-way lines | five-way lines per 1e9 slopes |
| --- | ---: | ---: | ---: | ---: | ---: |
| <= 1e2 | 2 | 6.3e9 | 1,260 | 26 | 4.15 |
| 1e2 - 1e4 | 21 | 1.3e10 | 1,222 | 29 | 2.29 |
| 1e4 - 1e6 | 290 | 1.8e10 | 1,418 | 23 | 1.27 |
| 1e6 - 1e8 | 4,497 | 2.6e10 | 1,647 | 33 | 1.27 |
| 1e8 - 1e10 | 74,903 | 3.3e10 | 1,740 | 57 | 1.72 |
| 1e10 - 1.2e12 | 1,484,164 | 8.8e10 | 1,611 | 28 | 0.32 |

- Per direction: (3,4) 13 five-ways (3.8 per 1e9 slopes), (27,28) 5 (7.4), (12,13) 2, (16,21) 2, (12,19) 2.
- b - a = 1 directions: 13.6% of the slopes, 23% of the five-way lines (1.7x).
- **For a deeper run:** the cheapest directions give the most five-ways per slope (cost <= 1e4: about 3 per 1e9),
  and the 1e10 - 1.2e12 band the least (0.3). A complete run of the 23 directions with cost <= 1e4 to 1e33 is about
  10x their 1e30 slopes (~2e11), i.e. about one more 7of9 day.

## F49 (4 November 2026): the mining rerun on the class-complete set to 1e30 (8,898 four-ways, 64 five-ways)

The set: every n <= 1e30 with a line in a direction of cost <= 1.2e12 (F48), which holds 94% of the known four-ways
and 97% of the five-ways below 1e30. Unbiased within that class, it extends F44's statistics from 2.5e23 to 1e30 and
from 12 to 64 five-ways. It contains no hubs or independent four-ways (they have no line).

**Exact checks (item 5):** recheck_all.py, verify_theorems.py --reps and thm14_check.py on all of it: 0 failures
(about 680,000 tests, including 18,222 collinear triples and 497,904 pairs for Theorem 14).

**1. Split primes, five-ways against size-matched four-ways (factor 3):** +0.48 on average (median +0.59; 43 of 64
above, sign test p ~ 0.005). F44's correction stands, with a small real excess: half a split prime, not 2-3.
Four-ways gain about 0.5 split primes per two decades (7.9 at 1e15-1e19 to 10.6 at 1e28-1e30).

**2. Five : four ratio by size:** 1:270, 1:66, 1:223, 1:165, 1:119, 1:156 over 1e15-1e19, ..., 1e28-1e30; overall
1:139. **No decline**: the 1:629 of 1e22-2.5e23 (F44) was a fluctuation.

**3. Transitions per line + free four-way:**

| n | line + free | bowtie | line + 2 free |
| --- | ---: | ---: | ---: |
| 1e15-1e23 | 1,236 | 9 (7.3e-3) | 1 (8.1e-4) |
| 1e23-1e26 | 1,849 | 11 (5.9e-3) | 1 (5.4e-4) |
| 1e26-1e28 | 2,278 | 18 (7.9e-3) | 1 (4.4e-4) |
| 1e28-1e30 | 3,450 | 22 (6.4e-3) | 0 |
| all | 8,813 | 60 (6.9e-3) | 3 (3.4e-4) |

- Bowtie rate steady at ~7e-3 (F36: 1e-2; F44: 6.6e-3).
- **The extra-free-point rate is about 3x lower than F36's 1e-3** (3 events, so 95% range 0.7e-4 - 1e-3) and, if
  anything, falls with n. Since "bowtie + free point" is the main six-way route, **F36's six : five estimate moves from
  about 1:500 to about 1:1,500 (range 1:500 - 1:5,000).** Expected six-ways below 1e30: about 0.1 or fewer.

**4. 3 | n:** 8 of 64 five-ways, against 15.6 expected from size-matched four-ways (Poisson p = 0.027). **Explained by
Theorem 13:** 3 | n exactly when 3 | b - a on every line of n. 24.9% of four-way lines have 3 | b - a but only 12.8% of
five-way lines: a five-way with 3 | n needs both of its lines in such directions, and the most productive five-way
directions (b - a = 1: (3,4), (12,13), (27,28)) cannot carry 3 | n. Independent lines would give 6.2%; observed
12.5%. A structural effect, not an anomaly; for six-ways (bowtie + point) expect 3 not to divide n in most cases.

## F50 (4 November 2026): the complete line search in C++ (`line_fast.py` + `lc_fast.cpp`), about 40x faster

**Design.** Python (the validated `line_complete.Direction`) prepares each job: heights, G-levels, residue-class
lattices, conic point, factorisations of E and |a - b| (about 5 ms per direction). A persistent C++ process per worker
does the inner loops: tier-1 box and tier-2 lattice points; raw points; **G from the levels** (G = Glo prod p^(v_p - lo),
with v_p from the primitive forms mod p^hi, so no 128-bit gcd of six numbers); reduced points; **n = E s1 s2 s3 / (a-b)^2**
without cubing (Theorem 13); the canonical-ordering check; and the exact count from the factorisation assembled from
E, the s_i (64-bit Pollard-Brent) and (a - b)^2, with representations only at s = f * (subset of split blocks) <=
(4n)^(1/3) (Theorem 5). Every 128-bit product is overflow-checked; an overflow sends the job back to Python.

**Validation:** `--checkg` (G from levels = gcd of the six coordinates) on every slope of 7 directions; 1e19, cost <= 1e7:
all 196,358 triples and all k >= 4 rows identical to Python; 1e30, 315 random directions of cost 1e6 - 1.2e12: triples
and largest k identical to the 7of9 Python run, direction by direction, and the 68 k >= 4 rows identical; gcd128
unit-tested on 18,485 random pairs up to 126 bits. One bug was caught by these checks: the 64-bit shortcut of the binary
gcd shifted a 64-bit result by the common power of 2 (lost bits above 64), which dropped 26 of 567 triples in one
direction; fixed before any run.

**Speed:** about 0.6 - 1 us per slope at 1e30 including counting (Python: about 29 us per slope on 7of9). The whole
1e30 run would take under an hour on 7of9; every direction (cost <= 1.2e12) to 1e33 (about 1.85e12 slopes) about 5 - 7
hours; n is limited to 2^125 (about 4e37) by the 128-bit arithmetic.

## F51 (6 November 2026): the complete line searches are certified; independent recount of the catalogue

- **Lemma 15 (proved):** the S-forms of every direction are definite, so the height bound
  n >= E M h^6 / ((a - b)^2 G^3) holds with M > 0.
- **Exact certificate (`certify_M.py`):** M certified by Sturm sequences on all 1,563,877 directions, and every integer
  height used in the 1e30 and 1e33 runs checked in exact rationals against every G-level: 0 failures (log in
  verify_gp/). With the certificate logs of the runs (every job present, chunks tiling), both statements are now proofs:
  no n <= 1e30 (resp. <= 999999999999999945575230987042816) with a line in a direction of cost <= 1.2e12 has six coprime
  representations.
- **Independent recount (`verify_gp/reps.gp`, PARI/GP only):** all 18,392 catalogue numbers, 139 five-ways included,
  agree in count and representations.
- **Literature (web, 6 Nov):** nothing found stating Theorems 9-14; a hand check of the classical sources is on TODO.md.

## F52 (6 November 2026): the complete line search to int(1e33): no six-way; 49 new five-ways

**Run** (7of9, `lf33_v2`: line_fast.py + lc_fast.cpp, 60 processes, 5 Nov 18:18 - 6 Nov 17:07, the last 7 hours on the
single (3,4) job): every allowed direction of cost <= 1.2e12, every coprime collinear triple with
n <= int(1e33) = 999999999999999945575230987042816, every n counted exactly. Files: `night_7of9/results_lf_1e33/`.

**Certificate:** 1,567,293 jobs, each logged once, equal to the planned job list (chunks of the 313 cheap directions
as split by the run's code); 1.312e12 slopes, 1.592e10 triples; no Python fallback; **largest k = 5**. With Lemma 15
and the height certificate (F51) this is a proof: **no n <= 999999999999999945575230987042816 with a line in a
direction of cost <= 1.2e12 has six coprime representations.**

**Results:** 17,954 numbers with k >= 4 (17,823 four-ways, 131 five-ways, 67 of them above 1e30); new to the catalogue
over the run: **49 five-ways** and about 6,700 four-ways, all verified by independent recount. 128 of the 130 known
five-ways below the bound are in the class (the same two outside it as at 1e30, lines of cost 8e12 - 1.3e13).
Catalogue: 18,873 four-ways, 142 five-ways, all agreeing with the PARI/GP recount at the time of F51 plus the
recount of each new entry.
- The F49 projection (about 160-170 five-ways in the class to 1e33, about 80 new) was high: 131 and 49. The class
  five-way count grew by 131 / 64 = 2.05 for a 1000x larger bound (n^0.10 rather than n^0.14).

## F53 (6 November 2026): five-ways from elliptic curves: bowties of a fixed direction pair lie on a genus-1 curve

**Setting.** A bowtie through a (3,4) line: the (3,4) triple of slope (s, r) (line_enum's conic parametrisation) and a
second line in direction (a2, b2) through its point i. That line has two more rational points exactly when the
discriminant of the residual quadratic, a binary quartic Delta(s, r) in the slope, is a square: the bowties of a fixed
(pair, i) are the rational points of **w^2 = Delta(r)**, generically genus 1 (an elliptic curve). For the two recurring
pairs, (3,4)+(9,52) at point 0 and (3,4)+(27,28) at point 1, Delta is irreducible (no square factor): **no polynomial
family** (F-4b, negative), but a group.

**Generation.** From the few points of small height (`hyperellratpoints`) and the known bowties of the pair, the group
law (the parabola through three points of w^2 = quartic meets it in a fourth) generates points of growing height;
each is a rational bowtie, and often an integral coprime one. Two rounds gave 16 distinct coprime bowtie numbers:
the 5 known ones (Bernstein's 506433677359393, and 1.06e26, 1.72e27, 6.5e29, 7.6e32 from the complete line searches),
and **11 new coprime five-ways from 1.49e50 to 1.69e165**, all verified (on the curve, coprime, five distinct
representations) and **counted exactly** from n = 37 s1 s2 s3 (Theorem 13 for the (3,4) line; the s_i of the triple
factored by PARI, at most 20 s each): **each has exactly 5 representations.** The largest coprime five-way known
before was 3.8e35.

**Why it matters:** a cheap generator of coprime five-ways of any size, one elliptic curve per (direction pair,
shared point), with exact counting still feasible to ~1e165 because n factors through the small s-values. A
six-way on such a curve needs an extra free point (F49: rare and getting rarer); but the generator can produce
thousands of five-ways for that test. Not yet known: how many direction pairs have curves of positive rank, and
what fraction of their points give integral coprime bowties (here 20 of 46 and 11 of 41 points).

**First general run (`bowtie_mine.py`, 6 Nov):** every catalogue bowtie (150, on 137 direction pairs) defines its curve.
- **Ranks:** nearly all Jacobians have rank 2 - 5 ((3,4)+(27,28): 3; (3,4)+(9,52): 5); only one (0 - 4 bound) unresolved.
- **Integrality is common:** most generated points give coprime bowties (226 of 240 on (3,4)+(9,52), 156 of 168 on
  (3,4)+(27,28)); failures are mostly a non-coprime base triple.
- **Counted:** 135 distinct five-ways below 1e130 (two rounds, frontier 10, 51 s), all exactly 5 representations;
  15 new (1e60 - 1e130). Two rounds jump to large heights quickly, so few points fall below the counting limit.
- **Bug:** some curves get 0 points (seed not recognised; mostly second direction (a2, b2) with a2 > b2): orientation.
- **Orientation fix:** a bowtie's two lines may share a representation only up to swap; the second line is then
  replaced by its mirror so both pass through the same point. After the fix every curve finds its points.
- **Systematic enumeration (group law on the quartic, no Weierstrass map):** the four points on a parabola sum to a
  fixed class, so with O a known point, K = F(O,O,O), -P = F(P,O,K), P + Q = F(F(P,Q,O),O,O) (checked: inverses,
  associativity, multiples). Small combinations (coefficients -2..2) of up to 5 known points per curve: on
  (3,4)+(9,52) all 48 lattice points are coprime bowties, but their n jump 1e15, 1e33, 1e69, 1e112, 1e123, 1e129,
  1e167, 1e194, ... **Points are sparse in n:** with canonical heights ~ log n, a curve of rank r has only about
  (log N)^(r/2) points with n <= N, so each curve gives a handful of five-ways below 1e130 and unlimited ones above.
  All 161 five-ways found below 1e130 were already in the catalogue (all k = 5).
- **So:** the curves are an unlimited source of coprime five-ways at large n, nearly every point a bowtie; the cost
  of using them is the exact count, which needs the s-values (about n^(1/3)) factored: seconds at 1e130, much more
  above 1e200. Getting many five-ways below 1e130 needs many more curves, not more points per curve.
- **PARI version (`bowtie_hunt.py`, `verify_gp/quartic2ell.gp`):** each quartic with a known point is mapped to
  Weierstrass form (Washington, Elliptic Curves, Thm 2.17; checked: points map and map back exactly, and E's group
  law agrees with the parabola law), `ellrank` (known points as hints) gives a full-rank set of independent points
  (ranks 2 - 5), and small combinations are mapped back and tested. Exact counts use only s = f * (split-block
  subsets) (Theorem 5), with factorisation time limits (unknown k reported as "?", none occurred).
  **Harvest of all 136 seeded curves:** 165 coprime five-ways below 1e500 (coefficients -3..3), every one exactly
  k = 5, all already in the catalogue (the earlier runs had found them): each curve holds only ~5 - 20 points below
  1e500.
- **New curves without a bowtie seed are not productive:** for base (3,4) and 800 second directions (x 3 points),
  85 quartics have small rational points (all of positive rank), but their points give non-integral second lines
  (124) or non-coprime base triples (108); restricting to directions compatible with Theorems 1 and 13 gives 6 bowtie
  points (one known number); multiples up to 12P of a generator never give a bowtie on 41 such curves. Integrality is
  carried by the seed: on seeded curves nearly every point is a bowtie, on unseeded ones almost none. Why is open.
- **Conclusion:** the curves amplify each known bowtie into its finitely many siblings below any counting limit and
  unlimited larger ones; new five-ways at countable sizes still come from new seeds, i.e. from line searches.

## F54 (7 November 2026): all 168 five-ways (to 1.7e165) pass every exact theorem; the bowtie rule holds out of sample

- **Theorems on the whole five-way list,** including the 24 curve-generated ones above 1e60 (s-values factored by
  PARI, n never factored): Theorem 5 (168), Theorems 7, 9, 10, 14 on 6,720 chords each, Theorem 13 and 1(b) on 666
  lines: no failure.
- **Bowtie anatomy (4a), out of sample:** on 165 bowties (26 more than when found), the shared point's rank by
  s = x + y on its two lines: {low, low} 31, {low, mid} 69, {mid, mid} 37, {mid, high} 10, {high, high} 18,
  **{low, high} 0**.
- **Correction and partial proof (same day).** The earlier "about 31 expected" assumed the nine rank pairs equally
  likely; random real bowties (no integrality) give {low, high} in 1.6% (random slopes) or 2.5% (the bowties' own
  slopes and shared-point positions), so about 4 expected and P(0) = 0.017: suggestive, not overwhelming.
  Split by the shared point C: **C a sum** (32): ranks only (1,1) 10, (1,2) 10, (2,2) 12 -- **proved**: sums have
  s > n^(1/3) and differences s < n^(1/3) (n = s t with t = s^2 - 3xy), and no line holds three positive points, so a
  sum C always has a difference with smaller s on each line and is never lowest. **C a difference** (133): (0,0) 31,
  (0,1) 69, (1,1) 27, (2,2) 6, never (1,2) or (0,2): when a difference C is highest on one line (both other points
  differences) it is highest on the other too (6 of 6). That remaining part is open and rests on few cases.

## F55 (7 November 2026): relationships inside bowties (165)

- **lcm(E1, E2) | n** for every bowtie (Theorem 2 for each line); this block of split primes is a median 37% of
  log n (max 61%).
- **Every bowtie contains two mirror hubs** (330 / 330): P + Q = -C = R + T gives P + (-R) = T + (-Q), so the chords
  P R-bar and T Q-bar (and P T-bar, R Q-bar) meet at one point. Their meeting points have large denominators (median
  5.6e5; only 6% <= 12, none integral), unlike genuine hubs (mostly D <= 12, F41).
- **The two lines' costs are unrelated:** ratio median 10^3.8, spread 1 - 10^14: one cheap line, the other anything.
- **E1 and E2 share a split prime in 43%** of bowties, against 17% for lines of different four-ways of similar size;
  but **no excess** against a random draw from n's own split primes (60 observed, 57.9 expected, n < 1e60): sharing
  only reflects that both divide the same n.
- With F53 (bowties of a fixed direction pair are points of one genus-1 curve) and F54 (the shared point is never
  the lowest-s point of one line and the highest of the other), that is the bowtie structure found so far.

## F56 (7 November 2026): integrality on seeded bowtie curves -- a coset law on small samples, retracted at scale

On (3,4)+(9,52) at point 0 (the curve of Bernstein's five-way), the 14 small rational points (hyperellratpoints,
height <= 3000, plus a known seed) are 6 bowties, 4 with a non-integral second line, 4 with a non-coprime base triple.
With O a bowtie point and the quartic group law:
- a non-bowtie point plus any multiple of a bowtie point keeps its class (36 / 36 for each kind);
- 2N is an integral coprime bowtie for every non-bowtie N (8 / 8); two "second line not integral" points sum to a
  bowtie (4 / 4); two "base not coprime" points can sum to a "second line not integral" point (so that label covers
  more than one coset; index >= 4, quotient of exponent 2).
**Second curve, (3,4)+(27,28) at point 1** (4 bowtie and 4 other small points): 2N a bowtie 4 / 4, but bowtie +
bowtie a bowtie only 3 / 6 and bad + bowtie keeps its class 8 / 12. Reason: being a bowtie depends only on x (the slope
r/s), and (x, w), (x, -w) are not group negatives but related by the involution P -> kappa - P. So **the bowtie points
are H together with kappa - H for a finite-index subgroup H** (a congruence condition on the points), not a subgroup
on their own; the first curve's tests happened to stay in H. This explains F53: a seed lies in H, so all combinations of seeds are bowties;
on unseeded curves the condition is a coset missing their small points (possibly empty; no multiple up to 12P lands in
it). Consequence claimed from 12 / 12 on two curves: 2N always a bowtie.

**RETRACTED at scale (same day, `bowtie_components.py`, all 138 seeded curves, Mordell-Weil combinations |c| <= 2):**
- **2N is not always a bowtie:** points with all coefficients even are bowties in 2,168 of 4,152 (52%), points with an
  odd coefficient in 3,562 of 23,922 (15%); only 25 of 138 curves have every even point a bowtie. Doubling enriches
  (3.5x) but is no rule. Even non-bowties: base triple not coprime 1,526, second line not integral 330, second line not
  coprime 128.
- **The class is not a function of the point's image in E(Q)/2E(Q)** (coefficients mod 2): only on 22 of 138 curves.
- **Nor of the bad-prime pattern** (the set of primes of bad reduction where the point is singular mod p on the minimal
  model): only on 3 of 13 curves tested. Component groups of order 4 are common (Tamagawa numbers 4), so a finer local
  invariant (the component itself, or conditions at primes of good reduction from the coprimality of the base triple)
  may be needed.
- So the integrality on seeded curves is a strong bias (most generated points are bowties; doubling helps), not yet a
  clean coset law; the "which direction pairs carry bowties" prediction is not available. Open.
- **Where the failures come from (`bowtie_gcdscan.py`, 60 curves, 6,204 points):** 3,845 fail because the base triple
  is not coprime, 630 because the second line is not integral. The common factor of the base triple is a small
  recurring set of primes: **37 (= E of the (3,4) base line) in 1,491**, then 3, 5, 7, and some larger primes.
  **Working hypothesis:** integrality and coprimality are local conditions on the slope (s : r) modulo a few prime
  powers (primes dividing E, E2, b - a, small primes). The slope is not a group homomorphism of the curve, so such a
  condition need not be a coset of a subgroup: this explains the failed coset tests and the partial effect of
  doubling. Next test: per prime p, is "p divides the base triple's gcd" a function of (s : r) mod p (or p^2)?

## F57 (7 November 2026): the bowtie condition is a list of congruences on the slope, at the primes of E1, E2, b2 - a2

**Base triple coprime** (depends only on the base direction and the slope (s : r); all coprime slopes with
1 <= s < 260, |r| <= 260): non-coprime exactly when a prime of E1 divides some point's gcd, and that is **decided by
(s : r) mod p** with **3 bad classes of p + 1**: (3,4), E = 37: 3 of 38 (7.9% of slopes); (12,13), E = 7 * 67: 3 of 8
mod 7 and 3 of 68 mod 67 (41%); (27,28), E = 2269: 3 of 2,270. No other prime ever divides the gcd.

**Second line integral** (points of two seeded curves, Mordell-Weil combinations |c| <= 3, `bowtie_secline.py`): the
denominators involve only **E2 and b2 - a2**: (3,4)+(9,52): primes 43 = b2 - a2 and 3253 = E2; (3,4)+(27,28): 2269 = E2.
Each is **decided by (s : r) mod p**, integral in exactly **2 classes** mod p (42 of 44 classes bad mod 43, 1,060 of
1,062 seen mod 3253, 113 of 115 seen mod 2269).

**Conjecture (to prove):** a rational point of a bowtie curve gives an integral coprime bowtie iff its slope (s : r)
avoids 3 classes mod each prime of E1 and lies in 2 classes mod each prime of E2 (and of b2 - a2 when it has split
primes). The 2 classes should be Theorem 3 (E2 | t at every point of line 2, so the shared point reduces mod p to a root
of x^2 - x y + y^2), the 3 classes the points of the base triple vanishing mod p; the data say these necessary
conditions are also sufficient. Under reduction mod p the group law is a homomorphism to the curve over F_p, and
"reduces to one of 2 points" is not a subgroup condition: hence the bias but no coset law (F56), and unseeded curves
whose reductions never reach the 2 points give no bowties. Gives a prediction: a direction pair can carry bowties only
if the curve has rational points reducing to those classes at every relevant prime.

## F58 (7 November 2026): F57 at scale; an exact integrality criterion; b - a divides n; a direction-pair filter; a 2-descent obstruction

`bowtie_congruence.py` (all 138 catalogue curves, 8,158 points), `bowtie_localfilter.py`, `bowtie_unseeded.py`, `bowtie_parity.py`.

1. **Which primes spoil a bowtie.** Base triple not coprime: only primes of E1 and of **b - a** (the 13 'other' primes
   of the first pass all divide b - a). Second line not integral: only primes of E2 and b2 - a2. Second line not
   coprime: primes of E1, b - a, E2, b2 - a2. Each is decided by (s : r) mod p, or mod p^2 (mostly coprimality at E2
   and b2 - a2 primes; 10 cases are not decided even mod p^2). Bad classes seen at base primes: at most 3.
2. **Exact criterion (proved, holds at all 8,158 points).** Along line 2 through the shared point (x, y),
   (x + t b2)^3 + (y - t a2)^3 = n gives A t^2 + 3(x b2^2 + y a2^2) t + 3(x^2 b2 - y^2 a2) = 0 with
   A = b2^3 - a2^3 = (b2 - a2) E2. Its roots are rational, so they are integers iff the monic quadratic has integer
   coefficients: **line 2 is integral iff A | 3(x b2^2 + y a2^2) and A | 3(x^2 b2 - y^2 a2).** This is why only primes of
   E2 and b2 - a2 appear. At p || E2 (p != 3) it is p | x b2^2 + y a2^2, i.e. the shared point reduces to one root of
   x^2 - x y + y^2 (holds at all 120 E2 primes tested; the weaker 'p | t' fails at 30). At p | b2 - a2 it is p | x + y.
3. **Local test: no obstruction.** A p-adic point in the good classes at every p || E2 exists on all 138 seeded and all
   2,394 unseeded (3,4)-based curves tested (q = 0 mod p there automatically, since A and the linear coefficient vanish).
4. **b - a divides n on every line** (18,671 distinct lines in the catalogue, no exception; (b - a)^2 | n in 4,438).
   With 2: a prime p = 2, 3 or = 2 mod 3 dividing b2 - a2 needs p | x + y = s, so p | n, so p | b - a (Theorem 14).
   **Filter: every non-split prime of b2 - a2 divides b - a, and vice versa.** True on all 138 seeded curves; removes
   201 of the 400 cheapest second directions for base (3,4) (b - a = 1); explains all 18 unseeded curves of the first scan
   (in each, a prime of b2 - a2 from {2, 3, 5} passes on 0 points).
5. **A global obstruction remains.** Base (3,4), second directions with a2, b2 < 60 passing the filter and having a point
   of height <= 60: (9,52), (27,28) (seeded, bowties) and **(3,16)**: rank 4, 2,400 points, each of 13, 37, 313 = E2
   passes on about half, **jointly on none**, and joint failure is a function of the coefficients mod 2 (0 of 16 classes),
   while each prime alone is not. So the obstruction lives in E(Q)/2E(Q): plausibly the E2 condition (shared point at a
   root, w = 0 mod p, i.e. 2P = kappa mod p) and the E1 condition pick incompatible classes mod 2E. Seeded curves have
   passing classes mod 2 (4 of 8, 4 of 16).
6. **Structure.** Since every condition depends only on the reduction of the point mod p^k, and reduction is a group
   homomorphism, the bowtie points of E(Q) are a union of cosets of the finite-index subgroup
   K = ker(E(Q) -> prod E(Z/p^k)) (F56's 'no single coset' is consistent with this). A curve has bowties iff the image of
   E(Q) in that finite group meets the good set: decidable from the generators, and the smallest bowtie is a closest-vector
   problem in the height lattice. Not yet implemented.

## F59 (7 November 2026): the bowtie conditions are component conditions; a decider for direction pairs

`bowtie_components2.py` (all 138 catalogue curves, points c in [-3, 3]^r), `bowtie_decide.py`,
results in `results_bowtie_curves/decide/`.

1. **Reduction type.** At every relevant prime (E1, b - a, E2, b2 - a2) the curve has multiplicative reduction I_n,
   mostly I4 (373 of 599), then I2, I6, I8, I10, I12, I14, I3.
2. **Integrality is a component condition.** With the origin at a known bowtie, the second line is integral at p
   (p | E2 or b2 - a2) **iff 2P is in E_0(Q_p)**, i.e. the component of P is 0 or n/2: 128 of 128 primes, no exception.
   Second-line coprimality at E1 primes follows the same rule in 80 clean cases. The base-coprimality conditions
   (the '3 bad classes' of F57) are **not** component conditions: they are a finer condition mod p inside components.
   So the integrality part has period n/2 in the Mordell-Weil coefficients (2 for I4), which is F58's mod-2 behaviour.
3. **(3,4)+(3,16) explained.** Second line coprime at 37 needs one parity, integral at 313 = E2 the other; on E(Q) the
   two parities agree, so the pair carries no bowtie (decider: OBSTRUCTED by (37, sec), (313, den)).
4. **Decider.** Find the classes of c mod M = lcm(n_p / 2) passing every periodic condition (empty: obstructed), then
   test points of those classes in order of canonical height (a closest-vector search). On (3,4)+(9,52) the smallest
   bowtie found is Bernstein's 506433677359393; on (3,4)+(27,28), 1.06e26.
5. **Catalogue run** (3,000 lowest-height points per curve): no seeded curve is obstructed (consistency); for every curve
   the smallest bowtie found is already in the catalogue; **1,095 bowtie numbers < 1e300, 917 not in the catalogue**
   (each at least a five-way; exact k not yet computed: factoring s-values of up to ~100 digits is too slow on the Mac,
   to run on 7of9). 7 curves failed (Python digit limit, now fixed), 6 have no generators from ellrank.
   `catalogue.txt.gz` lines: (a, b, i, a2, b2);n;known|new.

## F60 (7 November 2026): Mordell-Weil ranks of the five-way curves against four-way controls (ranks5 run, 7of9)

`night_7of9/ranks5/`: PARI ellrank on x^3 + y^3 = n with the representations as hints, 142 five-ways (F) and 284
size-matched line + free four-ways (C); `span_rank.txt` / `span.gp`: rank of the subgroup the representations span.

1. **Run mostly failed:** exact rank for 16 F and 33 C only, all with n <= 28 digits; the 366 failures stopped after
   23-40 min, far below the 6 h alarm, so they are errors (most likely memory: 30 jobs x 8 GB stack), not time-outs.
2. **Span of the representations = number of points - number of lines** (a line is a relation P + Q + R = 0, the
   point at infinity being a flex): 139 of 142 five-ways span rank 3 (bowties: 5 points, 2 lines), 3 span rank 4
   (one line: 137904678696613339, 236191447138323830299237, 153461072317103291251148239); all 284 controls span 3.
3. **Full rank is usually span + 1.** F (span 3): rank 3 once, 4 in 12, 6 once; F (span 4): ranks 4 and 6.
   C: rank 3 in 8, 4 in 23, 5 once, 6 once. Mean rank F 4.19, C 3.85 on these small samples (size-limited to <= 28
   digits): **no evidence that rank separates five-ways from four-ways**; the representations, not extra rank, carry
   the structure. A six-way would need span >= 3 (e.g. three lines on six points) -- rank is not the bottleneck.

## F61 (7 November 2026): decider on unseeded pairs -- two new bowtie direction pairs; a prediction for lf36

`bowtie_decide.py --base 3,4 --amax 100 --seedh 300 --npts 2000` (`results_bowtie_curves/decide/base34.*`): every second
direction (a2, b2 < 100) passing the non-split filter (F58.4): 1,364 pairs x 3 shared points = 4,092 curves.
(The three choices of shared point give the same bowties: the run is 3x redundant.)

- **4,071 curves have no rational point of height <= 300** (most quartics here are probably not even locally soluble).
- 7 pairs have points: **3 obstructed** ((3,16); (9,76) by 31, 37, 67, 211; (39,76) by 31, 37, 331 with M = 4),
  **4 carry bowties**: (9,52) and (27,28) (in the catalogue) and **two new pairs**:
  - **(3,4)+(75,76)**: rank 3, M = 4, 25 bowties < 1e300; smallest **2482960469777526557699371824606091** (34 digits),
    then 4.06e34, 8.53e34 -- exact k = 5 for all three (factored), representations verified directly;
  - **(3,4)+(27,76)**: rank 5, 80 bowties < 1e300; smallest 1.465e47, then 6.28e47, 7.67e50 (k = 5 each).
- 422 distinct bowtie numbers < 1e300 not in the catalogue from this run.
- **Prediction:** (3,4) is one of lf36's 23 directions, so the complete line search to 1e36 must contain the three
  (75,76) five-ways above (2.48e33 is above lf33's bound int(1e33), consistent with lf33 missing it).

## F62 (7 November 2026): decider on the other 22 lf36 base directions -- base (3,4) was the exception

`results_bowtie_curves/decide/run_bases.sh`: `bowtie_decide.py --base a,b --amax 100 --seedh 300 --npts 2000`, shared
point 0 only (F61), for the 22 lf36 directions other than (3,4). 28,283 curves.

- **28,120 have no rational point of height <= 300; 158 are obstructed; 5 are feasible.**
- The 5 feasible curves:

  | curve | rank | bowties < 1e300 | smallest |
  | --- | --- | --- | --- |
  | (27,28)+(3,4) | 3 | 42 | 1.058e26, known: the catalogue pair (3,4)+(27,28) seen from its other line |
  | (9,16)+(21,52) | 6 | 13 (+896 larger) | **7.18e161, new pair** |
  | (28,31)+(52,73) | 4 | 1 (+232 larger; only 240 points tested) | **2.21e242, new pair** |
  | (1,4)+(13,4) | 3 | 0 in 2,000 points | -- (feasible mod 2, no bowtie found) |
  | (28,31)+(52,43) | 4 | 0 in 1,352 points | -- (rerun after a parse error) |

- So outside (3,4) the only bowtie curves with numbers small enough to count are already in the catalogue. The two
  new pairs start at 162 and 243 digits: their s-values are far beyond factoring, so they add no six-way tests.
- No exact counts in this run (k pending for all bowtie numbers, F61 and the catalogue run included).
- Run notes: one curve of (25,28) hung PARI for over an hour and was killed (1,993 of 1,994 curves logged); every PARI
  call in the decider now has a 900 s timeout. PARI's `-8.97 E-5` (space before the exponent) broke the height-matrix
  parse on one curve; fixed.

## F63 (7-8 November 2026): exact counts of the 990 new bowtie numbers <= 300 digits -- 984 have k = 5, 6 unknown

`count_bowties.py` (new): factors n from the s-values of its five representations and the E's of its two lines
(Theorem 13), then counts every coprime representation exactly (`bowtie_hunt.count_reps`, Theorem 5). Check: on 28
catalogue bowties it reproduces every catalogue count (0 mismatches).

- Inputs: new (not in the catalogue) bowtie numbers <= 300 digits from the base runs (F61, F62; 436 numbers) and from
  the catalogue rerun `catalogue2.txt` (decider rerun recording representations, 0 errors; 554 numbers not in the
  base runs).
- **574 counted (287 + 287, 34 to 252 digits): every one has exactly k = 5.** No six-way. No factoring timeout (600 s)
  so far: the s-values factor easily.
- **Run killed by memory exhaustion** (the laptop, 24 GB, ran out of memory and the watchdog restarted it at 21:06):
  `count_reps` held every product of split prime blocks below (4n)^(1/3) in one list. At 252 digits n has 15-28 split
  primes (2^28 subsets); one worker reached 40 GB. 416 numbers (149 base + 267 catalogue, the largest) remain.
- Files: `results_bowtie_curves/decide/counted_{base34,bases,catalogue}.{txt,log}`, `catalogue2*`.
- **Completed 8 Nov** (`night_7of9/count_rest/`, fixed counter, 7of9 48 processes ~75 min + the last 6 on the laptop
  ~2 h): of the 416 remaining (177-300 digits), 410 k = 5, 6 unknown. **Total: 984 of 990 have exactly k = 5; no
  six-way.** Unknown (`count_rest/results/unfactored.txt`): one 271-digit number with 34 split primes (subset search
  over 1 h), and five numbers of 284-299 digits each with one s-value or E piece of 97-100 digits that PARI did not
  factor in 30 min (for ECM with large bounds or CADO-NFS).
- The 7of9 run stopped at 410/416 on an assertion: PARI's `alarm()` *returns* an error object on timeout (it does
  not raise), so `factor_many` read a timed-out piece as "no factors"; the product check caught it. Fixed (27169a0):
  type check, output-line check, and inconsistencies go to `.unk` instead of stopping the run. No wrong count was
  possible (a timed-out piece can only lose primes).
- Known coprime five-ways now: 199 in the catalogue + 981 counted bowtie numbers outside it = **1,180 distinct**
  (merge into the catalogue pending an independent `repsf` recount).

## F64 (8 November 2026): the line search to 1e36 in the 23 cheapest directions -- no six-way; 31 new five-ways

**Run** (7of9, `lf36_v4`: line_fast.py + lc_fast.cpp, the 23 directions of cost <= 1e4, n <= 10^36 exactly; output
7 Nov 09:41 - 8 Nov 05:48, 72,437 s on 60 processes; selfcheck and C++/Python validation passed). Files:
`night_7of9/results_lf_1e36/` (from `lf_all.tar.gz`).

**Certificate:** 94,458 jobs logged, each once, equal to the planned job list rebuilt with the run's own code
(`check_jobs.py`; chunks of all 23 directions tile); 1.891e12 slopes, 5.179e10 triples (log total = lf.log total); no
Python fallback; `certify_M.py --cmax 1e4 --B 10^36`: 23 directions, 0 failures. With Lemma 15 this is a proof:
**no n <= 10^36 with a line in one of the 23 directions of cost <= 1e4 has six coprime representations.**

**Results:** 8,407 numbers with k >= 4 (8,326 four-ways, **81 five-ways, largest k = 5**; 3 five-ways are written twice,
identical rows). Largest n 9.987e35.
- Consistency: all 4,733 rows below lf33's bound are in lf33 with the same k (lf36's directions are a subset of
  lf33's); no k disagrees with the catalogue on the overlap.
- **New to the catalogue: 31 five-ways and 3,609 four-ways, all above 1e33.** Five-ways per decade in the class:
  1e33: 7, 1e34: 16, 1e35: 10.
- **F61's prediction holds:** 2482960469777526557699371824606091 (the smallest (3,4)+(75,76) bowtie) is in lf36 with
  k = 5, and so are the other two (75,76) five-ways.
- **Decider cross-check:** all 49 decider bowties <= 1e36 with a line in one of the 23 directions are in lf36 (k = 5
  each). The other 87 decider bowties <= 1e36 have no such line and are all in the catalogue.
- **Shapes:** 79 of the 81 five-ways are bowties (two lines), 2 have one line. All 31 new ones are bowties: 3 on pairs
  the decider examined ((3,4)+(75,76)), **28 with a second direction outside the decider's range** (coefficients >= 100,
  up to (1828084, 1801353)). Base directions of the 31: (3,4) 12, (12,13) 4, (1,4) 3, (27,28) 3, (4,7) 2, (13,16) 2,
  (4,9), (16,19), (9,16), (12,19), (16,21) one each.
- So bowties with an expensive second line are common, and they are reachable only through the cheap line plus an exact
  count (or a decider run with a much larger amax).
- **Merged (8 Nov):** the 3,640 new rows, each recounted independently by `verify_gp/reps.gp` (PARI only): 0 mismatches
  in count or representations. Catalogue now 22,482 four-ways, 199 five-ways (22,681 rows).

## F65 (8 November 2026): decider stage 1 (second direction < 300) -- 5 new bowtie pairs; the seed limit was too low

`night_7of9/decide1000/` v1 stage 1 (7of9, 60 processes, 28 min): the 23 lf36 base directions, pairs with
100 <= max(a2, b2) < 300, shared point 0, seed height 300. 206,098 of 206,100 curves logged (results/stage1.*).

- 205,863 no point of height <= 300; 206 obstructed; 7 feasible; 21 gp 900 s timeouts; 1 parse error.
- **6 curves with bowties, 5 of them new pairs:** (3,4)+(75,124) 110 bowties < 1e300 (smallest 1.00e63);
  (3,4)+(117,244) 80 (4.35e73); (3,4)+(39,148) 70 (3.37e42); (4,7)+(112,223) 13 (6.26e80); (4,7)+(64,247) 3
  (1.75e157); plus (13,16)+(121,124) 112 (smallest 6.515e29, the lf36 bowtie). **387 new bowtie numbers < 1e300**
  (k >= 5 by construction; exact counts pending).
- **Rediscovery check failed for (1,12)+(49,192)** (lf36 bowtie 4.98e29): its only known point has height 7,349 > 300,
  and ellrank at default effort found no generators (rank 4; effort 3 finds 3 generators at once). With no
  generators, `vecextract(R[4], "1..0")` raised a PARI error and the curve was reported as a parse error (the stage 1
  parse error, (12,19)+(36,139), was this; with the fix it is obstructed).
- So "no point found" in F61, F62 and here only meant "no point of height <= 300". Seed search on point-free quartics
  is cheap (ratpoints sieve): 0.25 ms per curve at 300, 4 ms at 3e4, 33 ms at 1e5 (200 sample curves, max 242 ms).
- Fixes (bowtie_decide.py): ellrank effort-3 fallback when generators are missing; empty generator list handled;
  seed height 1e5. Test: with seed height 1e5 and no hint, (1,12,i,49,192) for i = 0, 1, 2 each give 12 bowties
  < 1e300 including 4.98e29. Bundle `decide1000_v2.tar.gz` redoes everything below 300 (235,748 curves).

## F66 (8 November 2026): decider v2 stage 1 (every pair with max(a2, b2) < 300, seed height 1e5) -- 23 bowtie pairs

`night_7of9/decide1000/` v2 (7of9, 60 processes, ~1 h): 23 lf36 base directions, 235,748 curves, 235,745 logged
(results_v2/). **All 10 rediscovery checks pass** (every lf36 bowtie with second direction < 300, (1,12)+(49,192)
included).

- 234,922 no point of height <= 1e5; 715 obstructed (v1: 206 for the 100-300 range); 27 feasible and searched;
  **81 undecided on gp's 900 s limit** (+3 unlogged).
- **23 curves with bowties < 1e300** (one more, (12,13)+(36,259), has only larger ones). New since F62 and F65 v1:
  (27,28)+(21,52) 89 bowties from 1.49e46 -- **a pair below 100 that F62 missed at seed height 300**; (3,4)+(225,268)
  55 (7.13e76); (27,28)+(81,112) 44; (27,28)+(81,100) 14 (6.75e66); (16,19)+(268,271) 14; (12,13)+(252,289) 12
  (6.02e67); (16,19)+(16,127) 7; (1,4)+(229,268) 6; (7,12)+(151,156) 2; (4,7)+(4,277) 1.
- 1,041 bowtie numbers < 1e300; **255 not in results/five_ways_all.txt** (k >= 5, exact counts pending).
- The 70 v1 bowties missing from v2 are all from (3,4)+(39,148), undecided in v2: its periodicity box (2M+1)^r =
  13^5 = 371,293 points (M 6, rank 5) gave 567 MB of gp output (146 s on the laptop; over 900 s under load). Of the
  81: 33 had no point at 300 in v1, 17 are pairs < 100, 21 timed out in v1 too, 10 were decided in v1 (probably now
  with more generators from the ellrank effort-3 fallback, so a larger box). v3 bundle: `--gptime 3600`; a resume
  reruns only the unfinished curves.
- **v3 retry** (7of9, 20 processes, gp limit 1 h, 17:14 - 20:11; `results_v3/`): 81 of the 84 unfinished curves done
  (3 still running when collected): 62 obstructed, 4 with bowties, 15 undecided again. Bowtie curves recovered:
  (3,4)+(39,148) 70 (v1's), and **new pairs (12,13)+(84,127) 18 (smallest 8.34e71), (12,13)+(84,121) 13 (9.91e110),
  (13,16)+(43,244) 7 (3.91e97)**.
- **Stage 1 total (max(a2, b2) < 300): 28 bowtie curves; 777 obstructed; 15 + 3 undecided** (gp over 1 h: periodicity
  box, mostly bases (28,31), (4,7), (25,28)). 1,149 bowtie numbers < 1e300; 293 not in five_ways_all.txt, now added
  there as k >= 5 (list: 1,755 = 1,180 exact k = 5 + 575 k >= 5).

## F67 (8 November 2026): triangles = six-ways; chord near-misses; a polynomial triangle decider

> **Correction (8 Nov):** the bowtie chord floor (6 | d) is THEOREMS.md Theorem 8 / Lemma 8a (F35, proved in October):
> chords between points of opposite 2- or 3-type have non-p-integral third points; F35 also noted that a six-way spanning
> rank 3 (a triangle does) is disfavoured. New here: the statistics on 1,717 five-ways and the fixed-direction quartic.

**Set-up.** Representations are points of x^3 + y^3 = n (both (x, y) and (y, x)); with the flex at infinity as origin,
A, B, C are collinear iff A + B + C = 0. A **triangle** -- three lines of three, pairwise sharing a point -- has
6 points (3 corners, 3 third points), so it is a six-way. A bowtie is a triangle missing one side; the side through
P (line 1) and Q (line 2) meets the cubic again in R = -(P + Q), always rational.

**Step 1: chord near-misses** (`triangles/near_miss.py`, all 1,717 five-ways incl. v2 stage 1, all 22,681 catalogue
four-ways; every chord between two known points not on a known line, R's denominator d):
- d = 1 cannot occur in exactly counted numbers (an integral R would be a known point on a known line), so this
  measures closeness only. Best chord per number: median d ~ n^(1/8) (huge cancellation: all s-values divide n).
- Four-ways: smooth tail down to d = 2 (720 chords with d <= 2; count(d <= D) ~ 1000 D^0.5).
- **Five-ways (bowties): nothing below d = 6.** 1,316 of the 1,330 chords with d <= 1e6 have 6 | d (smallest exactly
  6 = 2 x 3, 88 times); gcd(d, 6) is 1 or 6, almost never 2 or 3 (four-ways: all four). Smallest d prime to 6: 19.
  So bowtie chords carry a forced factor 6 (likely 2-adic from n odd -- every s odd -- and 3-adic mod 9; to prove).

**Step 2: triangles with fixed directions are finite and decidable by a quartic** (`triangles/tri_decide.gp`).
Lines a_i x + b_i y = c_i; corners on one cubic <=> f(V12) = f(V13) = f(V23), two cubic forms in (c1 : c2 : c3). Both
contain the concurrency line (checked: it is exactly their gcd); the residual conics meet in <= 4 points. So per
direction triple there are at most 4 triangles up to scaling, found as rational roots of a quartic resultant; then
one checks distinctness and that a single scaling makes all six points coprime integers.
- Examples (3,4),(27,28),(9,52) / (3,4),(27,28),(75,76) / (1,12),(49,192),(13,16): quartic irreducible, **no rational
  triangle at all**.
- **All 15,180 triples of the 23 lf36 base directions and their swaps (1.6 s): 18 rational triangles, none a coprime
  six-way** (3-6 distinct denominators among the six points; 6 of them also repeat a representation).
- No elliptic curves needed: a direction-triple scan costs ~0.1 ms per triple, so ~1e8 triples (about 460 directions)
  is a few hours on 7of9. Complete for triangle six-ways whose three directions are all in the scanned set.
- Inside a bowtie family (fixed pair, genus-1 curve) the third side is determined by the bowtie, so triangle
  completions are the step-1 chords; heuristically (Siegel on the genus-1 curve) only finitely many per family.

## F68 (8 November 2026): chord denominators obey the 2-adic half of F10; triangle scans to 150 directions

> **Correction (8 Nov):** "2 | d exactly when 4 does not divide ab" is Theorem 8's type rule at p = 2 restated (same
> 2-type <=> 4 | ab; the conceptual proof via reduction onto E(F_2) = Z/3 gives both directions). Not new. New here: the
> triangle scans only.

**Chords** (`triangles/chord_f10.py`, `chord_f10b.py`; every chord between two known points not on a known line:
71,278 from the five-ways, 413,476 from the four-ways). Direction (a, b) of the chord, denominator d of its third point:
- **2 | d exactly when 4 does not divide ab** -- no exception in either set. (F10: a line of three coprime integral
  points has 4 | ab; this is the converse for 2-integrality of the third point. Candidate theorem.)
- In five-ways 3 | d for exactly the same chords (8 + 8 exceptions): the d = 6 floor of F67 is F10's 2-adic rule.
- **No prime = 2 (mod 3) ever divides ab of a chord to an odd power** (all primes < 2000 checked): F10's other half
  holds automatically for chords; no small prime of ab divides d.
- Near-miss chords (d <= 1000) have direction costs |b^3 - a^3| from 1e2 to 1e47 (median ~1e13); **none is an allowed
  direction**. A bowtie's third side must have 4 | ab: 29% of bowtie chords do, with d >= 19 (mostly primes = 1 mod 3).

**Triangle scans** (`triangles/runN.gp`, every triple of the N cheapest allowed directions and their swaps):

| directions | triples | rational triangles | coprime six-ways | time |
| --- | --- | --- | --- | --- |
| 23 (lf36 bases) | 15,180 | 18 (1 in 840) | 0 | 1.6 s |
| 60 (cost <= 55,223) | 280,840 | 34 (1 in 8,300) | 0 | 39 s |
| 150 (cost <= 270,927) | 4,455,100 | 88 (1 in 50,600) | 0 | 717 s |

- The rate falls steeply with direction cost; ~0.16 ms per triple, so 1,000 directions (1.3e9 triples with swaps)
  would be ~60 core-hours.
- The 88 lie on 26 curves x^3 + y^3 = m (m cube-free), clustered on curves rich in small points: m = 19 (6), 91 (6),
  27937 (10), 152551 (8), **16776487 (4, the smallest coprime four-way)**. Every one fails coprimality: its six points
  have 3-6 different denominators (lcm up to 3.3e11).
- Reading: rational triangles with cheap directions come from small-height points on point-rich curves, where the
  denominators never agree. Coprime triangle six-ways, if any, need expensive directions; an exhaustive triple scan
  cannot get far there.

## F69 (8 November 2026): an explicit finite-index subgroup of bowties -- the infinitude proof plan holds numerically

**Plan** (for "infinitely many n with >= 5 coprime representations"): on one bowtie curve E (rational bowties of a fixed
direction pair = rational points of w^2 = Delta(s, r), genus 1), take a known bowtie P0 as origin. (1) Only primes of
N = E1 (b - a) E2 (b2 - a2) can spoil a bowtie. (2) At p | N, "good at p" is a p-adically open condition containing P0.
(3) So for k large, P0 + (E(Q) n E_k(Q_p) for all p | N) =: P0 + K is all bowties; K has finite index in E(Q), rank >= 1,
so infinitely many bowties, hence infinitely many n (finite fibres). Exactly-5 is out of reach; >= 5 (and >= 4) is not.

**Test on (3,4)+(9,52), point 0, P0 = Bernstein's 506433677359393** (`infinite_family/coset_test.py`, `spoilers.py`,
`kernel_test.py`, `kernel_seq.py`). E: rank 5, torsion Z/2; N's primes 37 = E1, 43 = b2 - a2, 3253 = E2 (b - a = 1).
- **Step 1 holds:** every failure among 726 points m * sum c_k G_k (c_k in {-1,0,1}, m = 1, 2, 4) is caused by 37, 43
  or 3253 only. m = 1: 68 of 242 bowties; m = 2: 236 (integrality at 43 and 3253 never fails in 2E(Q) -- the F59
  component conditions); the rest are coprimality: base triple at 37, second line at 43 (finer than components).
- **Explicit subgroup K = {P in 2E(Q) : P reduces to O mod 37 and mod 43 on the minimal model}:**
  - |c_k| <= 2 (3,124 points): K contains +-(0, 1, 1, -2, -2) only; both bowties.
  - **|c_k| <= 4 (59,048 points): 38 points in K, all 38 bowties**; outside K 3,034 of 59,010 fail.
  - **j * 2(G2 + G3 - 2 G4 - 2 G5), j = 1..10: all bowties**, n of 1,260 to 129,340 digits.
- So K = 2E(Q) n E_1(Q_37) n E_1(Q_43) (index about 32 x 1,600) appears to work with k = 1. For the proof:
  (a) the step-1 lemma in full (line-2 coprimality away from N: a one-point variant of Theorem 10);
  (b) points of K are coprime at 37 and 43 and integral at 43, 3253 (local, checkable mod 37^2, 43^2, 3253);
  (c) the finite-index / non-degeneracy argument (standard). Literature: no prior infinitude result for coprime
  >= 4- or >= 5-ways found (UlasPaperPlan A0d).

## F70 (8 November 2026): how much the triangle constraints cut (Theorem 1, Theorem 8, Lemmas 17-18)

`triangles/filter_measure.py`.
- **(A) Direction triples (Lemma 18):** the 300 directions of the F68 scan (150 cheapest allowed and swaps) fall into
  19 groups by nonsplit(b - a) (largest: 1 -> 80, 3 -> 56, 5 -> 28). Triples within a group: 116,956 of 4,455,100
  (**2.6%**). Of the scan's 88 rational triangles, **2** have all three sides in one group.
- **(B) Third sides of the 1,752 bowties** (two points off the shared one, one on each line; both chords between the two
  representations): 14,016 candidates -> 7,828 after the orientation rule (one 2-type and 3-type per line, Theorem 8;
  n odd and = +-1 mod 9) -> 7,008 after ab > 0 and 4 | ab (Theorem 1) -> **0 after E_3 | n** (Theorem 2 / Lemma 18).
  All 7,008 have E_3 <= n, so this is not a size effect: the part of log E_3 not shared with n is 0.15 at least and
  0.52 typically. (The norm condition and equal non-split parts were never reached.)
- **(C) Classes (Lemma 17):** four-ways made of one line plus one free representation (n odd, n = +-1 mod 9): the free
  representation is in the other class in **7,560 of 16,510** (46%), so it can never join that line in a triangle.
- Reading: among necessary conditions for closing a bowtie into a triangle, **E_3 | n is the decisive cheap test**:
  the chord direction's norm a^2 + ab + b^2 must divide n. It needs only the directions of the chords, not their third
  points, and suggests a search shape: a third side is a direction whose norm divides n -- i.e. built from n's split
  primes (and 3).

## F71 (9 November 2026): decider stage 2 (300 <= max(a2, b2) < 1000) -- 58 bowtie curves; the seed limit again

`night_7of9/decide1000/` v3 stage 2 (7of9, 44 processes, 8 Nov 18:59 - 9 Nov 02:12, ~7 h of the 14.5 h slot;
`results_stage2a/`): 2,093,527 of 2,093,530 curves logged (3 still running when collected).
- 2,091,788 no point of height <= 1e5; 1,618 obstructed; 79 feasible and searched; 41 undecided (gp over 1 h);
  1 no generators.
- **58 curves with bowties** (54 with bowties < 1e300; 4 only larger). Largest families: (3,4)+(363,364) 147 bowties
  < 1e300 from 4.51e37; (3,4)+(387,388) 124 from 2.40e47; (3,4)+(129,412) 62 from 4.82e37; (4,21)+(28,351) 51;
  (3,4)+(309,316) 41; (36,37)+(876,877) 39. Base (3,4) dominates again (17 of 58).
- 966 bowtie numbers < 1e300; **890 not in results/five_ways_all.txt**, added as k >= 5 (list: 2645 = 1180 exact
  k = 5 + 1465 k >= 5).
- **Rediscovery: 7 of 8** lf36 bowties with second direction in [300, 1000) found. **Missed: (3,4)+(453,964), 7.37e35**:
  its known point has height 224,967 > 1e5, so the curve was "no point found". Seeded with that point, the decider
  gives rank 3 and 13 bowties < 1e300 including 7.37e35. On the reduced quartic the first point appears between
  heights 2e5 and 3e5; a point-free search costs 0.28 s at 2e5 (vs 33 ms at 1e5), growing about as height^2.
- So, as in F65 v1, **"no point found" means "no point of height <= 1e5"**. Stages 1 + 2 together: 86 bowtie curves
  with second direction < 1000. Completeness would need a better point finder for everywhere locally soluble curves
  (2-descent on the quartic, or a local-solubility prefilter before a deep search) rather than a blanket 1e6 search
  (~4,000 core-hours).

## F72 (9 November 2026): E_3 | n on chords -- not circular; bowtie cross chords never have it; E's outside primes go to D

`triangles/e3_step0.py`, `e3_rates.py`, `e3_witness.py` (plan: `triangles/E3_plan.md`, steps 0-1).
- **Step 0 (circularity): the converse of Theorem 2 is false.** All 27,629 known lines have E | n (control), and
  **10,914 of 487,554 non-line chords have E | n** with a non-integral third point (smallest denominators 2, 4, 5).
  So F70 is not a restatement of "no third line".
- **Rates after the F70 filters** (types orientation, ab > 0, 4 | ab): four-way chords, one line 4,286 / 86,322
  (5.0%); no line 244 / 3,484 (7.0%); **bowtie cross chords 0 / 21,136.** (Correction, F73: the rate depends
  strongly on the size of E; size-adjusted only about 16 would be expected, not 1,000.)
- **Step 1 (witnesses):** every bowtie cross chord's E_3 has a prime outside n; the outside part always divides the
  third point's denominator D. The outside primes vary (13: 1,414; 19: 1,032; 7: 912; 31: 776; 67, 61, 79, ...; a prime
  < 2000 in only 55%): **no fixed witness prime**, so no uniform congruence obstruction of Theorem 8 type.
- **General fact (all 487,554 chords): the part of E coprime to n divides D.** Proof sketch: Theorem 13's identity holds
  for a rational third point, E s_P s_Q (X + Y) = (a - b)^2 n D; a prime p | E with p not dividing n divides neither
  s_P s_Q (they divide n) nor a - b (gcd(E, a - b) | 3), so v_p(E) <= v_p(D). Converse fails: 9,802 of the 10,914
  E | n chords still have D with primes outside 3n.
- **Open:** why does every bowtie cross chord have an E_3-prime outside n? Next: compare the split primes of E_3 with
  the s-values (Theorem 13 on lines 1 and 2), and test on bowtie curves whether the outside prime is forced by the
  pair's E_1, E_2 (family-level, plan step 2: finiteness route).

## F73 (9 November 2026): why bowtie cross chords avoid E_3 | n -- mostly size; two structural explanations fail

`triangles/eisenstein_share.py`, `e3_structure.py`, `e3_size.py`. Setting: pi_P = x + y w in Z[w], n = s_P N(pi_P),
and E_3 = N(pi_Q - pi_P) / g^2 for the chord PQ (g = integer content of pi_Q - pi_P).
- **Size explains most of F72's zero.** Among filtered four-way chords, the rate of E | n falls with
  r = log E / log n: 30-40% at r = 0.1-0.2, 8% at 0.35-0.4, 2% at 0.45-0.5, 0.4% at 0.5-0.55, <= 0.03% at r >= 0.55.
  Bowtie cross chords mostly have r = 0.6-0.7 (20,004 of 21,136), since they join points on different lines
  (E_3 about n^(2/3) / g^2 with small g). **Size-band-adjusted expectation: 16.2, observed 0** (most of the 16 from the
  ~340 cross chords with r = 0.3-0.5). The chords are not independent (about 8 per bowtie, bowties of one curve
  related), so this is a modest, not overwhelming, deficit. F72's "about 1,000 expected" was wrong.
- **Not shared Eisenstein factors:** the share log N(gcd(pi_P, pi_Q)) / log N(pi) is *higher* for bowtie cross pairs
  (median 0.48) than for four-way chords without E | n (0.34), and like those with E | n (0.45).
- **Not the s-differences:** with t1 = s_S - s_P, t2 = s_S - s_Q (pi_P - pi_S = t1 beta1 / (a - b) etc., beta = b - a w),
  E_3 g^2 = N(t2 beta2 - t1 beta1) (up to the line factors); in all 10,568 cross chords (shared-point orientation, types
  ok) E_3's outside part is coprime to t1 t2: the outside primes come from the binary quadratic form itself.
- **Not hubs:** E | n chords are mostly single (four-ways: 4,302 single, 228 hub); five-way filtered chords are never hubs.
- **Status:** "E_3 never divides n on bowtie cross chords" is mainly a size phenomenon with a small unexplained deficit.
  Not a candidate for a uniform theorem; a finiteness statement per curve (plan step 2) remains the realistic target.

## F74 (9 November 2026): what the rational triangles are -- small curves, integral anchors, a ladder to six-ways

`triangles/tri_props.gp` (`tri_props.out`): the 88 rational triangles of the F68 150-direction scan, each moved to its
cube-free curve x^3 + y^3 = m (n0 = num/den, num den^2 = m k^3, scale den/k).
- **Every one contains integral points of x^3 + y^3 = m** (coprime representations of m): 4 triangles with 4 integral
  points, 36 with 3, 38 with 2, 10 with 1, none with 0. They sit on 26 small curves (m = 19, 91, 152551, 27937, ...).
- **The four 4-point triangles are the smallest coprime four-way, m = 16776487** (= A047697(4)): its line of three
  representations plus the fourth, joined to two of them; the two missing third points have denominators 5 and 37
  (or 5 and 8917). The smallest four-way is "two points short" of a triangle six-way.
- **Any three representations of n not on one line are the corners of a rational triangle** (their three chords are the
  sides). So a triangle six-way is exactly: three representations whose three chord third points are all integral.
  The 3-point triangles here are mostly three corners (16) or two corners + one third (20), never a full integral side.
- **A ladder by the number j of integral points among the six:** j = 6 a six-way; j = 5 every bowtie (corners: the
  shared point and one point from each line; the cross chord's third is the one rational point); j = 4 a line plus a
  free point (four-ways); j <= 3 the small-curve triangles of the scan. The "distance" of a configuration from a six-way
  is measured by the denominators of its non-integral points (for bowties: F67's chord denominators, >= 6, and >= 19 once
  the orientation rule is applied).
- **Every denominator in the 88 triangles is odd** (as is m): the scan used allowed directions only (4 | ab), and by the
  2-adic rule of Theorem 8 / F68 (2 | d iff 4 does not divide ab) every third point is then 2-integral -- an independent
  confirmation. 3 is the most common denominator prime, then 7, 13, 37 (split primes and 3, as E's outside part | D).

## F75 (9 November 2026): near-miss ranking of the j = 4 triangles (four-ways = line + free point)

`triangles/j4_nearmiss.py` (`j4_nearmiss.txt`). For each of the 21,947 four-ways made of one line P1 P2 P3 and one free
representation F, the triangles with corners F, Pi, Pj (sides: the line, F-Pi, F-Pj) have 4 integral points;
distance to a six-way = d(R_i) d(R_j), the denominators of the two chord third points; best over the 3 pairs and both
orientations of F.
- **16776487 (the smallest coprime four-way) is the best near-miss of all: 185 = 5 x 37**, then 513 (1066365937),
  2936 (442245349), 4424 (1026062947).
- **Scaling law: distance ~ n^0.48** (median log distance / log n = 0.48 in every size band 10-39 digits; minimum
  0.253, for a 26-digit n). Near-misses do not get relatively closer with size; in absolute terms they recede.
- **No clustering on line directions** once size is accounted for: by absolute distance the cheap directions look
  enriched 2-6x (they dominate small n), but ranked by log distance / log n the top 2% has (3,4), (12,13), (4,1),
  (7,4) at 0.7-1.0x their overall share; only (36,37) (about 2x) and (108,127) (3 of 12) stand out, on small counts.
  Unlike bowties (which concentrate on base (3,4)), near-six-way triangles of four-ways are spread evenly.

## F76 (9 November 2026): the shapes of a six-way, and a census of the known four- and five-ways

`triangles/shape_census.py`. A line carries three representations and two lines share at most one, so six
representations carry at most four lines: complete quadrilateral (4 lines, rank 3), triangle (3, rank 3), bowtie + free
point (2, rank 4), two disjoint lines (2, rank 4), line + three free (1, rank 5), six free (0, rank 6). Paper:
Table tab:sixshapes ("Why no six-way?").
- **Census of the known coprime k-ways:** four-ways 21,947 = one line + one free point, 535 with no line; five-ways
  2,642 bowties, **3 = one line + two free points**, 0 with no line.
- **Two disjoint lines, one step away:** only those 3 five-ways (a chord F-G of the two free points would be a second,
  disjoint line). One has no admissible chord (types); best missing denominator 194,271,019 (about n^0.32, n of 27
  digits); next 1.1e15.
- Status by shape: quadrilateral impossible (Theorem 8c + Theorem 12: any n with a line is odd); triangle excluded
  heuristically (F35 gap principle; F75 near-misses recede as n^0.48); bowtie + free point the most likely; two
  disjoint lines open (not searched for); the rest need rank >= 5.

## F77 (9 November 2026): two disjoint lines -- a surface of general type; no linear families among the 23 base directions

`twolines/forms23.gp`, `twolines/equiv.gp`.
- **Set-up.** A line in direction d carries the raw triple of a slope (s, r) with n = F_d(s, r) / G^3, F_d = X^3 + Y^3
  for a raw point (X, Y) (a binary sextic, = E S1 S2 S3 / (a - b)^2, Lemma 15). Two lines of the same n in directions
  d1, d2 (disjoint or not) are rational points of the sextic surface **X: F_d1(s, r) = c F_d2(s', r') in P^3** (c from
  finitely many gcd normalisations). If F_d1, F_d2 have no repeated root, X is smooth, hence of general type
  (K = O(2)); by Bombieri-Lang its rational points lie on finitely many curves of genus <= 1 plus finitely many others.
  The **bowtie curves** (two lines sharing a point; genus 1, F53) are such curves on X. **Two disjoint lines come in
  infinite families only if X contains further curves of genus <= 1.**
- **Lines on X** = rational M in GL2 with F_d1 o M proportional to F_d2. Tested on all pairs of the 23 lf36 base
  directions (roots of the sextics, Moebius maps through three roots, rational check, exact polynomial identity):
  - every direction has **exactly 6 rational automorphisms** -- the 6 orderings of a triple (the expected trivial
    ones; validates the method). So **no parallel second line** (same direction, same n) in a linear family;
  - **no two distinct directions have equivalent sextics**: no lines on any X for these pairs;
  - no sextic has a repeated root: every X is smooth.
- So the simplest kind of infinite family of two-disjoint-line configurations does not exist among the 23 base
  directions. Conjecturally (Bombieri-Lang) their rational points are finite per pair off the bowtie curves and any other
  low-genus curves (not yet searched: conics and genus-1 curves on X).
- **Reference for the next step:** Ono and Trebat-Leder, *The 1729 K3 surface* (`refs/1510.00735v5.pdf`): two points
  on x^3 + y^3 = k(T) make the twist family an elliptic surface (K3, Picard number 18, rank 2 over Q(T)). The same
  method -- fix one line's parameter, view the other as a point on an elliptic curve over Q(T) -- is how to look for
  genus-1 curves on X beyond the bowtie curves.
- **Already covered by computation:** a six-way of shape "two disjoint lines" with a line in one of the 23 directions
  below 1e36 would have been counted by the certified lf36 search (F64), and with a line of cost <= 1.2e12 below
  int(1e33) by lf33 (F52); none exists.

## F78 (9 November 2026): ranking the five-ways as six-way candidates (bowtie + free point) -- the model collapses with size

> **Correction (F79, same day):** calibrated on 517,972 one-line numbers, this lambda model underestimates free
> representations about 350-fold (more for larger n and more split primes). Its absolute values and the 'collapse'
> are not reliable; use the empirical rates instead.

`triangles/free_point_rank.py` (`free_point_rank.txt`). For each exactly counted five-way <= 150 digits (710), the
expected number of free extra representations lambda(n) = sum over Theorem 5 candidates s (s = f x split blocks,
s <= (4n)^(1/3), not one of the five) of [m = (4n/s - s^2)/3 a positive integer] / (4 sqrt m) (density of squares
times 1/2 for parity). Factorisation redone from the s-values (all 710 in 49 s).
- **Top:** 506433677359393 (Bernstein, 15 digits) lambda 8.5e-5; 137904678696613339 (18 digits, one of the three
  "line + 2 free" five-ways) 1.7e-5; then 20-24-digit five-ways at 1e-6 - 3e-7.
- **By size (total lambda):** < 25 digits (15 numbers) 1.1e-4; 25-49 (170) 1.5e-6; 50-74 (67) 4e-14; 75-99 1e-21;
  100-124 7e-29; 125-149 8e-37. **Sum over all 710: 1.1e-4**, essentially all from the smallest five-ways, which are
  exactly counted (k = 5).
- **Calibration caveat:** far more pessimistic than the paper's empirical "one six-way per 300-1,500 five-ways" (rates
  measured below 1e30). Local densities (m a square mod small primes) can raise lambda by a modest factor, not 1e3.
  So either the model misses structure or the empirical rate does not extrapolate. Next: calibrate lambda on data --
  e.g. numbers with exactly one line (three-way lines from the A023050 / lf runs) and the observed frequency of a free
  fourth representation.
- Reading: for "bowtie + free point" the useful candidates are the smallest five-ways, all already counted; large bowtie
  numbers essentially cannot gain a free point by chance.

## F79 (9 November 2026): calibration -- "free" fourth representations are ~350x more common than random squares

`triangles/calibrate_free.py`, `free_hubs.py`. All lines n <= 1e21 in the 23 cheapest directions (line_fast
--triples: 517,976 distinct n, 3 s), each n counted exactly (collisions.all_reps).
- 517,972 numbers have exactly one line; **271 have a free representation** (one each), 4 have two lines.
- F78's lambda predicts 0.78 in total: **observed / predicted = 347**. The ratio grows with n (31 at 6-8 digits, 66,
  157, 378, 463, 539 at 21-23 digits) and with the number of split-prime blocks (71 at 5 blocks ... 1,169 at 10).
- **Empirical rate** of a free fourth representation per one-line number: 0.9% at 12-14 digits, 0.33% at 15-17,
  0.055% at 18-20, 0.020% at 21-23 (overall 5.2e-4) -- consistent with the paper's 3e-4 (F49, to 1e30).
- **Not hubs:** none of the 271 free points lies in a hub (two chords meeting at one rational point).
- **Likely cause (not tested):** the model treats m = (4n/s - s^2)/3 as a random integer; but m = d^2 is equivalent to
  t = n/s being a norm x^2 - xy + y^2 with x + y = s, and t, made of split primes, has about 2^k norm representations.
  A model counting norm representations of t is the next thing to try.
- Consequence: F78's ranking and its tiny absolute values are not reliable; the paper's empirical estimate (one six-way
  per 300-1,500 five-ways, decreasing with size) stands as the better guide.
- **Are free points constrained?** Proven for every representation (so for free points too): s = f x split blocks
  (Theorem 5), x y mod 3 common (Lemma 6), n odd so one even coordinate (Theorem 12), chord directions obey Theorem 14,
  chord thirds primitive (Theorem 10) with E's outside part in the denominator (Lemma 19), gap principle (heights,
  angles >= 60 deg). Not forced: the class (Lemma 17). Profile (`free_profile.py`, 271 free vs 813 line points of the
  same numbers): s / n^(1/3) median 0.58 vs 0.55; largest coordinate / n^(1/3) median 1.03 vs 1.04 (90%: 4.69 vs 3.48);
  both coordinates positive 32% vs 29%; share of n's split blocks in s 0.33 vs 0.29; **same class as the line 54.5%**
  (line points 100%, Lemma 17 check). So free points are typical representations of n, with a random class: the 350x
  excess is about the counting model (how often t = n/s is a norm with x + y = s), not a special kind of point.

## F80 (9 November 2026): a battery of checks on the free points -- structure, mostly explained by Theorems 3 and 5

`triangles/free_battery.py`, `free_E.py`: all 21,953 free representations of the catalogue (21,947 four-ways
"line + 1 free", the 3 five-ways "line + 2 free"); control: the 535 four-ways with no line.
- **A. Proven rules: 100%** -- non-split part of s (Theorem 5), x y mod 3 (Lemma 6), one even coordinate, Theorem 14
  on every chord F-P.
- **B. Order is not uniform:** s_F is the 2nd smallest of the four s-values in 33.7%, 3rd in only 15.6% (1st 23.2%,
  4th 27.4%; uniform would be 25% each, s.e. 0.3%); sizes mirror it. Free points tend to fall between the line's
  smallest and middle s-values. Open: may be a property of how a line's three s-values are spaced (Theorem 13's
  cubic); needs a control (e.g. a random representation of numbers with two known non-line points, or a model).
- **C. Shared factors:** median log gcd(s_F, s_P) / log n = 0.103 against 0.050 between the line's own points.
- **E. Relations:** no exact s_F s_Pi = +- s_Pj s_Pk; s_F | s_P1 s_P2 s_P3 (= (a - b)^2 n / E, Theorem 13) in 43%.
- **The line's E-primes:** in s for line points **never** (100%: Theorem 3, E | t on every point of a line); for free
  points **all-or-nothing** per prime: none 63.1%, all of n's power 36.9%, never part (Theorem 5: s takes whole
  split blocks). So free points put the line's E-blocks into s about a third of the time, which line points never do;
  this, and the near-coprimality of a line's three s-values, explains C and E2.
- **D. Nearly on a line:** best chord from F has denominator ~ n^0.14 (median; min n^0.008); the no-line control is not
  comparable (12 chords per number against 6).
- Reading: free points obey every general rule and look like typical representations; the visible structure (C, E)
  comes from the line's side (Theorem 3), and one feature (B, the order skew) is still unexplained.

## F81 (9 November 2026): free points -- the order skew is explained; cheap chords (D-lines) link all points of a multi-way

`triangles/free_controls.py` and inline checks (catalogue: 21,947 "line + free" four-ways, 535 no-line four-ways, 172
bowties <= 40 digits).
- **Order skew (F80 B) explained:** a Theorem-5 candidate s chosen with weight 1/sqrt(m) (m = (4n/s - s^2)/3) falls
  among the line's three s-values as rank 1-4 = 17.4 / 35.6 / 17.6 / 29.4% -- the free points' 23.2 / 33.7 / 15.6 /
  27.4%. A uniform candidate gives 64 / 24 / 6 / 6%. So the skew is where a valid s can lie, not a property of F.
- **Allowed chord directions: 50.00% for F (forced):** of F's two orientations exactly one has the line's 2-type, hence
  4 | ab (Theorem 8 / F68), and the norm half of Theorem 1 holds automatically for chords (F68).
- **Cheap chords.** Small directions recur among chords F -> line point -- (3,7) x40, (4,7) x35, (1,7) x32, (1,4) x29,
  (3,4) x27, (1,3) x27 -- in numbers up to 35 digits, each with the smallest possible third-point denominator
  (Theorem 7: D | (b - a) E; (1,3): 2, (1,4): 3, (4,7): 3, (3,7): 4, (3,4): 37). Share whose cheapest chord has cost
  <= 1e6 / 1e9 / 1e12: **free -> line 6.6 / 21 / 46%**; bowtie cross chords 19 / 41 / 70%; **no-line four-ways (any
  pair) 38 / 83 / 99.6%**. (A first control, line point -> swap of another line point, gave ~0% -- opposite-type chords;
  not a fair control.)
- **Reading:** points of the same n are pairwise linked by chords in cheap directions (D-lines, F30-F31) far more often
  than random pairs of integers of that size would be (that needs gcd(dx, dy) ~ n^(1/3) / |direction|). Likely cause:
  representations sharing a split prime ideal of n agree modulo it (F73: high Eisenstein gcd), so differences carry large
  common factors. Free points are typical in this respect, not special. This shared structure is very likely what the
  random-square model of F78 misses (F79's factor ~350).

## F82 (9 November 2026): pairs of representations lie on cheap chords (D-lines) -- real, and explained by Pell conics

`triangles/dline_g.py` and inline checks.
- **Real, with a fair control:** exhaustive four-ways n <= 2.5e23 (1,735; no search bias): cheapest of the 12 chords
  between representations has cost <= 1e6 / 1e9 / 1e12 in **64.6 / 91.5 / 99.9%**; control (representations of n
  against those of the next four-way, 32 pairs) 1.7 / 8.5 / 24.7%.
- **Not shared prime ideals** (my first guess): g = gcd(dx, dy) satisfies g (b - a) = +-(s_P - s_Q) (Theorem 14's
  identity), so all of g divides s_P - s_Q trivially; but g's primes are almost never primes of n (mean share of
  log g from primes of n: 0.034, no-line four-ways <= 26 digits).
- **Explanation (classical):** for Q = P + lambda (b, -a), the identity (checked in PARI)
      (x + lambda b)^3 + (y - lambda a)^3 - x^3 - y^3
        = lambda [3b x^2 - 3a y^2 + 3 lambda (b^2 x + a^2 y) + lambda^2 (b^3 - a^3)]
  shows that **P and Q represent the same n exactly when (x, y) lies on the conic
  3b x^2 - 3a y^2 + 3 lambda (b^2 x + a^2 y) + lambda^2 (b^3 - a^3) = 0** (the F58.2 quadratic read as a conic in P).
  For ab > 0 (allowed directions) the conic is indefinite: Pell-type, so one integer point gives infinitely many
  (a recurrence). Each small direction (a, b) and step lambda therefore carries an infinite family of equal sums of two
  cubes, small directions having small coefficients and hence small n. This is why pairs of representations
  concentrate on cheap chord directions -- the structured families that dominate the count of two-ways
  (Heath-Brown, Hooley; refs/aa7913.pdf, Hooleybf01111429.pdf), and the Pell route of UlasPaperPlan A0c.
- Consequences: (1) the random-square model (F78) ignores exactly this, hence F79's factor ~350; (2) a model of free
  points should count integer points on these Pell conics (by direction and lambda) instead of random squares;
  (3) coprimality and integrality of the third point are separate conditions on top (Theorems 7, 10).

## Negative results

- **N5 (7 November 2026): two picture-suggested bowtie patterns are not rules** (165 bowties; from the
  plot_bowtie.py picture of 118371660133721558473). (1) Lines staying within one cluster (all points with y > x, or
  all with x > y) against crossing: both crossing 95, one of each 64, both within 6; no link to cost (the line that
  stays within is the cheaper one 20 times, the costlier 44). (2) The cheaper line is not the grazing one: its points
  are more spread in 93 bowties, less in 72 (median spread ratio 10^0.05). The example's flat, grazing blue line was
  particular to it.

- **N5 (27 October 2026): multi-way curves do not improve Ta(k) or Ca(k) bounds.** Rank isn't what matters;
  small generator heights are.
  - The best curve found, M = 619538684309181 (rank 7, a four-way), gives Ca(12) ≤ 1.9·10⁸³, which is 10⁵⁶ times
    the published bound, and nothing at all within 10⁶⁰ of the published bounds for k ≥ 16.
  - The record curve M = 3956875867 (rank 6), run through the same pipeline (`curve_cabtaxi.py`), reproduces the
    published Ca(19) and Ca(22) exactly.
  - Points of canonical height ≤ 80: 10,191 on the record curve, 4,486 on ours.
  - Integral points have height about ⅓·log n, so curves with large n cannot compete. A better Ta(19) needs
    high-rank curves with *small* M (Elkies-style constructions), not our multi-way curves.
  - `curve_cabtaxi.py --taxicab` (positive points only, compared with the Ta bounds) was added for this.


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
- **N4 (25 October 2026): the F9 family never gains a fourth representation.** For all k = 1 … 1,000,000
  (n(k) up to about 10⁵⁰), n(k) = (9k² − 3k + 1)(9k² + 3k + 1)(27k⁴ + 9k² + 1) has exactly 3 coprime
  representations (exact divisor count, factoring the three polynomial factors separately; `family_k.py`,
  124 s).
  - **Reason (F15):** n(k) has few divisors (three mostly-prime polynomial factors), far below the hundreds
    multi-ways need.
  - **Lesson for the "polynomial family" idea:** useful families must have n factoring into many polynomial
    pieces, so that every member is automatically divisor-rich.

