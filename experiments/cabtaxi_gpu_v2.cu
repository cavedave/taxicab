// cabtaxi_gpu.cu -- GPU search for A047697: n = x^3 + y^3 with gcd(x,y) = 1, signs allowed,
// in at least K ways. Same mathematics and output format as cabtaxi.cpp (the validated CPU
// reference); built either with nvcc (GPU) or as plain C++ with -DHOST_ONLY (for testing).
//
// Range: 0 <= A < n <= B <= 10^24 (128-bit values; coordinates up to 5.8e11 fit 64 bits;
// the host check's x^3 stays below 2^128 until n ~ 1e26).
//
// Representations (unordered, each counted once):
//   sums         n = a^3 + b^3,           1 <= a <= b
//   differences  n = (c+d)^3 - c^3 = d^3 + 3 d c (c + d),   c, d >= 1
//
// Pipeline per segment [lo, hi) of n (segments split automatically until they fit the GPU):
//   1. count kernel   : raw pairs of each stream a (sums) / d (differences) in [lo, hi)
//   2. exclusive scan : write offsets
//   3. write kernel   : each pair's value as the 64-bit OFFSET n - lo (SENTINEL if gcd != 1);
//                       consecutive values by finite differences (additions, no multiplies)
//   4. select         : drop the SENTINELs (~39% of keys), so the sort sees coprime pairs only
//   5. radix sort     : only the low bits a segment's offsets can use (bit length of hi - lo)
//   6. run kernel     : values occurring >= K times -> small candidate list
//   7. host           : recover every representation of each candidate independently
//                       (O(n^(1/3)) exact search), verify, require count == GPU multiplicity
// Output lines are written in increasing n; <out>.progress holds the last completed n, so
// --resume continues an interrupted run. Progress and DONE lines report the time per phase.
//
// Builds:
//   RTX 5090 : nvcc -O3 -std=c++17 -gencode arch=compute_120,code=sm_120 -o cabtaxi_gpu cabtaxi_gpu.cu
//   RTX 4090 : ... arch=compute_89,code=sm_89     RTX 2080 Ti : ... arch=compute_75,code=sm_75
//   host-only: g++ -O3 -std=c++17 -fopenmp -DHOST_ONLY -x c++ cabtaxi_gpu.cu -o cabtaxi_host
// Run:
//   ./cabtaxi_gpu --selftest
//   ./cabtaxi_gpu --min 10000000000000000000 --max 100000000000000000000 --kmin 5 --out cab_1e20.txt
//   (--resume after an interruption; --part i/n --device d to split across GPUs)

#include <algorithm>
#include <chrono>
#include <cmath>
#include <cstdint>
#include <cstdio>
#include <cstdlib>
#include <cstring>
#include <map>
#include <string>
#include <vector>

#ifdef HOST_ONLY
  #define HD static inline
  #ifdef _OPENMP
    #include <omp.h>
  #endif
#else
  #include <cuda_runtime.h>
  #include <cub/cub.cuh>
  #define HD static inline __host__ __device__
  #define CU(x) do { cudaError_t e_ = (x); if (e_ != cudaSuccess) { \
      std::fprintf(stderr, "CUDA error %s at %s:%d\n", cudaGetErrorString(e_), __FILE__, __LINE__); std::exit(2); } } while (0)
#endif

typedef uint32_t u32; typedef uint64_t u64; typedef unsigned __int128 u128;
static const u64 SENTINEL = ~0ULL;
static const char* LIMIT_STR = "1000000000000000000000000";   // 1e24

// time per phase in ms, summed over all segments (GPU phases by CUDA events, host by clock)
enum { T_COUNT, T_SCAN, T_WRITE, T_SELECT, T_SORT, T_RUNS, T_HOST, T_N };
static const char* T_NAME[T_N] = {"count", "scan", "write", "select", "sort", "runs", "host"};
static double g_ms[T_N];
static std::string phase_split() {
  double tot = 0; for (double x : g_ms) tot += x;
  std::string s; char b[48];
  for (int i = 0; i < T_N; ++i) { std::snprintf(b, sizeof b, "%s%s %.0f%%", i ? " " : "", T_NAME[i], 100 * g_ms[i] / std::max(tot, 1e-9)); s += b; }
  return s;
}

[[noreturn]] static void fatal(const char* m) { std::fprintf(stderr, "FATAL: %s\n", m); std::exit(3); }

static std::string u128str(u128 x) {
  if (!x) return "0";
  char b[48]; int n = 0;
  while (x) { b[n++] = (char)('0' + (int)(x % 10)); x /= 10; }
  std::string s; while (n) s.push_back(b[--n]); return s;
}
static u128 parse_u128(const char* s) {
  if (!*s) fatal("empty number");
  u128 v = 0;
  for (const char* p = s; *p; ++p) {
    if (*p < '0' || *p > '9') fatal("numbers must be plain decimal digits (no 1e19)");
    const u128 nv = v * 10 + (u128)(*p - '0');
    if (nv / 10 != v) fatal("number too large");
    v = nv;
  }
  return v;
}

