#!/bin/bash
# run_batch.sh SKIP TOP -- hunt the curves ranked SKIP+1 .. SKIP+TOP (by Mestre-Nagao score).
#
#   D=/mnt/scratch/dcurran
#   nohup ~/taxi/run_batch.sh 0 10000      > $D/batch1.log 2>&1 &     # test: best 10,000 curves
#   nohup ~/taxi/run_batch.sh 10000 500000 > $D/batch2.log 2>&1 &     # overnight
#
# Scripts live next to this file (~/taxi); all data lives in $DATA (default /mnt/scratch/dcurran):
#   inputs   $DATA/seeds_1e18.csv, extra_seeds.csv (next to the scripts)
#   outputs  $DATA/ranked_curves.csv  (every curve scored; written by the first batch, reused after)
#            $DATA/batch_<out>_SKIP_TOP.csv (the seeds of this batch)
# Other curve sets: set SEEDS, RANKED and OUT (see run_split.sh).
#            $DATA/hunt18.csv + .ckpt (all batches append here; a curve never runs twice, and a
#                                      stopped batch resumes if you rerun the same command)
set -euo pipefail
HERE="$(cd "$(dirname "$0")" && pwd)"
DATA=${DATA:-/mnt/scratch/dcurran}
GP=${GP:-$HOME/pari/bin/gp}
SEEDS=${SEEDS:-"$DATA/seeds_1e18.csv $HERE/extra_seeds.csv"}   # override for other curve sets
RANKED=${RANKED:-$DATA/ranked_curves.csv}
OUT=${OUT:-$DATA/hunt18.csv}
B="$DATA/batch_$(basename "$OUT" .csv)_${1}_${2}.csv"
for f in $SEEDS; do [ -s "$f" ] || { echo "missing $f"; exit 1; }; done
echo "=== $(date) batch: ranks $(( $1 + 1 ))..$(( $1 + $2 ))   data in $DATA"
python3 "$HERE/curve_sieve.py" --gp "$GP" --seeds $SEEDS --procs 64 --skip "$1" --top "$2" \
        --ranked "$RANKED" --out "$B"
python3 "$HERE/curve_hunt.py" --gp "$GP" --seeds "$B" --procs 64 --out "$OUT" \
        --ub 1e165 --wmax 1e12 --width 10
echo "=== $(date) batch done"
