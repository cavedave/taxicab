#!/bin/bash
# Exact counts of the five-ways of results/five_ways_all.txt not yet counted (k >= 5), 151-300 digits (9 Nov 2026).
# The 277 up to 150 digits were counted on the laptop (all k = 5) and are skipped.
#   nohup ./run.sh > run.out 2>&1 &
# Each start runs at most HOURS (default 14.5) and stops cleanly; rerun with RESUME=1 to skip what is done.
set -u
PROCS=${PROCS:-48}; HOURS=${HOURS:-14.5}; GP=${GP:-$HOME/pari/bin/gp}
[ -x "$GP" ] || GP=gp
SKIP="counted_le150_laptop.txt"
[ -n "${RESUME:-}" ] && SKIP="$SKIP $(ls counted_part*.txt 2>/dev/null | tr '\n' ' ')"
PART=$(( $(ls counted_part*.txt 2>/dev/null | wc -l) + 1 ))
echo "== start $(date), part $PART, $PROCS processes, at most $HOURS h"
timeout ${HOURS}h python3 count_bowties.py uncounted_all.txt --out counted_part$PART.txt --maxdig 300 \
  --tlim 1800 --tcount 3600 --procs $PROCS --gp $GP --skip $SKIP > counted_part$PART.log 2>&1
echo "== exit $? $(date)"