// ---------------- exact integer helpers (host and device) ----------------
HD u64 icbrt(u128 n) {                                       // floor(cbrt(n)), n < 2^100
  u64 r = (u64)cbrt((double)n);
  while (r && (u128)r * r * r > n) --r;
  while ((u128)(r + 1) * (r + 1) * (r + 1) <= n) ++r;
  return r;
}
HD u128 fdiff(u64 d, u64 c) {                                // (c+d)^3 - c^3
  return (u128)d * d * d + 3 * (u128)d * c * (c + d);
}
HD u64 cmin(u64 d, u128 v) {                                 // smallest c >= 1 with fdiff(d,c) >= v
  if (fdiff(d, 1) >= v) return 1;
  const double D = (double)d, V = (double)v;
  const double disc = 9.0 * D * D * D * D - 12.0 * D * (D * D * D - V);
  const double est = (-3.0 * D * D + sqrt(disc > 0 ? disc : 0)) / (6.0 * D);
  u64 c = est < 1 ? 1 : (u64)est;
  while (c > 1 && fdiff(d, c - 1) >= v) --c;
  while (fdiff(d, c) < v) ++c;
  return c;
}
HD int ctz64(u64 x) {
#ifdef __CUDA_ARCH__
  return __ffsll((long long)x) - 1;
#else
  return __builtin_ctzll(x);
#endif
}
HD u64 gcd64(u64 a, u64 b) {                                 // binary gcd (no division)
  if (!a) return b; if (!b) return a;
  const int s = ctz64(a | b); a >>= ctz64(a);
  do { b >>= ctz64(b); if (a > b) { u64 t = a; a = b; b = t; } b -= a; } while (b);
  return a << s;
}
HD u64 first_b(u64 a, u128 lo) {                             // smallest b >= a with a^3 + b^3 >= lo
  const u128 a3 = (u128)a * a * a;
  if (lo <= 2 * a3) return a;
  const u64 b = icbrt(lo - a3 - 1) + 1;
  return b < a ? a : b;
}
HD u64 count_sum(u64 a, u128 lo, u128 hi) {
  const u128 a3 = (u128)a * a * a;
  if (2 * a3 >= hi) return 0;
  const u64 b0 = first_b(a, lo), b1 = icbrt(hi - 1 - a3);    // b1: largest b with a^3+b^3 < hi
  return b1 >= b0 ? b1 - b0 + 1 : 0;
}
HD u64 count_diff(u64 d, u128 lo, u128 hi) {
  if (fdiff(d, 1) >= hi) return 0;
  const u64 c0 = cmin(d, lo), c1 = cmin(d, hi);
  return c1 > c0 ? c1 - c0 : 0;
}
// write the n raw pairs of stream i into keys[0..n) as offsets from lo (finite differences)
HD void write_stream(u64 i, u64 amax, u64 n, u128 lo, u64* keys) {
  if (i < amax) {
    const u64 a = i + 1; u64 b = first_b(a, lo);
    u128 val = (u128)a * a * a + (u128)b * b * b;
    u128 step = 3 * (u128)b * b + 3 * (u128)b + 1;           // (b+1)^3 - b^3
    for (u64 j = 0; j < n; ++j, ++b) {
      keys[j] = gcd64(a, b) == 1 ? (u64)(val - lo) : SENTINEL;
      val += step; step += 6 * (u128)b + 6;
    }
  } else {
    const u64 d = i - amax + 1; u64 c = cmin(d, lo);
    u128 val = fdiff(d, c), step = 3 * (u128)d * (2 * c + d + 1);   // f(c+1) - f(c)
    for (u64 j = 0; j < n; ++j, ++c) {
      keys[j] = gcd64(c, d) == 1 ? (u64)(val - lo) : SENTINEL;
      val += step; step += 6 * (u128)d;
    }
  }
}

// ---------------- the segment engine ----------------
struct Cand { u64 off; u64 mult; };
static int sort_bits(u128 lo, u128 hi) {                     // bits needed by offsets n - lo, lo <= n < hi
  const u64 top = (u64)(hi - 1 - lo);
  return top ? 64 - __builtin_clzll(top) : 1;
}

