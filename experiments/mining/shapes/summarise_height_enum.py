#!/usr/bin/env python3
"""summarise_height_enum.py -- read shapes/height_enum.jsonl (height_enum.py): counts, new vs known, CPU rate.
With --write: append new five-ways to results/five_ways_all.txt as '>=5' (source F94), append new four-ways to
results/four_ways_generated.txt, and drop from that file any number now known to have >= 5 representations."""
import sys, json, collections
from pathlib import Path
if hasattr(sys, "set_int_max_str_digits"): sys.set_int_max_str_digits(0)
ROOT = Path(__file__).resolve().parents[3]
recs = [json.loads(l) for l in open(Path(__file__).resolve().parent / 'height_enum.jsonl')]
cpu = sum(r['cpu'] for r in recs); h = cpu / 3600
five, four = {}, {}
for r in recs:
    for n, p in r.get('five', []): five[int(n)] = (p, tuple(r['key']))
    for n, p in r.get('four', []): four[int(n)] = (p, tuple(r['key']))
four = {n: v for n, v in four.items() if n not in five}
F5 = ROOT / 'results/five_ways_all.txt'; F4 = ROOT / 'results/four_ways_generated.txt'
known5 = {int(l.split(';')[0]) for l in open(F5) if l[0].isdigit()}
cat = {int(l.split(';')[0]) for l in open(ROOT / 'results/a047697_catalogue.txt') if l[0].isdigit()}
known4 = {int(l.split(';')[0]) for l in open(F4) if l[0].isdigit()}
new5 = {n: v for n, v in five.items() if n not in known5 and n not in cat}
new4 = {n: v for n, v in four.items() if n not in known5 and n not in cat and n not in known4}
promoted = known4 & set(five)                    # F91 four-ways that turn out to have >= 5
notes = collections.Counter(r['note'].split(',')[0][:22] for r in recs)
band = lambda d: [sum(len(str(n)) < x for n in d) for x in (50, 100, 150, 200, 250, 301)]
print(f"curves {len(recs)} of 489: {dict(notes)}; CPU {h:.2f} h")
print(f"five-ways (<= 300 digits): {len(five)} distinct, {len(new5)} new; {len(five)/h:.0f} per CPU-hour ({len(new5)/h:.0f} new)")
print(f"  below 50/100/150/200/250/301 digits: {band(five)}; new: {band(new5)}")
print(f"four-ways: {len(four)} distinct, {len(new4)} new; {len(promoted)} F91 four-ways are in fact >= 5")
print(f"smallest new five-way: {min(new5, default=None)}")
if '--write' in sys.argv:
    with open(F5, 'a') as f:
        for n in sorted(new5): f.write(f"{n};>=5;" + ",".join(f"{x}:{y}" for x, y in new5[n][0]) + f";F94 height-bounded generation on bowtie curve (not yet counted) {new5[n][1]}\n")
    lines = [l for l in open(F4) if not (l[0].isdigit() and int(l.split(';')[0]) in promoted)]
    with open(F4, 'w') as f:
        f.writelines(lines)
        for n in sorted(new4): f.write(f"{n};>=4;" + ",".join(f"{x}:{y}" for x, y in new4[n][0]) + f";F94 line + free point on bowtie curve {new4[n][1]}\n")
    print(f"wrote {len(new5)} five-ways to {F5.name}; {len(new4)} four-ways added and {len(promoted)} removed in {F4.name}")
