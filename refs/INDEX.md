# Reference PDFs (inventory, 26 October 2026)

Every PDF in `taxicab/` and `~/Documents/sixes/`, with what it is and what we use it for. Duplicates are
listed once, with all their locations.

## Sums of two cubes: counting and growth (goal B)
| file | reference | use |
| --- | --- | --- |
| `refs/Hooleybf01111429.pdf` | C. Hooley, *On the representations of a number as the sum of two cubes*, Math. Z. 82 (1963) 259–266 | Σ r(n)² asymptotic; 2-ways ≪ x^(5/9+ε); lower bound ≫ x^(1/3) log x |
| `refs/aa7913.pdf` | D. R. Heath-Brown, *The density of rational points on cubic surfaces*, Acta Arith. 79 (1997) 17–30 | Cor.: at most O(x^(4/9+ε)) n ≤ x with ≥ 2 representations (non-negative cubes). Lines on the surface dominate the point count, the same idea as our goal B |
| `refs/1995 T3P.pdf`, `1995 T3P.pdf` | T. D. Wooley, *Sums of two cubes*, IMRN 1995 | elementary proof of Hooley's 5/9 bound, using 3 coplanar lines |
| `refs/On_Warings_problem_in_sums_of_three_cubes.pdf` | J. Pliego, arXiv:2010.14536 | Waring for sums of three cubes |
| `refs/2404.08190v1.pdf` | Benfield, Lippard, Roy, *End behavior of Ramanujan's taxicab numbers*, arXiv:2404.08190 | asymptotics of taxicab-type sequences |

## Taxicab and cabtaxi numbers: searches and bounds
| file | reference |
| --- | --- |
| `refs/sortedsums-…pdf`, `refs/bernstein_2001_sortedsums.pdf`, `sixes/six-one-five/taxicab.pdf`, `sixes/six-one-five/Bernstein-…2001.pdf` | D. J. Bernstein, *Enumerating solutions to p(a) + q(b) = r(c) + s(d)*, Math. Comp. 70 (2001) |
| `boyer-new.pdf` | C. Boyer, *New upper bounds for taxicab and cabtaxi numbers*, JIS 11 (2008) |
| `su3.pdf`, `refs/su_2016_more_upper_bounds_jis19.pdf` | Po-Chi Su, *More upper bounds on taxicab and cabtaxi numbers*, JIS 19 (2016) |
| `0802.1147v1.pdf`, `refs/0802.1147v1.pdf` | P. Emelyanov, *On hunting for taxicab numbers*, arXiv:0802.1147 |
| `what-is-the-value-of-taxicab-6-…pdf` | C. S. Calude, E. Calude, M. J. Dinneen, *What is the value of Taxicab(6)?*, J.UCS 9 (2003) |
| `1901.09053v1.pdf`, `seeds1901.09053v1.pdf` | Dinitz, Games, Roth, *Seeds for generalized taxicab numbers*, arXiv:1901.09053 |
| `refs/Thesis-final-version.pdf` | L. Mensh, *Variations of the taxicab problem* (undergraduate thesis) |
| `refs/2206.00465v1.pdf` | *Euler's and the taxicab relations and other numbers that can be written twice as sums of two cubed integers*, arXiv:2206.00465 |
| `refs/1405.7579v1.pdf` | Petrović et al., *Geometry of some taxicab curves* (taxicab *metric* geometry, not our problem) |

