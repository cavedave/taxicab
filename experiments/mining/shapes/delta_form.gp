\\ the branch form of a direction d = (a, b): Q = P + lam (b, -a) is on x^3 + y^3 = n(P) iff A lam^2 + B lam + C = 0,
\\ A = b^3 - a^3, B = 3(x b^2 + y a^2), C = 3(x^2 b - y^2 a); rational lam iff Delta = B^2 - 4AC is a square.
A = b^3 - a^3; B = 3*(x*b^2 + y*a^2); C = 3*(x^2*b - y^2*a);
D = B^2 - 4*A*C;
claim = 3*(b*(4*a^3 - b^3)*x^2 + 6*a^2*b^2*x*y + a*(4*b^3 - a^3)*y^2);
print("Delta = 3 [b(4a^3 - b^3) x^2 + 6 a^2 b^2 x y + a(4b^3 - a^3) y^2]: ", D - claim == 0);
q = claim / 3;
disc = polcoef(polcoef(q, 1, x), 1, y)^2 - 4 * polcoef(polcoef(q, 2, x), 0, y) * polcoef(polcoef(q, 0, x), 2, y);
print("discriminant of the bracket = 16 a b (b^3 - a^3)^2: ", disc - 16*a*b*(b^3 - a^3)^2 == 0);
