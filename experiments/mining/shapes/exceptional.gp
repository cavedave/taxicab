\\ when do two directions share a branch point (Lemma 20b)? resultant of the bracket forms q_d1(x, 1), q_d2(x, 1)
q(a, b) = b*(4*a^3 - b^3)*x^2 + 6*a^2*b^2*x + a*(4*b^3 - a^3);
R = polresultant(q(a1, b1), q(a2, b2), x);
F = factor(R);
print("resultant of q_d1, q_d2 factors as:");
for(i = 1, #F~, print("   ", F[i, 1], "   ^", F[i, 2]));