#ifdef HOST_ONLY
struct Engine {
  u64 cap; std::vector<u64> counts, off, keys;
  Engine(u64 cap_, u128) : cap(cap_) {}
  static double ms_since(std::chrono::steady_clock::time_point& t) {
    const auto now = std::chrono::steady_clock::now();
    const double ms = std::chrono::duration<double, std::milli>(now - t).count(); t = now; return ms;
  }
  bool run(u128 lo, u128 hi, int K, std::vector<Cand>& cand, u64& raw, u64& coprime) {
    auto t = std::chrono::steady_clock::now();
    const u64 amax = icbrt(hi / 2) + 1, total = amax + icbrt(hi) + 1;
    counts.assign(total, 0);
    #pragma omp parallel for schedule(dynamic, 4096)
    for (long long i = 0; i < (long long)total; ++i)
      counts[i] = (u64)i < amax ? count_sum((u64)i + 1, lo, hi) : count_diff((u64)i - amax + 1, lo, hi);
    g_ms[T_COUNT] += ms_since(t);
    off.assign(total + 1, 0);
    for (u64 i = 0; i < total; ++i) off[i + 1] = off[i] + counts[i];
    raw = off[total];
    g_ms[T_SCAN] += ms_since(t);
    if (raw > cap) return false;
    keys.resize(raw);
    #pragma omp parallel for schedule(dynamic, 4096)
    for (long long i = 0; i < (long long)total; ++i)
      if (counts[i]) write_stream((u64)i, amax, counts[i], lo, keys.data() + off[i]);
    g_ms[T_WRITE] += ms_since(t);
    keys.erase(std::remove(keys.begin(), keys.end(), SENTINEL), keys.end());
    coprime = keys.size();
    const int bits = sort_bits(lo, hi);                      // the GPU sorts only these bits: check they suffice
    if (bits < 64) for (u64 k : keys) if (k >> bits) fatal("offset exceeds sort_bits");
    g_ms[T_SELECT] += ms_since(t);
    std::sort(keys.begin(), keys.end());
    g_ms[T_SORT] += ms_since(t);
    for (u64 i = 0; i < coprime;) {
      u64 j = i + 1; while (j < coprime && keys[j] == keys[i]) ++j;
      if (j - i >= (u64)K) cand.push_back({keys[i], j - i});
      i = j;
    }
    g_ms[T_RUNS] += ms_since(t);
    return true;
  }
};
#else
// 128-bit kernel arguments are passed as two 64-bit halves (portable across CUDA versions)
__global__ void k_count(u64 lo0, u64 lo1, u64 hi0, u64 hi1, u64 amax, u64 total, u64* counts) {
  const u128 lo = ((u128)lo1 << 64) | lo0, hi = ((u128)hi1 << 64) | hi0;
  const u64 i = (u64)blockIdx.x * blockDim.x + threadIdx.x;
  if (i >= total) return;
  counts[i] = i < amax ? count_sum(i + 1, lo, hi) : count_diff(i - amax + 1, lo, hi);
}
__global__ void k_write(u64 lo0, u64 lo1, u64 amax, u64 total, const u64* counts, const u64* off, u64* keys) {
  const u128 lo = ((u128)lo1 << 64) | lo0;
  const u64 i = (u64)blockIdx.x * blockDim.x + threadIdx.x;
  if (i >= total || !counts[i]) return;
  write_stream(i, amax, counts[i], lo, keys + off[i]);
}
struct NotSentinel { __device__ bool operator()(const u64& x) const { return x != SENTINEL; } };
__global__ void k_runs(const u64* keys, u64 N, int K, Cand* cand, unsigned long long* ncand, u64 capc) {
  const u64 i = (u64)blockIdx.x * blockDim.x + threadIdx.x;   // keys: sorted, coprime pairs only
  if (i >= N) return;
  const u64 v = keys[i];
  if (i > 0 && keys[i - 1] == v) return;                   // not the start of a run
  u64 j = i + 1; while (j < N && keys[j] == v) ++j;
  if (j - i >= (u64)K) {
    const unsigned long long s = atomicAdd(ncand, 1ULL);
    if (s < capc) cand[s] = Cand{v, j - i};
  }
}
struct Engine {
  u64 cap, capc = 1 << 20, maxstreams = 0;
  u64 *d_counts = nullptr, *d_off = nullptr, *d_keys = nullptr, *d_keys2 = nullptr;
  Cand* d_cand = nullptr; unsigned long long* d_ncand = nullptr; int* d_nsel = nullptr;
  void* d_tmp = nullptr; size_t tmp_bytes = 0;
  std::vector<Cand> h_cand;
  cudaEvent_t ev[T_RUNS + 2];                                  // phase boundaries T_COUNT .. T_RUNS
  Engine(u64 cap_, u128 B) : cap(cap_) {
    for (auto& e : ev) CU(cudaEventCreate(&e));
    maxstreams = icbrt(B / 2) + icbrt(B) + 8;
    CU(cudaMalloc(&d_counts, (maxstreams + 1) * sizeof(u64)));
    CU(cudaMalloc(&d_off, (maxstreams + 1) * sizeof(u64)));
    CU(cudaMalloc(&d_keys, cap * sizeof(u64)));
    CU(cudaMalloc(&d_keys2, cap * sizeof(u64)));
    CU(cudaMalloc(&d_cand, capc * sizeof(Cand)));
    CU(cudaMalloc(&d_ncand, sizeof(unsigned long long)));
    CU(cudaMalloc(&d_nsel, sizeof(int)));
    size_t t1 = 0, t2 = 0, t3 = 0;
    cub::DoubleBuffer<u64> db(d_keys, d_keys2);
    CU(cub::DeviceRadixSort::SortKeys(nullptr, t1, db, (int)cap));       // all 64 bits: the upper bound
    CU(cub::DeviceScan::ExclusiveSum(nullptr, t2, d_counts, d_off, (int)maxstreams + 1));
    CU(cub::DeviceSelect::If(nullptr, t3, d_keys, d_keys2, d_nsel, (int)cap, NotSentinel()));
    tmp_bytes = std::max(t1, std::max(t2, t3));
    CU(cudaMalloc(&d_tmp, tmp_bytes));
    h_cand.resize(capc);
  }
  ~Engine() {                                              // release the card for the next engine
    cudaFree(d_counts); cudaFree(d_off); cudaFree(d_keys); cudaFree(d_keys2);
    cudaFree(d_cand); cudaFree(d_ncand); cudaFree(d_nsel); cudaFree(d_tmp);
    for (auto& e : ev) cudaEventDestroy(e);
  }
  Engine(const Engine&) = delete; Engine& operator=(const Engine&) = delete;
  bool run(u128 lo, u128 hi, int K, std::vector<Cand>& cand, u64& raw, u64& coprime) {
    const u64 amax = icbrt(hi / 2) + 1, total = amax + icbrt(hi) + 1;
    if (total > maxstreams) fatal("stream count exceeds allocation");
    const int T = 256;
    CU(cudaEventRecord(ev[T_COUNT]));
    k_count<<<(unsigned)((total + T - 1) / T), T>>>((u64)lo, (u64)(lo >> 64), (u64)hi, (u64)(hi >> 64), amax, total, d_counts);
    CU(cudaGetLastError());
    CU(cudaMemset(d_counts + total, 0, sizeof(u64)));
    CU(cudaEventRecord(ev[T_SCAN]));
    size_t tb = tmp_bytes;
    CU(cub::DeviceScan::ExclusiveSum(d_tmp, tb, d_counts, d_off, (int)total + 1));
    CU(cudaEventRecord(ev[T_WRITE]));
    CU(cudaMemcpy(&raw, d_off + total, sizeof(u64), cudaMemcpyDeviceToHost));
    add_ms(T_COUNT, T_WRITE);
    coprime = 0;
    if (raw > cap) return false;
    if (raw == 0) return true;
    k_write<<<(unsigned)((total + T - 1) / T), T>>>((u64)lo, (u64)(lo >> 64), amax, total, d_counts, d_off, d_keys);
    CU(cudaGetLastError());
    CU(cudaEventRecord(ev[T_SELECT]));
    tb = tmp_bytes;
    CU(cub::DeviceSelect::If(d_tmp, tb, d_keys, d_keys2, d_nsel, (int)raw, NotSentinel()));
    CU(cudaEventRecord(ev[T_SORT]));
    int nsel = 0;
    CU(cudaMemcpy(&nsel, d_nsel, sizeof(nsel), cudaMemcpyDeviceToHost));
    coprime = (u64)nsel;
    if (coprime > raw) fatal("select returned more keys than were written");
    cub::DoubleBuffer<u64> db(d_keys2, d_keys);                 // coprime keys now in d_keys2
    tb = tmp_bytes;
    CU(cub::DeviceRadixSort::SortKeys(d_tmp, tb, db, (int)coprime, 0, sort_bits(lo, hi)));
    CU(cudaEventRecord(ev[T_RUNS]));
    const u64* sorted = db.Current();
    CU(cudaMemset(d_ncand, 0, sizeof(unsigned long long)));
    if (coprime) k_runs<<<(unsigned)((coprime + T - 1) / T), T>>>(sorted, coprime, K, d_cand, d_ncand, capc);
    CU(cudaGetLastError());
    CU(cudaEventRecord(ev[T_RUNS + 1]));
    unsigned long long nc = 0;
    CU(cudaMemcpy(&nc, d_ncand, sizeof(nc), cudaMemcpyDeviceToHost));
    add_ms(T_WRITE, T_RUNS + 1);
    if (nc > capc) fatal("candidate buffer overflow: segment NOT complete (raise --kmin)");
    CU(cudaMemcpy(h_cand.data(), d_cand, nc * sizeof(Cand), cudaMemcpyDeviceToHost));
    cand.assign(h_cand.begin(), h_cand.begin() + nc);
    return true;
  }
  void add_ms(int from, int to) {                              // g_ms[p] += time from ev[p] to ev[p+1]
    for (int p = from; p < to; ++p) { float ms = 0; CU(cudaEventElapsedTime(&ms, ev[p], ev[p + 1])); g_ms[p] += ms; }
  }
};
#endif

