#!/bin/bash
# night_cpu.sh -- wide line and D-line search on the CPUs (FINDINGS F32: breadth, D-lines, exact counting of everything).
#   STAGES=dl     D-lines, both parities, the DDIRS cheapest directions at height DH        (7of9)
#   STAGES=lines  ordinary lines, directions LSKIP+1 .. LSKIP+LDIRS at height LH            (worf)
#   STAGES=all    both, one after the other
#   LDIRSFILE=dirs/x.txt  run lines on explicit directions; LOLDH=600  do not output triples already searched to that height
# Every candidate n is counted exactly (count_all.py), so every join, hub and star with >= 4 points shows up in the
# counted multi-ways; enumerators therefore write only n;[D;]a;b, gzip-compressed (--short, about 15 bytes a line).
# Finally line_structure.py gives the shape (line+free, hub, bowtie, ...) and line ranks/heights of every k >= 4.
# Run:  cd <dir> && STAGES=dl nohup bash night_cpu.sh > cpu.log 2>&1 &
set -u
W=$(pwd); C=$W/code; O=$W/cpu; mkdir -p $O $O/tmp
GP=${GP:-$HOME/pari/bin/gp}; TIMEV=${TIMEV:-/usr/bin/time -v}; P=${P:-56}; STAGES=${STAGES:-all}
DDIRS=${DDIRS:-20000}; DH=${DH:-400}; LSKIP=${LSKIP:-1400}; LDIRS=${LDIRS:-18600}; LH=${LH:-600}
LDIRSFILE=${LDIRSFILE:-}; LOLDH=${LOLDH:-0}; HERO=${HERO:-4}; HPMAX=${HPMAX:-200}; NMAX=${NMAX:-1e40}; AUTOM=${AUTOM:-}; DDIRSDIR=${DDIRSDIR:-}; DHERO=${DHERO:-4}; DHPMAX=${DHPMAX:-200}; DNMAX=${DNMAX:-1e40}; DPARS=${DPARS:-even odd}; DPOS=${DPOS:-}   # DPOS=1: --positive, only D-lines with both integer points positive (cubefree hunt)   # DDIRSDIR: D-line directions from <dir>/n3_even.txt, n3_odd.txt   # AUTOM=4.5: per-direction height where n passes NMAX (F39)   # HERO/HPMAX: >= HERO split primes below HPMAX (F36: 8 and 1000 for six-way hunting)     # LDIRSFILE: explicit directions (a,b per line); LOLDH: heights already searched
[ -n "$LDIRSFILE" ] && { [ -f "$LDIRSFILE" ] || { echo "no such file: $LDIRSFILE"; exit 1; }; LDIRSFILE=$(cd "$(dirname "$LDIRSFILE")" && pwd)/$(basename "$LDIRSFILE"); }
LSEL="--skip $LSKIP --dirs $LDIRS"; [ -n "$LDIRSFILE" ] && LSEL="--dirs-file $LDIRSFILE"
AUTO=""; [ -n "$AUTOM" ] && AUTO="--auto-height --auto-margin $AUTOM"
LOLD=""; [ "$LOLDH" -gt 0 ] && LOLD="--old-height $LOLDH --old-nmax 1e40"
cd $C
T() { echo "$1 $(date)" | tee -a $O/times.txt; }
count() {   # tag, files...: unique n -> exact counts
  local t=$1; shift
  for f in "$@"; do gzip -dc $f; done | cut -d';' -f1 | sort -u -S 8G -T $O/tmp | gzip -1 > $O/${t}_n.gz
  python3 count_all.py $O/${t}_n.gz --out $O/$t.multi --procs $P --gp $GP > $O/${t}_count.log
  T "$t counted: $(tail -1 $O/${t}_count.log)"
}
T "start STAGES=$STAGES P=$P DDIRS=$DDIRS DDIRSDIR=$DDIRSDIR DHERO=$DHERO DHPMAX=$DHPMAX DNMAX=$DNMAX DPARS=[$DPARS] DPOS=$DPOS DH=$DH LSEL=[$LSEL] LH=$LH LOLDH=$LOLDH HERO=$HERO HPMAX=$HPMAX NMAX=$NMAX AUTOM=$AUTOM"
if [ $STAGES != lines ]; then
  for par in $DPARS; do
    DSEL="--dirs $DDIRS"; [ -n "$DDIRSDIR" ] && DSEL="--dirs-file $(cd "$W" && cd "$DDIRSDIR" && pwd)/n3_$par.txt"
    $TIMEV python3 dline_enum.py --parity $par $DSEL --height $DH --nmax $DNMAX --dmax 1000000000 \
      --hero $DHERO --hero-pmax $DHPMAX ${DPOS:+--positive} --core 0 --procs $P --gp $GP --short --out $O/dl_$par.gz > $O/dl_$par.log 2> $O/dl_$par.time
    [ -s $O/dl_$par.gz ] || { T "DL STAGE FAILED, see cpu/dl_$par.time"; exit 1; }
    T "dl $par done"
  done
  count d $(for par in $DPARS; do echo $O/dl_$par.gz; done)
fi
if [ $STAGES != dl ]; then
  $TIMEV python3 line_enum.py $LSEL $LOLD $AUTO --height $LH --nmax $NMAX --hero $HERO --hero-pmax $HPMAX --core 0 \
    --procs $P --gp $GP --short --out $O/lines.gz > $O/lines.log 2> $O/lines.time
  [ -s $O/lines.gz ] || { T "LINE STAGE FAILED, see cpu/lines.time"; exit 1; }
  T "lines done"
  count l $O/lines.gz
fi
cat $O/*.multi | sort -u -t';' -k1,1 > $O/all.multi
python3 line_structure.py $O/all.multi --out $O/all_ls.csv --gp $GP > $O/shapes.txt 2>&1
T "shapes: $(tr '\n' ' ' < $O/shapes.txt)"
awk -F';' '$2>=5' $O/all.multi > $O/fives_plus.txt
T "k>=5 numbers: $(wc -l < $O/fives_plus.txt)   (any k>=6 line is the jackpot: $(awk -F';' '$2>=6' $O/fives_plus.txt | wc -l))"
