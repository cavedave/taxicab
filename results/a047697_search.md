# The search for A047697(6)

*Status, 26 October 2026: complete to 2.5 × 10²³. No six-way exists for n ≤ 2.5 × 10²³. There is no five-way between 10²² and 10²³, and exactly one between 10²³ and 2.5 × 10²³.*

[OEIS A047697](https://oeis.org/A047697) is the smallest positive number that can be written in *n* ways as
x³ + y³ with **gcd(x, y) = 1**, where x and y may be negative:

| n | a(n) | found by |
| ---: | ---: | --- |
| 1 | 1 | |
| 2 | 91 | classical |
| 3 | 3,367 | classical |
| 4 | 16,776,487 | Rathbun |
| 5 | 506,433,677,359,393 | Bernstein, 1999 |
| 6 | **unknown**: > 2.5 × 10²³ (this search) | |

Bernstein's 1999 search (*Enumerating solutions to p(a)+q(b)=r(c)+s(d)*, Math. Comp. 70, 2001, §7) found no
six-way below 2.5 × 10¹⁷. Nobody seems to have searched further since.

## Results so far

**No six-way exists for n ≤ 2.5 × 10²³**, so a(6) > 2.5 × 10²³. That is a million times past Bernstein's 2.5 × 10¹⁷.

Up to 10²³ there are exactly **eleven** numbers with five coprime representations: Bernstein's two and nine new ones
(table below). Between 10²³ and 2.5 × 10²³ there is exactly **one**, 236,191,447,138,323,830,299,237, which the line
method had found first (next section). So up to 2.5 × 10²³ there are exactly **twelve**.

| n | representations | source |
| ---: | --- | --- |
| 506,433,677,359,393 | 28065³ + 78532³ = 36489³ + 77074³ = 80025³ − 18218³ = 95866³ − 72087³ = 139264³ − 129951³ | Bernstein 1999 |
| 137,904,678,696,613,339 | 310998³ + 475963³ = 369286³ + 444027³ = 516931³ − 61128³ = 539755³ − 268446³ = 1365216³ − 1340093³ | Bernstein 1999 |
| 39,673,716,067,958,900,347 | 418491³ + 3408526³ = 1202338³ + 3360075³ = 3526755³ − 1612412³ = 3819196³ − 2521629³ = 14705344³ − 14643933³ | new |
| 95,793,117,931,950,826,933 | 5029461³ − 3155822³ = 5073261³ − 3264272³ = 5625154³ − 4348011³ = 23578300³ − 23520723³ = 26192350³ − 26145723³ | new |
| 118,371,660,133,721,558,473 | 752526³ + 4904113³ = 1138980³ + 4889497³ = 2936497³ + 4531470³ = 5004913³ − 1912674³ = 5682073³ − 4022364³ | new |
| 624,256,195,206,357,000,469 | 1807245³ + 8519464³ = 2355597³ + 8486416³ = 3095128³ + 8408973³ = 8884936³ − 4256883³ = 96589720³ − 96567411³ | new |
| 633,753,337,814,536,954,807 | 1019818³ + 8584815³ = 9764199³ − 6673148³ = 10245412³ − 7615641³ = 10475362³ − 8019441³ = 75791818³ − 75755025³ | new |
| 921,288,078,249,108,802,505 | 7544409³ + 7893776³ = 9742196³ − 1495911³ = 9846873³ − 3222808³ = 10393689³ − 5862904³ = 22982553³ − 22385788³ | new |
| 1,038,246,186,276,942,167,105 | 6530217³ + 9124898³ = 10125896³ − 46911³ = 10251009³ − 3390124³ = 11696457³ − 8251942³ = 31043073³ − 30679708³ | new |
| 2,724,248,230,569,896,697,541 | 3515718³ + 13891669³ = 7975069³ + 13039368³ = 8518752³ + 12818077³ = 10230894³ + 11824693³ = 41571781³ − 41039550³ | new |
| 5,306,775,242,131,114,520,041 | 9848424³ + 16326073³ = 13667257³ + 14016672³ = 17446393³ − 1518156³ = 18167545³ − 8834844³ = 61604281³ − 61134600³ | new |

Each new five-way was recounted by a separate Python program: an exhaustive search for every coprime
representation, sharing no code with the GPU search. Each has exactly five, the same five the GPU reported.
None of the nine new numbers appears in the OEIS. Rendered images are in `out/a047697/`.

## Five-ways beyond 10²³ found by the line method (not exhaustive)

The exhaustive search stops at 2.5 × 10²³. Above 10²³, the line method in `experiments/mining/` (F12–F14 in its
`FINDINGS.md`) has found **thirty-two new coprime five-ways** (13 by 26 October 2026 morning, 19 more on the spare CPUs of the
4 × RTX 5090 rental the same day; FINDINGS F26–F27).

**How the method works:**
- it enumerates collinear coprime triples on the cheapest line directions;
- it keeps numbers with the typical prime profile (at least 4 primes ≡ 1 (mod 3) below 200);
- it counts all representations of each kept number exactly, from its divisors.

**Each number below has exactly 5 coprime representations, by that exhaustive count.** The search itself is
**not** exhaustive, so there may be other five-ways between 2.5 × 10²³ and these numbers that it has not found. It
does not affect the bound a(6) > 2.5 × 10²³.

| n | the five representations |
| ---: | --- |
| 236,191,447,138,323,830,299,237 | 61736565³ + 9613558³ = 61857514³ − 7922043³ = 62141349³ − 15564158³ = 168364485³ − 165539942³ = 218687536³ − 217028739³ |
| 459,803,710,089,257,980,965,337 | 76134102³ + 26447809³ = 76599049³ + 21803592³ = 78197089³ − 26378418³ = 118734025³ − 106679892³ = 1256265265³ − 1256168142³ |
| 867,568,642,528,959,824,806,171 | 79186278³ + 71857339³ = 82498848³ + 67392259³ = 97363267³ − 38120748³ = 98534347³ − 44664678³ = 100778875³ − 53829834³ |
| 2,851,826,724,766,078,018,833,601 | 141276225³ + 31780576³ = 141812938³ − 5433591³ = 533144193³ − 529778636³ = 541153702³ − 537887943³ = 35577954550³ − 35577953799³ |
| 15,442,272,835,364,300,840,226,739 | 208066083³ + 185999278³ = 229129762³ + 150558771³ = 997367115³ − 992165396³ = 1359827104³ − 1357037685³ = 3716031604³ − 3715658805³ |
| 36,254,160,765,497,504,708,872,903 | 294244287³ + 220895650³ = 330766876³ + 40420503³ = 332226735³ − 74604338³ = 395112304³ − 294062121³ = 585346546³ − 547707777³ |
| 36,382,243,612,093,946,470,090,369 | 327379905³ + 108983764³ = 331356993³ + 4456108³ = 331560514³ − 40613655³ = 340899562³ − 147889719³ = 742131514³ − 719424375³ |
| 153,461,072,317,103,291,251,148,239 | 494803854³ + 318527815³ = 535294572³ + 42656431³ = 535525807³ − 49494084³ = 561275095³ − 285851646³ = 922950103³ − 858503742³ |
| 182,392,325,742,867,193,833,098,401 | 560392929³ + 185725408³ = 566852926³ + 62985465³ = 566965642³ + 52072617³ = 568693768³ − 115239711³ = 2392061926³ − 2381389095³ |
| 201,297,892,510,496,465,061,972,139 | 489586611³ + 437858752³ = 539188654³ + 354480075³ = 584713372³ + 111612531³ = 979060900³ − 903358221³ = 3200502658³ − 3193938597³ |
| 357,308,079,971,019,656,068,684,549 | 846426900³ − 629207651³ = 1083838668³ − 971136227³ = 1215221461³ − 1128533418³ = 2022747541³ − 1993208538³ = 2119473205³ − 2092621026³ |
| 581,834,611,748,164,220,101,952,821 | 879096213³ − 460320926³ = 914740341³ − 568334390³ = 1378449904³ − 1267724307³ = 1443979966³ − 1344232635³ = 1749407062³ − 1683590043³ |
| 889,713,631,299,214,636,707,596,167 | 769234300³ + 757432023³ = 962557023³ − 128278550³ = 977285572³ − 352174761³ = 1005378496³ − 502003689³ = 2573785222³ − 2528213361³ |
| 1,441,335,932,043,659,816,048,279,479 | 1110168886³ + 418087647³ = 1129711558³ − 76993377³ = 1134621759³ − 268413890³ = 1140344500³ − 346361241³ = 16593139390³ − 16591394241³ |
| 1,875,257,556,360,663,546,196,170,409 | 1207119244³ + 488147385³ = 1233162561³ − 6675638³ = 1233192244³ − 51389895³ = 1252231744³ − 445380615³ = 3519138118³ − 3467922447³ |
| 4,006,751,594,615,544,419,200,755,017 | 1310961369³ + 1205921552³ = 1498106073³ + 863797640³ = 1588105089³ + 112584722³ = 2031165105³ − 1635294802³ = 4259754201³ − 4184840344³ |
| 9,027,370,398,769,170,672,971,729,619 | 2108482492³ − 702242389³ = 2294140139³ − 1449721760³ = 6261916798³ − 6184215997³ = 6401494571³ − 6327205148³ = 280338678275³ − 280338639986³ |
| 34,501,269,164,386,329,986,697,851,653 | 3112812834³ + 1631078149³ = 3180904861³ + 1323131988³ = 4220557686³ − 3439222187³ = 4654339933³ − 4047865344³ = 32212272037³ − 32201184870³ |
| 34,547,209,243,400,012,474,421,281,413 | 3009879517³ + 1938067200³ = 3273732498³ − 813542459³ = 3274969189³ − 833101686³ = 3309374101³ − 1192760442³ = 28538987485³ − 28524841608³ |
| 104,153,248,919,447,127,324,401,999,977 | 4566097281³ + 2076500746³ = 4685537728³ + 1087381305³ = 4941984417³ − 2548178846³ = 5400565480³ − 3764776647³ = 21784073734³ − 21710666703³ |
| 278,052,073,362,590,568,252,158,271,051 | 5686474795³ + 4549643726³ = 5901626792³ + 4169835667³ = 6537360650³ − 1101282149³ = 6808394174³ − 3348526997³ = 6840095204³ − 3475331117³ |
| 498,424,028,328,865,332,465,535,957,193 | 6319209305³ + 6266529432³ = 7581618978³ + 3971154881³ = 7928696064³ − 193770151³ = 8241075630³ − 3942324943³ = 9842056296³ − 7691018407³ |
| 650,942,832,109,065,456,723,121,976,491 | 8699769675³ − 1958118194³ = 8726002774³ − 2380059477³ = 10358713762³ − 7722672933³ = 15296921728³ − 14306950221³ = 179885417164³ − 179878711437³ |
| 2,575,932,492,706,922,775,209,751,529,471 | 12967638766³ + 7339083735³ = 13703290599³ + 1396967938³ = 13745372542³ − 2761248873³ = 13903794628³ − 4818656961³ = 45438516016³ − 45018773505³ |
| 3,598,085,549,085,232,075,646,572,993,861 | 15386595285³ − 3547636154³ = 18568644922³ − 14101779483³ = 20137915846³ − 16593055275³ = 23066846596³ − 20547625635³ = 26452601488³ − 24613721571³ |
| 5,155,590,025,407,314,470,961,337,159,897 | 16898989774³ + 6907955297³ = 17275238488³ + 419526665³ = 18821942345³ − 11478536012³ = 19635702881³ − 13416804914³ = 27416737865³ − 24907904012³ |
| 7,016,830,156,515,525,773,263,162,950,169 | 18532209489³ + 8671605370³ = 19252446153³ − 4921681952³ = 19321401472³ − 5810453559³ = 26945469142³ − 23237088639³ = 27365113114³ − 23796613935³ |
| 7,621,954,168,931,821,961,653,299,403,879 | 15977212575³ + 15245486434³ = 19667909278³ + 2403386703³ = 19790098143³ − 5050134062³ = 27227685934³ − 23246995185³ = 28637269552³ − 25126440009³ |
| 12,134,354,169,911,534,158,461,101,130,403 | 22057691364³ + 11193189019³ = 22953757363³ + 3436791486³ = 23117727643³ − 6040810284³ = 32454415195³ − 28041404088³ = 66610022515³ − 65685628338³ |
| 19,008,553,084,548,906,511,372,979,784,727 | 23856656350³ + 17577371103³ = 26138219962³ + 10479173199³ = 37417606215³ − 32197665272³ = 41565306136³ − 37516206009³ = 291974927584³ − 291900583353³ |
| 241,472,402,714,194,053,046,481,660,069,701 | 61386644829³ + 21650020708³ = 62386748068³ − 11034203811³ = 62531784310³ − 14487717099³ = 110438541238³ − 103400090091³ = 120994399480³ − 115225584099³ |
| 378,855,256,022,502,299,689,661,564,666,966,839 | 626270232288³ + 510732064423³ = 677911772862³ + 406782587071³ = 750757691215³ − 353834410446³ = 760522164031³ − 393706007778³ = 794957352679³ − 498023881260³ |

**Rediscovery check:** the same method rediscovered 8 of the 11 known five-ways ≤ 10²³ (directions searched so far: the 1,000 cheapest).

**Recall against the exhaustive run 10²³ – 2.5 × 10²³:** the only five-way in that range (236,191,447,138,323,830,299,237)
had already been found by the line method, so recall there is 1 of 1. For four-ways it is 49 of 214 (23%): 159 of the 214
pass the `--core 0` prime filter, and the line searches found 48 of those (30%).

The five found on 26 October 2026 came from a deep search (slope height 4,000) of the 8 most productive cheap directions (`experiments/mining/FINDINGS.md` F26). The 3 it missed have no
line in the directions searched so far.

## The runs

| range of n | hardware | raw pairs | coprime pairs | time | raw pairs/s |
| --- | --- | ---: | ---: | ---: | ---: |
| 0 – 2.5 × 10¹⁷ (validation) | 7of9 CPU, Threadripper 3970X, 64 threads | 5.25 × 10¹¹ (est.) | 319,497,814,847 | 2,550 s | ≈ 2 × 10⁸ |
| 0 – 10¹⁹ | 7of9 CPU, Threadripper 3970X, 64 threads | *see cab2.log* | *see cab2.log* | ≈ 8 h | ≈ 2 × 10⁸ |
| 10¹⁹ – 10²⁰ | 1 × RTX 5090 (vast.ai) | 22,390,033,902,596 | 13,612,807,252,351 | 6,385 s | 3.51 × 10⁹ |
| 10²⁰ – 10²¹ | 1 × RTX 5090 (vast.ai) | 103,933,863,545,587 | 63,188,318,807,907 | 24,632 s | 4.22 × 10⁹ |
| 10²¹ – 10²² | 4 × RTX 5090 (vast.ai) | 482,445,237,654,261 | 293,304,518,606,519 | 24,825 s (wall) | 1.94 × 10¹⁰ (4 GPUs) |
| 10²² – 2 × 10²² | 1 × RTX 5090 (vast.ai), v3 code | 361,217,191,042,592 | 219,601,584,685,459 | 27,102 s | 1.33 × 10¹⁰ |
| 2 × 10²² – 3 × 10²² | 1 × RTX 5090 (vast.ai), v3 code | 302,973,499,093,645 | 184,191,835,825,468 | 22,775 s | 1.33 × 10¹⁰ |
| 3 × 10²² – 10²³ | 4 × RTX 5090 (vast.ai), v3 code | 1,575,207,039,548,206 | 957,638,204,314,922 | 33,612 s (wall) | 4.75 × 10¹⁰ (4 GPUs) |
| 10²³ – 2.5 × 10²³ | 4 × RTX 5090 (vast.ai), v3 code, kmin 4 | 2,403,447,083,666,895 | 1,461,155,509,448,848 | 49,484 s (wall) | 4.92 × 10¹⁰ (4 GPUs) |

"Raw pairs" counts every (x, y) generated. About 60.8% of them are coprime, close to 6/π² ≈ 0.608 as expected.

The work grows as B^(2/3), so each power of ten costs 10^(2/3) ≈ 4.64 times the one before. The measured raw
pair counts follow that: 1.04 × 10¹⁴ / 2.24 × 10¹³ = 4.64, and 4.82 × 10¹⁴ / 1.04 × 10¹⁴ = 4.64.

### The 4 × RTX 5090 run (10²¹ – 10²²)

The machine, as listed by vast.ai (instance 56520933):

| item | value |
| --- | --- |
| GPUs | 4 × NVIDIA GeForce RTX 5090, 32,607 MiB each (sm_120) |
| GPU memory in use | 91.1 / 127 GB |
| GPU memory bandwidth | 1,453.5 GB/s per card (as measured by vast.ai) |
| peak FP32 | 432.4 TFLOPS in total (unused here: this search is pure integer arithmetic) |
| CPU | Xeon Platinum 8469C, 96 of 192 threads allocated (the search uses 4) |
| RAM | 515.8 GB (the search uses about 0.5 GB) |
| bus | PCIe 5.0 ×16, 44 GB/s |
| CUDA | driver supports 13.0 |

Each GPU searches one quarter of the range with `--part k/4`. The parts are equal shares of work, not of n.
Status about 11.5 minutes in:

| part | GPU | covers n from | speed (raw pairs/s) | ETA at that point |
| --- | --- | --- | ---: | ---: |
| 1/4 | 0 | 10²¹ | 4.77 × 10⁹ | 24,574 s |
| 2/4 | 1 | about 2.6 × 10²¹ | 4.90 × 10⁹ | 23,914 s |
| 3/4 | 2 | about 4.7 × 10²¹ | 5.26 × 10⁹ | 22,230 s |
| 4/4 | 3 | about 7.2 × 10²¹ | 5.33 × 10⁹ | 21,947 s |
| **total** | | | **2.03 × 10¹⁰** | about 6.8 h |

Before the run, the script checked each card: every GPU passed the self-test, and GPU 0 reproduced the 10¹⁵
benchmark exactly (13,223,067,998 raw and 8,044,700,766 coprime pairs) in 12 seconds.

All four parts finished on 18 October 2026 (archive written 14:58 UTC). The four ranges join exactly, so
together they cover 10²¹ < n ≤ 10²² with no gaps:

| part | covers n | raw pairs | coprime pairs | time | raw pairs/s | five-ways |
| --- | --- | ---: | ---: | ---: | ---: | ---: |
| 1/4 | 10²¹ – 2,640,495,989,778,755,354,624 | 120,609,058,777,811 | 73,325,268,347,667 | 24,825 s | 4.86 × 10⁹ | 1 |
| 2/4 | – 4,737,586,505,830,182,682,624 | 120,611,014,216,745 | 73,326,016,681,776 | 23,748 s | 5.08 × 10⁹ | 1 |
| 3/4 | – 7,207,278,944,116,045,512,704 | 120,612,177,019,639 | 73,326,461,698,592 | 22,742 s | 5.30 × 10⁹ | 1 |
| 4/4 | – 10²² | 120,612,987,640,066 | 73,326,771,878,484 | 22,229 s | 5.43 × 10⁹ | 0 |
| **total** | | **482,445,237,654,261** | **293,304,518,606,519** | 26.0 GPU-h | 1.94 × 10¹⁰ | **3** |

The coprime fraction is 0.60795 (6/π² = 0.60793). No number had six or more representations.

### The 10²² – 3 × 10²² runs (one RTX 5090, v3)

This was an overnight run on 19–20 October 2026 with the faster v3 code (see `experiments/cabtaxi_gpu_speedup_plan.md`).
v3 was validated on the same card that evening: its outputs and pair counts were identical to the original code
at 10¹⁵ and 10²¹, and it ran 2.7 times faster.

- **Time:** 27,102 s, at 1.33 × 10¹⁰ raw pairs/s.
- **Pairs:** 3.612 × 10¹⁴ raw, matching the 3.61 × 10¹⁴ predicted from the B^(2/3) law. The coprime fraction is
  0.60795.
- **Result:** no five-way and no six-way in this range.

A second overnight run on the same card covered 2 × 10²² – 3 × 10²², 20 October 2026. Its files are named
`*_2e22_3.5e22*`, but the range searched was (2 × 10²², 3 × 10²²], as the log's `search` line and the DONE
line confirm.
- **Time:** 22,775 s at 1.33 × 10¹⁰ raw pairs/s.
- **Pairs:** 3.03 × 10¹⁴ raw (predicted 3.03 × 10¹⁴).
- **Result:** again no five-way and no six-way.

### The 3 × 10²² – 10²³ run (4 × RTX 5090, v3)

This ran on 20 October 2026, launched with `MIN=3e22 TAG=3e22_1e23 bash run_4x5090.sh`.
- **Checks before launch:** every GPU passed the selftest, including the windows up to 10²⁴, and the 10¹⁵
  benchmark reproduced the expected pair counts.
- **The four parts** cover the range with no gaps:

  | part | covers n | time | raw pairs/s |
  | --- | --- | ---: | ---: |
  | 1/4 | 3 × 10²² – 4.487 × 10²² | 32,547 s | 1.21 × 10¹⁰ |
  | 2/4 | – 6.161 × 10²² | 33,374 s | 1.18 × 10¹⁰ |
  | 3/4 | – 8.004 × 10²² | 33,612 s | 1.17 × 10¹⁰ |
  | 4/4 | – 10²³ | 33,155 s | 1.19 × 10¹⁰ |

- **Totals:** 1.5752 × 10¹⁵ raw pairs (predicted 1.5751 × 10¹⁵), coprime fraction 0.60794, 36.9 GPU-hours.
- **Padding** of the interleaved layout: 3.5–4.5%.
- **Result:** no five-way and no six-way.

### The 10²³ – 2.5 × 10²³ run (4 × RTX 5090, v3, kmin 4)

This ran on 26 October 2026, launched 09:30 UTC, last part finished about 23:15 UTC. It used `--kmin 4`, so it
also kept every four-way (for the mining work, and to measure the line method's recall).
- **Checks before launch:** every GPU passed the selftest, the 10¹⁵ benchmark matched the CPU program, and a
  smoke window 236191447138 × 10¹² – 236191447139 × 10¹² found the line-method five-way 236191447138323830299237
  with the same five representations.
- **The four parts** cover the range with no gaps:

  | part | covers n | raw pairs | time | raw pairs/s | four-ways | five-ways |
  | --- | --- | ---: | ---: | ---: | ---: | ---: |
  | 1/4 | 10²³ – 1.3318 × 10²³ | 600,859,433,593,448 | 48,271 s | 1.24 × 10¹⁰ | 78 | 0 |
  | 2/4 | – 1.6939 × 10²³ | 600,861,191,009,199 | 48,500 s | 1.24 × 10¹⁰ | 48 | 0 |
  | 3/4 | – 2.0839 × 10²³ | 600,862,626,406,603 | 48,987 s | 1.23 × 10¹⁰ | 50 | 0 |
  | 4/4 | – 2.5 × 10²³ | 600,863,832,657,645 | 49,484 s | 1.21 × 10¹⁰ | 38 | 1 |

- **Totals:** 2.4034 × 10¹⁵ raw pairs, coprime fraction 0.60795, 54.2 GPU-hours. Time split: sort 60–61%,
  write 14%, select 10–11%, count 8–10% (the sort is the target of the next speed-up, see below).
- **Result:** no six-way; one five-way (236,191,447,138,323,830,299,237); 214 four-ways.
- **Independent check:** all 215 numbers were refactored on the Mac (PARI) and their representations counted
  from the divisors of n (`experiments/mining/collisions.py`): every count and representation set matches.
- **Spare CPUs:** the line searches of FINDINGS F27 ran on the same machine (nice 19) without slowing the GPUs.

**Possible speed-up for later runs.** The radix sort moves about 51 GB per segment (7 passes over 56-bit keys)
and runs near the card's memory bandwidth. The keys are spread almost evenly over a segment and only values
occurring ≥ K times are needed, so one scatter pass into 65,536 buckets plus an exact duplicate count per bucket
in shared memory should do the same job with about a third of the traffic: an estimated 2–2.5× overall.
Not implemented yet.

### Five-ways per decade

| range | five-ways |
| --- | ---: |
| up to 10¹⁹ | 2 |
| 10¹⁹ – 10²⁰ | 2 |
| 10²⁰ – 10²¹ | 4 |
| 10²¹ – 10²² | 3 |
| 10²² – 10²³ | **0** |
| 10²³ – 2.5 × 10²³ | 1 |

The last decade costs 4.6 times the work of the one before, and before it ran the trend suggested roughly 4–8
five-ways in it. Finding none suggests the coprime five-ways thin out faster than the small counts from
10¹⁹–10²² implied, although numbers this small are noisy. It also makes a six-way just above 10²³ less likely.

## How the computation works

### What is counted
Every positive n ≤ B and every unordered representation n = x³ + y³ with gcd(x, y) = 1, written in one of two forms:

- **sums:** n = a³ + b³ with 1 ≤ a ≤ b
- **differences:** n = (c + d)³ − c³ = d³ + 3dc(c + d) with c, d ≥ 1

Each representation is generated exactly once. A number is reported if it is hit k ≥ 5 times. The search is
exhaustive: every pair with value in the range is generated, so "no six-way found" is a proof, not an estimate.

### Splitting the range
The range of n is cut into segments. Each segment holds about as many pairs as one GPU can sort at once,
around 1.4 billion on a 32 GB RTX 5090. Pair density falls like n^(−1/3), so the segment boundaries are equally
spaced in n^(2/3). If a segment turns out to be too big, it is split in half automatically. Segments are
independent, which is what lets `--part k/N` give each GPU its own share.

### What the GPU does for one segment [lo, hi)
1. **Count.** One thread per stream (each a for sums, each d for differences) works out how many of its values
   fall in [lo, hi). It uses exact integer cube roots for sums and an exact quadratic bound for differences.
2. **Scan.** A prefix sum turns those counts into write positions.
3. **Write.** Each thread writes its values in order. Consecutive values come from additions alone:
   (b+1)³ − b³ = 3b² + 3b + 1 for sums, and steps of 3d(2c + d + 1), each 6d more than the last, for differences.
   Each value is stored as the 64-bit **offset n − lo**, so 128-bit numbers up to 10²² sort as 64-bit keys.
   Pairs with gcd(x, y) > 1 are marked as discarded; the coprime test is a binary gcd (shifts and subtractions only).
4. **Sort.** CUB radix sort of the 64-bit keys.
5. **Find repeats.** One thread per sorted entry spots the start of each run of equal values and keeps those of
   length ≥ 5.

### What the CPU checks
For every value the GPU reports, the CPU **independently re-derives all its representations** by direct search:
every a with 2a³ ≤ n, and every d using the exact quadratic. That takes about n^(1/3) steps. It checks each
identity with exact 128-bit arithmetic and requires the count to equal the GPU's multiplicity. Any mismatch
stops the run. Results are written in increasing n, and a progress file allows `--resume` after an interruption.

### Validation before any result was trusted
- **Brute force:** every n ≤ 10⁷ with two or more representations matches an independent brute-force count,
  including the total of coprime pairs (36,368).
- **Known terms:** 91, 3,367, 16,776,487 and both of Bernstein's five-ways are recovered with exact
  representation sets.
- **Split ranges:** (0, 10¹²] gives exactly the same pairs as (0, 10¹¹] plus (10¹¹, 10¹²]: 80,226,285 coprime pairs.
- **Above 2⁶⁴:** a window just below 10²¹ gives 39 coprime pairs, matching a separate Python count.
- **Against the CPU program:** byte-identical output at 10¹² (63,974 numbers) and 10¹⁵ (91 numbers). The CPU
  program itself matches brute force to 10⁸ and reproduces Bernstein's 2.5 × 10¹⁷ search exactly.
- **On every GPU before every run:** the self-test above, and the 10¹⁵ pair counts reproduced exactly.

### Number theory used
Writing n = s · t with s = a + b and t = a² − ab + b²: for coprime a and b, every prime factor of t is 3 or
≡ 1 (mod 3), and gcd(s, t) divides 3. This is what makes the independent divisor-based checks possible, and
it explains the structure of the hits. The search itself does not rely on any filter that could skip a
genuine solution.

## Code and data
| file | role |
| --- | --- |
| `experiments/cabtaxi.cpp` | CPU reference (OpenMP), used for 0 – 10¹⁹ |
| `experiments/cabtaxi_gpu.cu` | GPU search (CUDA; also builds as plain C++ with `-DHOST_ONLY`) |
| `experiments/run_5090.sh`, `experiments/run_4x5090.sh` | build, self-test, benchmark and run scripts |
| `experiments/render_cabtaxi_png.py` | renders the identities as images (`out/a047697/`) |
| `a047697/` | logs and result files of the GPU runs |
| `experiments/mining/linesearch_4x5090/` | line-search results (n with ≥ 4 representations) from the rental's CPUs |

Search cost: about 140 GPU-hours on RTX 5090s (9 for 10¹⁹–10²¹, 26 for 10²¹–10²², 13.9 for 10²²–3 × 10²², 36.9 for 3 × 10²²–10²³, 54.2 for 10²³–2.5 × 10²³), plus about 9 CPU-hours on 7of9.