// ---------------- independent host recovery of all representations ----------------
struct Rep { u64 x; u64 y; int neg; };                       // n = x^3 + y^3 (neg=0) or x^3 - y^3 (neg=1)
static std::vector<Rep> recover(u128 n) {
  std::vector<Rep> r;
  for (u64 a = 1; 2 * (u128)a * a * a <= n; ++a) {
    const u128 a3 = (u128)a * a * a; const u64 b = icbrt(n - a3);
    if (b >= a && a3 + (u128)b * b * b == n && gcd64(a, b) == 1) r.push_back({a, b, 0});
  }
  for (u64 d = 1; fdiff(d, 1) <= n; ++d) {
    const u64 c = cmin(d, n);
    if (fdiff(d, c) == n && gcd64(c, d) == 1) r.push_back({c + d, c, 1});
  }
  std::sort(r.begin(), r.end(), [](const Rep& p, const Rep& q) {
    return p.neg != q.neg ? p.neg < q.neg : p.x != q.x ? p.x < q.x : p.y < q.y; });
  for (auto& x : r) {
    const u128 X = (u128)x.x * x.x * x.x, Y = (u128)x.y * x.y * x.y;
    if ((x.neg ? X - Y : X + Y) != n) fatal("recovered representation fails exact check");
  }
  return r;
}

