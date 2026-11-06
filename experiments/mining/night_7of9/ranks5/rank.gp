\\ rank.gp -- rank of x^3 + y^3 = N (Weierstrass Y^2 = X^3 - 432 N^2) with the integral points as hints
toW(N,x,y) = my(s = x + y); [12*N/s, 36*N*(x - y)/s];
{
rk(tag, grp, N, P) = my(E = ellinit([0,0,0,0,-432*N^2]), t = getabstime(), K = vector(#P, i, toW(N, P[i][1], P[i][2])), R);
  R = iferr(alarm(TLIM, ellrank(E, 0, K)), err, [-1,-1,0,[]]);
  print(tag, ";", grp, ";", N, ";", #P, ";", R[1], ";", R[2], ";", getabstime() - t);
}
