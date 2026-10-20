#!/bin/bash
# run_split.sh SKIP TOP -- hunt the split-prime curves ranked SKIP+1 .. SKIP+TOP.
#   First time only, build the curve list:
#     python3 ~/taxi/split_curves.py --pmax 200 --rmin 5 --rmax 8 --out /mnt/scratch/dcurran/split_curves.csv
#   Then:
#     nohup ~/taxi/run_split.sh 0 5000 > /mnt/scratch/dcurran/split1.log 2>&1 &
# Same machinery as run_batch.sh, with its own files: ranked_split.csv, hunt_split.csv(.ckpt).
HERE="$(cd "$(dirname "$0")" && pwd)"
DATA=${DATA:-/mnt/scratch/dcurran}
SEEDS="$DATA/split_curves.csv" RANKED="$DATA/ranked_split.csv" OUT="$DATA/hunt_split.csv" \
  DATA="$DATA" exec "$HERE/run_batch.sh" "$@"