// ---------------- driver ----------------
struct Out { FILE* f; std::map<u64, std::vector<std::string>> byk; };
static double p23(u128 x) { return std::pow((double)x, 2.0 / 3); }
static u128 from23(double y) { return (u128)std::pow(y, 1.5); }

static void search(u128 A, u128 B, int K, u64 cap, u64 nseg, Out* out, const char* progress,
                   u64& tot_raw, u64& tot_cop, bool quiet) {
  Engine eng(cap, B);
  const double A23 = p23(A), B23 = p23(B);
  std::vector<u128> edge(nseg + 1);
  for (u64 i = 0; i <= nseg; ++i) edge[i] = from23(A23 + (B23 - A23) * (double)i / (double)nseg);
  edge[0] = A + 1; edge[nseg] = B + 1;
  for (u64 i = 1; i < nseg; ++i) edge[i] = std::min(std::max(edge[i], edge[i - 1]), B + 1);
  const u128 maxwidth = (u128)1 << 62;                         // keep n - lo inside 64 bits
  auto t0 = std::chrono::steady_clock::now(); auto last = t0;
  for (u64 s = 0; s < nseg; ++s) {
    std::vector<std::pair<u128, u128>> stack{{edge[s], edge[s + 1]}};
    std::vector<std::pair<u128, u64>> segc;                  // (n, multiplicity)
    while (!stack.empty()) {                                 // sub-ranges in increasing order
      const u128 lo = stack.back().first, hi = stack.back().second; stack.pop_back();
      if (lo >= hi) continue;
      std::vector<Cand> c; u64 raw = 0, cop = 0;
      if (hi - lo > maxwidth || !eng.run(lo, hi, K, c, raw, cop)) {
        if (hi - lo < 2) fatal("cannot split segment further");
        const u128 mid = lo + (hi - lo) / 2;
        stack.push_back({mid, hi}); stack.push_back({lo, mid});
        continue;
      }
      tot_raw += raw; tot_cop += cop;
      for (auto& x : c) segc.push_back({lo + x.off, x.mult});
    }
    std::sort(segc.begin(), segc.end());
    const auto th = std::chrono::steady_clock::now();
    for (auto& x : segc) {
      auto reps = recover(x.first);
      if (reps.size() != x.second) {
        std::fprintf(stderr, "n=%s: GPU multiplicity %llu, host recovery %zu\n",
                     u128str(x.first).c_str(), (unsigned long long)x.second, reps.size());
        fatal("multiplicity mismatch");
      }
      if (out) {
        std::fprintf(out->f, "%s;%zu;", u128str(x.first).c_str(), reps.size());
        for (size_t t = 0; t < reps.size(); ++t)
          std::fprintf(out->f, "%s%llu:%s%llu", t ? "," : "", (unsigned long long)reps[t].x,
                       reps[t].neg ? "-" : "", (unsigned long long)reps[t].y);
        std::fprintf(out->f, "\n");
        out->byk[reps.size()].push_back(u128str(x.first));
      }
    }
    if (out) std::fflush(out->f);
    g_ms[T_HOST] += std::chrono::duration<double, std::milli>(std::chrono::steady_clock::now() - th).count();
    if (progress) {                                          // written only after output is flushed
      const std::string tmp = std::string(progress) + ".tmp";
      FILE* p = std::fopen(tmp.c_str(), "w");
      if (!p) fatal("cannot write progress file");
      std::fprintf(p, "%s %llu %llu\n", u128str(edge[s + 1] - 1).c_str(), (unsigned long long)tot_raw,
                   (unsigned long long)tot_cop);
      std::fclose(p); std::rename(tmp.c_str(), progress);
    }
    const auto now = std::chrono::steady_clock::now();
    if (!quiet && (std::chrono::duration<double>(now - last).count() > 30 || s == nseg - 1)) {
      last = now; const double el = std::chrono::duration<double>(now - t0).count();
      const double frac = (p23(edge[s + 1] - 1) - A23) / std::max(B23 - A23, 1e-9);
      std::printf("  %llu/%llu segments, n <= %s, raw=%llu coprime=%llu, %.0fs, %.3g raw pairs/s, ETA %.0fs\n",
                  (unsigned long long)(s + 1), (unsigned long long)nseg, u128str(edge[s + 1] - 1).c_str(),
                  (unsigned long long)tot_raw, (unsigned long long)tot_cop, el, tot_raw / std::max(el, 1e-9),
                  frac > 0 ? el / frac - el : 0.0);
      std::printf("    time split: %s\n", phase_split().c_str());
      std::fflush(stdout);
    }
  }
}

