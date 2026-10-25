# To prove: statements from the A047697 mining

*25 October 2026. Companion to `FINDINGS.md`, where the evidence comes from, and `TODO.md`, the short
list.*

**Setting.** n > 0, and its *coprime representations* n = x³ + y³ with gcd(x, y) = 1, signs allowed, unordered.
- For a representation write **s = x + y** and **t = x² − xy + y²**, so n = s·t.
- On the curve x³ + y³ = n, a representation is an integer point (x, y). Swapping x and y gives the point −P.
  The point at infinity (1 : −1 : 0) is a flex and serves as the origin, so **three points add to zero exactly
  when they are collinear**.
- A **split prime** is a prime p ≡ 1 (mod 3). These are the primes that split in the Eisenstein integers
  Z[ω] (ω a cube root of 1).

**Status labels:**
- **PROVED**: a complete argument is given here; it still needs writing up carefully.
- **SKETCH**: an argument whose main idea is clear, with details still to check.
- **OPEN**: we believe it, but have no argument yet.
- **CONJECTURE**: a statistical or global statement; a proof is not expected soon.

Each item gives the statement, the evidence, why we think it's true, what proving it would give us, and the
literature.

---

## 1. Primes ≢ 1 (mod 3) divide every s. Status: PROVED (p ≠ 3); SKETCH (p = 3)

**Statement.** If a prime p ≡ 2 (mod 3), or p = 2, divides n, then p divides s = x + y in **every** coprime
representation of n.
- For p = 3: 9 never divides t, and if 3 | t then 3 | s.
- So whenever 27 | n, every representation has 9 | s.

**Evidence.** It held in 100% of about 50,000 numbers (F1: all k = 1 to 5 groups, ≤ 10¹⁵, plus the five-ways).

**Proof (p ≠ 3).** n = s·t, so it is enough to show p ∤ t.
- Suppose p | t = x² − xy + y². Then p ∤ y, otherwise p | x too, contradicting coprimality.
- Then (2x − y)² ≡ −3y² (mod p), so −3 is a square mod p.
- For odd p ≠ 3 that forces p ≡ 1 (mod 3), by quadratic reciprocity.
- For p = 2: t is odd whenever x and y are not both even. If one is odd, t ≡ 1; if both are odd, t ≡ 1 − 1 + 1.

**Sketch (p = 3).** t = s² − 3xy. If 3 | t then 3 | s, and t ≡ −3xy (mod 9) with 3 ∤ xy (coprime and
3 | x + y), so v₃(t) = 1 exactly.

**Use.** It explains why primes ≡ 2 (mod 3) are rare in multi-way numbers. Each such prime must fit into every
s at once, which narrows the choices without adding to them. It is the analogue of Theorems A–D in the
34Family work (`~/Documents/sixes/six-one-five/34Family/THEOREMS.md`).

**Literature.** Classical. The fact that −3 is a square mod p exactly when p ≡ 1 (mod 3) is standard: see
K. Ireland and M. Rosen, *A Classical Introduction to Modern Number Theory*, Graduate Texts in Mathematics 84,
Springer, 2nd ed. 1990, ch. 9 ("Cubic and Biquadratic Reciprocity": Z[ω], splitting of primes, cubic
residues).

---

## 2. Local densities: 3/8 of coprime sums are divisible by 7, and the mod-9 ratio. Status: SKETCH

**Statement.**
- **(a)** Among coprime pairs (x, y), ordered by size, the share with 7 | x³ + y³ is **3/8**.
- **(b)** Coprime sums with n ≡ ±1 (mod 9) have **twice** the 3-adic local density of those with n ≡ ±2 (mod 9).
- **(c)** More generally, for a split prime p dividing n, a³ + b³ ≡ 0 (mod p) has about 3(p − 1) solutions,
  against about p for a typical residue. For p ≡ 2 (mod 3) there is no such gain.

**Evidence.** F1 and F2:
- 7 | n for 38.1% of one-ways against the predicted 37.5%;
- n mod 9 counts at k = 1: 134,381 (≡ 1) and 133,826 (≡ 8) against 67,509 (≡ 7) and 67,569 (≡ 2), which is
  2 : 1.

