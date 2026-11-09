\r tri_decide.gp
\r hits150.gp
\\ put each rational triangle on its cube-free curve x^3 + y^3 = m: n0 = num/den, num*den^2 = m*k^3, lam = den/k
cubefree(q) = { my(F = factor(q), m = 1, k = 1); for(i = 1, #F~, m *= F[i,1]^(F[i,2] % 3); k *= F[i,1]^(F[i,2] \ 3)); [m, k]; }
onetri(D, c, seen) = {
  my(T = six(D, c), n0, mk, m, lam, pts, key);
  if(!T, return(0));
  n0 = T[1]; mk = cubefree(numerator(n0) * denominator(n0)^2); m = mk[1]; lam = denominator(n0) / mk[2];
  if(lam^3 * n0 != m, print("SCALE FAIL ", D); return(0));
  pts = apply(p -> [lam * p[1], lam * p[2]], T[2]);
  key = Str(vecsort(apply(p -> vecsort([p[1], p[2]]), pts)));
  if(mapisdefined(seen, key), return(0));
  mapput(seen, key, 1);
  print("TRI m=", m, " D=", D, " pts=", pts);
  1;
}
runall() = {
  my(seen = Map(), cnt = 0);
  foreach(H, D,
    foreach(tri(D), c,
      if(c === "DEGENERATE", next);
      cnt += onetri(D, c, seen)));
  print("distinct triangles: ", cnt);
}
runall();
