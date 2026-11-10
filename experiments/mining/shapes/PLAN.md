# The shape route: configuration varieties of k-ways (agreed with the user 10 Nov 2026)

**Idea.** Representations of a multi-way are pairwise linked by cheap chords (F81-F82), each a Pell conic
(F82-F83). A configuration of k points with fixed chord directions is a cover of the (x, y)-plane cut out by square
conditions: a new point along a fixed direction from an existing point costs one square condition (the discriminant of
F58.2's quadratic, quadratic in (x, y)); a whole line costs one condition for two new points. The geometry of the
resulting variety decides whether rational configurations come in infinite families.

**CORRECTED 10 Nov (F86):** configurations are up to scaling, so the base is P^1, not a plane: m square conditions give a
curve of genus 1 + 2^(m-1)(m-2) (0, 1, 5, 17, 49 for m = 1..5); no K3 for four-ways. The old count, kept for the record:
**Dimension count (superseded):** star of cheap chords from one point --
k = 2: conic bundle (rational; Pell families, F83); k = 3: two quadrics, del Pezzo of degree 4 (rational points dense
once one exists); **k = 4: three quadrics, K3 surface (Elkies' territory)**; k = 5, 6: general type (finitely many by
Bombieri-Lang). Lines are "cheaper" (two points per condition), which is how bowtie five-ways come in infinite families.

**Steps.**
1. **Done (F85):** four-ways are stars of relatively cheap chords (91.5% / 53% within cost 1e12 for line+free / no-line,
   against 3.8% control). Refinement: directions grow ~ n^0.19 per coefficient; counts must sum over directions.
2. **Done (10 Nov): Proposition 20 in THEOREMS.md, table column in the paper.** Two disjoint lines: genus 5 on all
   10,626 base-direction triples (Lemma 20c). Open in it: Lemma 20c in general (the quartic's discriminant as a
   polynomial in the directions); the triangle's Siegel step written out.
   Earlier note -- **Started (F86):** genus formula and branch form verified, all real configurations have distinct branch points;
   six-way shapes: finite per direction set (Faltings / Theorem 8c / Siegel for the triangle). Remaining: the two
   disjoint lines cover; write the per-direction-set finiteness as a proposition.
   Original step: **Compute the varieties** in PARI for one example of each six-way shape (paper Table tab:sixshapes): equations,
   branch loci, genus / Kodaira dimension. Goal: a "geometry" column (rational / K3 / general type) proved, not
   hand-waved. A shape whose variety is not of general type is where infinite rational families of six-ways would live;
   Theorem 16's congruence argument could then make them integral and coprime.
3. **Elkies-style test on one K3** (refs/shape: Elkies 1988 and 2007): take a four-way's three chord directions, write
   down the K3, find an elliptic fibration, generate new four-ways from it -- a check that the geometry predicts real
   objects.
4. **Practical, separately:** Cremona-Fisher-Stoll minimisation (refs/shape/0908.1741v1.pdf) for the decider's missed
   curves (F65, F71).

**Caveats.** The surfaces may be singular, reducible or contain special curves (as the bowtie curves are), any of
which changes the answer -- that is what step 2 checks. "General type, so finitely many" rests on Bombieri-Lang
(conditional / heuristic in the paper).
