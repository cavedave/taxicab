#!/bin/bash
# run_ranks5.sh -- ranks of the curves x^3 + y^3 = n for all 142 coprime five-ways (F) and 2 size-matched line + free
# four-ways each (C), PARI ellrank with the integral points as hints (six_way_ideas / FINDINGS 4c).
# Run in this folder:  nohup bash run_ranks5.sh > ranks.log 2>&1 &      (re-running skips jobs already in out/)
# Output: results.txt  lines  tag;group;n;#points;rank_lower;rank_upper;ms   (-1 = error or time limit)
GP=${GP:-$HOME/pari/bin/gp}; PAR=${PAR:-30}; TLIM=${TLIM:-21600}; STACK=${STACK:-8000000000}
mkdir -p out
one() {
  tag=$1; grp=$2; n=$3; pts=$4
  [ -s out/$tag.txt ] && return
  printf 'default(parisizemax, %s);\nTLIM=%s;\n\\r rank.gp\nrk("%s", "%s", %s, %s);\n' "$STACK" "$TLIM" "$tag" "$grp" "$n" "$pts" \
    | $GP -q -D nbthreads=1 > out/$tag.txt 2> out/$tag.err
}
export -f one; export GP TLIM STACK
echo "start $(date)"
cat jobs.txt | xargs -P $PAR -L 1 bash -c 'one "$0" "$1" "$2" "$3"'
cat out/*.txt > results.txt
echo "done $(date): $(wc -l < results.txt) results"
