#!/bin/bash
# run_pos.sh -- positive hub search (cubefree_plan.md step 3, FINDINGS F42): dline_enum.py --positive on 3,000,000
# never-searched D-line directions (1,500,000 per parity, cost order), height 550, filter 7 split primes < 1,000,
# n <= 1e30. Chunks of 250,000 directions, cheapest first, alternating even and odd (e1 o1 e2 o2 ...), each in its
# own folder with its own count, so everything finished is safe whenever the run is stopped.
# Run:  cd ~/taxi/pos && nohup bash run_pos.sh > pos.log 2>&1 &
# worf: P=22 GP=/usr/bin/gp nohup bash run_pos.sh > pos.log 2>&1 &
set -u
H=$(pwd)
for i in 1 2 3 4 5 6; do
  for par in even odd; do
    c=${par:0:1}$i
    mkdir -p $H/$c && cd $H/$c && ln -sfn $H/code code && cp $H/night_cpu.sh . && cp $H/chunks/${par}_$i.txt n3_$par.txt
    echo "== $c start $(date)"
    STAGES=dl DPARS=$par DPOS=1 P=${P:-56} DDIRSDIR=. DH=550 DHERO=7 DHPMAX=1000 DNMAX=1e30 bash night_cpu.sh > cpu.log 2>&1
    tail -3 cpu/times.txt
    rm -f cpu/dl_*.gz cpu/d_n.gz
  done
done
echo "== all done $(date)"