## Elliptic curves x³ + y³ = n: integer points, rank, families (goals A and C)
| file | reference | use |
| --- | --- | --- |
| `refs/taxiSilv.pdf` = `refs/taxi.pdf` (identical), `refs/silverman_1993_taxicabs_sums_two_cubes.pdf` | J. H. Silverman, *Taxicabs and sums of two cubes*, Amer. Math. Monthly 100 (1993) | read; plan A0b |
| `refs/Thuebf01389220.pdf` | J. H. Silverman, *Integer points and the rank of Thue elliptic curves*, Invent. Math. 66 (1982) | N(A) ≤ κ^(r+1) for cube-free A (our "Theorem A") |
| `sixes/Silverman.pdf` | J. H. Silverman, *The Arithmetic of Elliptic Curves*, 2nd ed. (2009) | ch. VII for TOPROVE item 11; ch. IX integer points |
| `sixes/WyomingEllipticCurve.pdf` | J. H. Silverman, *An introduction to the theory of elliptic curves* (summer-school notes) | primer |
| `refs/elkies_rogers_2004_math0403116.pdf` | N. D. Elkies, N. F. Rogers, *Elliptic curves x³ + y³ = k of high rank*, arXiv:math/0403116 | high-rank curves of our exact family; C and the curve route |
| `refs/birch1966.pdf` | B. J. Birch, N. M. Stephens, *The parity of the rank of the Mordell–Weil group*, Topology 5 (1966) | root numbers |
| `refs/cassels-6-9.pdf` | J. W. S. Cassels, *Lectures on Elliptic Curves*, chs. 6–9 (excerpt) | |
| `refs/JacobianFinal.pdf` | S. Y. An, S. Y. Kim, *Jacobians of genus one curves* | Weierstrass forms of genus-1 curves (needed for A2/C2) |
| `refs/67_MORDELL.pdf`, `67_MORDELL.pdf` | Gebel, Pethő, Zimmer, *On Mordell's equation* | computing integer points |
| `refs/mahler040.pdf` | K. Mahler, *Note on Hypothesis K of Hardy and Littlewood*, J. London Math. Soc. 11 (1936) | (9ξ⁴)³ + (3ξ − 9ξ⁴)³ + (1 − 9ξ³)³ = 1 (used by Ulas §3) |
| `refs/jlms%2Fs2-28.1.1.pdf` | J. H. Silverman, *Integer points on curves of genus 1*, J. London Math. Soc. (2) 28 (1983) 1–7 | N_f(m) ≫ (log m)^(r/(r+2)) from a rank-r curve f = m₀z³; for x³ + y³: (log m)^(3/5). Mahler's denominator-clearing, so not coprime |
| `~/Downloads/Unsolved Problems … Guy … 9780387208602 ….djvu` (3rd ed., 2004; 1st ed. 1981 PDF alongside) | R. K. Guy, *Unsolved Problems in Number Theory*, D1 (pp. 209–213) | history and status: see UlasPaperPlan A0c |
| `refs/leech_1957_some_solutions_diophantine.pdf` | J. Leech, *Some solutions of Diophantine equations*, Proc. Camb. Phil. Soc. 53 (1957) | smallest positive 3-way |
| `refs/historyoftheoryo02dickuoft.pdf` | L. E. Dickson, *History of the Theory of Numbers*, vol. 2 | ch. XXI: chord formula, Werebrusow, Desboves |
| `refs/Kenneth Ireland, Michael Rosen - …pdf` | Ireland, Rosen, *A Classical Introduction to Modern Number Theory* | ch. 8 Gauss count for x³ + y³ = 1 mod p |

## Infinite families via Pell equations
| file | reference | use |
| --- | --- | --- |
| `refs/Karaatli.pdf` | O. Karaatli, R. Keskin, H. Zhu, *Infinitely many positive integer solutions of the quadratic Diophantine equations x² − 8B_n xy − 2y² = ±2^r*, Irish Math. Soc. Bull. 73 (2014) 29–45 | all solutions of indefinite binary quadratics as recurrence sequences (Pell, Pell–Lucas, balancing numbers). Template for the genus-0 indefinite case of A2/C2 |

## Ramanujan, 1729 and identities
| file | reference |
| --- | --- |
| `1510.00735v5.pdf`, `k31510.00735v5.pdf`, `refs/1510.00735v5.pdf` | K. Ono, S. Trebat-Leder, *The 1729 K3 surface* |
| `refs/hirschhorn1995.pdf` | M. D. Hirschhorn, *An amazing identity of Ramanujan*, Math. Mag. (1995) |
| `refs/paper40.pdf` | M. D. Hirschhorn, *A proof in the spirit of Zeilberger of an amazing identity of Ramanujan* |
| `refs/Ramanujan's Lost Notebook … Part IV …pdf` | Andrews, Berndt, *Ramanujan's Lost Notebook*, Part IV |
| `refs/2604.25017v1.pdf` | K. Gyarmati, *Ramanujan, the taxicab problem for polynomials, and the abc-conjecture*, arXiv:2604.25017 (2026) |
| `unusualAMI_43_from29to41.pdf`, `AMI_43_from29to41.pdf` | A. Bremner, A. Macleod, *An unusual cubic representation problem*, Ann. Math. Inform. 43 (2014) |

