#!/bin/bash
# run_n2.sh -- night 1, second half (28-29 Oct 2026). Runs one or more line searches one after another, each in its own folder.
#   worf:  cd /mnt/scratch/iamreddave && nohup bash n2/run_n2.sh worf > n2.log 2>&1 &
#   7of9:  cd ~/taxi && nohup bash n2/run_n2.sh 7of9 > n2.log 2>&1 &
# Progress:  cat n2.log; cat */cpu/times.txt
set -u
HERE=$(cd "$(dirname "$0")" && pwd); TOP=$(pwd)
B=${B:-}; for c in $HOME/taxi/night_n1.tar.gz $HOME/night_n1.tar.gz; do [ -z "$B" ] && [ -f $c ] && B=$c; done
[ -f "$B" ] || { echo "night_n1.tar.gz not found; run with B=<path>"; exit 1; }
run() {   # folder, direction file, settings...
  local d=$1 f=$2; shift 2
  echo "== $d: $f $* $(date)"
  mkdir -p $TOP/$d && cd $TOP/$d && tar xzf $B --strip-components=1 && cp -n $HERE/dirs/* dirs/ 2>/dev/null
  env "$@" STAGES=lines LDIRSFILE=dirs/$f bash night_cpu.sh > cpu.log 2>&1
  tail -3 cpu/times.txt; cd $TOP
}
case ${1:-} in
  worf)
    G=$(which gp)
    run n2_rest  rest_1143877.txt           P=22 GP=$G LH=800  HERO=7 HPMAX=1000 NMAX=1e30 AUTOM=4.5
    run n2_rich7 rich_E2_400000.txt         P=22 GP=$G LH=800  HERO=7 HPMAX=1000 NMAX=1e30 AUTOM=4.5
    run n2_leg7  7of9_n1_legacy_31_1400.txt P=22 GP=$G LH=5000 LOLDH=600 HERO=7 HPMAX=1000 NMAX=1e30 AUTOM=4.5 ;;
  7of9)
    run n2_deep  legacy_1401_20000.txt      P=56 LH=5000 LOLDH=800 HERO=7 HPMAX=1000 NMAX=1e30 AUTOM=4.5 ;;
  *) echo "usage: bash n2/run_n2.sh worf|7of9"; exit 1 ;;
esac
echo "== all done $(date)"
