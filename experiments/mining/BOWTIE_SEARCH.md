# The bowtie line search

How we look for numbers n that are a sum of two coprime cubes in five or six ways (A047697) without checking
every n:
1. build three representations at once from a straight line;
2. keep the n that look divisor-rich;
3. count all their representations exactly.

The interactive version, with figures, is `bowtie-line-search.html` (published at
https://claude.ai/artifact/3K5RyxRv4Ftikp77ooiYCu). The code is `line_enum.py` (lines), `cheap_search.py`
(filter and exact count) and `rank_dirs.py` (which directions pay). Results are in FINDINGS F12–F25.

## 1. Each representation is a point on a curve

- Fix n. Every way of writing n = x³ + y³ with integers x, y is a point (x, y) on the curve x³ + y³ = n.
- Negative cubes are allowed, so the curve runs off to infinity along the asymptote y = −x.
- The swap (y, x) is also on the curve: the same representation, seen from the other side.

The smallest number with three coprime representations (A047697(3)) is

    3367 = 15³ + (−2)³ = (−9)³ + 16³ = (−33)³ + 34³

All three points lie on one straight line, **3x + 4y = 37**:

| point | 3x + 4y |
| --- | --- |
| (15, −2) | 45 − 8 = 37 |
| (−9, 16) | −27 + 64 = 37 |
| (−33, 34) | −99 + 136 = 37 |

That is how most multi-way numbers are built: 87% of three-ways are collinear, and 90% of four-ways are a
line plus one free point (F17).

## 2. A line meets the curve three times

Put y = (c − 3x)/4 into x³ + y³ = n and multiply by 64:

    37x³ + 27c·x² − 9c²·x + (c³ − 64n) = 0

- Only the constant term involves n. So for every n, the three roots satisfy

      x₁ + x₂ + x₃ = −27c/37
      x₁x₂ + x₁x₃ + x₂x₃ = −9c²/37

- **Check with 3367** (c = 37):
  - 15 − 9 − 33 = −27;
  - 15·(−9) + 15·(−33) + (−9)·(−33) = −333 = −9·37.
- Choose two roots that fit these rules. The third follows, and n is whatever the cubes add up to.

**Cost.** In general a direction (a, b) gives the cubic (b³ − a³)x³ + 3a²c·x² − 3ac²·x + (c³ − b³n) = 0. The
number b³ − a³ (37 for (3, 4)) is the **cost** of the direction.
- Small cost means small numbers and many hits, so we search the cheapest directions first.
- Only directions where ab is a norm can carry three coprime points (F10): every prime ≡ 2 (mod 3) appears to
  an even power, and 2 at least squared.

## 3. The slope: walking round an ellipse

Eliminating the third root turns the two rules into one equation. For direction (a, b) it is the ellipse

    X² + XY + Y² = 3ab³        (for (3, 4):  X² + XY + Y² = 576)

with two of the roots given by x₁ = c(X − 9)/37 and x₂ = c(Y − 9)/37 for (3, 4).

**How the slopes give every triple:**
- Every rational point (X, Y) on the ellipse is a line with three points on some curve x³ + y³ = n.
- c is the smallest integer that makes all three x and y whole.
- To list every rational point, start at a known point, (−24, 0) for (3, 4), and draw a line through it with
  slope r/s. It cuts the ellipse at exactly one more point, which is rational.
- **Each slope gives one triple.** The **height** of the slope is max(|r|, s). Small heights give small n;
  raising the height reaches larger n.

| slope r/s | height | c | n | three points (x, y) |
| --- | ---: | ---: | ---: | --- |
| 1/0 | 1 | 37 | 3367 | (−33, 34) (15, −2) (−9, 16) |
| 2/1 | 2 | 259 | 2113921 | (−135, 166) (129, −32) (−183, 202) |
| 1/2 | 2 | 259 | 195841 | (9, 58) (57, 22) (−255, 256) |
| 3/1 | 3 | 481 | 14110579 | (−309, 352) (243, −62) (−285, 334) |
| 1/3 | 3 | 481 | 684019 | (75, 64) (51, 82) (−477, 478) |
| 2/3 | 3 | 703 | 9667693 | (−51, 214) (213, 16) (−675, 682) |
| 4/3 | 4 | 1369 | 244394731 | (−501, 718) (627, −128) (−1125, 1186) |
| 3/4 | 4 | 1369 | 96702571 | (−165, 466) (459, −2) (−1293, 1312) |
| 5/1 | 5 | 1147 | 174152377 | (−855, 928) (561, −134) (−543, 694) |
| 1/5 | 5 | 1147 | 26460217 | (297, 64) (−15, 298) (−1119, 1126) |
| **135/556** | **556** | **14889577** | **39673716067958900347** | (3360075, 1202338) (418491, 3408526) (−14643933, 14705344) |

The last row is one line of a five-way: the bowtie below.

## 4. The bowtie: two lines through a shared point

n = 39,673,716,067,958,900,347 = 7 · 19 · 31 · 37 · 109 · 283 · 1669 · 2203 · 2293 has five coprime
representations. On its curve they lie on two lines that cross at one of the points, the **hub**:

| line | cost b³ − a³ | points on it |
| --- | ---: | --- |
| 3x + 4y = 14889577 | 37 (cheap) | (3360075, 1202338), (418491, 3408526), **(−14643933, 14705344)** |
| 273x + 304y = 472630867 | 7,748,047 (expensive) | (3526755, −1612412), (−2521629, 3819196), **(−14643933, 14705344)** |

- **Three points per line, one shared:** 3 + 3 − 1 = 5. Seventeen of the eighteen five-ways we know have this
  shape.
- **Why lines matter:** on this curve, three points lie on a line exactly when they add up to zero in the
  curve's group law (the flex at infinity is the origin, and −P is the swap of P). A bowtie is two such
  relations sharing one point.

## 5. The search

- **We only need to find one line of a bowtie.** The cheap line gives n three representations for free.
  Then an exact count of all representations of n (from its divisors) finds the expensive line's two extra
  points automatically.
- **The steps:**
  1. **Directions:** pairs (a, b) whose lines can carry three coprime points, cheapest b³ − a³ first.
  2. **Slopes:** every slope r/s up to a height H. Each gives one triple and one n.
  3. **Filter** (F24 profile): keep n only if
     - at least two of 7, 13, 19, 37 divide it, and
     - it has at least four primes ≡ 1 (mod 3) below 200.

     All 18 known five-ways pass; about a third of candidates do.
  4. **Count:** factor each kept n and count every coprime representation exactly
     (s = x + y divides n, s³ ≤ 4n, and (4n/s − s²)/3 must be a perfect square). Four or more is a hit.

| run | directions | height | n up to | five-ways found |
| --- | --- | ---: | --- | --- |
| first sweep | 1–200 | 600 | 10³² | 9 (2 new) |
| second sweep | 201–500 | 600 | 10³² | 3 (2 new) |
| third sweep | 501–1000 | 600 | 10³² | 2 (2 new) |
| 7-filter run (F24) | 1–120 | 800 | 10⁴⁰ | 4 (1 new) |
| fourth sweep (F25) | 1001–1400 | 600 | 10³² | 1 (0 new) |
| deep search (F26) | 8 best | 4000 | 10⁴⁰ | 9 (5 new) |

**Why the deep search:**
- Expensive directions have dried up (F25).
- Most hits come from a few cheap directions: (3, 4) alone gave 48 of the 113 four-ways in F24.
- So the deep search returns to the eight most productive directions and raises the slope height from 600–800
  to 4,000.

| direction (a, b) | line | cost b³ − a³ |
| --- | --- | ---: |
| (3, 4) | 3x + 4y = c | 37 |
| (12, 13) | 12x + 13y = c | 469 |
| (36, 37) | 36x + 37y = c | 3,997 |
| (3, 16) | 3x + 16y = c | 4,069 |
| (12, 19) | 12x + 19y = c | 5,131 |
| (48, 49) | 48x + 49y = c | 7,057 |
| (57, 64) | 57x + 64y = c | 76,951 |
| (12, 49) | 12x + 49y = c | 115,921 |

## Why a six-way is hard this way

- **The cost of one more representation grows with k.** Four-ways to five-ways run from about 28:1 to 200:1
  in our data. Each extra representation needs 2–3 more primes ≡ 1 (mod 3).
- **"A five-way plus a lucky sixth point" needs roughly 100–300 five-ways.** We have 19.
- **The alternative** is to build a six-point structure directly: two disjoint lines, a bowtie plus a point, or
  a triangle of three lines. That is goal C in `UlasPaperPlan.md`.
