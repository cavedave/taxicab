#!/bin/bash
# bench.sh -- about 10-15 minutes on 7of9 before the overnight run: build, self-test every GPU, validate kmin 4
# against the 90 four-ways <= 1e15, time one GPU at 1e21 and at 2.5e23, time the Python line tools on the CPUs.
# Run from the unpacked bundle:  cd /mnt/scratch/dcurran/night && bash bench.sh 2>&1 | tee bench.log
set -u
W=$(pwd); C=$W/code; O=$W/bench; mkdir -p $O
GP=${GP:-$HOME/pari/bin/gp}; TIMEV=${TIMEV:-/usr/bin/time -v}
NVCC=${NVCC:-$(command -v nvcc || echo /usr/local/cuda/bin/nvcc)}
P=${P:-56}

CPU_ONLY=${CPU_ONLY:-0}            # CPU_ONLY=1 on worf: skip the GPU parts
echo "== machine"; date; nproc; free -g | head -2; df -h $W | tail -1; python3 --version; $GP --version-short 2>/dev/null || echo "gp at $GP?"
if [ $CPU_ONLY = 0 ]; then
nvidia-smi --query-gpu=index,name,memory.total,memory.used,utilization.gpu --format=csv

echo "== build ($NVCC)"
$NVCC -O3 -std=c++17 -gencode arch=compute_75,code=sm_75 -o $W/cabtaxi_gpu $C/cabtaxi_gpu.cu || { echo BUILD FAILED; exit 1; }

echo "== self-test, all 4 GPUs in parallel"
for d in 0 1 2 3; do $W/cabtaxi_gpu --selftest --device $d > $O/selftest_$d.log 2>&1 & done; wait
for d in 0 1 2 3; do echo "GPU $d: $(grep -c '\[selftest\] ok' $O/selftest_$d.log) ok, $(grep -c FAIL $O/selftest_$d.log) FAIL"; head -1 $O/selftest_$d.log; done

echo "== validation: 0 < n <= 1e15 at kmin 4 must equal the 90 known four-ways"
$W/cabtaxi_gpu --device 0 --max 1000000000000000 --kmin 4 --out $O/v1e15.txt > $O/v1e15.log 2>&1
diff <(grep -v '^#' $C/bench_1e15.txt | cut -d';' -f1,2 | sort) <(grep -v '^#' $O/v1e15.txt | cut -d';' -f1,2 | sort) > /dev/null \
  && echo "VALIDATION OK ($(grep -vc '^#' $O/v1e15.txt) numbers)" || echo "VALIDATION MISMATCH"
tail -1 $O/v1e15.log

echo "== GPU timing, about 3e11 raw pairs per window, GPU 0"
$W/cabtaxi_gpu --device 0 --min 1000000000000000000000 --max 1003400000000000000000 --kmin 4 --out $O/w1e21.txt > $O/w1e21.log 2>&1
grep -E "segment cap|DONE" $O/w1e21.log
$W/cabtaxi_gpu --device 0 --min 250000000000000000000000 --max 250021400000000000000000 --kmin 4 --out $O/w25e23.txt > $O/w25e23.log 2>&1
grep -E "DONE|split" $O/w25e23.log | tail -2
fi

echo "== CPU timing ($P processes)"
cd $C
$TIMEV python3 dline_enum.py --parity odd --dirs $((4*P)) --height 200 --nmax 1e40 --dmax 1000000000 --hero 4 --core 0 \
  --procs $P --gp $GP --out $O/dl.txt > $O/dl.log 2> $O/dl.time
grep -E "Elapsed|Maximum resident|User time" $O/dl.time; tail -1 $O/dl.log
$TIMEV python3 line_enum.py --skip 1400 --dirs $((4*P)) --height 300 --nmax 1e40 --hero 4 --core 0 \
  --procs $P --gp $GP --out $O/l.txt > $O/l.log 2> $O/l.time
grep -E "Elapsed|Maximum resident|User time" $O/l.time; tail -1 $O/l.log
cut -d';' -f1 $O/dl.txt $O/l.txt | sort -u > $O/ns.txt
python3 count_all.py $O/ns.txt --out $O/ns.multi --procs $P --gp $GP | tail -1
echo "== bench done $(date)"
