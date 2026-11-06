#!/bin/bash
# solo_band.sh -- one direction, very high slope height, in bands of s so the triple file stays small.
# Each band (S_MIN <= s <= S_MAX, |r| <= HEIGHT) is enumerated on all threads, counted exactly, kept as
# multi_<dir>_<band>.txt (n with >= 4 representations), then its triple file is deleted. Restartable.
# Slopes with max(|r|, s) <= OLD and n <= 1e40 are skipped (already searched by deep_cpu.sh).
#
#   DIR=3,4 HEIGHT=30000 OLD=15000 BAND=2500 PROCS=80 nohup bash solo_band.sh > /dev/null 2>&1 &
#   bash solo_band.sh status
set -euo pipefail
cd "$(dirname "$0")"
DIR=${DIR:-3,4}; HEIGHT=${HEIGHT:-30000}; OLD=${OLD:-15000}; BAND=${BAND:-2500}
PROCS=${PROCS:-$(( $(nproc) - 8 ))}; GP=${GP:-$(command -v gp || true)}
OUT=$HOME/linesearch/solo_${DIR/,/_}_h$HEIGHT; mkdir -p "$OUT"

if [ "${1:-run}" = "status" ]; then
  grep -E "^band|DONE" "$OUT/solo.log" 2>/dev/null | tail -n 30
  echo "five-ways or better so far:"; cat "$OUT"/multi_*.txt 2>/dev/null | awk -F';' '$2>=5' | cut -d';' -f1,2 | sort -u
  exit 0
fi
[ -n "$GP" ] || { echo "PARI/GP not found: apt-get install -y pari-gp"; exit 1; }

exec >> "$OUT/solo.log" 2>&1
echo "=== $(date -u) solo_band.sh ($DIR) height $HEIGHT, skip <= $OLD, band $BAND, $PROCS processes"
for (( lo=0; lo<=HEIGHT; lo+=BAND )); do
  hi=$(( lo + BAND - 1 < HEIGHT ? lo + BAND - 1 : HEIGHT ))
  [ -f "$OUT/done_$lo" ] && continue
  T0=$(date +%s)
  nice -n 19 python3 line_enum.py --gp "$GP" --only "$DIR" --chunks "$PROCS" --height "$HEIGHT" --nmax 1e40 \
      --s-min $lo --s-max $hi --old-height "$OLD" --old-nmax 1e40 --hero 4 --core 0 --procs "$PROCS" \
      --out "$OUT/lines_$lo.txt" > "$OUT/enum_$lo.log"
  T1=$(date +%s)
  nice -n 19 python3 cheap_search.py "$OUT/lines_$lo.txt" --gp "$GP" --procs "$PROCS" --rmin 4 \
      --out "$OUT/multi_$lo.txt" > "$OUT/count_$lo.log"
  T2=$(date +%s)
  touch "$OUT/multi_$lo.txt"
  echo "band s=$lo..$hi: $(tail -n 1 "$OUT/count_$lo.log" | sed 's/^ *//')  enum $((T1-T0))s count $((T2-T1))s"
  awk -F';' '$2>=5 {print "  *** " $1 " has " $2 " representations"}' "$OUT/multi_$lo.txt"
  rm -f "$OUT/lines_$lo.txt"; touch "$OUT/done_$lo"
done
echo "=== $(date -u) DONE"
