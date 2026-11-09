\\ equiv.gp -- are the line sextics F_d = X^3 + Y^3 (raw point of a line in direction d, a binary sextic in (s, r)) of
\\ two directions equivalent under a rational change of slope M (F_1(M (s, r)) = c F_2(s, r))? Such an M gives a line
\\ on the surface F_1(s, r) = c F_2(s', r') in P^3, i.e. a one-parameter family of pairs of lines with the same n.
\\ For d1 = d2, the maps are automorphisms; 6 of them (orderings of the triple) are expected and trivial.
\r forms23.gp
default(realprecision, 60);
sext(X, Y) = X^3 + Y^3;
mob(z, M) = (M[1,1]*z + M[1,2]) / (M[2,1]*z + M[2,2]);
\\ the Moebius map sending z1, z2, z3 to w1, w2, w3 (as a 2x2 matrix)
tomat(z1, z2, z3) = [z2 - z3, -z1*(z2 - z3); z2 - z1, -z3*(z2 - z1)];     \\ sends z1 -> 0, z3 -> oo, z2 -> 1
three(z, w) = matadjoint(tomat(w[1], w[2], w[3])) * tomat(z[1], z[2], z[3]);
near(x, S) = vecmin(apply(y -> abs(x - y), S)) < 1e-25;
ratmat(M) = {
  my(k = 0); for(i = 1, 4, if(abs(M[(i-1)\2+1, (i-1)%2+1]) > 1e-20, k = i; break));
  if(!k, return(0));
  my(N = M / M[(k-1)\2+1, (k-1)%2+1], R = matrix(2, 2));
  for(i = 1, 2, for(j = 1, 2, if(abs(imag(N[i,j])) > 1e-20, return(0)); R[i,j] = bestappr(real(N[i,j]), 10^12)));
  if(norml2(apply(x -> abs(x), N - R)) > 1e-30, return(0));
  R;
}
\\ all rational M with F1(M (s, r)) proportional to F2(s, r)
equivs(F1, F2) = {
  my(f1 = subst(F1, s, 1), f2 = subst(F2, s, 1), z = polroots(f1), w = polroots(f2), out = List());
  if(#z != 6 || #w != 6, return(["degree"]));
  forvec(ijk = vector(3, t, [1, 6]),
    if(#Set(ijk) < 3, next);
    my(M = three([z[1], z[2], z[3]], [w[ijk[1]], w[ijk[2]], w[ijk[3]]]), ok = 1);
    \\ M maps roots of F1 to roots of F2 ... we need the inverse direction for F1(M v) ~ F2(v); test both via exact check
    for(i = 4, 6, if(!near(mob(z[i], M), w), ok = 0; break));
    if(!ok, next);
    my(R = ratmat(M));
    if(R === 0, next);
    my(Ri = matadjoint(R), G = substvec(F1, [s, r], [Ri[2,2]*s + Ri[2,1]*r, Ri[1,2]*s + Ri[1,1]*r]));
    \\ exact: is G a constant multiple of F2 ?  (try both orders of (s, r) in the substitution)
    my(G2 = substvec(F1, [s, r], [Ri[1,2]*r + Ri[2,2]*s, Ri[1,1]*r + Ri[2,1]*s]), q);
    foreach([G, G2], GG,
      q = GG / F2;
      if(type(q) == "t_INT" || type(q) == "t_FRAC" || (type(q) == "t_POL" && poldegree(q, s) == 0 && poldegree(q, r) == 0),
        listput(out, R); break)));
  Set(Vec(out));
}
{
  my(nd = #FORMS, F = vector(nd, i, sext(FORMS[i][2], FORMS[i][3])), cnt = 0);
  for(i = 1, nd,
    my(sq = poldisc(subst(F[i], s, 1)));
    if(sq == 0, print("direction ", FORMS[i][1], ": sextic has a repeated root")));
  for(i = 1, nd, for(j = i, nd,
    my(E = equivs(F[i], F[j]));
    if(i == j, print("direction ", FORMS[i][1], ": ", #E, " rational automorphisms (6 expected: orderings)"),
      if(#E, cnt++; print("EQUIVALENT: ", FORMS[i][1], " ~ ", FORMS[j][1], " via ", E)))));
  print("pairs of distinct directions with equivalent sextics: ", cnt);
}
