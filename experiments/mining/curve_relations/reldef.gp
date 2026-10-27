default(parisizemax, 2*10^9); default(realprecision, 60);
toW(N,x,y) = my(s = x + y); [12*N/s, 36*N*(x - y)/s];
{
rel(N, P) = my(E = ellinit([0,0,0,0,-432*N^2]), K = vector(#P, i, toW(N, P[i][1], P[i][2])), H, U, out = List(), r, Q);
  H = ellheightmatrix(E, K);
  U = qflll(matconcat([matid(#K); round(H * 10^20)]));
  for(j = 1, #U, my(v = U[,j]); if(normlp(v, oo) > 1000 || abs(v~ * H * v) > 10^-12, next); Q = [0];
      for(i = 1, #K, if(v[i], Q = elladd(E, Q, ellmul(E, K[i], v[i]))));
      if(Q == [0], listput(out, v~)));
  r = #K - #out;
  print(N, ";", #K, ";", r, ";", Vec(out));
}
