#!/bin/bash
cd /Users/davidcurran/Documents/taxicab/experiments/mining
O=/private/tmp/claude-501/-Users-davidcurran-Documents-taxicab/ec66a8e8-5cad-47a6-b4ca-a3eae208059a/scratchpad/mac1
H=3000
echo "start $(date)" > $O/times.txt
/usr/bin/time -l python3 line_enum.py --only "3,4;1,4;4,7;12,13;4,9;7,12;1,12;13,16" --height $H --nmax 1e40 --hero 4 --core 0 --procs 8 --chunks 8 --out $O/lines.txt > $O/lines.log 2> $O/lines.time
echo "lines done $(date)" >> $O/times.txt
/usr/bin/time -l python3 dline_enum.py --parity even --dirs 8 --height $H --nmax 1e40 --dmax 1000000000 --hero 4 --core 0 --procs 8 --chunks 8 --out $O/dl_even.txt > $O/dl_even.log 2> $O/dl_even.time
echo "dl even done $(date)" >> $O/times.txt
/usr/bin/time -l python3 dline_enum.py --parity odd --dirs 8 --height $H --nmax 1e40 --dmax 1000000000 --hero 4 --core 0 --procs 8 --chunks 8 --out $O/dl_odd.txt > $O/dl_odd.log 2> $O/dl_odd.time
echo "dl odd done $(date)" >> $O/times.txt
