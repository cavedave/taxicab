#!/bin/bash
# Factor the 17 hard composites (88-100 digits) left from the count5 leftovers with CADO-NFS, smallest first.
# Output: factors.txt lines "N: p1 p2 ..." (TIMEOUT if over the limit). Env: THREADS (default 32), TLIM seconds (default 10800).
cd "$(dirname "$0")"
THREADS=${THREADS:-32}; TLIM=${TLIM:-10800}
CADO=${CADO:-$HOME/cado-nfs/cado-nfs.py}
[ -x "$CADO" ] || { echo "no CADO-NFS at $CADO (see cado_left.txt for the build)"; exit 1; }
echo "== start $(date), $THREADS threads, limit $TLIM s each"
while read -r N; do
  grep -q "^$N:" factors.txt 2>/dev/null && continue          # resume
  t0=$(date +%s)
  F=$(timeout "$TLIM" python3 "$CADO" "$N" -t "$THREADS" --workdir "/mnt/scratch/dcurran/cado_work/${N:0:12}" 2>"log_${N:0:12}.txt" | tail -1)
  if [ -n "$F" ]; then echo "$N: $F" >> factors.txt; else echo "$N: TIMEOUT" >> factors.txt; fi
  echo "${#N} digits: $(( $(date +%s) - t0 )) s  ${F:-TIMEOUT}"
done < hard_parts.txt
echo "== done $(date)"
