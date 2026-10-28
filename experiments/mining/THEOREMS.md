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

## Already proved in TOPROVE.md (to be copied here in full later)

- **Item 4:** no three positive points are collinear (convexity).
- **Item 7:** the (3k², 3k² + 1) family (a polynomial identity).
