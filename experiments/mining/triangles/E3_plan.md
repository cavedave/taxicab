# Plan: why E_3 never divides n for the third sides of a bowtie (F70), and can it be proved for a family?

*Written 8 Nov 2026 evening; to investigate 9 Nov. Background: THEOREMS.md Theorems 2, 8, 9, 10, 13, 14,
Lemmas 17-18; FINDINGS F67, F68, F70.*

**The observation (F70).** For all 1,752 bowties, every candidate third side (a chord through a point of line 1 and a
point of line 2, other than the shared point), after the orientation rule and 4 | ab, has E_3 = a^2 + ab + b^2 not
dividing n: 7,008 of 7,008, all with E_3 <= n (not a size effect). Typically half of log E_3 comes from primes
outside n; at least 15% always.

## Progress 9 Nov (F72)
- Step 0 done: converse of Theorem 2 false (10,914 non-line chords with E | n); bowtie cross chords 0 of 21,136 vs
  5-7% for four-way chords: genuinely special.
- Step 1 done: outside part of E_3 always divides D (general, all chords; one-line proof from Theorem 13); no fixed
  witness prime (13, 19, 7, 31, ... vary). So step 2 goes the finiteness route, after understanding why bowtie cross
  chords always have an outside prime (compare E_3's split primes with the s-values of lines 1 and 2).

## Step 0 -- circularity check (do first)

Theorem 2 says a line (three integer points) has E | n. **If the converse holds** -- a chord through two coprime
points with E | n always has an integral third point -- then "E_3 never divides n" just restates "no third line",
which is true for our bowties because their counts are exact. That would be the same trap as F67's "d = 1 never
occurs".
- **Data:** over every chord between two known points not on a known line (413,476 from the four-ways, 71,278 from
  the five-ways; `near_miss.py` / `chord_f10.py` machinery), count chords with E_3 | n. If some exist (with a
  non-integral third point), the converse fails and F70 is a genuine filter. If none exist, it suggests the converse.
- **Theory:** try to prove or refute "E | n implies the third point R is integral". Tools: Theorem 13's identities
  hold for rational third points (E s_1 s_2 s_R = (a - b)^2 n), Corollary 14a (the denominator of s_R divides E),
  Theorem 9 (D | X + Y iff D | b - a), Theorem 10 and Corollary 10a (if no prime = 1 mod 3 divides D then D | X + Y,
  so D | b - a). A guess to test: **the primes of E_3 not dividing n are exactly the split primes of D**, the
  denominator of R. If so, E_3 | n would mean D has no split primes, then Corollary 10a gives D | b - a, and the
  remaining question is whether that forces D = 1.
- **Outcome A (converse true):** E_3 | n is equivalent to "the chord is a line". Then F70 is not an independent
  obstruction, but it is still a useful **search tool**: for a given n, the only possible new lines (in particular
  triangle sides) have directions whose norm divides n, a finite list built from n's split primes and 3. That gives a
  cheap triangle test for any bowtie whose split primes are known, even when n is too big to count fully.
- **Outcome B (converse false):** E_3 | n is a genuine extra condition, and F70 says it fails on every bowtie chord.
  Then go to step 1 for real.

## Step 1 -- which primes witness E_3 not dividing n?

For every bowtie chord, record the primes p with v_p(E_3) > v_p(n) (the "witness primes").
- Are they always split primes (p = 1 mod 3), or 3? (E_3 is a norm, so only these can divide it.)
- Are they among the primes of E_1, E_2, b - a, b2 - a2 (the bowtie's own primes, as in Theorem 16's N), or of the
  denominator D of the chord's third point, or something else?
- Per curve (direction pair): is there a **fixed** witness prime for all bowties of that pair? (Compare F59: the
  bowtie conditions are periodic component conditions at a fixed finite set of primes.)

## Step 2 -- family-level proof, depending on step 1

- **If a fixed small set of primes always witnesses** (for example 3, or the primes of E_1 E_2): look for a congruence
  proof, like Theorem 8 / Lemma 8a. Show that for every point of the bowtie curve, v_p(E_3) > v_p(n) at that prime,
  using the curve's local structure (F59 components) at p. That would prove "no triangle through a bowtie of this
  pair" for the whole family: a uniform obstruction.
- **If the witnesses are large and vary:** no uniform obstruction. The statement becomes a finiteness result on each
  curve: E_3(P) | n(P) is one divisibility between values of fixed forms on a genus-1 curve, so only finitely many
  points (Siegel / Thue-Mahler type). Then the question is whether those finitely many can be listed (integral points
  on an auxiliary curve).
- Either way, connect with the toolkit: Lemma 18 (equal non-split parts, which the third side must also satisfy),
  Lemma 17 (one class), and the fixed-direction quartic (F67).

## Step 3 -- write up

Whatever survives goes into THEOREMS.md (a lemma for the converse question; a proposition for the family statement,
or its finiteness version) and FINDINGS (F71). Keep TO DO lists at the end, as for Theorem 16.

## Files

`triangles/near_miss.py` (chords, third points), `triangles/filter_measure.py` (F70 counts), `triangles/chord_f10.py`
(type/4 | ab split); data `results/five_ways_all.txt`, `results/a047697_catalogue.txt`.
