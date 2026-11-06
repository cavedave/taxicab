#!/bin/bash
# run_k3.sh -- every n with >= 3 coprime representations x^3 + y^3 (signs allowed), 1e17 < n <= 1e19, in three
# pieces one after the other (for OEIS A023050 and relatives). Each finished piece is complete on its own.
# Run:  cd /mnt/scratch/iamreddave/oeis && nohup bash run_k3.sh > k3.log 2>&1 &
set -u
export OMP_NUM_THREADS=${P:-22}
g++ -O3 -march=native -fopenmp -std=c++17 cabtaxi.cpp -o cabtaxi || { echo "BUILD FAILED"; exit 1; }
echo "== self-test $(date)"
./cabtaxi --max 1000000000000 --kmin 3 --out test_1e12.txt > test_1e12.log 2>&1; tail -3 test_1e12.log
grep -q "k=3: 1196 numbers" test_1e12.log || { echo "SELF-TEST FAILED (expected k=3: 1196, k=4: 11)"; exit 1; }
for r in "100000000000000000 1000000000000000000 1e17_1e18" "1000000000000000000 3000000000000000000 1e18_3e18" "3000000000000000000 10000000000000000000 3e18_1e19"; do
  set -- $r
  echo "== piece $3 start $(date)"
  ./cabtaxi --min $1 --max $2 --kmin 3 --out k3_$3.txt > k3_$3.log 2>&1
  tail -3 k3_$3.log
  echo "== piece $3 done $(date)"
done
echo "== all done $(date)"
