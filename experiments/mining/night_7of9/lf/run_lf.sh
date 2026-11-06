#!/bin/bash
# run_lf.sh -- complete line search with the C++ inner loops (line_fast.py + lc_fast.cpp; FINDINGS F50).
# Run in this folder:   nohup bash run_lf.sh > lf.log 2>&1 &
# Defaults: every allowed direction with cost <= 1.2e12, n <= 1e33.  Smaller first test:  CMAX=1e4 nohup bash run_lf.sh ...
# Resume after a stop:  RESUME=1 nohup bash run_lf.sh >> lf.log 2>&1 &
set -u
GP=${GP:-$HOME/pari/bin/gp}; PROCS=${PROCS:-60}; CMAX=${CMAX:-1.2e12}; BOUND=${BOUND:-1e33}
cd code
python3 -c "import numpy" || { echo "numpy missing: pip3 install --user numpy"; exit 1; }
g++ -O2 -std=c++17 -o lc_fast lc_fast.cpp || exit 1
if [ -z "${RESUME:-}" ]; then
  echo "== selfcheck (Python reference) $(date)"; python3 -u line_complete.py --selfcheck --gp $GP || exit 1
  echo "== validation: C++ against Python at 1e19, cost <= 1e7 $(date)"
  python3 -u line_complete.py --B 1e19 --cmax 1e7 --gp $GP --procs $PROCS --chunk 2e5 --out ../val_py_T.txt > /dev/null
  python3 -u line_fast.py --B 1e19 --cmax 1e7 --triples --gp $GP --procs $PROCS --chunk 2e5 --out ../val_cpp_T.txt
  python3 - <<'PY' || exit 1
py = {(l.split(";")[0], frozenset(tuple(sorted(map(int, q.split(":")))) for q in l.strip().split(";")[4].split(","))) for l in open("../val_py_T.txt") if l[0].isdigit()}
cc = {(l.split(";")[0], frozenset(tuple(sorted(map(int, q.split(":")))) for q in l.strip().split(";")[1].split(","))) for l in open("../val_cpp_T.txt") if l[0].isdigit()}
print("   triples: python", len(py), "C++", len(cc), "identical", py == cc)
raise SystemExit(0 if py == cc and len(py) == 196358 else 1)
PY
fi
echo "== run n <= $BOUND, cost <= $CMAX $(date)"
python3 -u line_fast.py --B $BOUND --cmax $CMAX --gp $GP --procs $PROCS --chunk 5e7 \
  --out ../lf_k4.txt --log ../lf_jobs.log ${RESUME:+--resume}
echo "== all done $(date)"
