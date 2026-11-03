# Three ideas for a six-way search far cheaper than exhaustive (3 November 2026)

Context: the exhaustive search costs about B^(2/3) pairs. The listed six-way "profile" constraints each remove only
20-70% (F44-F45). The strong cut is structural: a six-way almost certainly contains a line (97% of k >= 3 numbers do,
all 82 five-ways do). The three ideas below try to turn that into searches that are complete within a stated class.

## Idea 1: a line search that is complete within its class

**Claim to make:** "every n <= B having a line in a direction of cost b^3 - a^3 <= C has been counted exactly; none is
a six-way". Two ingredients, both now in reach:

1. **Per direction, an exact height bound.** By Theorem 13, n = E S1 S2 S3 / ((a - b)^2 G^3), where Si(s, r) is the
   x + y of the i-th point as a quadratic form in the slope (s, r) and G is the gcd divided out.
   - Measured (5 directions): every Si is **positive definite** (discriminant -3 k^2), so S1 S2 S3 >= m * h^6 with an
     explicit m from the forms' minima on the unit circle. No unbounded cancellation tail exists.
   - **G takes 2-4 values per direction** and divides a fixed number (12 for (3,4); 507 = 3*13^2 for (12,13); 48 for
     (3,16); 441 = 21^2 for (16,21); 588 = 3*14^2 for (27,28)), set by (s, r) modulo a fixed modulus. F39's "low
     tail" is the large-G classes (1.8% of slopes have G = 507 for (12,13)).
   - So for each direction and each G-class there is a rigorous H(a, b, B, G) beyond which n > B. Enumerate each
     class to its own height (the large-G classes are rare, so the extra cost is small).
   - To do: prove "Si definite" in general (looks like a norm form from Q(sqrt -3)) and "G divides g(a, b)"; compute m
     per direction.
2. **No split-prime filter.** Count every candidate exactly (0.1 ms each with PARI factorisation).

**Cost:** slopes per direction ~ (B / cost^2)^(1/3), so all directions up to cost C cost ~ B^(1/3) * log C slopes
(each direction class contributes about equally per decade of cost), plus one conic point per direction.
- B = 1e30, C = 1.2e12 (the directions already searched): order 1e11-1e12 slopes (Python ~2 us each) and order
  1e9-1e10 candidates to count exactly. On 7of9 (64 threads): hours to a day. Against ~1e20 pairs exhaustive.
- **Coverage of the class**, measured on exhaustive data: 99.9% of the lines of four- and five-ways <= 2.5e23 have cost
  <= 1e12 (max 1.19e12; median cost grows with n, 4e3 at <= 1e15 to 4e6 near 1e23). At 1e30 the needed C is
  larger (roughly cost <= sqrt(n) since n ~ cost^2 h^6); extrapolate and choose C so the measured coverage stays
  >= 99%; log C barely changes the slope count, but the number of directions (and conic points) grows like C^(2/3).
- **Open, and the step to a full line-class theorem:** a rigorous lower bound n >= g(cost) for every direction (data:
  n ~ cost^2, F39). With it, "every n <= B with any line" is complete at ~B^(1/3) polylog cost. Near-diagonal
  directions (b - a small, G up to ~3b^2) are where the bound is weakest and need care.

**What it would give the paper:** "no six-way <= 1e30 contains a line of cost <= C" as a theorem, and an exact
census of every line-carrying multi-way to 1e30 in that class (unbiased statistics far beyond 2.5e23).

## Idea 2: bowtie first

- **No cheap family per direction pair:** the 79 bowties use 79 different direction pairs.
- **But one direction dominates:** (3, 4) is in 15 of 79 bowties (19%), then (12, 13), (27, 28): the b = a + 1
  family (3k^2, 3k^2 + 1) of F9. By Theorem 13, b - a = 1 lines make n with no prime = 2 (mod 3) and 3 not dividing n,
  i.e. the "all split" profile of 83% of five-ways.
- **Exact counting already finds every bowtie through any enumerated line,** so a separate bowtie generator adds
  nothing once idea 1 runs. The useful form of idea 2 is **depth on the b - a = 1 directions**: run (3,4), (12,13),
  (27,28), ... complete (idea 1 bound) to much larger B, e.g. (3,4) to 1e36: about 1e11 slopes, 1e10 candidates
  (here a split-prime filter is acceptable: a hunt, not a theorem).

## Idea 3: stars around a point of small denominator

- A star (three chords through one rational R of denominator D) is six points with three relations. On D^3 n it is a
  seven-point star of integer points whose six outer points are multiples of D; for D = 1 it would be a seven-way.
- **Rate unknown:** no R carries three chords among ~500 hubs (x 3 meeting points each), so the rate per R is below
  about 6e-3 (95%). Hubs are 11% of four-ways, so if the rate were near that bound the star route would beat
  bowtie + free point (about 7e-6 per four-way); if a third chord is as rare as a second one per D-line candidate
  (7e-7, F41), stars are hopeless.
- **Cheap next step:** in the existing D-line outputs (night_7of9/results_29oct_hubs/, 276 M candidates), count R
  values hit by >= 2 D-lines, and among them >= 3, to measure the third-chord rate directly. Decide after that.

## Order

1. Idea 1 on the Mac for a few directions: rigorous H per G-class, check against the existing runs (must re-find
   every triple they found, and nothing with n <= B outside the bound). Then prove definiteness / G bound.
2. Idea 1 full run on 7of9 to 1e30, cost <= C, no filter.
3. Idea 2 as deep b - a = 1 runs.
4. Idea 3 measurement from existing D-line data.
