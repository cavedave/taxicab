# An FPGA for the coprime cabtaxi search (blue-sky notes)

*A sketch, not a plan. Nothing here has been built or measured.*

## The idea in one paragraph

Our GPU search spends most of its time **sorting**: every cube sum is written to memory, radix-sorted and read
back so that equal values end up next to each other. An FPGA can avoid the sort altogether. The values for a
fixed `a` (or fixed `d`) already come out in increasing order, so the job is to **merge many already-sorted
streams** into one sorted stream and look for runs of five or six equal values. That is Bernstein's heap
method (`refs/sortedsums…`) built as a circuit. Data never leaves the chip: no memory traffic, no sort, just a
pipeline that takes in one value per clock tick and passes on one value per tick.

## What the circuit might look like

```
  stream generators         merge tree (tournament)        run detector
  ┌──────────────┐
  │ a=1: b, b+1… │──┐
  │ a=2: …       │──┤      ┌─────┐
  │ …            │──┼────▶ │ min │──┐                    ┌──────────────┐
  │ d=1: c, c+1… │──┤      └─────┘  ├──▶ … ──▶ sorted ──▶│ equal to the │──▶ candidates
  │ d=2: …       │──┘      ┌─────┐  │        stream      │ previous 4?  │    (to a CPU for
  └──────────────┘    ...  │ min │──┘                    └──────────────┘     exact checking)
                           └─────┘
```

- **Generators.** Each stream holds a 128-bit value and its finite difference, and steps with additions only:
  next sum = value + step, next step = step + 6b + 6 (or + 6d). A coprime filter (binary gcd, a short pipeline
  of shifts and subtractions) marks pairs to skip. Stream state (a, b, value, step: about 40 bytes) sits in
  on-chip block RAM, so millions of streams can be stored, each paused until the merge needs it.
- **Merge tree.** A tournament of comparators repeatedly picks the smallest value among all streams and refills
  from that stream's generator. With a pipelined tree this produces about one value per clock tick.
- **Run detector.** It compares each output with the previous four and passes any run of five or more to a
  host computer, which re-derives all representations exactly. This is the same independent check the GPU
  version uses.
- **Parallelism.** Split the range of n into slices (or residue classes) and put one merge tree per slice on
  the chip, as many as fit.

**Rough throughput guess.** About 300–500 million values per second per merge tree. A large FPGA might hold
10–30 trees, so somewhere around 3–15 × 10⁹ pairs per second. That's comparable to one or a few RTX 5090s, at
a fraction of the power. This is a guess to be checked with a small prototype, not a promise.

**Hard parts.** Managing millions of streams in a tree. Keeping a 128-bit comparator tree fast enough to run
at a high clock speed. Feeding slices evenly. The FPGA build tools themselves, where compiling a design takes
hours and timing problems are common.

## Hardware

| level | examples | rough cost |
| --- | --- | --- |
| learning | Digilent Arty A7, Terasic DE10-Nano, Lattice ECP5 boards (open-source toolchain) | £100–250 |
| serious prototype | AMD/Xilinx Kintex UltraScale+ boards | £1,000–4,000 |
| production | AMD Alveo U55C / U250, Intel Agilex cards; or rented in the cloud (e.g. AWS F2 instances) | rent by the hour |

## How to learn it

1. **Digital logic basics:** gates, flip-flops, clocks, pipelines. *Digital Design and Computer
   Architecture* (Harris & Harris) is the standard first book.
2. **A hardware language.** Verilog/SystemVerilog is the classic route. HLS (high-level synthesis: write C++,
   the tools generate hardware; AMD Vitis HLS) is closer to the C++ we already have and is a reasonable way in
   for a stream-processing design like this.
3. **Simulate before buying hardware.** Verilator (fast and open source) or Icarus Verilog. The design can be
   tested against our CPU program's output, exactly as the GPU code was.
4. **A ladder of small projects:** blink an LED → a UART link to the PC → a 128-bit adder pipeline → one
   cube-sum generator → a 2-way merge → an 8-way tournament → full streams with on-chip storage → run detection.
   Each step can be checked against `cabtaxi.cpp`.
5. **Good free resources:** Nandland (beginner tutorials), the ZipCPU blog (careful, rigorous FPGA practice),
   and the AMD Vitis HLS tutorials (for the C++ route).

## Who has used FPGAs (or custom hardware) for number theory

- **Integer factoring.** Hardware has long been studied for the sieving step of the number field sieve:
  Shamir and Tromer's **TWIRL** design (2003, a proposed custom chip) and **SHARK** (Franke et al., 2005).
  The **elliptic curve method** of factoring has been run on FPGAs (Gaj et al., CHES 2006). **COPACOBANA**
  (2006) was a cluster of cheap FPGAs used for code breaking and ECM.
- **Cryptanalysis by exhaustive search**: the EFF's DES cracker (1998, custom chips) is the classic
  "custom hardware beats general computers on one brute-force job" example.
- **Equal sums of like powers / taxicab-type searches.** I'm not aware of any FPGA search. The published
  records (Bernstein; Butler; Hollerbach; the GPU work on Euler's conjecture variants) used CPUs and GPUs. That's
  worth a literature check, since an FPGA search here could itself be novel.

## Cost reality

Rented, an FPGA saves nothing. A cloud FPGA hour (AWS F1/F2) costs roughly $1.50–2. That's several times
the price of an RTX 5090 hour on vast.ai, which measured 3.5–5 × 10⁹ pairs/s here. The power saving goes to
the provider, not to you. Owned, the electricity difference over a 30-hour run is a few pounds, while a
production FPGA card costs more than a 5090. FPGAs pay off for jobs that run continuously for months on
owned hardware. A few dozen GPU-hours per step is not that. (Prices are approximate; check before deciding.)

## Verdict

An FPGA fits the *shape* of this problem better than a GPU does. It's a streaming merge with no sort, mostly
additions and comparisons, and almost no memory traffic. But it's a project of months, and the likely payoff
is a few times the speed of a rented GPU per pound, not orders of magnitude. It's worth doing for the learning
and novelty. It's not the fastest route to a(6) > 10²³.
