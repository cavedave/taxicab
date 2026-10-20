#!/bin/bash
# validate_v3.sh -- one-GPU check of cabtaxi_gpu.cu (v3: 32-bit gcd on a running remainder, 64-bit
# steps, warp-interleaved writes) against the frozen v1 (produced the 1e19..1e22 results) and v2
# (select + bit-limited sort, validated 19 Oct 2026).  About 35 minutes.
#
#   bash validate_v3.sh     # needs cabtaxi_gpu.cu, cabtaxi_gpu_v1.cu, cabtaxi_gpu_v2.cu next to it
#
# Steps (any failure stops the script):
#   1. build all three (sm_120)
#   2. v3 selftest (includes windows below 1e22, 1e23, 1e24 checked against window_count.py)
#   3. 1e15 benchmark, kmin 4: v1, v2, v3 outputs byte-identical, pair counts as before
#   4. 1.03e21 < n <= 1.05e21 (contains the five-way 1038246186276942167105) with v1, v2, v3:
#      identical outputs and pair counts; speed-ups from the times
#   5. 5e22 < n <= 5.01e22 with v2 and v3: identical, and the speed at the scale of the next run
#   6. optional Nsight Compute profile of the v3 write kernel (skipped if ncu or counters are unavailable)
# Everything goes to ~/a047697/validate_v3/ ; summary in summary.txt
set -euo pipefail
D=$HOME/a047697/validate_v3; mkdir -p "$D"; cd "$(dirname "$0")"
exec > >(tee -a "$D/summary.txt") 2>&1
echo "=== $(date -u) validate_v3.sh"
nvidia-smi --query-gpu=index,name,memory.total --format=csv,noheader
md5sum cabtaxi_gpu.cu cabtaxi_gpu_v1.cu cabtaxi_gpu_v2.cu

echo "--- 1. build"
nvcc -O3 -std=c++17 -gencode arch=compute_120,code=sm_120 -o cabtaxi_gpu cabtaxi_gpu.cu
nvcc -O3 -std=c++17 -gencode arch=compute_120,code=sm_120 -o cabtaxi_gpu_v1 cabtaxi_gpu_v1.cu
nvcc -O3 -std=c++17 -gencode arch=compute_120,code=sm_120 -o cabtaxi_gpu_v2 cabtaxi_gpu_v2.cu

echo "--- 2. selftest (v3)"
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
ratio() { awk "BEGIN{printf \"%.2f\", $(secs $1)/$(secs $2)}"; }

echo "--- 3. 1e15 benchmark, kmin 4"
run cabtaxi_gpu_v1 bench_v1 --max 1000000000000000 --kmin 4
run cabtaxi_gpu_v2 bench_v2 --max 1000000000000000 --kmin 4
run cabtaxi_gpu    bench_v3 --max 1000000000000000 --kmin 4
grep -q "raw pairs=13223067998 coprime pairs=8044700766" "$D/bench_v3.log" || { echo "BENCHMARK MISMATCH"; exit 1; }
same bench_v1 bench_v2; same bench_v1 bench_v3

echo "--- 4. v1 / v2 / v3 on 1.03e21 < n <= 1.05e21"
run cabtaxi_gpu_v1 ab_v1 --min 1030000000000000000000 --max 1050000000000000000000 --kmin 5
run cabtaxi_gpu_v2 ab_v2 --min 1030000000000000000000 --max 1050000000000000000000 --kmin 5
run cabtaxi_gpu    ab_v3 --min 1030000000000000000000 --max 1050000000000000000000 --kmin 5
same ab_v1 ab_v2; same ab_v1 ab_v3
grep -q "^1038246186276942167105;5;" "$D/ab_v3.txt" || { echo "KNOWN FIVE-WAY MISSING"; exit 1; }
echo "at 1e21: v1 $(secs ab_v1) s, v2 $(secs ab_v2) s, v3 $(secs ab_v3) s; v3 vs v1 $(ratio ab_v1 ab_v3)x, v3 vs v2 $(ratio ab_v2 ab_v3)x"

echo "--- 5. v2 / v3 on 5e22 < n <= 5.01e22"
run cabtaxi_gpu_v2 big_v2 --min 50000000000000000000000 --max 50100000000000000000000 --kmin 5
run cabtaxi_gpu    big_v3 --min 50000000000000000000000 --max 50100000000000000000000 --kmin 5
same big_v2 big_v3
echo "at 5e22: v2 $(secs big_v2) s, v3 $(secs big_v3) s; v3 vs v2 $(ratio big_v2 big_v3)x"
echo "=== $(date -u) ALL CHECKS PASSED"

echo "--- 6. optional: Nsight Compute on one v3 write kernel"
if command -v ncu > /dev/null; then
  ncu --kernel-name k_write --launch-skip 3 --launch-count 1 \
      --section SpeedOfLight --section MemoryWorkloadAnalysis --section WarpStateStats --section Occupancy \
      ./cabtaxi_gpu --min 50000000000000000000000 --max 50010000000000000000000 --kmin 5 --out "$D/ncu_run.txt" \
      > "$D/ncu_k_write.txt" 2>&1 && grep -E "Throughput|Warp Cycles|Stall|Achieved Occupancy|Duration" "$D/ncu_k_write.txt" | head -40 \
    || { echo "ncu failed (often: no permission for GPU counters in a container); see $D/ncu_k_write.txt"; tail -n 3 "$D/ncu_k_write.txt"; }
else
  echo "ncu not installed: skipped"
fi
