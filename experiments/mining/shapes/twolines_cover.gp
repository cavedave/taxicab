\\ two disjoint lines: P on line 1 (direction d1), chord P -> Q in direction d3, line 2 through Q (direction d2).
\\ Q = P + lam (b3, -a3), lam = (-B3 + w3) / (2 A3), w3^2 = Delta_d3(x, y). Delta_d2(Q) = alpha + beta w3 (mod w3^2 = Delta_d3);
\\ the cover w2^2 = alpha + beta w3 of the genus-1 curve C13 (w1^2 = Delta_d1, w3^2 = Delta_d3) is branched at the zeros of
\\ the norm alpha^2 - beta^2 Delta_d3 (a quartic form): 4 distinct roots, none shared with Delta_d1 or Delta_d3 -> r = 8, genus 5.
Dl(a, b, X, Y) = 3*(b*(4*a^3 - b^3)*X^2 + 6*a^2*b^2*X*Y + a*(4*b^3 - a^3)*Y^2);
check(d1, d2, d3) = {
  my(a1 = d1[1], b1 = d1[2], a2 = d2[1], b2 = d2[2], a3 = d3[1], b3 = d3[2], A3 = b3^3 - a3^3, B3, lam, Qx, Qy, F, al, be, Nm, D1, D3, y = 1);
  B3 = 3*(x*b3^2 + y*a3^2);
  lam = (-B3 + w)/(2*A3); Qx = x + lam*b3; Qy = y - lam*a3;
  F = Dl(a2, b2, Qx, Qy);                                   \\ polynomial in x and w
  F = subst(F, w, w);                                      \\ reduce w^2 -> Delta_d3(x, 1)
  D3 = Dl(a3, b3, x, 1); D1 = Dl(a1, b1, x, 1);
  F = polcoef(F, 0, w) + polcoef(F, 2, w)*D3 + w*polcoef(F, 1, w);
  al = polcoef(F, 0, w); be = polcoef(F, 1, w);
  Nm = al^2 - be^2*D3;
  if(Nm == 0, return("norm vanishes identically (split cover)"));
  if(poldegree(Nm, x) < 4, return(Str("norm degree ", poldegree(Nm, x), " (a root at infinity: check homogeneously)")));
  if(poldisc(Nm) == 0, return("repeated root"));
  if(poldegree(gcd(Nm, D1)) > 0 || poldegree(gcd(Nm, D3)) > 0, return("root shared with Delta_d1 or Delta_d3"));
  "genus 5";
}
B = [[1,4],[1,12],[1,16],[3,4],[3,16],[4,7],[4,9],[4,13],[4,19],[4,21],[7,12],[7,16],[9,16],[12,13],[12,19],[13,16],[16,19],[16,21],[25,28],[27,28],[28,31],[36,37],[48,49]];
{
  my(cnt = Map(), tot = 0);
  forvec(ijk = [[1, #B], [1, #B], [1, #B]], my(i = ijk[1], j = ijk[2], k = ijk[3]);
    if(i == j || j == k || i == k, next);
    my(r = check(B[i], B[j], B[k])); tot++;
    if(mapisdefined(cnt, r), mapput(cnt, r, mapget(cnt, r) + 1), mapput(cnt, r, 1)));
  print(tot, " ordered direction triples (d1, d2, d3): ", Mat(cnt));
}
