# decide1000: bowtie decider on the 23 lf36 base directions, second direction up to 1000

Why (F64): of the 79 bowties found by the 1e36 line search, only 8 have a second direction with a2, b2 < 100
(F62's limit); 10 have < 300, 18 have < 1000. Each decider curve with bowties gives dozens below 1e300 (six-way tests).

## v2 (8 Nov): seed height 1e5, ellrank effort-3 fallback

v1's stage 1 (seed height 300) missed (1,12)+(49,192): its only known point has height 7,349, and ellrank at default
effort found no generators (rank 4; effort 3 finds 3 at once). Seed search on point-free quartics costs ~33 ms per
curve at height 1e5 (max 242 ms in 200 samples), so v2 uses 1e5 and redoes the whole range below 300 (F61/F62 and
v1 stage 1 all used 300). Logs are named v2_stage*, so v1's logs are never resumed.

## Run on 7of9

    scp decide1000_v2.tar.gz 7of9:/mnt/scratch/dcurran/
    ssh 7of9
    cd /mnt/scratch/dcurran && tar xzf decide1000_v2.tar.gz && cd decide1000
    STAGE=1 nohup ./run.sh > v2_stage1.out 2>&1 &       # ~40 min
    tail -f v2_stage1.out

Stage 2 (two runs of at most 14.5 h each; the second resumes where the first stopped):

    STAGE=2 nohup ./run.sh > v2_stage2a.out 2>&1 &
    STAGE=2 nohup ./run.sh > v2_stage2b.out 2>&1 &      # later, the second slot

Stop early at any time: `pkill -f bowtie_decide; pkill -f "gp -q"`; resume with the same STAGE.

## Collect

    tar czf ~/decide1000_out.tar.gz v2_stage*.log v2_stage*.txt v2_stage*.out

## Checks to make on the results

- Curves: stage 1 235,748; stage 2 2,093,530. v1 stage 1 (206,100 curves, seed 300) took 28 min on 60 processes.
- The lf36 bowties each stage must rediscover (base + second direction):
  stage 1 (10): (3,4)+(9,52) 5.06e14, 7.61e32; (3,4)+(27,28) 1.06e26, 1.72e27, 6.51e29; (3,4)+(75,76) 2.48e33, 4.06e34,
  8.53e34; (1,12)+(49,192) 4.98e29; (13,16)+(121,124) 6.51e29.
  stage 2 (8): (3,4)+(273,304) 3.97e19; (3,4)+(975,976) 1.54e25; (3,4)+(453,964) 7.37e35; (4,7)+(364,367) 3.44e30;
  (4,7)+(28,751) 3.64e30; (12,13)+(156,859) 1.56e34; (27,28)+(189,400) 1.54e25; (16,21)+(64,309) 9.21e20.
- 'RANKTIMEOUT' lines: curves where ellrank took over 120 s (not decided; list them).
- Then count the new bowties with count_bowties.py (exact k), as in F63.
