# check_jobs.py CODE_DIR lf_jobs.log -- rebuild the planned job list of the lf36_v4 run (B = 10^36, cost <= 1e4, chunk 5e7) with the
# run's own code and compare with the job log: every job once, chunks tiling. Run from inside lf36_v4/code (for gp files).
import sys, collections
code, log = sys.argv[1], sys.argv[2]
sys.path.insert(0, code)
import line_enum as L
from line_fast import job_lines
B = 10**36; chunk = 5e7
dirs = [(a, b) for c, a, b in L.dirs_by_cost(10000, L.allowed_f) if c > 0]
P = L.conic_points(dirs, "gp")
plan = []
for (a, b), P0 in zip(dirs, P):
    for jl in job_lines(a, b, P0, B, chunk): plan.append(tuple(map(str, jl[:4])))
logged = collections.Counter(tuple(l.split(";")[:4]) for l in open(log) if l.strip())
pl = collections.Counter(plan)
print("directions", len(dirs), "planned jobs", len(plan), "distinct", len(pl), "| logged lines", sum(logged.values()), "distinct", len(logged))
print("missing from log", len(pl - logged), "| extra in log", len(logged - pl), "| logged twice", sum(1 for v in logged.values() if v > 1))
# tiling of chunks per direction
by = collections.defaultdict(list)
for a, b, lo, hi in pl: by[(a, b)].append((int(lo), None if hi == "None" else int(hi)))
bad = 0
for d, iv in by.items():
    if len(iv) == 1: continue
    iv.sort()
    if iv[0][0] != 0 or any(iv[i + 1][0] != iv[i][1] + 1 for i in range(len(iv) - 1)): bad += 1
print("directions split into chunks", sum(len(v) > 1 for v in by.values()), "| tiling failures", bad)
tr = sum(int(l.split(";")[5]) for l in open(log) if l.strip())
print("triples in log", tr)
