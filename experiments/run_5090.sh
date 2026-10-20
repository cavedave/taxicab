#!/bin/bash
# run_5090.sh -- build, verify, benchmark, then extend the A047697 search on one rented RTX 5090.
#
#   bash run_5090.sh              # build + selftest + benchmark + main run (1e19, 1e20]
#   bash run_5090.sh resume       # continue the main run after an interruption
#
# Every stage must pass before the next starts. Results go to ~/a047697/.
# The CPU run already covers n <= 1e19 (no six-way), so the main run starts at 1e19.
set -euo pipefail
MIN=10000000000000000000          # 1e19
MAX=100000000000000000000         # 1e20
DIR=$HOME/a047697; mkdir -p "$DIR"; cd "$(dirname "$0")"
LOG=$DIR/run.log
exec > >(tee -a "$LOG") 2>&1
echo "=== $(date -u) run_5090.sh ${1:-}"
nvidia-smi --query-gpu=name,memory.total,driver_version --format=csv,noheader

if [ "${1:-}" != "resume" ]; then
  echo "--- 1. build (sm_120 = RTX 5090)"
  nvcc -O3 -std=c++17 -gencode arch=compute_120,code=sm_120 -o cabtaxi_gpu cabtaxi_gpu.cu
  echo "--- 2. selftest (brute force, known terms, split ranges, above 2^64)"
  ./cabtaxi_gpu --selftest | tee "$DIR/selftest.txt"
  grep -q "^\[selftest\] PASSED" "$DIR/selftest.txt" || { echo "SELFTEST FAILED: stopping"; exit 1; }
  echo "--- 3. benchmark to 1e15 (must match the CPU program exactly)"
  ./cabtaxi_gpu --max 1000000000000000 --kmin 4 --out "$DIR/bench_1e15.txt" | tee "$DIR/bench.txt"
  grep -q "raw pairs=13223067998 coprime pairs=8044700766" "$DIR/bench.txt" \
    || { echo "BENCHMARK PAIR COUNTS DIFFER FROM CPU REFERENCE: stopping"; exit 1; }
  grep -q "^506433677359393;5;" "$DIR/bench_1e15.txt" || { echo "BENCHMARK MISSED A047697(5): stopping"; exit 1; }
  echo "benchmark OK"
  echo "--- 4. main run: $MIN < n <= $MAX, kmin 5"
  ./cabtaxi_gpu --min $MIN --max $MAX --kmin 5 --out "$DIR/cab_1e19_1e20.txt"
else
  echo "--- resuming main run"
  ./cabtaxi_gpu --min $MIN --max $MAX --kmin 5 --out "$DIR/cab_1e19_1e20.txt" --resume
fi
echo "=== $(date -u) finished. Copy $DIR back before destroying the instance."
grep -c "" "$DIR/cab_1e19_1e20.txt" | awk '{print "result lines (incl. header):", $1}'
grep ";6;" "$DIR/cab_1e19_1e20.txt" && echo "*** SIX-WAY FOUND ***" || echo "no six-way in this range"
