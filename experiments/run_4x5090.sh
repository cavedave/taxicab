#!/bin/bash
# run_4x5090.sh -- A047697 search for MIN < n <= MAX on one instance with several RTX 5090s.
#
#   bash run_4x5090.sh            # build + selftest + benchmark, then one process per GPU
#   bash run_4x5090.sh resume     # restart every part from its own progress file
#   bash run_4x5090.sh status     # progress and time split per part
#
# Defaults: 1e22 < n <= 1e23, kmin 5 (override with MIN=... MAX=... KMIN=... TAG=...).
# 1e21..1e22 was run with cabtaxi_gpu_v1.cu (files cab_1e21_1e22_partK.txt, run_1e22_partK.log);
# anything above 1e22 needs v2 (limit 1e24).
# Each GPU g searches part g+1 of NGPU equal-work pieces (--part), writing
#   ~/a047697/cab_${TAG}_partK.txt   and   ~/a047697/run_${TAG}_partK.log
# When every log shows DONE:  cd ~ && tar czf /workspace/a047697_${TAG}.tar.gz a047697
set -euo pipefail
MIN=${MIN:-10000000000000000000000}        # 1e22
MAX=${MAX:-100000000000000000000000}       # 1e23
KMIN=${KMIN:-5}
TAG=${TAG:-1e22_1e23}
DIR=$HOME/a047697; mkdir -p "$DIR"; cd "$(dirname "$0")"
NGPU=$(nvidia-smi --query-gpu=name --format=csv,noheader | wc -l)
MODE=${1:-run}

if [ "$MODE" = "status" ]; then
  for k in $(seq 1 "$NGPU"); do
    L=$DIR/run_${TAG}_part$k.log
    echo "part $k: $(grep -E '^DONE| segments, ' "$L" 2>/dev/null | tail -n 1)"
    echo "        $(grep 'time split' "$L" 2>/dev/null | tail -n 1 | sed 's/^ *//')"
  done
  grep -h ";[6-9];" "$DIR"/cab_${TAG}_part*.txt 2>/dev/null && echo "*** SIX-WAY OR MORE FOUND ***" || true
  exit 0
fi

LOG=$DIR/setup_${TAG}.log
exec > >(tee -a "$LOG") 2>&1
echo "=== $(date -u) run_4x5090.sh $MODE  ($NGPU GPUs)"
nvidia-smi --query-gpu=index,name,memory.total --format=csv,noheader

if [ "$MODE" != "resume" ]; then
  echo "--- build (sm_120)"
  nvcc -O3 -std=c++17 -gencode arch=compute_120,code=sm_120 -o cabtaxi_gpu cabtaxi_gpu.cu
  echo "--- selftest on every GPU"
  for g in $(seq 0 $((NGPU-1))); do
    CUDA_VISIBLE_DEVICES=$g ./cabtaxi_gpu --selftest > "$DIR/selftest_gpu$g.txt"
    grep -q "^\[selftest\] PASSED" "$DIR/selftest_gpu$g.txt" || { cat "$DIR/selftest_gpu$g.txt"; echo "SELFTEST FAILED on GPU $g: stopping"; exit 1; }
    echo "GPU $g selftest PASSED"
  done
  echo "--- benchmark to 1e15 on GPU 0 (must match the CPU program exactly)"
  ./cabtaxi_gpu --max 1000000000000000 --kmin 4 --out "$DIR/bench_1e15_4x.txt" > "$DIR/bench_4x.txt"
  grep -q "raw pairs=13223067998 coprime pairs=8044700766" "$DIR/bench_4x.txt" \
    || { cat "$DIR/bench_4x.txt"; echo "BENCHMARK MISMATCH: stopping"; exit 1; }
  grep "^DONE" "$DIR/bench_4x.txt"
  echo "benchmark OK"
  RESUME=""
else
  RESUME="--resume"
fi

echo "--- launching $NGPU parts: $MIN < n <= $MAX, kmin $KMIN"
for g in $(seq 0 $((NGPU-1))); do
  k=$((g+1))
  nohup ./cabtaxi_gpu --device $g --part $k/$NGPU --min $MIN --max $MAX --kmin $KMIN \
        --out "$DIR/cab_${TAG}_part$k.txt" $RESUME >> "$DIR/run_${TAG}_part$k.log" 2>&1 &
  echo "part $k on GPU $g: pid $!"
done
echo "=== launched. Check with:  TAG=$TAG bash $(pwd)/run_4x5090.sh status"
