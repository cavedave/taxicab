# OEIS extensions (31 October 2026)

Computed with the exhaustive CPU search `experiments/cabtaxi.cpp` (every coprime pair x^3 + y^3, signs allowed) and,
for k >= 4, the A047697 catalogue (`results/a047697_catalogue.txt`, GPU-complete to 1e22). The non-coprime test in
`experiments/mining/oeis_bfiles.py`: n is a sum of two non-coprime nonzero cubes iff n = d^3 m (d >= 2) with m a sum
of two cubes (divisor test on the PARI factorisation).

| file | sequence | terms | complete to | check against the existing b-file |
| --- | --- | ---: | --- | --- |
| b293648_10000.txt | A293648 | 10,000 | 1e13 | all 325 old terms identical |
| b293649_10000.txt | A293649 | 10,000 | 1e13 | all 100 old terms identical |
| b293651_10000.txt | A293651 | 10,000 | 1e15 | old 165 terms all present; **14 terms missing from the old b-file** (A293651_missing_terms.txt) |
| b023050_1e17.txt | A023050 | 107 | 1e17 | all 41 old terms identical |
| new_coprime_ge4_ways_1118.txt | new: coprime (signed) in >= 4 ways | 1,118 | 1e22 | first 91 (<= 1e15) agree with an independent Mac CPU run |
| new_coprime_ge5_ways_12.txt | new: coprime (signed) in >= 5 ways | 12 | 2.5e23 | GPU search |

The A293651 b-file of 2017 misses every term whose representations include a difference of nearly equal cubes with
|x| > 10,000 (e.g. 513926497 = 16^3 + 801^3 = 502^3 + 729^3 = 13089^3 - 13088^3).
A023050 beyond 1e17: `experiments/oeis_run_k3.sh` (worf, 1e17 - 1e19 in three pieces).
