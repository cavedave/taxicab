# Line-search recall of the 12 exhaustive five-ways (n <= 2.5e23), FINDINGS F92

    python3 line_enum.py --dirs-file shapes/recall12/dirs12.txt --height 2000 --chunks 4 --nmax 2.5e23 --hero 0 --procs 6 --out shapes/recall12/lines12.txt
    python3 shapes/recall12/check12.py shapes/recall12

`dirs12.txt`: the 19 line directions of the 12 five-ways. `lines12.txt` (3.0 M triples, about 42 s on 6 cores) is not committed.
