# Plan: finish the F63 bowtie counts on 7of9

Status 7 Nov 2026: 574 of 990 new bowtie numbers (<= 300 digits) counted, all k = 5 (F63). The laptop run died of
memory exhaustion in the old `count_reps`; fixed (depth-first, deadline; commit 3018005). 416 numbers remain
(177-300 digits) -- `remain_416.txt`. Start this when the current 7of9 run has finished.

## Run

    scp count_rest_v1.tar.gz 7of9:/mnt/scratch/dcurran/        # bundle at the repo root
    ssh 7of9
    cd /mnt/scratch/dcurran && tar xzf count_rest_v1.tar.gz && cd count_rest
    which gp && python3 --version                              # needs PARI gp; Python 3.8 is fine
    PROCS=48 nohup ./run.sh > run.out 2>&1 &
    tail -f counted_rest.log                                   # "i/416 done, k counts {...}"; any k >= 6 prints *** SIX-WAY

Limits per number: factoring 1800 s (`--tlim`), subset search 3600 s (`--tcount`). Expected time: on the laptop,
3 numbers of 252 digits took ~9.5 min on 3 workers (mostly factoring), so ~416/48 rounds of a few minutes -> a few hours.

## Collect

    tar czf ~/count_rest_out.tar.gz counted_rest.txt counted_rest.txt.unk counted_rest.log

Locally: copy `counted_rest.*` to `results_bowtie_curves/decide/`, and update F63 with the final tally (and the k = ?
numbers, with reasons, from `counted_rest.txt.unk`).

## Afterwards

- Numbers in `.unk` with `factor:` -> longer ECM / CADO-NFS on the listed pieces (about a third the size of n).
- Numbers in `.unk` with `count:` (too many split primes) -> a C/PARI inner loop with modular square pre-filters.
