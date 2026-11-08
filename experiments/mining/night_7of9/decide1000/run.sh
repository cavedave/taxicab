#!/bin/bash
# Decider on the 23 lf36 base directions, second directions up to AMAX (F62 did a2, b2 < 100).
#   Stage 1:  STAGE=1 nohup ./run.sh > v2_stage1.out 2>&1 &     pairs with max(a2, b2) < 300 (235,748 curves, ~40 min)
#   Stage 2:  STAGE=2 nohup ./run.sh > v2_stage2a.out 2>&1 &    pairs with 300 <= max(a2, b2) < 1000 (2,093,530 curves)
# Each start runs at most HOURS (default 14.5) and then stops cleanly (GNU timeout kills the whole process group,
# gp included). Starting again with the same STAGE resumes: curves already in the log are skipped. Jobs run in order
# of max(a2, b2), so a stopped run covers every pair below some value. Curves that ended in ERROR (e.g. a gp timeout)
# are rerun on resume. v3: gp calls may take up to 1 h (the periodicity box (2M+1)^r reached 567 MB of output at M 6, rank 5).
set -u
STAGE=${STAGE:-1}; PROCS=${PROCS:-60}; HOURS=${HOURS:-14.5}
export PATH="$HOME/pari/bin:$PATH"
command -v gp > /dev/null || { echo "gp not found"; exit 1; }
case $STAGE in
  1) AMIN=0; AMAX=300 ;;      # v2 redoes < 100 too: F61/F62 used seed height 300
  2) AMIN=300; AMAX=1000 ;;
  *) echo "STAGE must be 1 or 2"; exit 1 ;;
esac
BASES="3,4 1,4 4,7 12,13 4,9 7,12 1,12 13,16 4,13 27,28 16,19 9,16 7,16 36,37 3,16 1,16 12,19 16,21 25,28 4,19 48,49 28,31 4,21"
OUT=$PWD/v2_stage$STAGE      # v2: seed height 1e5 (v1's 300 missed (1,12)+(49,192), a point of height 7,349)
cd experiments/mining
echo "== stage $STAGE start $(date), $PROCS processes, at most $HOURS h"
timeout ${HOURS}h python3 -u bowtie_decide.py --base $BASES --amin $AMIN --amax $AMAX --seedh 100000 --npts 2000 --gptime 3600 \
  --procs $PROCS --log $OUT.log --out $OUT.txt --resume
rc=$?
if [ $rc -eq 124 ]; then echo "== stopped at the time limit $(date): start again with STAGE=$STAGE to resume"
else echo "== stage $STAGE finished (exit $rc) $(date)"; fi
