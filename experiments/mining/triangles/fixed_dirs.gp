\\ fixed_dirs.gp -- triangles with three fixed line directions: lines a_i x + b_i y = c_i; corners V_ij = L_i n L_j
\\ must lie on one cubic x^3 + y^3 = n: f(V12) = f(V13) = f(V23). Two cubic forms in (c1 : c2 : c3).
f(V) = V[1]^3 + V[2]^3;
V(i, j, D, C) = matsolve([D[i][1], D[i][2]; D[j][1], D[j][2]], [C[i], C[j]]~);
tri(D) = {
  my(C = [c1, c2, c3], v12 = V(1,2,D,C), v13 = V(1,3,D,C), v23 = V(2,3,D,C), F1, F2, g, R1, R2, conc, res);
  F1 = numerator(f(v12) - f(v13)); F2 = numerator(f(v13) - f(v23));
  conc = matdet([D[1][1], D[1][2], c1; D[2][1], D[2][2], c2; D[3][1], D[3][2], c3]);   \\ concurrency (linear)
  g = gcd(F1, F2);
  R1 = F1 / g; R2 = F2 / g;
  res = factor(polresultant(subst(R1, c3, 1), subst(R2, c3, 1), c1));
  printf("dirs %s: gcd of the two cubics = %s (concurrency line %s); residual degrees %d, %d; resultant in c2 factors %s\n",
         D, factor(g)[,1]~, conc, poldegree(subst(subst(R1, c2, c1), c3, c1)), poldegree(subst(subst(R2, c2, c1), c3, c1)), res[,1]~);
}
tri([[3,4],[27,28],[9,52]]);
tri([[3,4],[27,28],[75,76]]);
tri([[1,12],[49,192],[13,16]]);
