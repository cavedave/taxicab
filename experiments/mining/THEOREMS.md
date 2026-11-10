# Theorems: proofs for the A047697 line method

*26 October 2026. Proofs for statements in `TOPROVE.md`; evidence is in `FINDINGS.md`.*
*`verify_theorems.py` re-checks every statement here against the data.*

## Setting and notation

- n ≠ 0 is an integer. A *point* is an integer solution (x, y) of x³ + y³ = n. It is *coprime* if
  gcd(x, y) = 1.
- A *line* is a x + b y = c with integers a, b, c and gcd(a, b) = 1.
- The *direction* of the line is (a, b), up to an overall sign.
- Throughout:
  - D = b³ − a³;
  - E = a² + ab + b², so D = (b − a)·E;
  - a point on the line has s = x + y and t = x² − xy + y², with n = s·t.

**Lemma 0 (the cubic).** Let b ≠ 0. Put y = (c − a x)/b into x³ + y³ = n and multiply by b³:

    D·x³ + 3a²c·x² − 3ac²·x + (c³ − b³n) = 0.                                    (1)

- Two points of the line with the same x are equal, since b ≠ 0.
- If D ≠ 0, then **three distinct points of the curve on the line** are exactly the three roots x₁, x₂, x₃ of (1).
  So

      e₁ = x₁ + x₂ + x₃ = −3a²c / D,
      e₂ = x₁x₂ + x₁x₃ + x₂x₃ = −3ac² / D,                                         (2)
      e₃ = x₁x₂x₃ = (b³n − c³) / D.

- If D = 0, then b = a, so (a, b) = ±(1, 1). Equation (1) then has degree ≤ 2, and the line meets the curve in at
  most two points.
- If b = 0 (a vertical line x = c), then y³ = n − c³ has one real root, so there is at most one point.

*(Identities checked symbolically in PARI.)*

---

## Theorem 1 (direction rule; TOPROVE item 6, both parts)

*If a line a x + b y = c contains three distinct coprime points of x³ + y³ = n, then:*
- **(a)** *a·b > 0, a ≠ b, and a·b is a norm from Q(√−3): every prime p ≡ 2 (mod 3) divides a·b to an
  even power;*
- **(b)** *a·b is even. Together with (a), this gives 4 | a·b and an even power of 2 in a·b.*

This is exactly the rule `line_enum.allowed()` uses (FINDINGS F10).

**Proof of (a).**
1. **Excluded cases.** By Lemma 0, b ≠ 0 and D ≠ 0, so a ≠ b. By symmetry (swap x and y) a ≠ 0 as well.
2. **Line through the origin.** If c = 0, then (1) reads D x³ = b³ n. That has at most one rational root, which is
   impossible. So c ≠ 0.
3. **The conic.** Put uᵢ = xᵢ / c. By (2), u₁ + u₂ + u₃ = s₀ := −3a²/D and Σuᵢuⱼ = p₀ := −3a/D.
   - Eliminate u₃ = s₀ − u₁ − u₂, and shift vᵢ = uᵢ − s₀/3. This gives

         v₁² + v₁v₂ + v₂² = s₀²/3 − p₀ = 3ab³ / D²       (identity checked in PARI).

   - With X = D·v₁ and Y = D·v₂ this is the conic

         X² + XY + Y² = 3ab³,                                                      (3)

     with a rational point (X, Y).
4. **The norm form.** X² + XY + Y² = N(X − Yω), the norm from Q(ω) = Q(√−3), where ω² + ω + 1 = 0.
   - It is positive definite. If X = Y = 0, then u₁ = u₂ = s₀/3, and then u₃ = s₀/3 too, so the three points
     coincide. Hence 3ab³ = N(X − Yω) > 0, so a·b > 0.
5. **Which rationals are norms.** A positive rational is a norm from Q(√−3) exactly when every prime
   p ≡ 2 (mod 3) divides it to an even power.
   - Z[ω] is a principal ideal domain: 3 ramifies, primes p ≡ 1 (mod 3) split, and primes p ≡ 2 (mod 3) stay
     inert.
   - So the norms of elements of Z[ω] are the positive integers with even v_p for every p ≡ 2 (mod 3).
   - A rational norm is N(β)/d² with β ∈ Z[ω] and d ∈ Z, which preserves those parities.
6. **Conclusion.** v_p(3ab³) = v_p(a) + 3v_p(b) ≡ v_p(ab) (mod 2) for p ≠ 3. ∎(a)

**Proof of (b).** Suppose a and b are both odd. (They cannot both be even, since gcd(a, b) = 1.)
1. **D and c.**
   - E = a² + ab + b² is odd, so v₂(D) = v₂(b − a) =: k ≥ 1.
   - e₁ is an integer, so by (2) v₂(c) ≥ v₂(D) = k (since a is odd).
   - In particular c is even.
2. **The points are odd.** Mod 2 the line reads x + y ≡ c ≡ 0, so each point has x ≡ y (mod 2). A coprime
   point cannot have both coordinates even, so **every xᵢ is odd**.
3. **Parity of e₁.** e₁ = x₁ + x₂ + x₃ is a sum of three odd numbers, so it is odd. By (2),
   v₂(e₁) = v₂(c) − k = 0, so v₂(c) = k exactly.
4. **Parity of e₂: the contradiction.**
   - e₂ = x₁x₂ + x₁x₃ + x₂x₃ is a sum of three odd numbers, so it is odd.
   - But by (2), v₂(e₂) = 2v₂(c) − k = k ≥ 1, so e₂ is even.

So a·b is even, and by (a) its power of 2 is even, so it is at least 2. ∎(b)

**Remarks.**
- Part (a) is the necessary half. Conversely, if a·b > 0, a ≠ b and a·b is a norm, then (3) has a rational
  point, hence infinitely many (a conic with one rational point is rational). Each point gives a rational
  collinear triple on some curve x³ + y³ = n. Clearing denominators gives integer triples. Whether a *coprime*
  one exists is not claimed. Empirically every allowed direction has one.
- Part (b) uses coprimality essentially. Without it, scaling an odd-direction rational triple gives integer
  triples with a common factor.
- **Literature:** (a) is presumably implicit in Werebrusow's parametrisation (Dickson vol. 2 ch. XXI,
  M² + MN + N² = 3ω²φψ). We have not found (b) stated anywhere.

---

## Theorem 2 (E divides c and n; TOPROVE item 8)

*If a line a x + b y = c contains three distinct points of x³ + y³ = n (coprimality not needed), then
E = a² + ab + b² divides c and n.*

**Proof.**
1. **E is coprime to a and b.** E ≡ b² (mod a), so gcd(E, a) = gcd(b², a) = 1. Similarly gcd(E, b) = 1.
2. **E | c.** By (2), D divides 3a²c, because e₁ is an integer.
   - **For a prime p ≠ 3:** v_p(E) ≤ v_p(D) ≤ v_p(3a²c) = v_p(c), since p ∤ a.
   - **For p = 3, if 3 | E:**
     - E = (a − b)² + 3ab, so 3 | E forces a ≡ b (mod 3) with 3 ∤ ab, and then v₃(E) = 1.
     - Also 3 | (b − a), so v₃(D) = v₃(b − a) + 1 ≥ 2.
     - From D | 3a²c: v₃(c) ≥ v₃(D) − 1 ≥ 1 = v₃(E).

   So E | c.
3. **E | n.** By (2), b³n = c³ + D·e₃. Here E | c and E | D, so E | b³n. Since gcd(E, b) = 1, E | n. ∎

**Remark.** The same argument gives (b − a) | 3c, since gcd(b − a, a) = 1. Combined with E | c, this says c is
nearly a multiple of D. Examples: direction (3, 4) has E = 37 = D, and every c found is a multiple of 37.

---

## Theorem 3 (E divides t at every point of the line; TOPROVE item 12)

*If a line a x + b y = c contains three distinct coprime points of x³ + y³ = n, then E divides
t = x² − xy + y² at each of them.*

**Proof.** Take one of the points. By Lemma 0's substitution, b·s = (b − a)·x + c (checked in PARI). Let p | E.
- **p ≠ 3.**
  - p ∤ (b − a): if p divided both E and b − a, then a ≡ b, so E ≡ 3a² (mod p), forcing p | 3a. That is
    impossible, since p ∤ a and p ≠ 3.
  - p ∤ x: if p | x then, since p | c (Theorem 2), p | b·y, so p | y. That contradicts coprimality.
  - So p ∤ b·s, hence p ∤ s, and v_p(t) = v_p(n) ≥ v_p(E) (Theorem 2).
