#!/bin/bash
# run_lc.sh -- complete line search to 1e30 (six_way_ideas.md idea 1; FINDINGS F47): every coprime collinear triple with
# n <= 1e30 in every allowed direction of cost <= 1.2e12, every n counted exactly; numbers with k >= 4 listed.
# Run in this folder:   nohup bash run_lc.sh > lc.log 2>&1 &
# Resume after a stop:  RESUME=1 nohup bash run_lc.sh >> lc.log 2>&1 &
set -u
GP=${GP:-$HOME/pari/bin/gp}; PROCS=${PROCS:-60}
cd code
python3 -c "import numpy" || { echo "numpy missing: pip3 install --user numpy"; exit 1; }
echo "== selfcheck $(date)"; python3 -u line_complete.py --selfcheck --gp $GP || exit 1
if [ -z "${RESUME:-}" ]; then
  echo "== validation 1e19 $(date)"
  python3 -u line_complete.py --B 1e19 --cmax 1e7 --count --gp $GP --procs $PROCS --chunk 2e5 --out ../val_1e19_k4.txt --log ../val_1e19.log
  echo "   distinct k>=4 numbers: $(grep -v '^#' ../val_1e19_k4.txt | cut -d';' -f1 | sort -u | wc -l)  (expect 263)"
fi
echo "== run 1e30 $(date)"
python3 -u line_complete.py --B 1e30 --cmax 1.2e12 --count --gp $GP --procs $PROCS --chunk 2e7 \
  --out ../lc_1e30_k4.txt --log ../lc_1e30_jobs.log ${RESUME:+--resume}
echo "== all done $(date)"
