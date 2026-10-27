#!/bin/bash
# deep_cpu.sh -- deep line search (FINDINGS F26 method) on the spare CPU threads of a GPU rental.
# One direction at a time: enumerate its slopes up to HEIGHT (all threads), count the candidates exactly,
# keep only n with >= 4 representations, delete the big triple file, move on.
# Runs at nice 19 so the GPU search's own host threads always come first.
#
#   bash deep_cpu.sh            # needs python3 and PARI/GP (apt-get install -y pari-gp)
#   bash deep_cpu.sh status     # what has finished, and every five-way or better so far
#
# Directions: the 30 cheapest allowed ones plus (12,49) and (57,64) (F24/F26). Slope regions already searched
# are skipped: the 8 deep-search directions to height 4000 / n <= 1e40, all others to 600 / n <= 1e32.
# Output in ~/linesearch/: multi_A_B.txt (n;k;reps for k >= 4), deep_cpu.log (per-direction counts).
set -euo pipefail
cd "$(dirname "$0")"
OUT=$HOME/linesearch; mkdir -p "$OUT"
HEIGHT=${HEIGHT:-12000}
PROCS=${PROCS:-$(( $(nproc) - 8 ))}
GP=${GP:-$(command -v gp || true)}

if [ "${1:-run}" = "status" ]; then
  grep -E "^\(|DONE" "$OUT/deep_cpu.log" 2>/dev/null | tail -n 40
  echo "five-ways or better so far:"; cat "$OUT"/multi_*.txt 2>/dev/null | awk -F';' '$2>=5' | cut -d';' -f1,2 | sort -u
  exit 0
fi
[ -n "$GP" ] || { echo "PARI/GP not found: apt-get install -y pari-gp"; exit 1; }

DEEP8=" 3,4 12,13 12,19 3,16 36,37 12,49 57,64 48,49 "
DIRS=$(python3 -c "import line_enum as L; print(' '.join(f'{a},{b}' for a,b in L.directions(30)))")" 12,49 57,64"

exec >> "$OUT/deep_cpu.log" 2>&1
echo "=== $(date -u) deep_cpu.sh height $HEIGHT, $PROCS processes, gp $GP"
for d in $DIRS; do
  t="${d/,/_}"
  [ -f "$OUT/done_$t" ] && continue                      # finished in an earlier (interrupted) run
  if [[ "$DEEP8" == *" $d "* ]]; then OH=4000; ON=1e40; else OH=600; ON=1e32; fi
  T0=$(date +%s)
  nice -n 19 python3 line_enum.py --gp "$GP" --only "$d" --chunks "$PROCS" --height "$HEIGHT" --nmax 1e40 \
      --old-height $OH --old-nmax $ON --hero 4 --core 0 --procs "$PROCS" --out "$OUT/lines_$t.txt" > "$OUT/enum_$t.log"
  T1=$(date +%s)
  nice -n 19 python3 cheap_search.py "$OUT/lines_$t.txt" --gp "$GP" --procs "$PROCS" --rmin 4 \
      --out "$OUT/multi_$t.txt" > "$OUT/count_$t.log"
  T2=$(date +%s)
  touch "$OUT/multi_$t.txt"
  echo "($d) skip<=$OH: $(tail -n 1 "$OUT/count_$t.log" | sed 's/^ *//')  enum $((T1-T0))s count $((T2-T1))s"
  awk -F';' '$2>=5 {print "  *** " $1 " has " $2 " representations"}' "$OUT/multi_$t.txt"
  rm -f "$OUT/lines_$t.txt"; touch "$OUT/done_$t"
done
echo "=== $(date -u) DONE"