**Why we think it's true.**
- **(a)** Cubes mod 7 are {0, ±1}. Of the 48 residue pairs (x, y) mod 7 that are not both 0, exactly 18 have
  x³ + y³ ≡ 0. Coprime pairs are equidistributed over such classes, a standard sieve fact.
- **(b), (c)** Direct counts of solutions mod 9 and mod p.

**Use.** It is the basis of the local-density (Hardy–Littlewood "singular series") model of how many
representations n should have. That model explains F1 and F2: why multi-way numbers favour split primes,
7 | n, odd n and n ≡ ±1 (mod 9). It is also the theory behind the candidate filter in `cheap_search.py`.

**Exact local counts are classical (Gauss).** For p ≡ 1 (mod 3) write 4p = A² + 27B² with A ≡ 1 (mod 3). Then
the number of solutions of x³ + y³ = 1 in F_p is exactly p − 2 + A (Ireland & Rosen, ch. 8 "Gauss and Jacobi
Sums", §4, Theorem 2, p. 97, via Jacobi sums).
- The count for x³ + y³ ≡ n depends on the cubic residue class of n mod p. That is the cube-residue pattern seen
  mod 7 and mod 13 in F2, where residues that are cubes (mod 13: 1, 5, 8, 12) behave differently.
- These counts give the exact local factors for the model C1.

**Literature:**
- Hooley, "On the representations of a number as the sum of two cubes", Math. Z. 82 (1963);
- Heath-Brown, "The density of rational points on cubic surfaces", Acta Arith. 79 (1997);
- for the singular series of binary cubic forms in general, the Hardy–Littlewood circle-method literature.

---

## 3. The 3 | n anomaly. Status: OPEN

**Statement to explain.** The share of n with 3 | n moves with k as 25% (k = 1) → 24% (k = 2) → 31% (k = 3) →
12% (k = 4) → 0% (k = 5): up, then down (F1).

**Why it may be real.** The 3-adic picture has several levels (the exponent of 3 in n, n mod 27, the 9 | s case
of item 1). Different levels may favour three-ways and four-ways differently.

**What to do.** Compute the exact 3-adic local densities for each v₃(n) and n mod 27, and compare them with the
counts by k. The k ≥ 4 samples are small (204 four-ways), so first check that the anomaly survives more data.

---

## 4. No three positive points are collinear. Status: PROVED

**Statement.** No straight line meets x³ + y³ = n (n > 0) in three points with x, y > 0. So a collinear
triple of representations always contains at least one difference.

**Evidence.** Of 11,056 collinear triples, those with 0, 1 and 2 sums number 3,750, 3,535 and 3,771; there
are **none with 3 sums** (F7). All 25 coprime three-ways made only of sums are of the "independent" kind.

**Proof.** In the positive quadrant, x³ + y³ is a convex function, so the region x³ + y³ ≤ n with x, y ≥ 0 is
convex. Its boundary arc is strictly convex, and a line meets a strictly convex arc at most twice.

**Use.** Cubefree taxicab k-ways (OEIS A080642: all sums, coprime) cannot use the line mechanism, so they need k
independent points and hence rank of about k. That explains why cubefree Ta(4) ≈ 1.8 × 10¹⁸ but
A047697(4) ≈ 1.7 × 10⁷, and why the cubefree problem needs high-rank curves rather than line search.

**Literature.** Elementary. Compare Silverman's theorem in item 9.

---

## 5. No tangent relations among coprime integer points. Status: SKETCH

**Statement.** If P = (x, y) is a coprime integer point of x³ + y³ = n and |x³ − y³| > 3, then the third
intersection of the tangent line at P is **not** an integer point. So relations of the form 2P + Q = 0 between
coprime representations essentially never occur.

**Evidence.** Up to 10¹⁵, every exact relation among the integer points is either a 3-term ±1 relation (a
line) or a 4-term ±1 relation (a "hub"). **No coefficient 2 occurs anywhere** (F5: 2,012 numbers, exact).

**Why we think it's true.**
- The classical duplication formula for x³ + y³ = n gives the tangent's third point as
  ( x(x³ + 2y³)/(x³ − y³), −y(2x³ + y³)/(x³ − y³) ), up to the swap/sign convention.
- Since gcd(x, y) = 1, gcd(x³ − y³, x) = gcd(y³, x) = 1.
- So integrality needs x³ − y³ | x³ + 2y³, hence x³ − y³ | 3y³, hence (by coprimality again) x³ − y³ | 3.

**Checked (25 October 2026):** this point lies exactly on x³ + y³ = n for 20,000 random coprime (x, y), and it
was never an integer point when |x³ − y³| > 3. Still to do: the small cases |x³ − y³| ≤ 3, and whether the
tangent's third point is this point or its swap (it doesn't affect integrality).

