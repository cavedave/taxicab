\\ triangle on the bowtie curve (3,4)+(9,52), shared point = raw point 0, line 2 direction (a2, b2) = (9, 52).
\\ Sixth point R = third point of the chord through B (raw point j = 1 or 2) and C (a line-2 point); by Theorem 8a its
\\ denominator comes from Den = x_B y_B - x_C y_C. Reduce w^2 = Delta: Den = alpha + beta w; norm N = alpha^2 - beta^2 Delta.
\\ Siegel needs N to have >= 3 distinct roots (points at infinity of (c - alpha)^2 = beta^2 Delta).
\r raw34.gp
a2 = 9; b2 = 52; A = b2^3 - a2^3;
Bt = 3*(X0*b2^2 + Y0*a2^2); Ct = 3*(X0^2*b2 - Y0^2*a2); Delta = Bt^2 - 4*A*Ct;
red(f) = { my(c0 = polcoef(f, 0, w), c1 = polcoef(f, 1, w), c2 = polcoef(f, 2, w), c3 = polcoef(f, 3, w), c4 = polcoef(f, 4, w));
           [c0 + c2*Delta + c4*Delta^2, c1 + c3*Delta]; }      \\ alpha + beta w
nrm(f) = { my(v = red(f)); v[1]^2 - v[2]^2*Delta; }
Xc = 2*A*X0 + (-Bt + w)*b2; Yc = 2*A*Y0 - (-Bt + w)*a2;
{
  foreach([1, 2], j,
    my(Xb = 2*A*eval(Str("X", j)), Yb = 2*A*eval(Str("Y", j)), Den, Nx, Ny, N, sq, dN, rx);
    Den = Xb*Yb - Xc*Yc;
    Nx = Xc^2*Yb - Xb^2*Yc; Ny = Xb*Yc^2 - Xc*Yb^2;
    N = nrm(Den); sq = N / gcd(N, deriv(N));
    dN = poldegree(sq);
    rx = polresultant(N / content(N), nrm(Nx) / content(nrm(Nx)));
    printf("B = raw point %d: norm of Den has degree %d in r, %d distinct finite roots%s; resultant with the norm of the x-numerator %s\n",
           j, poldegree(N), dN, if(poldegree(N) < 8, " (+ root at infinity)", ""), if(rx == 0, "= 0 (shared factor!)", "!= 0"));
  );
}
\\ remove the common factor: G = gcd of the norms of Den, Nx, Ny; the reduced denominator's norm is N_Den / G
{
  foreach([1, 2], j,
    my(Xb = 2*A*eval(Str("X", j)), Yb = 2*A*eval(Str("Y", j)), Den, Nx, Ny, ND, G, Nr, sq);
    Den = Xb*Yb - Xc*Yc; Nx = Xc^2*Yb - Xb^2*Yc; Ny = Xb*Yc^2 - Xc*Yb^2;
    ND = nrm(Den); G = gcd(gcd(ND, nrm(Nx)), nrm(Ny)); Nr = ND / G; sq = Nr / gcd(Nr, deriv(Nr));
    printf("B = raw point %d: common factor of degree %d (%s); reduced denominator norm: degree %d, %d distinct roots\n",
           j, poldegree(G), Str(factor(G)[,1]~), poldegree(Nr), poldegree(sq));
  );
}