// brute force for the self-test: n -> number of coprime signed representations, n <= N
static std::map<u64, u64> brute(u64 N) {
  std::map<u64, u64> m;
  for (u64 a = 1; 2 * a * a * a <= N; ++a)
    for (u64 b = a; a * a * a + b * b * b <= N; ++b) if (gcd64(a, b) == 1) ++m[a * a * a + b * b * b];
  for (u64 d = 1; fdiff(d, 1) <= N; ++d)
    for (u64 c = 1; fdiff(d, c) <= N; ++c) if (gcd64(c, d) == 1) ++m[(u64)fdiff(d, c)];
  return m;
}

static int selftest(u64 cap) {
  int fails = 0;
  auto lines = [](FILE* f) { std::map<std::string, std::string> m; char line[8192]; std::rewind(f);
    while (std::fgets(line, sizeof line, f)) { std::string s(line); auto p = s.find(';');
      if (p != std::string::npos) m[s.substr(0, p)] = s; } return m; };
  {  // 1. full pipeline vs brute force on (0, 1e7], tiny segments to force many splits
    const u64 N = 10000000; auto bf = brute(N);
    FILE* f = std::tmpfile(); Out o{f, {}}; u64 r = 0, c = 0;
    search(0, N, 2, std::min<u64>(cap, 5000), 50, &o, nullptr, r, c, true);
    std::map<u64, u64> got; for (auto& kv : lines(f)) got[std::stoull(kv.first)] = std::stoull(kv.second.substr(kv.second.find(';') + 1));
    std::fclose(f);
    std::map<u64, u64> want; u64 bcop = 0;
    for (auto& kv : bf) { bcop += kv.second; if (kv.second >= 2) want[kv.first] = kv.second; }
    const bool ok = got == want && c == bcop;
    std::printf("[selftest] %s  every n <= 1e7 with >= 2 reps: %zu numbers, coprime pairs %llu (brute force %llu)\n",
                ok ? "ok  " : "FAIL", got.size(), (unsigned long long)c, (unsigned long long)bcop);
    fails += !ok;
  }
  {  // 2. known A047697 terms and Bernstein's second five-way, exact coordinate sets
    struct KT { const char* n; int k; const char* line; } kt[] = {
      {"91", 2, "91;2;3:4,6:-5\n"}, {"3367", 3, "3367;3;34:-33,15:-2,16:-9\n"},
      {"16776487", 4, nullptr}, {"506433677359393", 5, "506433677359393;5;28065:78532,36489:77074,80025:-18218,95866:-72087,139264:-129951\n"},
      {"137904678696613339", 5, "137904678696613339;5;310998:475963,369286:444027,516931:-61128,539755:-268446,1365216:-1340093\n"}};
    for (auto& t : kt) {
      const u128 n = parse_u128(t.n);
      FILE* f = std::tmpfile(); Out o{f, {}}; u64 r = 0, c = 0;
      search(n - 1, n, t.k, cap, 1, &o, nullptr, r, c, true);
      auto m = lines(f); std::fclose(f);
      bool ok = m.count(t.n) && std::stoi(m[t.n].substr(m[t.n].find(';') + 1)) == t.k;
      if (ok && t.line) {                                    // compare exact pairs (as sets)
        auto pairs = [](const std::string& s) { std::vector<std::string> v; std::string rest = s.substr(s.rfind(';') + 1);
          size_t p = 0; while (p < rest.size()) { size_t q = rest.find_first_of(",\n", p); if (q == std::string::npos) q = rest.size();
            if (q > p) v.push_back(rest.substr(p, q - p)); p = q + 1; } std::sort(v.begin(), v.end()); return v; };
        ok = pairs(m[t.n]) == pairs(t.line);
      }
      std::printf("[selftest] %s  n=%s has %d coprime representations%s\n", ok ? "ok  " : "FAIL", t.n, t.k,
                  t.line ? " (exact pairs match)" : "");
      fails += !ok;
    }
  }
  {  // 3. split ranges add up exactly: (0,1e12] = (0,1e11] + (1e11,1e12]
    u64 r1 = 0, c1 = 0, r2 = 0, c2 = 0, r3 = 0, c3 = 0;
    search(0, 1000000000000ULL, 3, cap, 7, nullptr, nullptr, r1, c1, true);
    search(0, 100000000000ULL, 3, cap, 3, nullptr, nullptr, r2, c2, true);
    search(100000000000ULL, 1000000000000ULL, 3, cap, 5, nullptr, nullptr, r3, c3, true);
    const bool ok = r1 == r2 + r3 && c1 == c2 + c3 && c1 == 80226285ULL;   // CPU reference count
    std::printf("[selftest] %s  split ranges: coprime %llu = %llu + %llu (CPU reference 80226285)\n",
                ok ? "ok  " : "FAIL", (unsigned long long)c1, (unsigned long long)c2, (unsigned long long)c3);
    fails += !ok;
  }
  {  // 4. above 2^64: a narrow window near 1e21 must match independent recovery for every n
    const u128 lo = parse_u128("999999999999000000000"), hi = parse_u128("999999999999200000000");
    FILE* f = std::tmpfile(); Out o{f, {}}; u64 r = 0, c = 0;
    search(lo, hi, 1, cap, 1, &o, nullptr, r, c, true);     // K=1: every value is recovered and checked
    auto m = lines(f); std::fclose(f);
    u64 reps = 0; for (auto& kv : m) reps += std::stoull(kv.second.substr(kv.second.find(';') + 1));
    const bool ok = reps == c && c > 0;
    std::printf("[selftest] %s  window just below 1e21 (above 2^64): %llu coprime pairs, all %zu values re-derived independently\n",
                ok ? "ok  " : "FAIL", (unsigned long long)c, m.size());
    fails += !ok;
  }
  {  // 5. windows above 1e22 against constants from window_count.py (independent exact Python count):
     //    all coprime pairs, and the values with >= K reps with sum of (n - lo) * reps over them.
     //    The last window ends at the cube 10^24 (186 values; K=2 keeps host recovery short).
    struct W { const char* lo; const char* hi; int K; u64 pairs, values, offsum; } win[] = {
      {"9999999999999000000000", "10000000000000000000000", 1, 26, 26, 14299982169ULL},
      {"99999999999999000000000", "100000000000000000000000", 1, 9, 9, 3335768422ULL},
      {"999999999999999900000000", "1000000000000000000000000", 2, 188, 1, 299997813ULL}};
    for (auto& w : win) {
      const u128 lo = parse_u128(w.lo), hi = parse_u128(w.hi);
      FILE* f = std::tmpfile(); Out o{f, {}}; u64 r = 0, c = 0;
      search(lo, hi, w.K, cap, 1, &o, nullptr, r, c, true);   // every value with >= K reps is recovered
      auto m = lines(f); std::fclose(f);
      u64 reps = 0, offsum = 0;
      for (auto& kv : m) {
        const u64 k = std::stoull(kv.second.substr(kv.second.find(';') + 1));
        reps += k; offsum += (u64)(parse_u128(kv.first.c_str()) - lo) * k;
      }
      const bool ok = (w.K > 1 || reps == c) && c == w.pairs && m.size() == w.values && offsum == w.offsum;
      std::printf("[selftest] %s  window below %s: %llu coprime pairs, %zu values with >= %d reps (Python: %llu, %llu)\n",
                  ok ? "ok  " : "FAIL", w.hi, (unsigned long long)c, m.size(), w.K, (unsigned long long)w.pairs,
                  (unsigned long long)w.values);
      fails += !ok;
    }
  }
  std::printf("[selftest] %s\n", fails ? "FAILED" : "PASSED");
  return fails ? 1 : 0;
}

