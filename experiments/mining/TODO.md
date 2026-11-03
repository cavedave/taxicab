# Proof TODO (experimental phase first; nothing here is proved yet)

1. If p ≢ 1 (mod 3) and p | n, then p | s = x + y for every coprime representation n = x³ + y³. Handle
   p = 3 and its exponents separately. Holds in 100% of about 50,000 cases (F1).
2. The density of 7 | n among coprime sums is 3/8 (cubes mod 7). Elementary; write it down.
3. The ratio of 3-adic local densities is 2:1 for n ≡ ±1 against n ≡ ±2 (mod 9). Check it, and the
   9- and 27-adic structure behind the 3 | n anomaly in F1.
4. No three points of x³ + y³ = n with x, y > 0 are collinear (convexity of x³ + y³ ≤ n in the positive
   quadrant). Never violated in 11,056 collinear triples (F7).
5. Every relation among the integer points ≤ 10¹⁵ is 3-term ±1 (a line) or 4-term ±1 (a hub) (F5). Is there a
   reason tangent relations (2P + Q = 0) never occur among coprime integer points?
6. Line directions: prove that coprime integer collinear triples on a x + b y = c need a·b = w² + 3v² (from the
   conic w² + 3v² = 12ab³c²/(b³ − a³)²), and that a·b must be even (no line has a, b both odd). Holds for all
   11,155 lines (F10).
7. The F9 identity: three collinear points on 3k² x + (3k² + 1) y = 27k⁴ + 9k² + 1 with
   n = (9k² − 3k + 1)(9k² + 3k + 1)(27k⁴ + 9k² + 1). Verified symbolically; check whether it is classical.
8. Every line a x + b y = c through three coprime integer points of x³ + y³ = n has E = a² + ab + b² dividing c
   and n (sketch in F11; check the factor 3 and the case where b − a shares factors). Holds for all 11,176
   lines.

9. Third point of a chord (F44): R = (X/D, Y/D) always has gcd(X, Y) = 1 (166,228 chords, none failing, including
   27 | n). If p | X, Y then p ∤ D and p³ | n: rule this out. (The companion D | X + Y ⟺ D | b − a is proved:
   THEOREMS.md, Theorem 9.)
   Coprimality is what matters: on every number with >= 2 coprime representations with |coordinates| <= 4,000
   (11,431 numbers, 1,013 with a cube factor; 46,256 chords) it never fails, while the same chords scaled by 2
   (non-coprime points on 8n) fail 19,628 times. Proof idea: if p | X, Y then R reduces mod p to the singular
   point (0:0:1) of x³ + y³ ≡ 0, which coprime points never do; points with nonsingular reduction form a subgroup.
   Gap: that argument breaks when the chord reduces to a component line of the cone (x₁y₂ ≡ x₂y₁ mod p), which
   for p ≡ 2 (mod 3) is every chord; a p-adic argument using p³ | n should close it.