## x³ ± y³ = aᵏ ± bᵏ and our own papers
| file | reference |
| --- | --- |
| `refs/ulas.pdf`, `refs/2402.06567v2.pdf`, `sixes/six-one-five/2402.06567v2.pdf` | M. Ulas, *On the Diophantine equation x³ ± y³ = aᵏ ± bᵏ*, arXiv:2402.06567v2 |
| `refs/growth.pdf`, `sixes/paper/pdf/growth.pdf` | D. Curran, *Growth rates of solutions to x³ ± y³ = aᵏ + bᵏ* (draft, September 2026) |
| `sixes/paper/pdf/architecture.pdf` | D. Curran et al., *Euler sums using GPUs* (draft, August 2026) |
| `sixes/wagstaff8.pdf` | S. S. Wagstaff Jr., *Equal sums of two distinct like powers*, JIS 25 (2022) |
| `sixes/six-one-five/s_trick.pdf` | own note: the s = x + y trick for k = 4 sums |

## Equal sums of like powers (sixes project)
| file | reference |
| --- | --- |
| `sixes/S0025-5718-1967-0222008-0.pdf` | Lander, Parkin, Selfridge, *A survey of equal sums of like powers*, Math. Comp. (1967) |
| `sixes/ekl.pdf` | R. L. Ekl, *New results in equal sums of like powers*, Math. Comp. 67 (1998) |
| `sixes/S0025-5718-02-01445-X.pdf` | Math. Comp. 72 (2002) 1051–1054, *The smallest …* (equal sums of like powers) |
| `sixes/pte.pdf` | Math. Comp. 72 (2002) 2063–2070, computations on the Prouhet–Tarry–Escott problem |
| `sixes/20005a1d_837.pdf` (+ ` (1)` copy), `sixes/On_Equal_Sums_of_Sixth_Powers_searchable.pdf` | A. Choudhry, *On equal sums of sixth powers*, Indian J. Pure Appl. Math. 25 (1994) |
| `sixes/1602.08698v1.pdf` | A. Choudhry, *Equal sums of like powers with minimum number of terms* |
| `sixes/plms%2Fs3-43.3.544.pdf` | A. Bremner, *A geometric approach to equal sums of sixth powers*, PLMS (1981) |
| `sixes/1-s2.0-0022314X81900196-main.pdf` | A. Bremner, *A geometric approach to equal sums of fifth powers*, JNT 13 (1981) |
| `sixes/1108.0462v1.pdf` | all solutions of a⁶ + b⁶ = c⁶ + … + g⁶ below 250000 |
| `sixes/2603.05549v2.pdf` | J. Braun, *The fourth known primitive solution to a⁵ + b⁵ + c⁵ + d⁵ = e⁵* (2026) |
| `sixes/2512.00551v2.pdf` | V. Asiryan, *The linear slicing method for equal sums of like powers* (2025) |
| `sixes/2101.09390v2.pdf` | A. Newton, J. Rouse, *Integers that are sums of two rational sixth powers* |
| `sixes/ANTS-XV_elkies-goel.pdf` | N. D. Elkies, G. Goel, *On powerful integers expressible as sums of two coprime fourth powers* |
| `sixes/Finding_95800…Connection_Machine.pdf` (+ copy in `six-one-five/`) | Frye, finding 95800⁴ + 217519⁴ + 414560⁴ = 422481⁴ |
| `sixes/2504.10759v1.pdf` (+ ` (1)` copy) | Cynk, Kocel-Cynk, *Elliptic and K3 fibrations on double octic Calabi–Yau threefolds* (2025) |

## General / unrelated
| file | reference |
| --- | --- |
| `sixes/Andrews-NumberTheory.pdf` | G. E. Andrews, *Number Theory* |
| `sixes/six-one-five/pomerance.pdf` | C. Pomerance, *A tale of two sieves* |
| `sixes/xor_filter.pdf` | Graf, Lemire, *Xor filters* |
| `sixes/0003155v1.pdf` | A. Leykin, *Definitive computation of Bernstein–Sato polynomials* |
| `sixes/Using_Heuristic_Algorithms_…Knapsack….pdf` | knapsack heuristics |
| `sixes/cdc_prompt.pdf` | prompt document for a cycle double cover proof |
| `refs/jacobian.pdf` | *A counterexample to the Jacobian conjecture* |
| `refs/halmos__naive_set_theory.pdf` | P. Halmos, *Naive Set Theory* |

## Still wanted
- A. Rosenstiel, J. A. Dardis, C. R. Rosenstiel, Bull. IMA 27 (1991) 155–157: the smallest non-cube-free
  five-way 6963472309248; possible families (goal C).
- S. Lang, *Elliptic Curves: Diophantine Analysis* (1978), p. 140: Dem'janenko–Lang conjecture (optional).
