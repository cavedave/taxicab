\r triangle_norm.gp
\\ identify the common factor H: which natural quantity has norm proportional to G = 8251 r^2 + 11059 r + 13867 (or a power)?
G = 8251*r^2 + 11059*r + 13867;
{
  my(Xb = 2*A*X1, Yb = 2*A*Y1, cands = [["x_B - x_C", Xb - Xc], ["y_B - y_C", Yb - Yc], ["s_B - s_C", (Xb + Yb) - (Xc + Yc)],
        ["x_B y_C - x_C y_B", Xb*Yc - Xc*Yb], ["x_B + y_B (s_B)", Xb + Yb], ["s_C", Xc + Yc], ["x_C", Xc], ["y_C", Yc]]);
  foreach(cands, c, my(N = nrm(c[2]), g = gcd(N, G), v = 0, NN = N);
    while(poldegree(gcd(NN, G)) == 2 && poldegree(NN) >= 2, NN = NN / G; v++);
    printf("%-22s norm degree %2d; G divides it to power %d\n", c[1], poldegree(N), v));
}
