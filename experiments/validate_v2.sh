#!/bin/bash
# validate_v2.sh -- one-GPU check of cabtaxi_gpu.cu (v2: select + bit-limited sort + 1e24 limit)
# against the frozen cabtaxi_gpu_v1.cu that produced the 1e19..1e22 results.  About 30 minutes.
#
#   bash validate_v2.sh            # needs cabtaxi_gpu.cu and cabtaxi_gpu_v1.cu next to it
#
# Steps (any failure stops the script):
#   1. build both (sm_120)
#   2. v2 selftest (includes windows below 1e22, 1e23, 1e24 checked against window_count.py)
#   3. 1e15 benchmark, kmin 4: v1 and v2 outputs byte-identical, pair counts as before
#   4. A/B on 1.03e21 < n <= 1.05e21 (contains the five-way 1038246186276942167105): identical
#      outputs and pair counts; the speed-up is the ratio of the two times
#   5. v2 alone on 5e22 < n <= 5.01e22: speed at the scale of the next run
# Everything goes to ~/a047697/validate_v2/ ; summary in summary.txt
set -euo pipefail
D=$HOME/a047697/validate_v2; mkdir -p "$D"; cd "$(dirname "$0")"
exec > >(tee -a "$D/summary.txt") 2>&1
echo "=== $(date -u) validate_v2.sh"
nvidia-smi --query-gpu=index,name,memory.total --format=csv,noheader
md5sum cabtaxi_gpu.cu cabtaxi_gpu_v1.cu

echo "--- 1. build"
nvcc -O3 -std=c++17 -gencode arch=compute_120,code=sm_120 -o cabtaxi_gpu cabtaxi_gpu.cu
nvcc -O3 -std=c++17 -gencode arch=compute_120,code=sm_120 -o cabtaxi_gpu_v1 cabtaxi_gpu_v1.cu

echo "--- 2. selftest (v2)"
./cabtaxi_gpu --selftest | tee "$D/selftest.txt"
grep -q "^\[selftest\] PASSED" "$D/selftest.txt" || { echo "SELFTEST FAILED"; exit 1; }

run() {  # run <binary> <tag> <args...>: prints the DONE line, keeps output and log
  local bin=$1 tag=$2; shift 2
  "./$bin" "$@" --out "$D/$tag.txt" > "$D/$tag.log"
  grep "^DONE" "$D/$tag.log"; grep "^time split" "$D/$tag.log" || true
}
same() {  # same <tag1> <tag2>: result files and pair counts must agree
  cmp "$D/$1.txt" "$D/$2.txt" || { echo "OUTPUT DIFFERS: $1 vs $2"; exit 1; }
  local p1 p2
  p1=$(grep -o "raw pairs=[0-9]* coprime pairs=[0-9]*" "$D/$1.log")
  p2=$(grep -o "raw pairs=[0-9]* coprime pairs=[0-9]*" "$D/$2.log")
  [ "$p1" = "$p2" ] || { echo "PAIR COUNTS DIFFER: $p1 vs $p2"; exit 1; }
  echo "identical: $1 = $2 ($p1, $(grep -vc '^#' "$D/$1.txt") numbers)"
}
secs() { grep -o "time=[0-9]*s" "$D/$1.log" | tr -dc 0-9; }

echo "--- 3. 1e15 benchmark, kmin 4"
run cabtaxi_gpu_v1 bench_v1 --max 1000000000000000 --kmin 4
run cabtaxi_gpu    bench_v2 --max 1000000000000000 --kmin 4
grep -q "raw pairs=13223067998 coprime pairs=8044700766" "$D/bench_v2.log" || { echo "BENCHMARK MISMATCH"; exit 1; }
same bench_v1 bench_v2

echo "--- 4. A/B on 1.03e21 < n <= 1.05e21"
run cabtaxi_gpu_v1 ab_v1 --min 1030000000000000000000 --max 1050000000000000000000 --kmin 5
run cabtaxi_gpu    ab_v2 --min 1030000000000000000000 --max 1050000000000000000000 --kmin 5
same ab_v1 ab_v2
grep -q "^1038246186276942167105;5;" "$D/ab_v2.txt" || { echo "KNOWN FIVE-WAY MISSING"; exit 1; }
echo "speed-up v1 -> v2 at 1e21: $(secs ab_v1) s -> $(secs ab_v2) s = $(awk "BEGIN{printf \"%.2f\", $(secs ab_v1)/$(secs ab_v2)}")x"

echo "--- 5. v2 at 5e22"
run cabtaxi_gpu speed_5e22 --min 50000000000000000000000 --max 50100000000000000000000 --kmin 5
echo "=== $(date -u) ALL CHECKS PASSED"