**Use.** It explains why lines, and not tangents, carry the multi-representation structure. It also means a
six-way built from relations must use lines or hubs, which constrains the shapes a six-way can take.

**Literature.**
- J. W. S. Cassels, *Lectures on Elliptic Curves*, LMS Student Texts 24 (Cambridge, 1991), ch. 6 exercises
  ("formula of Desboves" for the third intersection of a tangent) and ch. 7 ("Non-singular cubics. The group
  law"). Extract in `refs/cassels-6-9.pdf`.
- Dickson vol. 2, ch. XXI (Desboves, Lucas). The duplication formula goes back to Fermat and Euler.

---

## 6. Which line directions can carry coprime triples. Status: norm part SKETCH; parity part OPEN

**Statement.** Suppose a line a x + b y = c (gcd(a, b) = 1) passes through three coprime integer points of
x³ + y³ = n. Then:
- **(a)** a·b > 0, and a·b is a norm from Q(√−3): every prime ≡ 2 (mod 3) appears to an even power;
- **(b)** a·b is **even** (equivalently, given (a), 4 | a·b). No such line has a and b both odd.

**Evidence.** All 11,155 lines up to 10¹⁷, across 2,605 directions: **no exception** to either part (F10).
- The 2-adic valuations of a·b are 2 (1,511 directions), 4 (436), 6 (134), 8 (53) and 10 (2), never 0.
- The rule is also predictive: every candidate direction with cost |b³ − a³| < 10⁵ (80 of them) does occur.

**Why (a) holds.**
- Eliminating one root from the two Vieta equations on the line, which do not depend on n, gives the conic
  w² + 3v² = 12·a·b³·c²/(b³ − a³)².
- This needs a rational point, and w² + 3v² represents a positive rational exactly when it is a norm from
  Q(√−3).
- 12·a·b³·c²/(b³ − a³)² is 3·a·b times a square, and 3 is a norm, so a·b must be a norm.

**Why (b) might hold.** Unknown. A 2-adic analysis looks like the way in:
- if a and b are both odd, then b³ − a³ is even, so the root sum −3a²c/(b³ − a³) forces 2-power conditions
  on c;
- combined with the coprimality of all three points, that may force a contradiction.

**Use.** It is the rule that tells the line search which directions to enumerate and in what order
(`line_enum.py`). A proof makes it complete: no direction outside the rule can ever contribute.

**Literature.** The norm-form condition is probably implicit in Werebrusow's general solution of
x³ + y³ = x₁³ + y₁³ = x₂³ + y₂³, which uses M² + MN + N² = 3ω²φψ (Matem. Sbornik 27, 1909; summarised in
Dickson vol. 2, p. 562). The parity condition has not been found anywhere.

---

## 7. The (3k², 3k² + 1) line family. Status: PROVED (polynomial identity)

**Statement.** For every integer k:

    (27k⁴ + 6k² + 1)³ − (27k⁴ + 6k²)³
      = (9k³ + 6k² + 1)³ − (9k³ − 3k² + 3k)³
      = (9k³ + 3k² + 3k)³ − (9k³ − 6k² − 1)³
      = (9k² − 3k + 1)(9k² + 3k + 1)(27k⁴ + 9k² + 1)

and all three points lie on the line 3k²·x + (3k² + 1)·y = 27k⁴ + 9k² + 1.

**Proof.** A polynomial identity, checked symbolically in PARI (F9). k = 1 gives 3367 = A047697(3).

**Still to do.**
- Check that the three points are coprime for every k (true for k = 1 to 5).
- Explain why, within the near-diagonal directions (m + 1, m), exactly m = 3k² works for c = a² + ab + b².
  The derivation in F9 shows the discriminant is 12m(m + 1)², a square exactly when 3m is a square.
- Decide whether the family is classical (Werebrusow's general solution; Mahler-type identities).

**Literature.** Dickson vol. 2, ch. XXI; Mahler, "Note on Hypothesis K of Hardy and Littlewood",
J. London Math. Soc. 11 (1936), whose identity has the same 9k³ and 9k⁴ ingredients.

---

## 8. A line's E = a² + ab + b² divides c and n. Status: SKETCH

**Statement.** For any line a x + b y = c through three coprime integer points of x³ + y³ = n, the number
E = a² + ab + b² divides c and divides n. (The factor 3 needs care.)

**Evidence.** All 11,176 lines, including the five-ways: no exception (F11).

**Why.**
- Substituting the line gives (b³ − a³)x³ + 3a²c·x² − 3ac²·x + (c³ − b³n) = 0, with b³ − a³ = (b − a)·E.
- The root sum −3a²c / ((b − a)E) is an integer, and gcd(a, E) = 1, so E | 3c. That gives E | c when 3 ∤ E.
- The root product (b³n − c³) / ((b − a)E) is an integer, so E | b³n − c³. Then E | c gives E | b³n, and
  since gcd(b, E) = 1, E | n.

**Use.** It turns a factorisation of n into the complete list of possible line directions through its points,
so all lines of a given n can be found from its divisors (the per-n line finder).

---

## 9. Background theorem: many integer points force high rank. KNOWN (Silverman)

**Statement.** There is a constant c > 1 such that for every cube-free A, the number of integer points on
x³ + y³ = A is less than c^r(A), where r(A) is the rank.

**Our data.**
- Taxicab five-, six- and seven-way curves have ranks clustering near k (F3).
- The coprime five-ways' points span rank 3 with two line relations (F4).

**What we would want.** An **explicit** c. With it, "a coprime six-way needs rank ≥ r₀" becomes a proved lower
bound, usable to rule out families of curves.

**Literature.**
- J. H. Silverman, "Integer points and the rank of Thue elliptic curves", *Invent. Math.* 66 (1982) 395–404,
  in `refs/Thuebf01389220.pdf`. **Theorem A:** for a cubic form f with non-zero discriminant there are
  *effective* constants κ (absolute) and m₀ (depending on f) such that N_f(m) < κ^(R_f(m)+1) for all cube-free m
  with |m| > m₀. The paper does not state κ numerically; it would have to be extracted from the proof (Theorems
  B and C).
- **Silverman's open question** (same paper): is sup N_f(m), over cube-free m, infinite? An affirmative answer
  for even one form, e.g. x³ + y³, would give elliptic curves over Q of arbitrarily large rank. **So whether
  coprime k-ways exist for every k is tied to the unbounded-rank problem.** This is context for C3; a single
  six-way is a far weaker claim.
- Dem'janenko stated Theorem A earlier without a correct proof; Lang's commentary discusses it.
- Popular summary: `refs/silverman_1993_taxicabs_sums_two_cubes.pdf`.

---

## 10. Root numbers. KNOWN (Birch–Stephens, via Stephens' thesis); VERIFIED on our data

**Observation.** The root number of x³ + y³ = n is almost entirely determined by n mod 9 and by the parity of
the number of primes ≡ 2 (mod 3) dividing n (F2). The few exceptions are probably 3-adic or come from squared
factors.

**The formula** (Birch & Stephens 1966, p. 298, citing Stephens' 1965 Manchester PhD thesis). For cube-free A:

    (−1)^rank(x³ + y³ = A) = −w₃ · ∏ w_p   (over primes p ≠ 3 dividing A)

- w₃ = −1 if A ≡ ±1 or ±3 (mod 9), and +1 otherwise;
- w_p = −1 if p ≡ 2 (mod 3), and +1 otherwise.

(The parity of the rank equals the parity given by the root number, under the parity conjecture.)

**Verified (25 October 2026):** it agrees with PARI's `ellrootno` on all 4,315 cube-free n tested (2,000
one-ways at 10¹⁵ and 3,000 multi-ways ≤ 10¹⁵), with 0 disagreements. The "exceptions" in F2 are exactly the
n that are not cube-free (685 of the sample), where this formula does not apply.

**Side remark (Birch–Stephens):** it implies, under BSD, that every prime ≡ 4, 7, 8 (mod 9) is a difference of
two rational cubes. This is Sylvester's conjecture.

**Literature.**
- B. J. Birch and N. M. Stephens, "The parity of the rank of the Mordell–Weil group", *Topology* 5 (1966)
  295–299;
- Zagier & Kramarz, "Numerical investigations related to the L-series of certain elliptic curves" (1987).

---

## 11. Same-line chords have denominators divisible by 3. Status: OPEN (exact empirical law)

**Statement.** Let P, Q, R be coprime integer points of x³ + y³ = n on one line (P + Q + R = 0). Then the third
intersection of the line through P and −Q (that is, the point Q − P, if it is not itself a representation)
has denominator divisible by 3.

**Evidence.** 33,168 such chords from all coprime k ≥ 3 numbers ≤ 10¹⁵: 100% divisible by 3. Chords between
points not on a common line: 52.7% (F18).

**Why it may hold.**
- For integers x³ ≡ x (mod 3), so every representation has x + y ≡ n (mod 3).
- Reduction mod 3 turns x³ + y³ = n into (x + y)³ = n, a curve with additive reduction.
- For collinear integer points the difference Q − P should lie in the kernel of reduction, E₁(Q₃), so its
  denominator is divisible by 3.
- Tools: the reduction of points modulo a prime and the filtration E₀ ⊃ E₁ (Silverman, *The Arithmetic of
  Elliptic Curves*, ch. VII); the component group at p = 3 for these CM curves.

**Use.** It shows that a five-way's same-line near-misses can never close into a sixth representation, so
near-miss searches can ignore them.

## 12. Points on a line carry the line's E in their t. Status: PROVED (given item 8)

**Statement.** If (x, y) lies on a x + b y = c, a line through three coprime representations, then
E = a² + ab + b² divides t = x² − xy + y². Hence E (apart from a factor of 3) never divides s = x + y for those
points.

**Proof.** By item 8, E | c, so a·x ≡ −b·y (mod E). Then a²t = (ax)² − (ax)(ay) + a²y² ≡ b²y² + aby² + a²y² =
E·y² ≡ 0 (mod E). Since gcd(a, E) = gcd(a, b²) = 1, E | t. Then gcd(s, t) | 3 gives the second part.

**Evidence.** 33,465 of 33,465 line points (F19). By contrast, the free point of a "line + free point" four-way
has E | s in 26% of cases.

## Conjectures (statistical; not expected to be proved soon)

- **C1, local-density model.** The number of coprime representations of n behaves like a Poisson variable
  whose mean is a size factor times the product of the local densities in item 2. Test: it should reproduce
  the exact counts of k = 2, 3, 4 up to 10¹⁵ and the 11 five-ways up to 10²³.
- **C2, the cost ordering.** The number of lines in an allowed direction (a, b) up to a bound falls off as a
  power of |b³ − a³|. Supported by F10, where line counts roughly follow the cost order.
- **C3, the six-way.** A coprime six-way exists. By analogy with the five-ways (F4, F13), it most likely has at
  least one cheap line and 10–12 split primes. The line search (`cheap_search.py`) is the tool built around
  that expectation. The exhaustive search shows A047697(6) > 10²³.

---

## Next steps for this file

1. Write the PROVED items (1, 4, 7) out in full, in the style of 34Family's `THEOREMS.md`.
2. Add a `verify_theorems.py` that checks items 1, 2(a), 4, 5, 6, 8 and 10 against every dataset in
   `FINDINGS.md`.
3. Attack item 6(b) (parity) and the p = 3 parts of items 1 and 8.
4. Look up the exact duplication formula (item 5) and the Birch–Stephens formula (item 10).
