#!/usr/bin/env python3
"""max_lines.py -- the most lines k coprime representations can carry (patterns realisable in the sense of
line_patterns.py: the system q_a + q_b + q_c = 0 forces no q_i = 0, q_i = q_j, q_i = -q_j). Realisability is closed under
removing lines, so a DFS adding lines in lexicographic order, pruning impossible patterns, finds the maximum."""
import sys, itertools, time
sys.path.insert(0, 'shapes')
from line_patterns import kernel
def possible(k, lines):
    if not lines: return True
    K = kernel([[1 if i in L else 0 for i in range(k)] for L in lines], k)
    Q = [tuple(b[i] for b in K) for i in range(k)]
    if any(all(x == 0 for x in q) for q in Q): return False
    for i, j in itertools.combinations(range(k), 2):
        if Q[i] == Q[j] or all(a == -b for a, b in zip(Q[i], Q[j])): return False
    return True
def best(k, deadline):
    triples = list(itertools.combinations(range(k), 3)); top = [0, []]
    def dfs(start, lines):
        if time.time() > deadline: return
        if len(lines) > top[0]: top[0], top[1] = len(lines), list(lines)
        if len(lines) + (len(triples) - start) <= top[0]: return
        for t in range(start, len(triples)):
            T = triples[t]
            if any(len(set(T) & set(L)) > 1 for L in lines): continue
            lines.append(T)
            if possible(k, lines): dfs(t + 1, lines)
            lines.pop()
    dfs(0, []); return top
if __name__ == "__main__":
    for k in range(3, 10):
        t0 = time.time(); m, ex = best(k, t0 + 300)
        done = time.time() - t0 < 300
        print(f"k = {k}: at most {m} lines{'' if done else ' (time limit hit: lower bound)'}  e.g. {ex}  ({time.time() - t0:.1f} s)", flush=True)
