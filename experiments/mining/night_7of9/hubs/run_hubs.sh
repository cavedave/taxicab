#!/bin/bash
# run_hubs.sh -- hub (D-line) search, 29-30 Oct 2026: 150,000 never-searched directions of each parity, height 550,
# filter 7 split primes < 1,000, n <= 1e30. Even parity first, then odd, each in its own folder with its own count,
# so the even results are safe even if the odd half is stopped early.
# Run:  cd ~/taxi/hubs && nohup bash run_hubs.sh > hubs.log 2>&1 &
set -u
H=$(pwd)
for par in even odd; do
  mkdir -p $H/$par && cd $H/$par && ln -sfn $H/code code && cp $H/night_cpu.sh $H/n3_$par.txt .
  echo "== $par start $(date)"
  STAGES=dl DPARS=$par P=${P:-56} DDIRSDIR=. DH=550 DHERO=7 DHPMAX=1000 DNMAX=1e30 bash night_cpu.sh > cpu.log 2>&1
  tail -3 cpu/times.txt
done
echo "== all done $(date)"