int main(int argc, char** argv) {
  u128 A = 0, B = parse_u128("1000000000000000"); u64 cap = 0, nseg = 0; int K = 5, device = 0, part = 0, parts = 0;
  bool resume = false, st = false; std::string out = "cab_gpu.txt";
  for (int i = 1; i < argc; ++i) {
    std::string a = argv[i];
    auto nx = [&]() -> const char* { if (i + 1 >= argc) fatal("missing value"); return argv[++i]; };
    if (a == "--max") B = parse_u128(nx());
    else if (a == "--min") A = parse_u128(nx());
    else if (a == "--kmin") K = (int)parse_u128(nx());
    else if (a == "--out") out = nx();
    else if (a == "--segments") nseg = (u64)parse_u128(nx());
    else if (a == "--cap") cap = (u64)parse_u128(nx());
    else if (a == "--device") device = (int)parse_u128(nx());
    else if (a == "--part") { if (std::sscanf(nx(), "%d/%d", &part, &parts) != 2 || part < 1 || part > parts) fatal("--part i/n"); }
    else if (a == "--resume") resume = true;
    else if (a == "--selftest") st = true;
    else { std::printf("usage: cabtaxi_gpu [--selftest] --max B [--min A] [--kmin K] [--out f] [--resume]\n"
                       "                   [--device d] [--part i/n] [--segments S] [--cap pairs]\n"); return 1; }
  }
#ifndef HOST_ONLY
  CU(cudaSetDevice(device));
  cudaDeviceProp prop; CU(cudaGetDeviceProperties(&prop, device));
  size_t freeb = 0, totb = 0; CU(cudaMemGetInfo(&freeb, &totb));
  const u64 streams_bytes = 2 * (icbrt(B / 2) + icbrt(B) + 16) * 8;
  if (!cap) cap = (u64)((freeb * 0.75 - streams_bytes) / 17);   // two key buffers + radix temp
  cap = std::min<u64>(cap, 2000000000ULL);                       // CUB counts are int
  std::printf("GPU %d: %s (sm_%d%d), %.1f GB free, segment cap %llu pairs\n", device, prop.name,
              prop.major, prop.minor, freeb / 1e9, (unsigned long long)cap);
#else
  (void)device;
  if (!cap) cap = 50000000;
  std::printf("host-only build, segment cap %llu pairs\n", (unsigned long long)cap);
#endif
  std::fflush(stdout);
  if (st) return selftest(std::min<u64>(cap, 300000000ULL));   // test sizes need far less than a full card
  if (B > parse_u128(LIMIT_STR)) fatal("--max is limited to 10^24");
  if (A >= B) fatal("--min must be below --max");
  if (parts) {
    const double A23 = p23(A), B23 = p23(B);
    const u128 lo = part == 1 ? A : from23(A23 + (B23 - A23) * (part - 1) / parts);
    const u128 hi = part == parts ? B : from23(A23 + (B23 - A23) * part / parts);
    A = lo; B = hi;
  }
  const std::string progress = out + ".progress";
  if (resume) {
    FILE* p = std::fopen(progress.c_str(), "r"); char buf[64] = {0};
    if (!p || std::fscanf(p, "%63s", buf) != 1) fatal("--resume: no readable progress file");
    std::fclose(p);
    const u128 done = parse_u128(buf);
    if (done < A || done > B) fatal("--resume: progress outside (min, max]");
    if (done == B) { std::printf("already complete to %s\n", buf); return 0; }
    std::printf("resuming after n = %s\n", buf); A = done;
  }
  if (!nseg) nseg = (u64)std::max(1.0, 1.2 * (p23(B) - p23(A)) / (0.5 * (double)cap));
  FILE* f = std::fopen(out.c_str(), resume ? "a" : "w"); if (!f) fatal("cannot open output");
  if (!resume) std::fprintf(f, "# cabtaxi_gpu: n = x^3 + y^3, gcd(x,y)=1, signs allowed; all %s < n <= %s with >= %d representations\n",
                            u128str(A).c_str(), u128str(B).c_str(), K);
  std::fflush(f);
  Out o{f, {}}; u64 raw = 0, cop = 0;
  const auto t0 = std::chrono::steady_clock::now();
  std::printf("search %s < n <= %s, kmin=%d, %llu segments\n", u128str(A).c_str(), u128str(B).c_str(), K,
              (unsigned long long)nseg);
  std::fflush(stdout);
  search(A, B, K, cap, nseg, &o, progress.c_str(), raw, cop, false);
  std::fclose(f);
  const double el = std::chrono::duration<double>(std::chrono::steady_clock::now() - t0).count();
  std::printf("DONE %s < n <= %s raw pairs=%llu coprime pairs=%llu kmin=%d time=%.0fs (%.3g raw pairs/s)\n",
              u128str(A).c_str(), u128str(B).c_str(), (unsigned long long)raw, (unsigned long long)cop, K, el,
              raw / std::max(el, 1e-9));
  std::printf("time split: %s\n", phase_split().c_str());
  for (auto it = o.byk.rbegin(); it != o.byk.rend(); ++it) {
    std::printf("  k=%llu: %zu numbers, smallest:", (unsigned long long)it->first, it->second.size());
    for (size_t i = 0; i < it->second.size() && i < 4; ++i) std::printf(" %s", it->second[i].c_str());
    std::printf("\n");
  }
  return 0;
}
