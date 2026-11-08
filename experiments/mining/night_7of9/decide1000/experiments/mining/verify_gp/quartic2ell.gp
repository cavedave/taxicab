\\ quartic2ell.gp -- v^2 = Q(u) with Q(0) = q0^2 (q0 != 0) to Weierstrass form and back (Washington, Elliptic Curves,
\\ Thm 2.17).  Q = a u^4 + b u^3 + c u^2 + d u + q0^2.
\\   E: y^2 + a1 x y + a3 y = x^3 + a2 x^2 + a4 x + a6, a1 = d/q0, a2 = c - d^2/(4 q0^2), a3 = 2 q0 b, a4 = -4 q0^2 a, a6 = a2 a4
\\   (u, v) -> x = (2 q0 (v + q0) + d u)/u^2, y = (4 q0^2 (v + q0) + 2 q0 (d u + c u^2) - d^2 u^2/(2 q0))/u^3
\\   (x, y) -> u = (2 q0 (x + c) - d^2/(2 q0))/y,  v = -q0 + u (u x - d)/(2 q0)
{
q2e(Q, q0) = my(a = polcoef(Q,4), b = polcoef(Q,3), c = polcoef(Q,2), d = polcoef(Q,1), a2 = c - d^2/(4*q0^2));
  ellinit([d/q0, a2, 2*q0*b, -4*q0^2*a, a2*(-4*q0^2*a)]);
}
{
toE(Q, q0, u, v) = my(c = polcoef(Q,2), d = polcoef(Q,1));
  if(u == 0, [0], [(2*q0*(v + q0) + d*u)/u^2, (4*q0^2*(v + q0) + 2*q0*(d*u + c*u^2) - d^2*u^2/(2*q0))/u^3]);
}
{
toQ(Q, q0, P) = my(c = polcoef(Q,2), d = polcoef(Q,1), u, v);
  if(#P == 1 || P[2] == 0, return(0)); u = (2*q0*(P[1] + c) - d^2/(2*q0))/P[2]; v = -q0 + u*(u*P[1] - d)/(2*q0); [u, v];
}
\\ comps(Em, P, ps): for the minimal model Em and a point P on it, the primes of ps at which P reduces to the singular
\\ point mod p (P not in E_0(Q_p)); a point with v_p(x) < 0 reduces to O, which is non-singular
{
comps(Em, P, ps) = my(out = List(), x, y, fx, fy);
  if(#P == 1, return(Vec(out)));
  x = P[1]; y = P[2];
  foreach(ps, p,
    if(valuation(x, p) < 0, next);
    fx = Em.a1*y - 3*x^2 - 2*Em.a2*x - Em.a4; fy = 2*y + Em.a1*x + Em.a3;
    if(valuation(fx, p) > 0 && valuation(fy, p) > 0 && valuation(y^2 + Em.a1*x*y + Em.a3*y - x^3 - Em.a2*x^2 - Em.a4*x - Em.a6, p) > 0, listput(out, p)));
  Vec(out);
}
