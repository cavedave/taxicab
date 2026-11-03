TLIM=900;
default(parisizemax, 2*10^9);
toW(N,x,y) = my(s = x + y); [12*N/s, 36*N*(x - y)/s];
{
rk(N, P) = my(E = ellinit([0,0,0,0,-432*N^2]), t = getabstime(), K = vector(#P, i, toW(N, P[i][1], P[i][2])), R);
  R = iferr(alarm(TLIM, ellrank(E, 0, K)), err, [-1,-1,0,[]]);
  print(N, ";", R[1], ";", R[2], ";", #P, ";", getabstime() - t);
}
