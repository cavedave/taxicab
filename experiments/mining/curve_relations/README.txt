curve_relations/ -- ranks of the curves x^3 + y^3 = n and exact integer relations among their integral points (FINDINGS F33).
  all_multi.txt   the 1,378 coprime k >= 4 numbers used (n;k;x:y,...): exhaustive four-ways <= 1e17 and at 1e23-2.5e23,
                  the 43 five-ways, and the Mac line-search union (linesearch_mac/union_4plus.txt)
  ranks.txt       n;rank lower;rank upper;#points;ms  (PARI ellrank with the integral points as hints; -1 = 900 s timeout);
                  434 curves, the smallest (the screen was stopped before the large n)
  relations.txt   n;k;rank of the integral points;[relation vectors]  -- every relation c_1 P_1 + ... + c_k P_k = 0 with
                  |c_i| <= 1000, from LLL on [identity; 10^20 * height-pairing matrix], each checked exactly with elladd
  all_ls.csv      line_structure.py shapes of the same numbers
  rank1.gp, reldef.gp   the GP code: rk(n, [[x,y],...]) and rel(n, [[x,y],...])
