Overnight run, 27 October 2026
==============================
7of9 GPUs (4 x RTX 2080 Ti): re-find every coprime four-way 0 < n <= 1e22 (kmin 4, exhaustive).
7of9 CPUs (56 of 64 threads): D-lines, both parities, 20,000 cheapest directions, height 400.
worf CPUs (32 threads):        ordinary lines, directions 1,401 - 20,000, height 600.
Every candidate is counted exactly; enumerators keep only n;[D;]a;b (gzip), so disk stays around 10 GB per machine.
The code is about 10x faster than the Mac test version (integer arithmetic instead of Fraction; identical output).

1. Unpack on each machine (7of9: /mnt/scratch/dcurran/night):
     mkdir -p <dir> && cd <dir> && tar xzf ~/night7of9.tar.gz --strip-components=1

2. Benchmark, send me the logs:
     7of9:  bash bench.sh 2>&1 | tee bench.log                      (~15 min; GPUs and CPUs)
     worf:  CPU_ONLY=1 P=30 GP=<path to gp> bash bench.sh 2>&1 | tee bench.log
   (If nvcc is not on PATH: NVCC=/usr/local/cuda-12.8/bin/nvcc bash bench.sh ...)
   7of9 checks: every GPU self-test ok, VALIDATION OK (the 90 four-ways <= 1e15).

3. Overnight (sizes may change after the benchmark, e.g. DH=300 or LH=500):
     7of9:  nohup bash night_gpu.sh > gpu.log 2>&1 &
            STAGES=dl nohup bash night_cpu.sh > cpu.log 2>&1 &
     worf:  STAGES=lines P=30 GP=<path to gp> nohup bash night_cpu.sh > cpu.log 2>&1 &
   Progress:  tail cpu/times.txt gpu.log;  tail -2 gpu/*.log
   Re-running night_gpu.sh skips finished parts and resumes interrupted ones.

4. Morning: pack the small results and copy them to the Mac:
     tar czf ~/night_results_$(hostname).tar.gz $(ls -d gpu/*.txt gpu/*.log gpu/*.progress cpu/*.multi cpu/*.log cpu/*.time \
         cpu/times.txt cpu/all_ls.csv cpu/shapes.txt cpu/fives_plus.txt bench.log gpu.log cpu.log 2>/dev/null)
   (the cpu/*.gz candidate files stay on the servers unless we want per-direction yields)
