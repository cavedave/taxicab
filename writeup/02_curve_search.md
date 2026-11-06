# The targeted search: lines and hubs on the curve x³ + y³ = n

*Draft, 29 October 2026, for "An attempt to find a coprime six-way sum of two cubes". Sources:
`experiments/mining/THEOREMS.md` (proofs), `experiments/mining/FINDINGS.md` (F4–F40, data), `cubefree.md` §3,
`experiments/mining/line_enum.py`, `dline_enum.py`, `count_all.py`, `line_structure.py`, `curve_relations/`.*

The exhaustive search (previous section) costs B^(2/3) and stops at 2.5·10²³. To look further we use the
structure of the curve x³ + y³ = n: most multiple representations are not independent, but are tied together by
lines. This section explains that structure, the search built on it, what it found, and where it stops.

## 1. The geometry

**The curve.** For fixed n, the coprime representations of n are integer points of the elliptic curve
C_n : x³ + y³ = n. Its point at infinity O = (1 : −1 : 0) is a flex. Taking O as the zero of the group law:
- three points of C_n are **collinear** exactly when P + Q + R = 0;
- −(x, y) = (y, x): the negative of a point is its swap.

So a representation of n gives two points, (x, y) and (y, x), and a line through three integer points is a
3-term relation among them. The third point of the chord through (x, y) and (x₁, y₁) is

  R = ((x₁²y − x²y₁)/d, (xy₁² − x₁y²)/d),  d = xy − x₁y₁,

the classical formula of Werebrusow and Desboves (Dickson, *History* II, ch. XXI); on 3367, (15, −2) and (−9, 16)
give (−33, 34). The line mechanism itself is therefore classical. What follows is, as far as we can find, new: a
census of how often it accounts for multiplicity, the rules that make it searchable, and the search.

**The shapes of multi-ways** (exact, `line_structure.py`):

| set | line + free point | hub | independent |
| --- | ---: | ---: | ---: |
| 204 four-ways ≤ 10¹⁷ (complete) | 184 (90 %) | 11 (5 %) | 9 (4 %) |
| 214 four-ways 10²³–2.5·10²³ (complete) | 188 (88 %) | 24 (11 %) | 2 (1 %) |
| 1,107 four-ways ≤ 10²² (complete) | | | 26 (2.3 %) |

- **Line + free point:** three representations on a line, a fourth unrelated.
- **Bowtie:** two lines through a shared representation, 5 points. Almost every five-way is a bowtie
  (the rest are a line + two free points).
- **Hub:** P₁ + P₂ = P₃ + P₄; the chords P₁P₂ and P₃P₄ meet the curve again at the same *non-integral* point R,
  usually of small denominator D (57 % have D ≤ 6). Multiplying by D, a hub of n is a bowtie of D³n whose outer
  points are multiples of D (F30). A line through two integer points and a point of denominator D is a **D-line**.
- **Independent:** no relation at all among the integer points.

**Only lines and hubs occur** (F33). For 1,378 coprime k ≥ 4 numbers we computed the height-pairing matrix of the
integral points, searched for integer relations by LLL (coefficients ≤ 1,000) and checked each exactly with the group
law. All 1,403 relations found have 3 or 4 terms, every coefficient ±1: lines and hubs. There are no tangents
(2P = Q + R) and no longer relations. So a search for lines and D-lines sees all the structure there is.

**Independent multi-ways come from rank.** Four independent integral points need rank ≥ 4; their curves have mean
rank 5.3 (exact ranks 4–8, unbiased sample ≤ 10²²), against 3.8 for line + free and 4.2 for hubs of the same size.
Two mechanisms make multi-ways: **structure** (relations; the points span rank 3) and **rank** (no relations, on
curves of unusually high rank). The cubefree record A080642(4) = 1801049058342701083 is a pure rank example
(rank 4).

## 2. Theorems that make lines searchable

Notation: a line a x + b y = c with gcd(a, b) = 1; **cost** D = b³ − a³; E = a² + ab + b², so D = (b − a)E.

