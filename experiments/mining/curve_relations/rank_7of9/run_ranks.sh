#!/bin/bash
# run_ranks.sh -- PARI ellrank for the 7 'independent' four-ways in 1e22 - 2.5e23 whose rank ran out of memory on the
# Mac (2 GB stack). One gp per curve, in parallel, 16 GB stack each, 4-hour limit. Uses the PARI 2.19 build.
# Run in this folder:  nohup bash run_ranks.sh > ranks.log 2>&1 &
# Output: ranks_new.txt  (n;rank lower;rank upper;#points;ms ; -1 = error or time limit)
GP=${GP:-$HOME/pari/bin/gp}
i=0
while read -r line; do
  i=$((i+1))
  printf '\\r rank1.gp\nTLIM=14400; default(parisizemax, 16*10^9);\n%s\n' "$line" > c$i.gp
  $GP -q -D nbthreads=1 < c$i.gp > c$i.out 2> c$i.err &
done < curves.txt
wait
cat c*.out > ranks_new.txt
echo "done $(date)"; cat ranks_new.txt
