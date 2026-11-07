#!/bin/bash
# decider on the other 22 lf36 base directions, shared point 0 only, a2, b2 < 100
cd "$(dirname "$0")/../.."
for B in ${BASES:-1,4 4,7 12,13 4,9 7,12 1,12 13,16 4,13 27,28 16,19 9,16 7,16 36,37 3,16 1,16 12,19 16,21 25,28 4,19 48,49 28,31 4,21}; do
  t=${B/,/_}
  python3 bowtie_decide.py --base $B --amax 100 --seedh 300 --npts 2000 --procs 8 --out results_bowtie_curves/decide/base$t.txt > results_bowtie_curves/decide/base$t.log 2>&1
  echo "$B done $(date)"
done