- **Theorem 1 (direction rule).** If a line carries three distinct coprime points, then a·b > 0, a ≠ b, a·b is a
  norm from Q(√−3) (every prime ≡ 2 (mod 3) to an even power), and a·b is even, hence 4 | ab. Proof: the three
  roots of the cubic in x satisfy Vieta relations independent of n; eliminating one root gives the conic
  X² + XY + Y² = 3ab³, so 3ab³ is a positive norm; a 2-adic parity argument on e₁, e₂ excludes a, b both odd.
  Part (a) is probably implicit in Werebrusow's parametrisation; we have not found (b) stated anywhere.
  Empirically: all 11,155 lines of all coprime k ≥ 3 up to 10¹⁷ obey it, and every allowed direction up to cost 10⁵
  occurs.
- **Theorem 2.** E divides c and n. So every n carried by a line in direction (a, b) is a multiple of E.
- **Theorem 4 (complete enumeration).** For an allowed direction, the coprime collinear triples correspond to the
  rational points of the conic X² + XY + Y² = 3ab³, i.e. to the reduced slopes r/s through one fixed rational point
  P₀ (found by PARI `qfsolve`); only the primitive multiple c₀ can give coprime points. So "direction (a, b)
  searched to slope height H" is an exact statement.
- **Theorem 7 (D-lines).** The denominator D of the third point divides (b − a)E. D-line directions obey the norm
  rule, with a·b even for odd D and odd for even D.
- **Theorem 8 (types at 2 and 3).** For n odd, exactly one coordinate of each point is even; for n ≡ ±1 (mod 9),
  exactly one is divisible by 3. A chord between points of opposite type has a non-integral third point, so all
  points of a line share the same type. Consequence: **no six coprime representations form a complete
  quadrilateral** (four lines, each through three of the six) when n is odd or n ≡ ±1 (mod 9). All 82 known
  five-ways are odd.
- **Convexity.** No line meets x³ + y³ = n in three points with positive coordinates (the positive arc bounds a
  strictly convex region). So every line contains a difference, and the line method can never produce an
  all-positive (cubefree taxicab) multi-way; those need hubs or rank (`cubefree.md` §3–4).

## 3. The search

1. **Directions.** All allowed directions in increasing cost, complete (an early ordering missed near-diagonal
   directions with b ≥ 2000, from about rank 1,400; fixed 28 October 2026).
2. **Slopes.** For each direction, sweep reduced slopes r/s with max(|r|, s) ≤ H, compute the second conic point,
   turn it into the primitive collinear triple, and keep it if the three points are coprime. Integer arithmetic
   throughout; each triple is checked exactly.
3. **Filter.** Keep n with at least R split primes (p ≡ 1 mod 3) below 1,000, and two of {7, 13, 19, 37}. Three quarters of the five-ways
   have ≥ 7 such primes, against about a fifth of line candidates; the free-point rate roughly doubles per extra prime
   (F36).
4. **Exact count of every candidate.** For each kept n (factorised by PARI), all coprime representations are
   counted from the divisors: for each s | n with s ≤ (4n)^(1/3), test whether (4n/s − s²)/3 is a square
   (`count_all.py`, about 10⁴ n per second per core). No candidate is sampled; any line candidate with extra
   representations is found whatever its shape.
5. **D-lines** (`dline_enum.py`): the same enumeration, keeping triples with two coprime points and one point of
   denominator 2 ≤ D ≤ 10⁹. Two D-lines with the same n and R form a hub. This is the only source of hubs.

**Where n comes from.** For a direction of cost D and slope height h, n ≈ D²·h⁶ (fit over 60 directions × 8
heights, rms 1.2 decades). So cheap directions reach large n only at large heights, and expensive directions give
large n at small heights. With a cap n ≤ N, each direction is enumerated only to the height where n passes N
(`--auto-height`); this keeps 94 % of candidates in 36 % of the time.