- **p = 3.** Then v₃(E) = 1, and 3 divides both b − a and c, so 3 | b·s and hence 3 | s. Since t = s² − 3xy,
  3 | t.

So E | t. ∎

---

## Theorem 4 (the slope enumeration is complete; plan item 1b)

Fix an allowed direction (a, b) with 0 < a < b, and a rational point P₀ = (X₀, Y₀) on the conic (3). For a
reduced slope r/s (gcd(r, s) = 1, s ≥ 0, and r = 1 when s = 0), let P(r, s) be the second intersection of the
conic with the line through P₀ in direction (s, r). This is what `line_enum.triples()` computes:
- m = −B/Q(s, r) with B = 2X₀s + X₀r + Y₀s + 2Y₀r and Q(s, r) = s² + sr + r²;
- P = P₀ + m·(s, r).

*Statement:*
- **(i)** Every rational point P ≠ P₀ of (3) equals P(r, s) for exactly one reduced slope.
- **(ii)** Ordered rational triples (u₁, u₂, u₃) with Σuᵢ = s₀ and Σuᵢuⱼ = p₀ correspond one-to-one to rational
  points of (3), by X = D·u₁ + a² and Y = D·u₂ + a². (Here D·s₀/3 = −a².)
- **(iii)** For a rational triple u, the set of c making all xᵢ = c·uᵢ and yᵢ = c(1 − a·uᵢ)/b integral is c₀·Z,
  where c₀ is the least positive such c. Every point of the c = k·c₀ triple is k times a point of the c₀ triple.
  So **only c = ±c₀ can give coprime points**, and `line_enum` uses exactly c₀ (with an overall sign flip to make
  n > 0).

*Consequence:*
- A coprime collinear triple in direction (a, b) or its mirror (b, a), the mirror giving the swapped points
  (same n), is found by `line_enum.py --height H` if and only if one of its ≤ 6 orderings has a slope of
  height max(|r|, s) ≤ H.
- So "searched direction (a, b) to height H" is an exact statement. A triple is printed once per ordering whose
  slope lies in the searched region, which explains the duplicates seen with `--chunks` (F26).

**Proof.**
- **(i)** Conics: the line through P₀ and P has a direction vector (X − X₀, Y − Y₀). Divide it by the gcd of the
  numerators after clearing denominators, and fix the sign, to get a unique reduced (s, r).
  - Substituting P₀ + m·(s, r) into (3) gives m·B + m²·Q(s, r) = 0, since P₀ is on the conic.
  - Q is positive definite, so Q(s, r) > 0, and the second root m = −B/Q is rational.
  - If B = 0 (the tangent), the "second" point is P₀ itself.
- **(ii)** This is Theorem 1's elimination run backwards: X = D(u₁ − s₀/3) = D·u₁ + a², and u₃ = s₀ − u₁ − u₂.
- **(iii)** The integrality conditions are "c·q is an integer" for finitely many rationals q, so the admissible c
  form a subgroup of Z.

Ordering, mirroring and the sign flip are bookkeeping. ∎

**Remark.** The ≤ 6 orderings correspond to the ≤ 6 rational points of (3) that give the same unordered triple.
The minimal height over them is what the coverage statement uses. A per-triple "height" (the minimum) would
make coverage claims independent of P₀. The current claims are made for the P₀ that PARI's `qfsolve` returns,
which is recorded implicitly by running the same code.

---

## Theorem 5 (primes ≢ 1 (mod 3) in a coprime representation; TOPROVE item 1, now complete)

*Let n = x³ + y³ with gcd(x, y) = 1, and let s = x + y and t = x² − xy + y² (so n = s·t). Then:*
- **(a)** *If p ≡ 2 (mod 3), or p = 2, then p ∤ t. So p | n implies v_p(s) = v_p(n).*
- **(b)** *v₃(t) ≤ 1, and 3 | t ⟺ 3 | s.*
- *Consequently v₃(n) ∈ {0} ∪ {2, 3, …}, and 27 | n forces 9 | s in every representation.*

**Proof.**
- **(a)** As in TOPROVE item 1: if p | t then p ∤ y, so (2x − y)² ≡ −3y² (mod p), and −3 is a square mod p. For an
  odd prime p ≠ 3 that forces p ≡ 1 (mod 3). For p = 2, t is odd when x and y are not both even.
- **(b)** t = s² − 3xy.
  - If 3 | t then 3 | s², so 3 | s. Conversely, if 3 | s then 3 | t.
  - If 3 | s, then 3 ∤ x: otherwise 3 | y as well, contradicting coprimality. Likewise 3 ∤ y.
  - So t ≡ −3xy (mod 9) with 3 ∤ xy, which gives v₃(t) = 1.
- **Consequence:**
  - If 3 ∤ s, then 3 ∤ t, so v₃(n) = 0.
  - Otherwise v₃(n) = v₃(s) + 1 ≥ 2, and v₃(n) ≥ 3 gives v₃(s) ≥ 2. ∎

(Part (a) is classical. The consequence v₃(n) ≠ 1 is the classical "n ≢ ±3 (mod 9)".)

---

## Lemma 6 (all representations of n share xy mod 3; first half of TOPROVE item 11)

*If (x, y) and (x', y') are coprime representations of the same n, then xy ≡ x'y' (mod 3).*

**Proof.**
- **If 3 | n:** then 3 | s for both representations (Theorem 5). So x ≡ −y (mod 3), with x a unit mod 3, and
  xy ≡ −x² ≡ −1 (mod 3). The same holds for x'y'.
- **If 3 ∤ n:**
  - x³ ≡ x (mod 3), so s ≡ n (mod 3), and 3 ∤ s.
  - From (x + y)³ = n + 3xy(x + y): 3xy·s = s³ − n.
  - s³ mod 9 depends only on s mod 3, which is n mod 3. So s³ − n (mod 9) depends only on n, and hence so does
    xy ≡ ((s³ − n)/3)·s⁻¹ (mod 3). ∎

**What it gives for item 11.** The chord through P = (x, y) and −Q = (y_Q, x_Q) meets the curve again at the
point with coordinates

    X = (y_Q²·y − x²·x_Q) / Δ,   Y = (x·x_Q² − y_Q·y²) / Δ,   Δ = x·y − x_Q·y_Q

This is the chord formula of Werebrusow/Desboves (TOPROVE item 11, FINDINGS F18), applied to the points (x, y)
and (x₁, y₁) = (y_Q, x_Q). It is checked on 3367: (15, −2) and (−9, 16) give (−33, 34). By Lemma 6, **3 | Δ for every pair of representations**.

**Item 11 therefore reduces to:** for P and Q on a common line through a third representation, the chord's
numerators are prime to 3, so the 3 in Δ survives reduction. This step is still **OPEN**.
- **Data** (all coprime k ≥ 3 numbers ≤ 10¹⁵): in all 136,672 ordered same-line pairs, min v₃(numerators) = 0,
  while v₃(Δ) ranges from 1 to 8.
- **For other pairs,** the numerators are divisible by 3 in about 85% of cases, cancelling the 3. That is why
  only 52.7% of those chords keep it (F18).
