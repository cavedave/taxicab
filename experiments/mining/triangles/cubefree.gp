\r tri_decide.gp
\r hits150.gp
cf(q) = { my(F = factor(q), m = 1); for(k = 1, #F~, m *= F[k,1]^(F[k,2] % 3)); m; }
M = Map(); seen = Map();
{ foreach(H, D, foreach(tri(D), c, if(c === "DEGENERATE", next); my(T = six(D, c)); if(T,
    my(q = numerator(T[1]) * denominator(T[1])^2, m = cf(q), L = lcm(apply(p -> lcm(denominator(p[1]), denominator(p[2])), T[2])));
    if(mapisdefined(M, m), mapput(M, m, mapget(M, m) + 1), mapput(M, m, 1));
    printf("m %d  lcm of denominators %d  D %s\n", m, L, D)))); }
print("triangles per cube-free m: ", Mat(M));
