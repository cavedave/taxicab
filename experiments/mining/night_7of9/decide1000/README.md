# decide1000: bowtie decider on the 23 lf36 base directions, second direction up to 1000

Why (F64): of the 79 bowties found by the 1e36 line search, only 8 have a second direction with a2, b2 < 100
(F62's limit); 10 have < 300, 18 have < 1000. Each decider curve with bowties gives dozens below 1e300 (six-way tests).

## Run on 7of9

    scp decide1000_v1.tar.gz 7of9:/mnt/scratch/dcurran/
    ssh 7of9
    cd /mnt/scratch/dcurran && tar xzf decide1000_v1.tar.gz && cd decide1000
    STAGE=1 nohup ./run.sh > stage1.out 2>&1 &         # first: measures time per curve at larger coefficients
    tail -f stage1.out                                  # one line per curve; '*** SIX-WAY' if k >= 6 appears

Stage 2 (two runs of at most 14.5 h each; the second resumes where the first stopped):

    STAGE=2 nohup ./run.sh > stage2a.out 2>&1 &
    STAGE=2 nohup ./run.sh > stage2b.out 2>&1 &         # later, the second slot

Stop early at any time: `pkill -f bowtie_decide; pkill -f "gp -q"`; resume with the same STAGE.

## Collect

    tar czf ~/decide1000_out.tar.gz stage*.log stage*.txt stage*.out

## Checks to make on the results

- Curves: stage 1 206,100; stage 2 2,093,530 (F62's 28,283 took ~40 min on 8 laptop processes: ~0.7 s per curve).
- The lf36 bowties each stage must rediscover (base + second direction):
  stage 1: (1,12)+(49,192) 4.98e29; (13,16)+(121,124) 6.51e29.
  stage 2: (3,4)+(273,304) 3.97e19; (3,4)+(975,976) 1.54e25; (3,4)+(453,964) 7.37e35; (4,7)+(364,367) 3.44e30;
  (4,7)+(28,751) 3.64e30; (12,13)+(156,859) 1.56e34; (27,28)+(189,400) 1.54e25; (16,21)+(64,309) 9.21e20.
- 'RANKTIMEOUT' lines: curves where ellrank took over 120 s (not decided; list them).
- Then count the new bowties with count_bowties.py (exact k), as in F63.
