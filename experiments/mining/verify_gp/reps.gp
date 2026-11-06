\\ reps.gp -- independent recount (PARI/GP only, no code shared with the searches): every coprime (x, y), x >= y,
\\ with x^3 + y^3 = n.  s = x + y divides n and s^3 <= 4n; then 4n/s - s^2 = 3 d^2, x = (s + d)/2, y = (s - d)/2.
reps(n) = {
  my(L = List(), D = divisors(n), t, m, d, x, y);
  foreach(D, s,
    if(s^3 > 4*n, next);
    t = 4*(n/s) - s^2; if(t < 0 || t % 3, next);
    m = t/3; if(!issquare(m, &d), next);
    if((s + d) % 2, next);
    x = (s + d)/2; y = (s - d)/2;
    if(y == 0 || gcd(x, y) != 1 || x^3 + y^3 != n, next);
    listput(L, [x, y]));
  vecsort(Vec(L), , 4);
}
\\ repsf(n, f): the same, with the factorisation f of n supplied (divisors from f; for n too large to factor directly)
repsf(n, f) = {
  my(L = List(), D = divisors(f), t, m, d, x, y);
  foreach(D, s,
    if(s^3 > 4*n, next);
    t = 4*(n/s) - s^2; if(t < 0 || t % 3, next);
    m = t/3; if(!issquare(m, &d), next);
    if((s + d) % 2, next);
    x = (s + d)/2; y = (s - d)/2;
    if(y == 0 || gcd(x, y) != 1 || x^3 + y^3 != n, next);
    listput(L, [x, y]));
  vecsort(Vec(L), , 4);
}