- **Next idea:** use the line relation (Theorem 2's root relations for the three points) to compute the
  numerators mod 3.

---

## Theorem 7 (denominators of D-lines; FINDINGS F30–F31)

**Statement.** Let P₁ = (x₁, y₁) and P₂ = (x₂, y₂) be distinct integer points of x³ + y³ = n on the line
a x + b y = c (a, b coprime, a ≠ b, c ≠ 0), and let R = (x_R, y_R) be the third intersection, with common
denominator D (R = (X/D, Y/D) in lowest terms). Then

  **D divides (b − a)·E**, where E = a² + ab + b².

In particular, if D is even then a and b are both odd.

**Proof.** Substituting y = (c − a x)/b into x³ + y³ = n and multiplying by b³ gives the cubic in x of the setting:

    (b³ − a³) x³ + 3a²c x² − 3ac² x + (c³ − b³ n) = 0,

whose three roots are x₁, x₂, x_R. By Vieta, x₁ + x₂ + x_R = −3a²c / (b³ − a³) = −3a²c / ((b − a) E).
Since x₁ + x₂ is an integer, the denominator of x_R divides (b − a)E. Exchanging the roles of x and y (the line is
b y + a x = c, the cubic in y has leading coefficient a³ − b³), the denominator of y_R also divides (b − a)E.
So D, the lcm of the two denominators, divides (b − a)E.
For the last sentence: a, b coprime, so not both even, and then E = a² + ab + b² is odd (one of the three terms is
odd and the other two even, or all three odd). So an even D needs b − a even, i.e. a and b both odd. ∎

**Checked:** 32 directions (16 of each parity), thousands of D-lines at slope height 120, and 561,055 D-lines
≤ 10¹⁷: no exception (`dline_analyse.py` reports the check).

**Open half of the parity rule (observed, F30–F31):** if a and b are both odd, D is always even (never an odd
divisor of (b − a)E alone, e.g. (1, 3) gives D ∈ {2, 26}, never 13). Not proved.

---

## Theorem 8 (types at 2 and 3; no complete quadrilateral; FINDINGS F35)

**Setting.** n > 0, and the coprime representations of n are integer points P = (x, y) of x³ + y³ = n, where
P and its swap (y, x) are different points of the same representation. For a prime p ∈ {2, 3}, the **p-type** of
P is 0 if p | x and p ∤ y, and 1 if p | y and p ∤ x. Swapping flips the type.
- **When types are defined:** for every representation of n exactly when p = 2 and n is odd (then exactly one
  coordinate is even), or p = 3 and n ≡ ±1 (mod 9). In the latter case one coordinate is divisible by 3, because if
  neither is, then n ≡ 0 or ±2 (mod 9); and coprimality excludes both.

**Lemma 8a.** If P = (x, y) and Q = (x₁, y₁) have opposite p-types, the third point R of the chord PQ is not
p-integral.

*Proof.* The third point is R = ((x₁²y − x²y₁)/d, (xy₁² − x₁y²)/d) with d = xy − x₁y₁. This is the classical
chord formula for the Fermat cubic: X³ + Y³ = n and collinearity reduce to identities given
x³ + y³ = x₁³ + y₁³, and both were verified exactly on all 82,860 point pairs of the catalogue. Say p | x and
p | y₁ (the opposite case is symmetric).
- **The numerator is a p-unit:** x·y₁² is divisible by p and x₁·y² is not, so xy₁² − x₁y² is not divisible by p.
- **The denominator is divisible by p:** both xy and x₁y₁ are, so p | d.

Hence the y-coordinate of R has negative p-adic valuation. ∎

(For p = 2 there is also a conceptual proof. For odd n the plane cubic x³ + y³ = n z³ has good reduction at 2,
and reduction is a homomorphism onto E(F₂) = {(1:1:0), (1:0:1), (0:1:1)} ≅ Z/3, sending the two types to ±g.
Since P + Q + R = 0, opposite types give R ↦ 0 = (1:1:0), that is z ≡ 0 (mod 2).)

**Corollary 8b (lines keep their type).** If p-types are defined, the three points of a collinear integral triple
(as they lie on the line) have the same p-type. Otherwise two of them are opposite, and by 8a the third is not
integral.

**Theorem 8c (no complete quadrilateral).** If n is odd or n ≡ ±1 (mod 9), there are no six distinct coprime
representations of n forming a complete quadrilateral: four lines, each through three of the six, every two lines
meeting in one of them.

*Proof.* We use the group law with zero at the flex (1 : −1 : 0): three points are collinear exactly when they sum
to zero, and −(x, y) = (y, x). The torsion is trivial for curves with integral points of this kind (cube-free part
of n not 1 or 2).
- **Set-up.** Take two lines meeting at representation A: ℓ₁ ∋ A, B, C and ℓ₂ ∋ A, D, E. The other two lines each
  meet ℓ₁ and ℓ₂ in distinct points and meet each other at the sixth point X; label so that ℓ₃ ∋ B, D, X and
  ℓ₄ ∋ C, E, X.
- **Choosing points.** On each line choose the actual collinear points: a + b + c = 0 on ℓ₁, σ_a a + d + e = 0 on
  ℓ₂, σ_b b + σ_d d + x = 0 on ℓ₃, σ_c c + σ_e e + x′ = 0 on ℓ₄, where the σ are ±1 and x′ = ε x (same
  representation X).
- **Signs from types.** Writing τ = ±1 for the type, τ(−P) = −τ(P), and by 8b each line has a single type. That
  forces **σ_b = σ_a σ_d and σ_c = σ_a σ_e.** From ℓ₁ and ℓ₂: d + e = σ_a (b + c).
- **Case σ_a = +1.** Then x = −σ_b(b + d) and x′ = −σ_c(c + e). So c + e = δ(b + d) with δ = ±1.
  - δ = +1: together with b + c = d + e this gives 2(e − b) = 0, so e = b: the same representation.
  - δ = −1: then b + c + d + e = 0 and b + c = d + e, so 2(b + c) = 0, so a = 0.
- **Case σ_a = −1.** Then x = −σ_b(b − d) and x′ = −σ_c(c − e), so c − e = δ(b − d), with b + c = −(d + e).
  - δ = +1: 2(b + e) = 0, so e = −b: the same representation.
  - δ = −1: b + c = d + e = −(b + c), so a = 0.

Every case contradicts distinctness or a ≠ 0. ∎

**Remarks.**
- **The type constraint is essential.** Without it (σ_b = −σ_a σ_d allowed), the configuration x = σ_b(d − b),
  x′ = −x is consistent: it is the A3 root configuration (12 vectors, 6 representations, 4 relations).
- **Data:** for all 69 bowtie five-ways, both candidate sixth points ±(B − E) and ±(B − D) have denominators
  divisible by 2 and by 3 (138 of 138), exactly as 8a predicts. They are chords between points of opposite type at
  both primes.
- **Coverage:** all 72 known coprime five-ways have n odd; of the 6,785 four-ways only 8 (n even, n ≢ ±1 mod 9) lie
  outside the theorem.
- **Why it matters (F35, heuristic):** by the gap principle, six integral points of nearly equal height spanning
  rank 3 must be close to the A3 configuration. So a coprime six-way needs its points to span rank ≥ 4, for example
  a bowtie plus a free point (as the three known "line + 2 free" five-ways span rank 4), or arise by rank.

---

## Theorem 9 (the coordinate sum of a chord's third point; FINDINGS F44)

**Statement.** Let P₁, P₂ be distinct integer points of x³ + y³ = n on the line a x + b y = c (gcd(a, b) = 1), and
let the third intersection be R = (X/D, Y/D) in lowest terms (gcd(X, Y, D) = 1). Then gcd(X, D) = gcd(Y, D) =
gcd(a, D) = gcd(b, D) = 1, and

  **D | X + Y  ⟺  D | b − a.**

So x_R + y_R is an integer exactly when D divides b − a. In a hub, both chords through R therefore agree on
whether D | b − a.

**Proof.** X³ + Y³ = D³n and aX + bY = cD.
- If a prime p divides D and Y, then p | X³ = D³n − Y³, so p | X, contradicting lowest terms. Likewise for X.
- If p | D and p | a, then p | bY = cD − aX; but p ∤ b (gcd(a, b) = 1) and p ∤ Y. Likewise for b.
- Modulo D: a(X + Y) + (b − a)Y ≡ 0. If D | X + Y then (b − a)Y ≡ 0, and Y is a unit, so D | b − a. If D | b − a
  then a(X + Y) ≡ 0, and a is a unit, so D | X + Y. ∎

**Checked:** all 166,228 chords of the catalogue with a non-integral third point.

**Companion:** gcd(X, Y) = 1 as well; see Theorem 10.

---

## Theorem 10 (a chord through two coprime points meets the curve again in a primitive point; FINDINGS F44)

**Statement.** Let P = (x, y) and Q = (u, v) be integer points of x³ + y³ = n, each with coprime coordinates,
on the line a x + b y = c (gcd(a, b) = 1, a ≠ b), and let R = (X/D, Y/D) (lowest terms) be the third
intersection. Then **gcd(X, Y) = 1.** (Coprimality is needed: doubling P and Q, on the curve for 8n, breaks it.)

**Proof.** b ≠ 0, since a vertical line meets the curve in at most one point (Setting). Suppose a prime p divides
X and Y.
1. p ∤ D (lowest terms), so x_R = X/D is p-integral and divisible by p; and p | n, since X³ + Y³ = D³n.
2. p ∤ x and p ∤ u: if p | x then p | y³ = n − x³, against gcd(x, y) = 1.
3. p | c, from aX + bY = cD.
4. Substituting y = (c − a x)/b, the x-coordinates x, u, x_R are the roots of
   L x³ + 3a²c x² − 3ac² x + (c³ − b³n) = 0, with L = b³ − a³ ≠ 0.
5. e₂: xu + x_R(x + u) = −3ac²/L. The left side is a p-unit (xu is a unit, the rest divisible by p), so
   v_p(L) = v_p(3ac²) ≥ 2.
6. p ∤ a: otherwise p ∤ b and L ≡ b³ (mod p) is a unit, against 5.
7. e₁: x + u + x_R = −3a²c/L has valuation v_p(3) + v_p(c) − (v_p(3) + 2v_p(c)) = −v_p(c) < 0, yet the left side
   is p-integral (1, 2). Contradiction. ∎

**Remarks.**
- Only coprimality at p is used, and p³ | n is a consequence, not an assumption.
- With D = 1 it says the third integer point of a line through two coprime integer points is coprime.
- With Theorem 9: every hub point R is a primitive point of D³n, with D | (b − a)E.

**Corollary 10a (integer coordinate sum; explains F30 §1).** If no prime ≡ 1 (mod 3) divides D, then D | X + Y,
and so (Theorem 9) D | b − a for every chord with that third point.
*Proof.* By Theorem 10, (X, Y) is a coprime representation of N = D³n, so Theorem 5 applies to it. For p | D with
p = 2 or p ≡ 2 (mod 3): p ∤ t_R, so v_p(X + Y) = v_p(N) ≥ 3v_p(D). For p = 3: v₃(t_R) ≤ 1, so
v₃(X + Y) ≥ 3v₃(D) − 1 ≥ v₃(D). ∎
Checked on the 7,202 catalogue chords with such D (all have D | X + Y); with a prime ≡ 1 (mod 3) in D, only
2,048 of 25,596 do. F30 had found integer s_R in 33 of 35 hubs, the exceptions having D-primes 7, 43, 103, … .

**Checked:** all 166,228 non-integral chords of the catalogue, and 46,256 chords of every number with ≥ 2
coprime representations with |coordinates| ≤ 4,000 (1,013 of them with a cube factor). Found by mining (F44),
then proved.

---

## Proposition 11 (a cheap proven filter on pairs: the non-split part of s; FINDINGS F45)

**Statement.** Let n > 0 have a coprime representation (x, y), s = x + y, and let f be the part of s made of
primes p ≢ 1 (mod 3) (with its full power). If n has at least k coprime representations, then

  **m_k · f ≤ (4n)^{1/3}**,  where m_4 = 19, m_5 = 31, m_6 = 37

are the k-th smallest products of distinct prime powers of primes ≡ 1 (mod 3) (1, 7, 13, 19, 31, 37, …).

**Proof.** By Theorem 5, every prime p ≢ 1 (mod 3) dividing n divides every s_i = x_i + y_i to the same power
(v_p(n) for p ≠ 3, v₃(n) − 1 for p = 3), and a prime p ≡ 1 (mod 3) divides s_i to power 0 or v_p(n). So every
s_i = f · m_i with m_i a product of distinct blocks p^{v_p(n)}, p ≡ 1 (mod 3), and f is the same for all
representations. Distinct representations have distinct s_i (s determines t = n/s and then {x, y}). And
s_i³ ≤ 4n, since t_i = (s_i² + 3(x_i − y_i)²)/4 ≥ s_i²/4. So k representations need k distinct values f·m_i ≤ (4n)^{1/3},
the largest of which is at least f·m_k. ∎

**Use.** Every pair of the same n has the same f, so a search may drop every pair with m_k f > (4n)^{1/3} and still
find every n with ≥ k representations: exhaustive for k ≥ 4 (m = 19) or k ≥ 6 (m = 37). Mod 2 is the special case
p = 2: an even n puts all its 2s into f.

**Checked:** none of the 36,122 representation pairs of the catalogue's four- and five-ways is cut at its own level.
Cut on census pairs at 2·10²³: 27% (k ≥ 6), 24% (k ≥ 4); differences (row d = s, so a whole row at once) 23% / 20%,
sums 33% / 31%.

---

## Theorem 12 (even n has no lines; FINDINGS F45)

**Statement.** If n is even, no line contains three distinct coprime points of x³ + y³ = n (representations or
their swaps). So every multi-way with n even is a hub or "independent" (rank).

**Proof.** n even and gcd(x, y) = 1 force x ≡ y ≡ 1 (mod 2) at every point. Suppose a x + b y = c holds three of
them. By Theorem 1(b) a·b is even, and gcd(a, b) = 1, so exactly one of a, b is even.
- a even: L = b³ − a³ is odd, and e₁ = x₁ + x₂ + x₃ = −3a²c/L is even; but it is a sum of three odd numbers.
- b even: the same with the y-coordinates (the line is b y + a x = c, e₁(y) = −3b²c/(a³ − b³)). ∎

**Checked:** 524 even n with k ≥ 3 (all three-ways 1e17 – 1e19 and the catalogue): no collinear triple. Odd n: 97% of
253,395 have one.

**Consequence.** Lines are the commonest source of extra representations (8,393 of 8,928 four-ways are line + free),
and even n cannot use them. This is why even n are 33% of ordinary sums but 0.7% of four-ways (12 of 1,736 below
2.5e23, all hubs), 0.2% of three-ways and 0 of 82 five-ways: a mechanism, not just a smaller local density. A six-way
with n even would have to come from hubs and rank alone.

---

## Theorem 13 (the s-cubic of a line; a line's direction fixes the non-split part of n; FINDINGS F46)

**Statement.** Let three points (xᵢ, yᵢ) of x³ + y³ = n lie on a x + b y = c (gcd(a, b) = 1, b ≠ 0, a ≠ b), and put
sᵢ = xᵢ + yᵢ, E = a² + ab + b². Then

  **E·Σsᵢ = 3c(a + b),  E·Σ_{i<j} sᵢsⱼ = 3c²,  E·s₁s₂s₃ = (a − b)²·n,**

i.e. the sᵢ are the roots of E z³ − 3c(a + b) z² + 3c² z − (a − b)² n.

*Proof.* On the line c = a xᵢ + b yᵢ = (a − b)xᵢ + b sᵢ, so xᵢ = (c − b sᵢ)/(a − b). Substitute into Vieta for the
x-cubic L x³ + 3a²c x² − 3ac² x + (c³ − b³n) (L = (b − a)E): e₁ gives the first identity; e₂ with the first gives
b²Eσ₂ = 3b²c², the second; e₃ with both gives −b³Eσ₃ = −b³(a − b)²n, the third. ∎

**Corollary 13a (the direction fixes the non-split part).** If the three points are coprime, then for every prime
p ≢ 1 (mod 3): **v_p(b − a) = v_p(sᵢ)** for each i, and p^{v_p(sᵢ)} | c. So the non-split part of b − a is the
non-split part of every s on the line, which is the non-split part f of n (Theorem 5: v_p(n) for p ≡ 2 mod 3,
v₃(n) − 1 for p = 3).
*Proof.* p ∤ E for p ≡ 2 (mod 3) (E is a norm from Z[ω]); for p = 3, v₃(E) = 1 if 3 | a − b, else 0. All sᵢ have
the same valuation e' (Theorem 5), so the third identity gives 2v_p(a − b) + v_p(n) − v_p(E) = 3e'. For p ≡ 2 (mod 3)
(e' = v_p(n)): v_p(b − a) = e'. For p = 3:
- 3 | n (so v₃(n) ≥ 2, e' = v₃(n) − 1 ≥ 1): if 3 ∤ b − a then v₃(E) = 0 and v₃(n) = 3v₃(n) − 3, i.e. 2v₃(n) = 3,
  impossible; so 3 | b − a, v₃(E) = 1, and 2v₃(b − a) + v₃(n) − 1 = 3v₃(n) − 3 gives v₃(b − a) = v₃(n) − 1 = e'.
- 3 ∤ n (e' = 0): if 3 | b − a then v₃(E) = 1 and 2v₃(b − a) − 1 = 0, impossible by parity; so v₃(b − a) = 0 = e'.
The second identity gives v_p(c) ≥ e' (2v_p(c) + v_p(3) − v_p(E) ≥ 2e'). ∎

**Corollary 13b (Theorem 12 again).** For p = 2: 2 | n would force 2 | b − a, so a, b both odd, against Theorem 1(b).

**Checked:** the three identities on all 492,028 lines of the catalogue and of every three-way 1e17 – 1e19;
nonsplit(b − a) = nonsplit(s) on all of them; v_p(b − a) = e' exactly in all 366,672 (line, p) cases.

**Consequences.**
- n's non-split part is set by the direction alone: a line in direction (a, b) only produces n whose primes
  ≢ 1 (mod 3) are those of b − a, with those exponents (3: one more). With Proposition 11, directions whose b − a has a
  large non-split part f can only make n with few representations (k ≥ 6 needs 37 f ≤ (4n)^{1/3}).
- b − a is odd for every line (Theorem 1(b)), so lines give odd n only.
- Split primes (p ≡ 1 mod 3) carry no such rule (F46 table).

---

## Theorem 14 (every chord: the non-split part of n divides b − a; FINDINGS F46)

**Statement.** Let P₁ = (x₁, y₁) and P₂ = (x₂, y₂) be coprime integer points of x³ + y³ = n with P₂ ≠ P₁ and P₂ not
the swap of P₁, and let a x + b y = c be the chord through them (gcd(a, b) = 1). For every prime p ≢ 1 (mod 3),

  **v_p(b − a) ≥ v_p(s)**, and **v₂(b − a) ≥ v₂(s) + 1**,

where s = x₁ + y₁ (all representations share v_p(s): v_p(n) for p ≠ 3, v₃(n) − 1 for p = 3; Theorem 5). So the
non-split part of n (3: one power less; 2: one more) divides b − a for **every pair** of representations; lines
(Theorem 13a) are the case of equality.

**Proof.** Put δ = x₂ − x₁, ε = y₂ − y₁, g = gcd(δ, ε), s₁ = s, s₂ = x₂ + y₂. The direction is (a, b) = ±(ε, −δ)/g,
so **b − a = ±(s₁ − s₂)/g**. Expanding x₂³ + y₂³ = x₁³ + y₁³ gives the exact identity (checked in PARI)

  (s₂ − s₁) · B = 3 s₁ ε (2x₁ − s₁ − ε),  B = 3x₁² + 3x₁(δ − ε) + δ² − δε + ε².

Let e = v_p(s₁) = v_p(s₂) ≥ 0 (if p ∤ n there is nothing to prove except at p = 2, where n is then odd and the claim
is v₂(b − a) ≥ 1 only if 2 | n; for odd n read the bound as v₂ ≥ 0). If p ∤ g, then v_p(b − a) = v_p(s₁ − s₂) ≥ e,
and at p = 2 (n even, every point has both coordinates odd, so δ and ε are even, so 2 | g) this case does not occur.
If p | g, then p | δ and p | ε, and p ∤ x₁ (coprimality, since p | n when e ≥ 1):
- p ≥ 5: B ≡ 3x₁² is a unit and 2x₁ − s₁ − ε ≡ 2x₁ is a unit, so v_p(s₂ − s₁) = e + v_p(ε). The same identity with the
  roles of x and y exchanged gives v_p(s₂ − s₁) = e + v_p(δ). Hence v_p(g) = min(v_p δ, v_p ε) = v_p(s₁ − s₂) − e and
  **v_p(b − a) = e** exactly.
- p = 3: v₃(B) = 1 (3x₁² has valuation 1, the rest is divisible by 9), and 2x₁ − s₁ − ε is a unit, so the 3 on the
  right cancels B's and again v₃(b − a) = e.
- p = 2: B is odd and 2x₁ − s₁ − ε is even, so v₂(s₂ − s₁) ≥ e + v₂(ε) + 1, likewise with δ: v₂(b − a) ≥ e + 1. ∎

**Corollary 14a (s-denominator).** For a chord whose third point R is not integral, s_R = 3c(a + b)/E − s₁ − s₂
(Theorem 13's first identity), so the denominator of x_R + y_R divides E.

**Corollary 14b (hub matching rule).** If chords (a, b; P₁, P₂) and (a′, b′; P₃, P₄) meet at the same R, then from
Theorem 13's third identity (a − b)² E′ s₃ s₄ = (a′ − b′)² E s₁ s₂.

**Checked:** Theorem 14 on all 3,158,936 pairs of points of the catalogue and of every three-way 1e17 – 1e19
(`thm14_check.py`); 14a on all 166,228 non-integral chords; 14b on all 3,298 hub chord pairs; the s-cubic identities
on all 166,228 non-integral chords as well as the 492,028 lines.

---

## Lemma 15 (the S-forms of a direction are definite; the height bound of the complete line search, F47)

**Statement.** Fix a direction (a, b), a != b, a b > 0 (Theorem 1), the conic point P0 of line_enum, and the raw points
(b p_i, T - a p_i) of slope (s, r) (line_enum.chord_points; T = Z D Q, Q = s^2 + s r + r^2, D = b^3 - a^3). Each
S_i(s, r) = b p_i + T - a p_i (the x + y of raw point i) is a **definite** binary quadratic form.

**Proof.** The raw coordinates are binary forms with integer coefficients, and two identities hold for all rational
(s, r), hence as polynomial identities, hence for all real (s, r): the three raw points lie on one curve
x^3 + y^3 = n_raw(s, r), and n_raw = E S1 S2 S3 / (a - b)^2 (Theorem 13). Suppose S_i(s, r) = 0 for some real
(s, r) != (0, 0). Then n_raw = 0, so every raw point satisfies x^3 + y^3 = 0, i.e. x = -y over R: all three lie on
x + y = 0. They also lie on a x + b y = b T with T != 0 (Q is definite, Z, D != 0). Two distinct lines (a != b) meet in
one point, so the three points coincide, i.e. u1 = u2 = u3 = s0/3, and by Theorem 4 (ii) the conic point is
(X, Y) = (D s0/3 + a^2, D s0/3 + a^2) = (0, 0). But X^2 + X Y + Y^2 = 3 a b^3 > 0 (a b > 0). So S_i has no real zero
besides (0, 0): it is definite. QED

**Consequence (the height bound).** M := min |S1 S2 S3| over max(|s|, |r|) = 1 is positive, and for a slope of
height h whose gcd is G, n = E S1 S2 S3 / ((a - b)^2 G^3) >= E M h^6 / ((a - b)^2 G^3). So n <= B forces
h <= H(G) = (B (a - b)^2 G^3 / (E M))^(1/6), the bound line_complete / line_fast enumerate to. M is certified exactly
(Sturm sequences, `certify_M.py`).

**Certificate (6 November 2026, `verify_gp/certify_M_all.log`):** for all 1,563,877 allowed directions of cost
<= 1.2e12, |S1 S2 S3| >= M_cert = M (1 - 1e-12) on the three edges of the half-square (PARI polsturm: no root, positive
at the end point), and for both run bounds (int(1e30) and int(1e33) = 999999999999999945575230987042816) and every
G-level the integer height used covers every integer h <= H(G, M_cert) (exact rationals). The first pass used a
too-strict test (used >= H rather than used >= floor H) and flagged 6 (direction, G) pairs in 4 near-diagonal
directions at the 1e33 bound whose H(G, M_cert) exceeded the used integer by < 1e-3; all pass the correct test.

(Observed and not needed: disc(S_i) = -3 k^2 for an integer k, the same for the three forms.)

---

## Theorem 16 (infinitely many n with at least five coprime representations; FINDINGS F69) -- 8 Nov 2026, for review

**Setting (F53, F58).** Fix a base direction (a, b) (Theorem 1), its conic point, a second direction (a2, b2)
(gcd(a2, b2) = 1, a2 != b2) and an index i in {1, 2, 3}. Put E1 = a^2 + ab + b^2, A = b2^3 - a2^3 = (b2 - a2) E2,
E2 = a2^2 + a2 b2 + b2^2, and N = (b - a) E1 A.
- A primitive slope (s, r) gives the raw triple (three integer points, binary forms in (s, r), Lemma 15) on a line of
  direction (a, b). Divide all six coordinates by their gcd G: points P1, P2, P3 = (x_j, y_j), integers, not all six
  divisible by any prime, on x^3 + y^3 = n with n = x_1^3 + y_1^3.
- Line 2 through the shared point (x, y) = P_i: (x + t b2, y - t a2). On the curve, t = 0 or
  A t^2 + B t + C = 0, B = 3(x b2^2 + y a2^2), C = 3(x^2 b2 - y^2 a2) (F58.2). Its two further points are rational
  exactly when B^2 - 4AC = w^2: the rational points (s, r, w) of the genus-1 curve C_{pair}: w^2 = Delta(s, r).
- (s, r, w) is a **bowtie** if P1, P2, P3 and the two line-2 points X_+-, Y_+- are integral, coprime, and the five
  are distinct representations.

**Lemma 16a (base triple).** If some P_j is not coprime at a prime p, then p | (b - a) E1.
*Proof.* Say p | x_1, y_1. Since not all six coordinates are divisible by p, some P_k (k != 1) has a coordinate
prime to p, and then (as x_k^3 + y_k^3 = n) both are. p^3 | n, and p | c where a x + b y = c is the line
(c = a x_1 + b y_1). So a x_k + b y_k = 0 and x_k^3 + y_k^3 = 0 mod p. If p | b, then p does not divide a, so
p | x_k, then p | y_k: contradiction. Otherwise y_k = -a x_k / b, so x_k^3 (b^3 - a^3) / b^3 = 0 mod p, and p does not
divide x_k: p | b^3 - a^3 = (b - a) E1. QED

**Lemma 16b (line 2 integral; F58.2).** If (s, r, w) is a rational point and P_i is an integer point, the line-2 points
are integral at every prime p not dividing A.
*Proof.* The roots t of A t^2 + B t + C are rational; for p not dividing A, t^2 + (B/A) t + C/A has p-integral
coefficients, so both roots are p-integral (a rational root of a monic p-integral polynomial is p-integral). Then
x + t b2 and y - t a2 are p-integral. QED

**Lemma 16c (line 2 coprime).** If P_i is coprime and X = x + t b2, Y = y - t a2 are integers, then gcd(X, Y) has no
prime factor outside A.
*Proof.* Let p | X, Y. If p | t, then p | x and p | y: impossible. So t is a unit mod p, and (x, y) = t (-b2, a2) mod
p, hence n = x^3 + y^3 = t^3 (a2^3 - b2^3) = -t^3 A mod p. But p^3 | X^3 + Y^3 = n, so p | A. QED

**Corollary 16d (only N matters).** For every rational point of C_{pair} (outside finitely many degenerate points),
every failure to be a bowtie other than distinctness happens at a prime dividing N.
*Proof.* 16a at primes not dividing (b - a) E1 makes P1, P2, P3 coprime (so P_i is); then 16b and 16c at primes not
dividing A. QED
- **Data:** on (3,4)+(9,52) (N's primes 37, 43, 3253) every failure among 726 test points is at one of these (F69).

**Lemma 16f (the quartic Delta; TO DO item 1).** Let (X_i(s, r), Y_i(s, r)) be the raw point i of the base line
(binary quadratic forms with integer coefficients, from `line_enum.chord_points`: Q = s^2 + sr + r^2, the p_i and
T = Z D Q all have degree 2). Put
    B~ = 3(X_i b2^2 + Y_i a2^2),   C~ = 3(X_i^2 b2 - Y_i^2 a2),   A = b2^3 - a2^3,   Delta = B~^2 - 4 A C~.
Then Delta is a binary quartic form with integer coefficients, and for a primitive (s, r) with base point
P_i = (X_i, Y_i)/g on x^3 + y^3 = n:
1. the points of line 2 through P_i on the curve are P_i (t = 0) and the roots of A t^2 + B t + C = 0, where
   B = B~/g and C = C~/g^2;
2. its other two points are rational if and only if Delta(s, r) is the square of a rational (equivalently, of an
   integer) number.
*Proof.* Expanding, (x + t b2)^3 + (y - t a2)^3 - x^3 - y^3 = t (A t^2 + B t + C) with B = 3(x b2^2 + y a2^2) and
C = 3(x^2 b2 - y^2 a2) (an identity in x, y, t, a2, b2; checked symbolically in PARI). With (x, y) = (X_i, Y_i)/g, B and
C are B~/g and C~/g^2, so the discriminant B^2 - 4AC = Delta(s, r)/g^2. A quadratic with rational coefficients and A != 0
has rational roots iff its discriminant is a rational square; Delta(s, r) is an integer, and an integer that is a
rational square is an integer square. Degree: B~ has degree 2 and C~ degree 4 in (s, r), so Delta is a quartic form.
QED
- *Code:* `bowtie_mine.Curve` sets q = 9 t1^2 - 12 A t2 with t1 = X b2^2 + Y a2^2 and t2 = X^2 b2 - Y^2 a2 (raw
  coordinates at s = 1), which is exactly Delta(1, r); the identity q = B~^2 - 4AC~ was also checked symbolically.
  C_{pair} is defined as w^2 = Delta(s, r), so its rational points are exactly the slopes with rational line-2 points.

**Lemma 16g (finite fibres; TO DO item 2).** The map from rational points (s, r, w) of C_{pair} to the unordered base
triple {P1, P2, P3} has fibres of at most 12 points.
*Proof.* By Theorem 4 (i), reduced slopes (s, r) correspond one-to-one with the rational points P != P0 of the conic
(3) (P0 itself comes from the single tangent slope, which gives no triple). By Theorem 4 (ii), points of (3)
correspond one-to-one with ordered triples (u1, u2, u3), u = x/c; and by Theorem 4 (iii) the coprime triple
determines (u1, u2, u3) up to order (u = x/c does not change when the triple is scaled by +-1). An unordered triple has
at most 6 orderings, so at most 6 slopes; each slope gives at most two points (s, r, +-w). QED
- *Used in Theorem 16 step 5:* each n has finitely many representations, hence finitely many possible base triples,
  hence (16g) finitely many points of K mapping to it.

**Lemma 16e (openness at p | N).** Let P0 be a bowtie on C_{pair}. For each prime p there is an open neighbourhood
U_p of P0 in C_{pair}(Q_p) such that every rational point in U_p is integral and coprime at p (all five points).

*Set-up.* C_{pair} is the curve w^2 = Delta(s, r) in weighted projective space P(1, 1, 2), with Delta a binary quartic
form with integer coefficients, squarefree with nonzero discriminant (checked for the instance below: irreducible,
disc != 0), so C_{pair} is smooth of genus 1. **Delta is exactly the discriminant of line 2 computed from raw
coordinates** (Lemma 16f).
A point of C_{pair}(Q_p) has a representative (s, r, w) with (s, r) in Z_p^2 primitive and w in Z_p (w^2 = Delta(s, r)
is p-integral); the representative is unique up to (s, r, w) -> (u s, u r, u^2 w), u in Z_p^*.

*The quantities.* For a representative (s, r, w) put, with g = G(s, r) the gcd of the six raw coordinates
(for rational (s, r)) and tau_{+-} = (-B~ +- w) / (2A):
- base points: P_j = R_j(s, r) / g, R_j the raw point j (j = 1, 2, 3);
- line-2 points: Q_{+-} = (X_i + tau_{+-} b2, Y_i - tau_{+-} a2) / g.
(Indeed with x = X_i/g the quadratic of F58.2 has roots t = tau/g, so x + t b2 = (X_i + tau b2)/g.)
"Integral and coprime at p" for all five points means, for each of the five numerator pairs (U, V) -- R_j, or
(X_i + tau b2, Y_i - tau a2) --
    v_p(U) >= v_p(g), v_p(V) >= v_p(g), and min(v_p(U), v_p(V)) = v_p(g).                         (*)
For rational (s, r) primitive in Z^2, v_p(g) = min over the six raw coordinates of v_p: the p-part of g is
determined by the raw coordinates alone. **Invariance:** a rational point's primitive integer representative and any
Z_p-primitive representative differ by a unit u in Z_p^*. The raw coordinates are binary forms of degree d = 2, so
B~ has degree d, C~ degree 2d, Delta = B~^2 - 4AC~ degree 2d = 4, and (s, r, w) -> (u s, u r, u^d w). Then tau_{+-}
and the line-2 numerators X_i + tau b2, Y_i - tau a2 all scale by u^d, as do the raw coordinates. Multiplying by the
unit u^d changes no valuation, so every valuation in (*) can be computed from any Z_p-primitive representative.

*Proof.* Fix a representative (s0, r0, w0) of P0. Since P0's two line-2 points are distinct, w0 != 0. Since P0 is a
bowtie, all ten coordinates of its five points are nonzero; so the six raw coordinates at (s0, r0) and the four
numerators X_i + tau b2, Y_i - tau a2 at (s0, r0, w0) are nonzero p-adic numbers. Let V be the largest of their
p-adic valuations and of v_p(w0), and fix m > V + v_p(4 A) + 2 v_p(w0) + 1.
Let U_p be the set of points of C_{pair}(Q_p) having a representative (s, r, w) with
(s, r) = (s0, r0) mod p^m and w = w0 mod p^m. This is open, and contains P0.
At such a representative, every raw coordinate (a form with integer coefficients) is congruent mod p^m to its value
at (s0, r0); as m exceeds its valuation, the valuation is unchanged. So the six raw valuations, and v_p(g), are those
of P0. Likewise B~ = B~(s0, r0) mod p^m and w = w0 mod p^m, so tau_{+-} = tau_{+-}(P0) mod p^{m - v_p(2A)}, and each
numerator X_i + tau b2, Y_i - tau a2 is congruent to its P0-value modulo p^{m - v_p(2A)}, with m - v_p(2A) > V:
again the valuations are unchanged. Hence (*) holds at every point of U_p exactly as at P0, where it holds.
(The choice of sign of w is consistent on U_p: w = w0 mod p^m with m > v_p(w0) excludes w = -w0. Swapping the sign
only swaps Q_+ and Q_-, and (*) is symmetric anyway.) QED

**Theorem 16.** Suppose C_{pair} has a bowtie P0 and the elliptic curve E = (C_{pair}, P0) has positive rank. Then
infinitely many n have at least five coprime representations as x^3 + y^3 (so at least four).
*Proof.*
1. *Topology.* An isomorphism of curves over Q between C_{pair} and a Weierstrass model, sending P0 to O, is a
   homeomorphism on Q_p-points (a morphism of varieties over Q_p is continuous for the p-adic topology on Q_p-points,
   and so is its inverse; e.g. Poonen, *Rational Points on Varieties*, Section 2.5, or Silverman AEC VII), and the
   group law, being given by morphisms, is continuous. Let N be as in the Setting; for each p | N take U_p
   from 16e. On a minimal Weierstrass model at p, the subgroups E_k(Q_p) = {P : v_p(x(P)) <= -2k} + {O} (k >= 1) form a
   basis of open neighbourhoods of O (Silverman, AEC VII.2-3). So there is k_p with E_{k_p}(Q_p) contained in (the
   image of) U_p.
2. *Finite index.* Let K = E(Q) intersected with E_{k_p}(Q_p) for every p | N. Each quotient E(Q_p)/E_k(Q_p) is finite
   (E/E_0 finite by the Neron model, E_0/E_1 = nonsingular points of the reduction, E_j/E_{j+1} = F_p), and E(Q)/K
   injects into their product. So K has finite index in E(Q); since rank E(Q) >= 1, K is infinite.
3. *Every point of K is good at every prime.* At p | N: points of K lie in U_p, so all five points are integral and
   coprime at p (16e). At p not dividing N: Corollary 16d.
4. *Degeneracies.* The conditions "two of the five points are the same representation ((x, y) ~ (y, x))" and "some
   coordinate is 0" are polynomial conditions in (s, r, w): Zariski-closed subsets of the irreducible curve C_{pair}.
   They are proper (P0 satisfies none), hence finite. Removing them leaves infinitely many points of K, each a bowtie:
   five distinct coprime representations of its n.
5. *Infinitely many n.* Each n != 0 has finitely many representations, hence finitely many bowties (five-element sets
   of its representations with the line structure). A bowtie determines its base triple, and by Lemma 16g each base
   triple comes from at most 12 points of C_{pair}. So each n arises from finitely many points of K, and K, being
   infinite, gives infinitely many n. QED

**Instance (F69).** (a, b, i, a2, b2) = (3, 4, 1, 9, 52) (i = 1 is code index 0), P0 = Bernstein's
506433677359393, rank 5, torsion Z/2, N's primes 37, 43, 3253. Numerically k = 1 works at 37 and 43 within 2E(Q):
all 38 points of 2E(Q) n E_1(Q_37) n E_1(Q_43) with |c_k| <= 4 are bowties, and the multiples j c,
c = (0, 1, 1, -2, -2), j = 1..10 (n of 1,260 to 129,340 digits).

**Checks for the instance (8 Nov):** Delta irreducible, disc(Delta) != 0 (genus 1, irreducible); Delta = B~^2 - 4AC~
on raw coordinates (ratio 1 at six slopes); torsion Z/2 (PARI elltors), so each of the five generators (canonical
heights 5.5 - 18.9, regulator 75,786) has infinite order: rank >= 1 (indeed >= 5).
Literature: no prior infinitude result for coprime >= 3-, 4- or 5-ways found (UlasPaperPlan A0d).

**TO DO before Theorem 16 goes into the paper (open, 8 Nov 2026):**
1. ~~**Delta = B~^2 - 4AC~ as forms.**~~ **Done (9 Nov): Lemma 16f** (the substitution identity, checked symbolically;
   Delta is the code's q by definition).
2. ~~**The count in step 5.**~~ **Done (9 Nov): Lemma 16g** (at most 12 points per base triple, from Theorem 4).
3. ~~**Continuity in step 1.**~~ **Done (9 Nov):** step 1 now states it with a reference (Poonen, *Rational Points on
   Varieties* 2.5; Silverman AEC VII). Check the exact section numbers against the books before citing.
4. **Independent read.** Have someone other than the author of this draft check 16a-16e and the five steps.

---

## Toolkit for triangles (six-ways from three lines; FINDINGS F67-F68) -- 8 Nov 2026

A **triangle** is three lines, each through three coprime representations of n, every two lines sharing one of them
(the corner). It has six distinct representations: a six-way. A bowtie is a triangle missing one side. In the group
law with the flex at infinity as zero (collinear <=> sum 0, -(x, y) = (y, x)), corners a, b, c give third points
-(sigma a + sigma' b) etc. for suitable signs.

## Lemma 17 (the class of a representation; lines never change class)

**Setting.** n odd and n = +-1 (mod 9), so that both the 2-type and the 3-type of Theorem 8 are defined for every
coprime point. Write tau_p(P) = +1 if p | x, -1 if p | y (P = (x, y), p in {2, 3}).

**Definition.** mu(P) = tau_2(P) tau_3(P): mu = +1 if the even coordinate of P is also the one divisible by 3, and
-1 otherwise. Swapping x and y flips both types, so mu(y, x) = mu(x, y): **mu is a property of the representation**
{x, y}, its *class*.

**Statement.** The three representations on any line have the same class. Hence all representations in a connected
configuration of lines (a bowtie, a triangle, any chain of lines sharing points) lie in one class.

*Proof.* By Corollary 8b (at p = 2 and at p = 3), the three points of the line, as they lie on it, have one 2-type
and one 3-type. So mu, the product, is constant on the line; and mu does not depend on which of P, swap(P) lies on
the line. A chain of lines sharing points then propagates the class. QED

**Consequences for triangles.**
- A triangle six-way of n has its six representations in one class, so that class must contain at least six of
  n's representations. A bowtie fixes the class of any sixth representation that would complete it to a triangle:
  representations of n in the other class can never complete it.
- Unlike the complete quadrilateral (Theorem 8c), classes do not forbid triangles; they restrict which
  representations can play a part.

**Checked (8 Nov):** all 18,653 numbers of the catalogue and results/five_ways_all.txt with n odd and n = +-1 mod 9:
**0 of 19,938 lines** contain two classes; **7,887 numbers have representations in both classes** (10,766 in one
class only). Relation to Lemma 6 (all representations share xy mod 3): Lemma 6 is about 3 | x y vs not, uniform
over n; Lemma 17 compares which coordinate carries the 2 and the 3, and genuinely varies within n.

## Lemma 18 (lines of the same n have compatible directions)

**Statement.** Let a x + b y = c and a' x + b' y = c' be two lines, each through three coprime representations of
the same n (gcd(a, b) = gcd(a', b') = 1, a != b, a' != b'). Then
1. **nonsplit(b - a) = nonsplit(b' - a')**, where nonsplit(m) = product of p^{v_p(m)} over primes p not = 1 (mod 3);
   both equal f(n), the non-split part of n (with one power of 3 fewer: Theorem 5's convention);
2. **E | n and E' | n** (E = a^2 + ab + b^2), so lcm(E, E') | n;
3. b - a and b' - a' are odd and n is odd (Theorem 1(b), Theorem 12).
For a triangle all three sides satisfy 1-3 pairwise: nonsplit(b_1 - a_1) = nonsplit(b_2 - a_2) = nonsplit(b_3 - a_3)
and lcm(E_1, E_2, E_3) | n.

*Proof.* 1 is Corollary 13a applied to each line: the non-split part of b - a is the non-split part f of n, which
depends only on n. 2 is Theorem 2 for each line. 3 is Theorem 1(b) and Theorem 12. QED

**Consequences.**
- This sharpens the direction-pair filter of F58.4 (every non-split prime of b2 - a2 divides b - a and vice versa)
  to **equality of the non-split parts, exponents included**.
- For a triangle search over direction triples: group directions by nonsplit(b - a) and only form triples within a
  group; and n is at least lcm(E_1, E_2, E_3) times the cube-free constraints of Theorem 13.
- For a bowtie curve with base (a, b) and second direction (a2, b2): any third side through two of its points must
  have nonsplit(b3 - a3) = nonsplit(b - a), and E_3 | n.

**Checked (8 Nov):** all 1,752 five-ways of results/five_ways_all.txt with at least two lines: the lines agree on
nonsplit(b - a) in every case, and every line's E divides n (Corollary 13a was already checked on 492,028 lines).

---

## Lemma 19 (a chord's E outside n goes into the denominator; FINDINGS F72)

**Statement.** Let P, Q be coprime integer points of x^3 + y^3 = n, not on a common known line, with chord
a x + b y = c (gcd(a, b) = 1, a != b), and third point R = (X/D, Y/D) in lowest terms. For every prime p != 3
dividing E = a^2 + ab + b^2 but not n: v_p(E) <= v_p(D). (So the part of E coprime to 3n divides D.)
*Proof.* Theorem 13's identities are Vieta for the line's cubic and hold for a rational third root as well; with
s_R = (X + Y)/D the third reads E s_P s_Q (X + Y) = (a - b)^2 n D. Let p != 3, p | E, p not dividing n.
- p does not divide s_P or s_Q: they divide n (n = s t).
- p does not divide a - b: E = (a - b)^2 + 3ab, so p | E and p | a - b give p | 3ab, so p | a or p | b, and then
  p | a and p | b (as p | a - b): against gcd(a, b) = 1.
Comparing p-adic valuations: v_p(E) + v_p(X + Y) = v_p(D), and v_p(X + Y) >= 0. QED
- *p = 3:* 3 | E exactly when 3 | a - b, so the argument above does not apply; the data say the statement holds at 3 as
  well (to prove separately).
**Checked:** all 487,554 chords of the catalogue four-ways and the five-ways (F72): the part of E coprime to n always
divides D.

**Toolkit, observations (F74, not yet lemmas):**
- Any three representations of n not on a line are the corners of a rational triangle; a triangle six-way = three
  representations whose three chord third points are integral.
- Ladder by integral points j among the six: bowties are j = 5 triangles; line + free point four-ways give j = 4.
- With allowed side directions (4 | ab) every third point is 2-integral (Theorem 8's 2-adic rule): no even denominator
  among the 88 rational triangles of the 150-direction scan.

## Proposition 20 (six-ways are finite for each fixed set of chord directions; FINDINGS F86) -- 10 Nov 2026, draft

**Setting.** A *configuration* is a finite set of points of x^3 + y^3 = n (n free) with prescribed incidences: some
triples collinear (lines) and some pairs joined by chords in prescribed primitive directions d = (a, b). Rational
configurations are taken up to scaling (any rational configuration scales to an integral one), so a configuration is
determined by one point P up to scaling, (x : y) in P^1, and by square roots.

**Lemma 20a (branch form).** For a point P = (x, y) and a direction d = (a, b) with b^3 != a^3, the points
Q = P + lambda (b, -a) != P on the curve of P are the roots of A lambda^2 + B lambda + C = 0 (A = b^3 - a^3,
B = 3(x b^2 + y a^2), C = 3(x^2 b - y^2 a); Lemma 16f), and they are rational iff
    Delta_d(x, y) = 3 [b(4a^3 - b^3) x^2 + 6 a^2 b^2 x y + a(4b^3 - a^3) y^2]
is a rational square. The bracket has discriminant 16 ab (b^3 - a^3)^2, so for ab > 0 its two roots are real, distinct
and conjugate in Q(sqrt(ab)). (Identities checked symbolically, `shapes/delta_form.gp`.) A line through P in direction
d gives both roots, i.e. two points for one square condition.

**Lemma 20b (stars).** For m directions from one point P with pairwise distinct branch points (no two Delta's share a
root), the curve w_i^2 = Delta_{d_i}(x, y) (i = 1..m) over P^1 is irreducible (the Delta's are independent modulo
squares) and, by Riemann-Hurwitz for a (Z/2)^m cover branched simply over 2m points, has genus
    g = 1 + 2^(m-1) (m - 2):   0, 1, 5, 17, 49 for m = 1, ..., 5.
- m = 2 with two lines through P is the bowtie curve (genus 1, F53); a line and a chord give "line + free" four-ways.
- **Checked:** branch points distinct on all 2,642 bowties, 21,947 line + free four-ways and 535 no-line four-way stars
  (`shapes/branch_check.py`).
- **When can branch points coincide? (F87)** The resultant of the bracket forms of d1, d2 is (a1 b2 - a2 b1)^2 S(d1, d2)
  for an explicit sextic S. *Both* branch points shared means proportional forms; with t = a/b the coefficient ratios
  give (u - t)(4 + ut(t + u)) = 0, so for allowed directions (t, u > 0) u = t: **distinct allowed directions never share
  both branch points (proved).** One shared branch point is rational, so it needs ab and a'b' both perfect squares;
  S != 0 for all 2,423,301 such pairs with a, b <= 3600 (not proved in general).

**Lemma 20c (two disjoint lines).** Line 1 through P (direction d1), a chord P -> Q (direction d3), line 2 through Q
(direction d2): the first two conditions give a genus-1 curve C13; the third is w2^2 = Delta_{d2}(Q) = alpha + beta w3, a
double cover of C13 branched at the zeros of the norm alpha^2 - beta^2 Delta_{d3}, a quartic form. When the quartic has
four distinct roots, none shared with Delta_{d1} or Delta_{d3}, there are r = 8 branch points and the genus is
1 + r/2 = 5. **Checked:** all 10,626 ordered triples of distinct directions among the 23 lf36 base directions
(`shapes/twolines_cover.gp`).

**Proposition 20.** Fix the incidence pattern of a six-way and all chord directions involved, and assume the branch
points are distinct (Lemmas 20b, 20c; true in every case checked). Then:
1. **bowtie + free point, two disjoint lines, line + three free points, six free points:** the rational configurations
   are the rational points of a curve of genus 5, >= 5, 17, 49 respectively, hence **finite** (Faltings);
2. **complete quadrilateral:** no integral coprime configuration at all (Theorem 8c, with Theorem 12);
3. **triangle:** the rational configurations are the points of the bowtie curve (genus 1; the sixth point, the third
   intersection of the chord through the two outer corners, is automatically rational), so there can be infinitely many
   rational triangles; but the sixth point is integral only where a non-constant function on the bowtie curve takes
   S-integral values (its denominator's primes are not bounded: Lemma 19), so **finitely many integral ones** per curve
   (Siegel). *(Sketch, made concrete for (3,4)+(9,52) in F87: R's denominator comes from Den = x_B y_B - x_C y_C
   (Theorem 8a), a form alpha + beta w; after cancelling the factor it shares with R's numerators, its norm has 6
   distinct roots, so each equation Den = c is a plane curve with >= 3 points at infinity -- finitely many integral
   points (Siegel). Remaining: bound the gcd of the values, not only of the forms.)*

So **for every fixed set of chord directions, there are only finitely many six-ways of each shape.** This does not bound
the number of six-ways overall: directions are unbounded (F85: chord direction coefficients grow about as n^0.19).

**Status.** 20a: proved (identities). 20b: proved given distinct branch points (a checkable condition). 20c: genus
proved given the stated root conditions, checked for the 23 base directions; the general case needs the quartic's
discriminant as a polynomial in the directions. Part 3: sketch. Faltings' theorem is ineffective: finiteness, not a list.

## Already proved in TOPROVE.md (to be copied here in full later)

- **Item 4:** no three positive points are collinear (convexity).
- **Item 7:** the (3k², 3k² + 1) family (a polynomial identity).
