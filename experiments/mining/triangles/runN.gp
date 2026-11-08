\r tri_decide.gp
runN(Dl, tag) = {
  my(cnt = 0, hits = 0, cop = 0, t0 = getwalltime(), rt = Map());
  forsubset([#Dl, 3], s,
    my(D = vecextract(Dl, s), S);
    cnt++; S = tri(D);
    foreach(S, c,
      if(c === "DEGENERATE", next);
      my(T = six(D, c));
      if(T,
        hits++;
        my(st = status(T), m = core(numerator(T[1]) * denominator(T[1])^2));
        if(st[3] && st[1] == 6, cop++; print("*** COPRIME TRIANGLE SIX-WAY ", D, " n0 ", T[1]));
        print("TRI ", D, " core ", m, " reps ", st[1], " dens ", st[2]))));
  printf("%s: %d directions (with swaps), %d triples, %d rational triangles, %d coprime six-ways, %d s\n", tag, #Dl, cnt, hits, cop, (getwalltime() - t0) \ 1000);
}
