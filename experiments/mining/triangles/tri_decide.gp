\\ tri_decide.gp -- rational triangles (six-ways up to scaling) with three given line directions.
\\ Lines a_i x + b_i y = c_i; corners V_ij on x^3 + y^3 = n  <=>  f(V12) = f(V13) = f(V23). After removing the
\\ common concurrency line the two residual conics meet in <= 4 points: rational triangles = rational roots.
f(V) = V[1]^3 + V[2]^3;
ratroots(p) = { if(p == 0 || poldegree(p) < 1, return([])); my(F = factor(p)[,1], r = List()); for(k = 1, #F, if(poldegree(F[k]) == 1, listput(r, -polcoef(F[k], 0) / polcoef(F[k], 1)))); Vec(r); }
V(i, j, D, C) = matsolve([D[i][1], D[i][2]; D[j][1], D[j][2]], [C[i], C[j]]~);
tri(D) = {
  my(C = [c1, c2, c3], F1, F2, g, R1, R2, out = List(), sols);
  F1 = numerator(f(V(1,2,D,C)) - f(V(1,3,D,C))); F2 = numerator(f(V(1,3,D,C)) - f(V(2,3,D,C)));
  g = gcd(F1, F2); R1 = F1 / g; R2 = F2 / g;
  \\ affine charts c3 = 1 (and c3 = 0 separately)
  foreach([1, 0], z,
    my(r1 = subst(R1, c3, z), r2 = subst(R2, c3, z));
    if(z == 0, r1 = subst(r1, c2, 1); r2 = subst(r2, c2, 1);
      foreach(ratroots(gcd(r1, r2)), x, listput(out, [x, 1, 0])),
      my(res = polresultant(r1, r2, c1));
      if(res == 0, listput(out, "DEGENERATE"); next);
      foreach(ratroots(res), y,
        foreach(ratroots(gcd(subst(r1, c2, y), subst(r2, c2, y))), x, listput(out, [x, y, 1])))));
  Vec(out);
}
\\ six points of the triangle for a solution c = [c1, c2, c3]: corners and the third point on each side
third(P, Q, n) = { my(u = Q[1] - P[1], v = Q[2] - P[2], t); if(u^3 + v^3 == 0, return(0)); t = -3*(P[1]*u^2 + P[2]*v^2)/(u^3 + v^3) - 1; [P[1] + t*u, P[2] + t*v]; }
six(D, c) = {
  my(v12 = V(1,2,D,c), v13 = V(1,3,D,c), v23 = V(2,3,D,c), n = f(v12), pts);
  if(n == 0 || v12 == v13 || v12 == v23 || v13 == v23, return(0));
  pts = [v12, v13, v23, third(v12, v13, n), third(v12, v23, n), third(v13, v23, n)];
  if(#select(p -> p === 0, pts), return(0));
  [n, pts];
}
\\ status of a triangle: number of distinct representations (x,y) ~ (y,x), and whether one scaling makes all six coprime integers
status(T) = {
  my(pts = T[2], reps = Set(apply(p -> vecsort([p[1], p[2]]), pts)), dens = Set(apply(p -> lcm(denominator(p[1]), denominator(p[2])), pts)), L, ok = 1);
  L = lcm(dens);
  foreach(pts, p, my(X = p[1]*L, Y = p[2]*L); if(denominator(X) != 1 || denominator(Y) != 1 || gcd(X, Y) != 1, ok = 0));
  [#reps, #dens, ok];
}
