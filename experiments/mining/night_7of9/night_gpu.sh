#!/bin/bash
# night_gpu.sh -- re-find every coprime four-way (and five-way) for 0 < n <= 1e22 at kmin 4 on the 4 GPUs.
#   stage A: 0 - 1e21      (about 1.3e14 raw pairs; the 0 - 1e17 part re-checks the 204 known four-ways)
#   stage B: 1e21 - 1e22   (about 4.8e14 raw pairs)
# Each GPU takes the same quarter (by work) of each stage. Re-running the script skips finished parts and resumes interrupted ones.
# Run:  nohup bash night_gpu.sh > gpu.log 2>&1 &
# Other range (integers):  GMIN=10000000000000000000000 GMAX=100000000000000000000000 GTAG=1e22_1e23 nohup bash night_gpu.sh > gpu.log 2>&1 &
# To stop for the day: pkill -f night_gpu.sh; pkill -f cabtaxi_gpu   -- the same command later resumes every part.
set -u
W=$(pwd); O=$W/gpu; mkdir -p $O
run() {   # device, part, min, max, tag
  local d=$1 p=$2 lo=$3 hi=$4 t=$5
  local f=$O/cab_${t}_part$p.txt
  if grep -q "^DONE" $O/cab_${t}_part$p.log 2>/dev/null; then echo "$t part $p already done"; return; fi
  local R=""; [ -s $f.progress ] && R="--resume"          # continue an interrupted part
  $W/cabtaxi_gpu --device $d --part $p/4 --min $lo --max $hi --kmin 4 --out $f $R >> $O/cab_${t}_part$p.log 2>&1
  echo "GPU $d $t part $p finished $(date): $(grep DONE $O/cab_${t}_part$p.log | tail -1)"
}
GMIN=${GMIN:-}; GMAX=${GMAX:-}; GTAG=${GTAG:-}    # e.g. GMIN=1e22 range: one stage over (GMIN, GMAX], 4 parts
echo "start $(date)"
for d in 0 1 2 3; do
  if [ -n "$GMIN" ]; then ( run $d $((d+1)) $GMIN $GMAX $GTAG ) &
  else
  ( run $d $((d+1)) 0 1000000000000000000000 0_1e21
    run $d $((d+1)) 1000000000000000000000 10000000000000000000000 1e21_1e22 ) &
  fi
done
wait
echo "all GPU stages done $(date)"
