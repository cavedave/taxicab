\r tri_decide.gp
\\ every triple of the 23 lf36 base directions and their swaps (46 directions)
B = [[1,4],[1,12],[1,16],[3,4],[3,16],[4,7],[4,9],[4,13],[4,19],[4,21],[7,12],[7,16],[9,16],[12,13],[12,19],[13,16],[16,19],[16,21],[25,28],[27,28],[28,31],[36,37],[48,49]];
runall(Dl) = {
  my(cnt = 0, hits = 0, deg = 0, t0 = getwalltime());
  forsubset([#Dl, 3], s,
    my(D = vecextract(Dl, s), S);
    cnt++; S = tri(D);
    foreach(S, c,
      if(c === "DEGENERATE", deg++; next);
      my(T = six(D, c));
      if(T,
        hits++;
        my(st = status(T));
        print("TRI ", D, " n0 ", T[1], ": distinct reps ", st[1], ", distinct denominators ", st[2], ", coprime six-way ", st[3]))));
  printf("%d triples, %d rational triangles, %d degenerate, %d ms\n", cnt, hits, deg, getwalltime() - t0);
}
runall(concat(B, apply(d -> [d[2], d[1]], B)));
