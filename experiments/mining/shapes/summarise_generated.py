#!/usr/bin/env python3
"""summarise_generated.py -- read shapes/generated.jsonl (from generate_multiways.py): counts, new vs known, CPU rates, digits.
With --write: append new five-ways (<= 300 digits) to results/five_ways_all.txt as '>=5' and write new four-ways to
results/four_ways_generated.txt (the catalogue holds exactly-counted numbers only)."""
import sys, json, collections
from pathlib import Path
if hasattr(sys, "set_int_max_str_digits"): sys.set_int_max_str_digits(0)
ROOT = Path(__file__).resolve().parents[3]
recs = [json.loads(l) for l in open(Path(__file__).resolve().parent / 'generated.jsonl')]
cpu = sum(r['cpu'] for r in recs); h = cpu / 3600
notes = collections.Counter(r['note'].split(',')[0] for r in recs)
five, four = {}, {}
for r in recs:
    for n, p in r['five']: five[int(n)] = (p, tuple(r['key']))
    for n, p in r['four']: four[int(n)] = (p, tuple(r['key']))
four = {n: p for n, p in four.items() if n not in five}
known = {int(l.split(';')[0]) for l in open(ROOT / 'results/five_ways_all.txt') if l[0].isdigit()}
cat = {int(l.split(';')[0]) for l in open(ROOT / 'results/a047697_catalogue.txt') if l[0].isdigit()}
new5 = {n: p for n, p in five.items() if n not in known and n not in cat}
new4 = {n: p for n, p in four.items() if n not in known and n not in cat}
band = lambda d: sorted(collections.Counter(min(len(str(n)) // 50 * 50, 300) for n in d).items())
print(f"curves {len(recs)}: {dict(notes)}; CPU {cpu:.0f} s = {h:.2f} CPU-hours")
print(f"five-ways (k>=5): {len(five)} distinct, {len(new5)} new, {len(five)/h:.0f} per CPU-hour ({len(new5)/h:.0f} new); digit bands {band(five)}")
print(f"four-ways (k>=4): {len(four)} distinct, {len(new4)} new, {len(four)/h:.0f} per CPU-hour ({len(new4)/h:.0f} new); digit bands {band(four)}")
print(f"smallest new five-way: {min(new5, default=None)}\nsmallest new four-way: {min(new4, default=None)}")
for lo in (0, 50, 100, 150, 200, 300):
    print(f"  five-ways with < {lo + 50 if lo < 300 else 'inf'} digits: {sum(len(str(n)) < lo + 50 for n in five) if lo < 300 else len(five)}")
if '--write' in sys.argv:
    w5 = sorted(n for n in new5 if len(str(n)) <= 300)
    with open(ROOT / 'results/five_ways_all.txt', 'a') as f:
        for n in w5: f.write(f"{n};>=5;" + ",".join(f"{x}:{y}" for x, y in new5[n][0]) + f";F91 generated on bowtie curve (not yet counted) {new5[n][1]}\n")
    with open(ROOT / 'results/four_ways_generated.txt', 'w') as f:
        f.write("# n;>=4;representations;source -- coprime four-ways (at least) generated on bowtie curves (shapes/generate_multiways.py, F91);\n"
                "# every listed representation verified, k not counted exactly. Not in a047697_catalogue.txt.\n")
        for n in sorted(new4): f.write(f"{n};>=4;" + ",".join(f"{x}:{y}" for x, y in new4[n][0]) + f";F91 line + free point on bowtie curve {new4[n][1]}\n")
    print(f"wrote {len(w5)} five-ways to five_ways_all.txt, {len(new4)} four-ways to four_ways_generated.txt")
