\\ smoke_ellrank.gp -- PARI/GP smoke test for the elliptic-curve splitting-factor recipe
\\
\\ Run:  gp -q experiments/smoke_ellrank.gp
\\
\\ The curve x^3 + y^3 = N is handled in Weierstrass form Y^2 = X^3 - 432 N^2 via
\\   X = 12N/(x+y),  Y = 36N(x-y)/(x+y)      and back      x,y = (36N +- Y)/(6X).
\\ A rational point (u/w, v/w) with u,v > 0 means N*w^3 = u^3 + v^3: w is a splitting factor.
\\
\\ Test 1: 1729. ellrank should report rank 2 (Silverman 1993 expects generators (1,12), (9,10)).
\\ Test 2: Ta(5). Rank >= 5 (our Python test: its 5 integer points span only rank 4, the
\\         m=79 point is independent). Pass = the positive points from small combinations of the
\\         generators reproduce Boyer's splitting factors {79,127,139,727,4622} (JIS 2008, Fig. A3).

default(parisizemax, 4*10^9);
print("PARI/GP version: ", version());
if(lex(version()[1..2], [2,15]) < 0, error("need PARI/GP >= 2.15 (ellrank)"));

Wcurve(N) = ellinit([0,0,0,0,-432*N^2]);
toW(N,x,y) = my(s = x + y); [12*N/s, 36*N*(x - y)/s];
toXY(N,P) = [(36*N + P[2])/(6*P[1]), (36*N - P[2])/(6*P[1])];

\\ positive points among sum c_i G_i, |c_i| <= C; returns sorted denominators <= wmax
splitfactors(E, N, G, C, wmax) =
{
  my(r = #G, S = List(), P, xy, w);
  forvec(v = vector(r, i, [-C, C]),
    P = [0];
    for(i = 1, r, if(v[i], P = elladd(E, P, ellmul(E, G[i], v[i]))));
    if(P == [0], next);
    xy = toXY(N, P);
    if(xy[1] > 0 && xy[2] > 0,
      w = lcm(denominator(xy[1]), denominator(xy[2]));
      if(w <= wmax, listput(S, w))));
  vecsort(Vec(S), , 8);   \\ 8 = remove duplicates
}

\\ ---- Test 1: 1729 ----
{
  my(N = 1729, E = Wcurve(N), t = getabstime(), R);
  R = ellrank(E);
  printf("\n[1729] rank between %d and %d, %d points found (%d ms)\n",
         R[1], R[2], #R[4], getabstime() - t);
  if(R[1] == 2 && R[2] == 2, print("[1729] PASS: rank 2"), print("[1729] CHECK: expected rank 2"));
}

\\ ---- Test 2: Ta(5) ----
{
  my(N = 48988659276962496, E = Wcurve(N), t, R, G, F, boyer = [79,127,139,727,4622], known);
  known = [toW(N,38787,365757), toW(N,107839,362753), toW(N,205292,342952),
           toW(N,221424,336588), toW(N,231518,331954), toW(N,582162/79,28906206/79)];
  for(i = 1, #known, if(!ellisoncurve(E, known[i]), error("known point ", i, " not on curve")));
  print("\n[Ta5] all 6 known points are on the curve");
  t = getabstime();
  R = ellrank(E, 1, known);
  printf("[Ta5] ellrank: rank between %d and %d, %d independent points (%d s)\n",
         R[1], R[2], #R[4], (getabstime() - t)\1000);
  t = getabstime();
  G = ellsaturation(E, R[4], 1000);
  printf("[Ta5] saturated at primes <= 1000 (%d s)\n", (getabstime() - t)\1000);
  print("[Ta5] generator heights: ", strjoin(apply(P -> strprintf("%.3f", ellheight(E, P)), G), ", "));
  t = getabstime();
  F = splitfactors(E, N, G, 2, 10000);
  printf("[Ta5] positive-point denominators <= 10000 from |c_i| <= 2: %s (%d s)\n",
         F, (getabstime() - t)\1000);
  if(#setminus(Set(boyer), Set(F)) == 0,
    print("[Ta5] PASS: all of Boyer's splitting factors ", boyer, " found"),
    print("[Ta5] MISSING: ", setminus(Set(boyer), Set(F)),
          "  (try a larger C in splitfactors, or the rank is not fully known)"));
}
quit;