**What predicts yield** (worf runs, per 1,000 directions): directions whose E has ≥ 3 split primes below 1,000
yield 6.1 five-ways, against 0.18 for E with none. E helps only by making n richer (E | n): at a fixed number of
split primes in n, E adds nothing. Individual primes carry no weight beyond the count.

## 4. Results

**Catalogue** (`results/a047697_catalogue.txt`, every entry recounted exactly): 8,571 coprime four-ways and 82
coprime five-ways, of which 12 lie below the exhaustive bound and **70 above it, all found by this search**
(largest 3.8·10³⁵). All five-ways found by lines are bowties or line + two free points.

**Recall against the exhaustive data.** Within the directions and heights searched, the line method missed no
four-way that passes its filter (10²³–2.5·10²³, F28). Overall recall of four-ways falls with n, from 50–70 % below
10¹⁶ to about 27 % at 10²¹, because the heights needed grow like n^(1/6). For five-ways recall is higher, since
either line of a bowtie suffices: the only five-way in 10²³–2.5·10²³ had already been found by lines.

**Saturation below 10³⁰** (F40). By 29 October every allowed direction with cost ≤ 1.2·10¹² had been searched, at
filter 7, to the height where n passes 10³⁰ (beyond that cost almost no slope stays below 10³⁰). In the last runs,
40 of 50 five-way finds were rediscoveries. Below 10³⁰ the line method has found most of what it can reach.

**Hubs** (29–30 October; analysis in progress): 300,000 never-searched D-line directions, filter 7, n ≤ 10³⁰,
276 million candidates counted exactly: 473 four-ways (204 hubs, 10 independent, 259 line + free) and 4 five-ways,
all bowties. Per candidate, D-lines yield about 40× fewer four-ways than ordinary lines.

## 5. Why no six-way, and how rare they should be

- **Shapes.** A six-way needs three relations among six points, or fewer relations and higher rank. The gap
  principle (Helfgott–Venkatesh 2006) puts the integral points of a multi-way on a thin height shell (median spread
  4.5 %) at mutual angles ≥ 60° (|cos| ≤ ½ in all 2,832 pairs without a common line). Six such points in rank 3 must
  form the A3 configuration, the complete quadrilateral, which Theorem 8c excludes; the triangle of three lines is
  excluded heuristically. What remains has rank ≥ 4: **bowtie + free point** (the dominant route), two disjoint
  lines, or line + hub, plus the rank route.
- **Rate.** A free point added to a line costs about 1.5·10⁻⁶ per line candidate overall, rising steeply with the
  number of split primes and falling 5–10× per four decades of n. Assuming the same rate for a bowtie, this predicts about
  **one six-way per 300–1,500 five-ways** (central 1 : 500) at our sizes.
- **Observed.** We found 82 five-ways and no six-way. With the 23 new five-ways of 27–29 October the expected number
  of six-ways was about 0.02–0.08, so not finding one says nothing against the estimate.

## 6. Limits

- **Not exhaustive.** The search cannot prove that no six-way exists below any bound; only the GPU search does that.
- **What it cannot see:** six-ways without a line (only hubs or rank), and numbers whose lines are in directions or
  heights not searched, or that fail the filter (filter 8 keeps 44 of the 72 five-ways known on 28 October, filter 7
  keeps 55).
- **Above 10³⁰** the free-point rate per candidate is lower still; a hunt there is only worthwhile with a new signal
  that raises the six-way chance per candidate by about 10×.

## 7. Attribution summary

- **Classical:** the chord construction (Werebrusow, Desboves), the norm-form parametrisation, the group law and
  the gap principle.
- **Apparently new:** the census of shapes (lines, hubs, independent; only ±1 relations); Theorem 1(b), E | n,
  the complete slope enumeration and the search built on them; D-lines and hubs as bowties on D³n; Theorem 8 and
  the exclusion of the complete quadrilateral; the convexity consequence for cubefree taxicab numbers; 70 coprime
  five-ways above 2.5·10²³ (literature still to be checked against Butler's and Boyer's lists).
