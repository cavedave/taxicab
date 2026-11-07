#!/bin/bash
# Exact counts of the 416 bowtie numbers left over from F63 (177-300 digits). Run in this directory:
#   nohup ./run.sh > run.out 2>&1 &
# PROCS: one gp per worker; memory is flat (~100 MB per worker), so up to ~60 is fine on 7of9.
PROCS=${PROCS:-48}
python3 count_bowties.py remain_416.txt --out counted_rest.txt --maxdig 300 --tlim 1800 --tcount 3600 --procs $PROCS > counted_rest.log 2>&1
echo "finished $(date)" >> counted_rest.log
