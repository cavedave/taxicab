// lc_fast.cpp -- inner loops of line_complete.py in C++ (six_way_ideas.md idea 1, fast version).
// Reads job lines (written by line_fast.py) from stdin; for each job enumerates the slopes of its tiers, keeps every
// canonical coprime triple with n <= B (same rules as line_complete.run_dir), counts its n exactly from the
// factorisation n = E s1 s2 s3 / (a-b)^2 (Theorem 13; s_i = x_i + y_i factored by Pollard-Brent), and prints
//   R n;k;x:y,...            for k >= 4
//   C a;b;s_lo;s_hi;slopes;triples;kmax     certificate line per job (same as line_complete --log)
//   F a b s_lo s_hi          the job overflowed 128 bits somewhere: the driver reruns it in Python
//   T n;x:y,x:y,x:y          every triple (only with --triples, for validation)
//  job header: a b s_lo s_hi H1 x0 y0 Z E D (a-b) Glo ...
// Build: g++ -O2 -std=c++17 -o lc_fast lc_fast.cpp
#include <cstdio>
#include <cstdint>
#include <cstdlib>
#include <cstring>
#include <cmath>
#include <vector>
#include <string>
#include <algorithm>
#include <map>
typedef __int128 i128; typedef unsigned __int128 u128; typedef int64_t i64; typedef uint64_t u64;

struct Overflow {};
static inline i128 mul(i128 a, i128 b) { i128 r; if (__builtin_mul_overflow(a, b, &r)) throw Overflow(); return r; }
static inline i128 add(i128 a, i128 b) { i128 r; if (__builtin_add_overflow(a, b, &r)) throw Overflow(); return r; }
static inline i128 sub(i128 a, i128 b) { i128 r; if (__builtin_sub_overflow(a, b, &r)) throw Overflow(); return r; }
static inline i128 iabs(i128 a) { return a < 0 ? -a : a; }
static inline i64 abs64(i64 a) { return a < 0 ? -a : a; }
static inline int ctz128(u128 x) { u64 lo = (u64)x; return lo ? __builtin_ctzll(lo) : 64 + __builtin_ctzll((u64)(x >> 64)); }
static inline u64 bgcd64(u64 a, u64 b) {
    if (!a) return b; if (!b) return a;
    int sh = __builtin_ctzll(a | b); a >>= __builtin_ctzll(a);
    do { b >>= __builtin_ctzll(b); if (a > b) { u64 t = a; a = b; b = t; } b -= a; } while (b);
    return a << sh;
}
static i128 gcd128(i128 sa, i128 sb) {                           // binary gcd, 64-bit path when both fit
    u128 a = (u128)iabs(sa), b = (u128)iabs(sb);
    if (!(a >> 64) && !(b >> 64)) return (i128)bgcd64((u64)a, (u64)b);
    if (!a) return (i128)b; if (!b) return (i128)a;
    int sh = ctz128(a | b); a >>= ctz128(a);
    do { b >>= ctz128(b); if (a > b) { u128 t = a; a = b; b = t; } b -= a;
         if (!(a >> 64) && !(b >> 64)) return (i128)((u128)bgcd64((u64)a, (u64)b) << sh); } while (b);
    return (i128)(a << sh);
}
static i64 gcd64(i64 a, i64 b) { a = a < 0 ? -a : a; b = b < 0 ? -b : b; while (b) { i64 t = a % b; a = b; b = t; } return a; }

static std::string s128(i128 v) {
    if (v == 0) return "0";
    bool neg = v < 0; u128 u = neg ? (u128)(-v) : (u128)v; char buf[64]; int i = 63; buf[i] = 0;
    while (u) { buf[--i] = '0' + (int)(u % 10); u /= 10; }
    if (neg) buf[--i] = '-';
    return std::string(buf + i);
}
static i128 p128(const char* s) { i128 v = 0; bool neg = false; if (*s == '-') { neg = true; s++; } while (*s >= '0' && *s <= '9') v = v * 10 + (*s++ - '0'); return neg ? -v : v; }

// ---------- 64-bit factoring (Miller-Rabin deterministic + Pollard-Brent) ----------
static u64 mulmod(u64 a, u64 b, u64 m) { return (u64)((u128)a * b % m); }
static u64 powmod(u64 a, u64 e, u64 m) { u64 r = 1; a %= m; while (e) { if (e & 1) r = mulmod(r, a, m); a = mulmod(a, a, m); e >>= 1; } return r; }
static bool is_prime(u64 n) {
    if (n < 2) return false;
    for (u64 p : {2ULL, 3ULL, 5ULL, 7ULL, 11ULL, 13ULL, 17ULL, 19ULL, 23ULL, 29ULL, 31ULL, 37ULL}) { if (n % p == 0) return n == p; }
    u64 d = n - 1; int s = 0; while ((d & 1) == 0) { d >>= 1; s++; }
    static const u64 small_b[] = {2, 3, 5, 7, 11, 13, 17}, all_b[] = {2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37};
    const u64* bs = n < 341550071728321ULL ? small_b : all_b; int nb = n < 341550071728321ULL ? 7 : 12;
    for (int bi = 0; bi < nb; bi++) { u64 a = bs[bi];
        u64 x = powmod(a, d, n); if (x == 1 || x == n - 1) continue;
        bool comp = true; for (int r = 1; r < s; r++) { x = mulmod(x, x, n); if (x == n - 1) { comp = false; break; } }
        if (comp) return false;
    }
    return true;
}
static u64 gcdu(u64 a, u64 b) { while (b) { u64 t = a % b; a = b; b = t; } return a; }
static u64 rho(u64 n) {
    if (n % 2 == 0) return 2;
    static u64 seed = 1;
    for (;;) {
        u64 c = (seed++ % (n - 1)) + 1, y = 2, m = 128, g = 1, r = 1, q = 1, x = 0, ys = 0;
        auto f = [&](u64 v) { return (mulmod(v, v, n) + c) % n; };
        do { x = y; for (u64 i = 0; i < r; i++) y = f(y); u64 k = 0;
             do { ys = y; for (u64 i = 0; i < std::min(m, r - k); i++) { y = f(y); q = mulmod(q, x > y ? x - y : y - x, n); }
                  g = gcdu(q, n); k += m; } while (k < r && g == 1);
             r <<= 1; } while (g == 1);
        if (g == n) { do { ys = f(ys); g = gcdu(x > ys ? x - ys : ys - x, n); } while (g == 1); }
        if (g != n) return g;
    }
}
static std::vector<u64> SMALLP;
static void init_small() { for (u64 p = 2; p < 1000; p++) { bool ok = true; for (u64 q = 2; q * q <= p; q++) if (p % q == 0) { ok = false; break; } if (ok) SMALLP.push_back(p); } }
static void factor64(u64 n, std::map<u64, int>& out, bool top = true) {
    if (n == 1) return;
    if (top) for (u64 p : SMALLP) { if (p * p > n) break; while (n % p == 0) { out[p]++; n /= p; } }
    if (n == 1) return;
    if (n < 1000000) { out[n]++; return; }                         // no factor below 1000 and n < 1000^2: prime
    if (n == 1) return;
    if (is_prime(n)) { out[n]++; return; }
    u64 d = rho(n); factor64(d, out, false); factor64(n / d, out, false);
}

static u128 isqrt128(u128 x) {
    if (x == 0) return 0;
    u128 r = (u128)std::sqrt((long double)x);
    while (r * r > x) r--;
    while ((r + 1) * (r + 1) <= x) r++;
    return r;
}
static u128 icbrt128(u128 x) {
    u128 r = (u128)std::cbrt((long double)x);
    while (r * r * r > x) r--;
    while ((r + 1) * (r + 1) * (r + 1) <= x) r++;
    return r;
}

// ---------- a job ----------
struct Extra { i64 p, lo, hi, q; i64 f[6][3]; };                  // primitive forms mod q = p^hi
struct Entry { i64 Hx; std::vector<std::pair<i64, i64>> want; i64 ux, uy, vx, vy; };
struct Job {
    i64 a, b, s_lo, s_hi, H1; i128 x0, y0, Z, E, D, Glo; i64 amb;
    std::vector<std::pair<i64, int>> Ef, Df;                      // factorisations of E and |a - b|
    std::vector<Extra> ex; std::vector<Entry> en;
};
static i64 DS = -1, DR = 0; static i128 B; static bool TRIPLES = false, NOCOUNT = false, NOCANON = false, CHECKG = false;

static void member(const Job& J, i64 s, i64 r, std::vector<std::pair<i64, i64>>& out) {
    out.clear();
    for (const Extra& e : J.ex) {
        i64 g = e.q;
        for (int k = 0; k < 6 && g > 1; k++) {
            i128 v = ((i128)e.f[k][0] * s % e.q * s + (i128)e.f[k][1] * s % e.q * r + (i128)e.f[k][2] * r % e.q * r) % e.q;
            g = gcd64(g, (i64)v);
        }
        i64 v = 0; while (g % e.p == 0 && g > 1) { g /= e.p; v++; }
        if (v > e.lo) out.push_back({e.p, v});
    }
}

struct Stats { u64 slopes = 0, triples = 0; int kmax = 0; };

static void process(const Job& J, i64 s, i64 r, Stats& st) {
    st.slopes++;
    i128 Q = (i128)s * s + (i128)s * r + (i128)r * r;
    i128 Bn = add(add(mul(2 * J.x0, s), mul(J.x0, r)), add(mul(J.y0, s), mul(2 * J.y0, r)));
    i128 NX = sub(mul(J.x0, Q), mul(Bn, s)), NY = sub(mul(J.y0, Q), mul(Bn, r));
    i128 W = mul(J.Z, Q), T = mul(W, J.D), a2W = mul((i128)J.a * J.a, W);
    i128 pp[3] = {sub(NX, a2W), sub(NY, a2W), sub(sub(-a2W, NX), NY)};
    i128 X[3], Y[3];
    for (int i = 0; i < 3; i++) { X[i] = mul(J.b, pp[i]); Y[i] = sub(T, mul(J.a, pp[i])); }
    i128 G = J.Glo;                                                  // G = Glo * prod p^(v_p - lo) (levels, line_complete)
    for (const Extra& e : J.ex) {
        i64 g = e.q;
        for (int k = 0; k < 6 && g > 1; k++) {
            i128 v = ((i128)e.f[k][0] * s % e.q * s + (i128)e.f[k][1] * s % e.q * r + (i128)e.f[k][2] * r % e.q * r) % e.q;
            g = (i64)bgcd64((u64)g, (u64)(v < 0 ? -v : v));
        }
        i64 v = 0; while (g > 1 && g % e.p == 0) { g /= e.p; v++; }
        for (i64 t = e.lo; t < v; t++) G = mul(G, e.p);
    }
    if (CHECKG) {
        i128 G2 = 0; for (int i = 0; i < 3; i++) G2 = gcd128(G2, gcd128(X[i], Y[i]));
        if (G2 != G) { std::fprintf(stderr, "G mismatch at %lld %lld: %s vs %s\n", (long long)s, (long long)r, s128(G).c_str(), s128(G2).c_str()); std::exit(3); }
    }
    for (int i = 0; i < 3; i++) { X[i] /= G; Y[i] /= G; }
    // validity: nonzero, coprime, three distinct representations
    for (int i = 0; i < 3; i++) { if (X[i] == 0 || Y[i] == 0 || gcd128(X[i], Y[i]) != 1) return; }
    auto key = [&](int i) { i128 u = X[i], v = Y[i]; return u < v ? std::make_pair(u, v) : std::make_pair(v, u); };
    if (key(0) == key(1) || key(0) == key(2) || key(1) == key(2)) return;
    // n = E s1 s2 s3 / (a - b)^2 (Theorem 13), sign from the points
    i128 S[3]; for (int i = 0; i < 3; i++) S[i] = add(X[i], Y[i]);
    if (S[0] == 0 || S[1] == 0 || S[2] == 0) return;
    long double est = std::log((long double)J.E) + std::log(std::fabs((long double)S[0])) + std::log(std::fabs((long double)S[1])) +
                      std::log(std::fabs((long double)S[2])) - 2 * std::log((long double)abs64(J.amb));
    bool dbg = (s == DS && r == DR);
    if (dbg) std::fprintf(stderr, "est %Lf logB %Lf S %s %s %s G %s\n", est, std::log((long double)B), s128(S[0]).c_str(), s128(S[1]).c_str(), s128(S[2]).c_str(), s128(G).c_str());
    if (est > std::log((long double)B) + 1e-6) return;           // n > B (with margin: the exact test follows)
    i128 rem = (i128)J.amb * J.amb, fac[4] = {J.E, iabs(S[0]), iabs(S[1]), iabs(S[2])};
    for (int i = 0; i < 4; i++) { i128 g = gcd128(fac[i], rem); fac[i] /= g; rem /= g; }
    if (rem != 1) throw Overflow();                                // cannot happen (Theorem 13); treat as fallback
    i128 n = 1; for (int i = 0; i < 4; i++) n = mul(n, fac[i]);
    bool neg = (S[0] < 0) ^ (S[1] < 0) ^ (S[2] < 0);              // sign of E s1 s2 s3
    if (dbg) std::fprintf(stderr, "n %s neg %d\n", s128(n).c_str(), (int)neg);
    if (n > B) return;
    if (NOCANON) { st.triples++; return; }
    // canonical ordering (least-height slope among the orderings), as line_complete.canon_slope
    i128 c = add(mul(J.a, X[0]), mul(J.b, Y[0]));
    i64 bh = -1, bs = 0, br = 0;
    for (int i = 0; i < 3; i++) for (int j = 0; j < 3; j++) {
        if (i == j) continue;
        i128 base = mul((i128)J.a * J.a, c);
        i128 dx = sub(mul(J.Z, add(mul(J.D, X[i]), base)), mul(J.x0, c));
        i128 dy = sub(mul(J.Z, add(mul(J.D, X[j]), base)), mul(J.y0, c));
        if (c < 0) { dx = -dx; dy = -dy; }                           // direction of (dx, dy) / (c Z): divide out c's sign
        if (dx == 0 && dy == 0) continue;
        i128 g = gcd128(dx, dy); dx /= g; dy /= g;
        if (dx < 0 || (dx == 0 && dy < 0)) { dx = -dx; dy = -dy; }
        if (iabs(dx) > ((i128)1 << 62) || iabs(dy) > ((i128)1 << 62)) continue;   // far beyond any searched height
        i64 S_ = (i64)dx, R_ = (i64)dy, h = std::max(abs64(R_), S_);
        if (bh < 0 || h < bh || (h == bh && (S_ < bs || (S_ == bs && R_ < br)))) { bh = h; bs = S_; br = R_; }
    }
    if (dbg) std::fprintf(stderr, "canon %lld %lld\n", (long long)bs, (long long)br);
    if (!(bs == s && br == r)) return;
    st.triples++;
    if (NOCOUNT) return;
    i128 Xo[3], Yo[3]; for (int i = 0; i < 3; i++) { Xo[i] = neg ? -X[i] : X[i]; Yo[i] = neg ? -Y[i] : Y[i]; }
    if (TRIPLES) {
        std::printf("T %s;%s:%s,%s:%s,%s:%s\n", s128(n).c_str(), s128(Xo[0]).c_str(), s128(Yo[0]).c_str(),
                    s128(Xo[1]).c_str(), s128(Yo[1]).c_str(), s128(Xo[2]).c_str(), s128(Yo[2]).c_str());
    }
    // factorisation of n from E, s_i, (a-b)^2
    std::map<u64, int> F;
    for (auto& pe : J.Ef) F[pe.first] += pe.second;
    for (int i = 0; i < 3; i++) { i128 v = iabs(S[i]); if (v >> 64) throw Overflow(); factor64((u64)v, F); }
    for (auto& pe : J.Df) F[pe.first] -= 2 * pe.second;
    // representations: s = f * (subset of split blocks) <= (4n)^(1/3) (Theorem 5), 4n/s - s^2 = 3 d^2
    i128 f = 1; std::vector<i128> blocks;
    for (auto& pe : F) {
        if (pe.second < 0) throw Overflow();
        if (pe.second == 0) continue;
        i128 pk = 1; for (int e = 0; e < pe.second; e++) pk = mul(pk, (i128)pe.first);
        if (pe.first % 3 == 1) blocks.push_back(pk);
        else if (pe.first == 3) { for (int e = 0; e < pe.second - 1; e++) f = mul(f, 3); }
        else f = mul(f, pk);
    }
    { i128 chk = 1; for (auto& pe : F) for (int e = 0; e < pe.second; e++) chk = mul(chk, (i128)pe.first); if (chk != n) throw Overflow(); }
    if ((u128)n > ((u128)1 << 125)) throw Overflow();
    u128 L = icbrt128((u128)4 * (u128)n);
    std::vector<i128> cand{f};
    if ((u128)f > L) cand.clear();
    for (i128 bk : blocks) {
        size_t m = cand.size();
        for (size_t i = 0; i < m; i++) { i128 v = cand[i]; if ((u128)v <= L / (u128)bk) cand.push_back(v * bk); }
    }
    int k = 0; std::vector<std::pair<i128, i128>> reps;
    for (i128 sv : cand) {
        u128 t = (u128)4 * (u128)n / (u128)sv; u128 s2 = (u128)sv * (u128)sv;
        if (t < s2) continue;
        u128 m3 = t - s2; if (m3 % 3) continue;
        u128 m = m3 / 3, d = isqrt128(m); if (d * d != m) continue;
        if (((u128)sv + d) % 2) continue;
        i128 x = ((i128)sv + (i128)d) / 2, y = ((i128)sv - (i128)d) / 2;
        if (y == 0 || gcd128(x, y) != 1) continue;
        k++; reps.push_back({x, y});
    }
    if (k < 3) throw Overflow();                                   // the triple itself must be found: bug guard
    if (k > st.kmax) st.kmax = k;
    if (k >= 4) {
        std::sort(reps.begin(), reps.end(), [](auto& p, auto& q) { return p > q; });
        std::string line = "R " + s128(n) + ";" + std::to_string(k) + ";";
        for (size_t i = 0; i < reps.size(); i++) line += (i ? "," : "") + s128(reps[i].first) + ":" + s128(reps[i].second);
        std::puts(line.c_str());
    }
}

static void box_points(const Job& J, i64 ux, i64 uy, i64 vx, i64 vy, i64 S0, i64 S1, i64 R0, i64 R1,
                       const std::vector<std::pair<i64, i64>>& want, i64 H1, Stats& st) {
    long double det = (long double)ux * vy - (long double)uy * vx;
    long double js[4]; int c = 0;
    for (i64 s : {S0, S1}) for (i64 r : {R0, R1}) js[c++] = ((long double)ux * r - (long double)uy * s) / det;
    i64 jlo = (i64)std::floor(*std::min_element(js, js + 4)) - 1, jhi = (i64)std::ceil(*std::max_element(js, js + 4)) + 1;
    std::vector<std::pair<i64, i64>> mem;
    for (i64 j = jlo; j <= jhi; j++) {
        long double lo = -1e30L, hi = 1e30L; bool empty = false;
        i64 cs[2] = {ux, uy}, off[2] = {j * vx, j * vy}, A[2] = {S0, R0}, Bd[2] = {S1, R1};
        for (int t = 0; t < 2; t++) {
            if (cs[t] == 0) { if (!(A[t] <= off[t] && off[t] <= Bd[t])) empty = true; continue; }
            long double x1 = (long double)(A[t] - off[t]) / cs[t], x2 = (long double)(Bd[t] - off[t]) / cs[t];
            lo = std::max(lo, std::ceil(std::min(x1, x2) - 1e-9L)); hi = std::min(hi, std::floor(std::max(x1, x2) + 1e-9L));
        }
        if (empty) continue;
        for (i64 i = (i64)lo; i <= (i64)hi; i++) {
            i64 s = i * ux + j * vx, r = i * uy + j * vy;
            if (s < S0 || s > S1 || r < R0 || r > R1) continue;
            if ((s == 0 && r != 1) || gcd64(r, s) != 1) continue;
            if (std::max(abs64(r), s) <= H1) continue;
            member(J, s, r, mem); if (mem != want) continue;
            process(J, s, r, st);
        }
    }
}

static bool read_job(Job& J) {
    // a b s_lo s_hi H1 x0 y0 Z E D amb | nE (p e)* | nD (p e)* | nex (p lo hi q f[18])* | nen (Hx nw (p v)* ux uy vx vy)*
    char tok[128];
    auto I = [&]() -> i128 { if (std::scanf("%127s", tok) != 1) throw 1; return p128(tok); };
    try {
        J = Job(); J.a = (i64)I(); J.b = (i64)I(); J.s_lo = (i64)I(); J.s_hi = (i64)I(); J.H1 = (i64)I();
        J.x0 = I(); J.y0 = I(); J.Z = I(); J.E = I(); J.D = I(); J.amb = (i64)I(); J.Glo = I();
        int nE = (int)I(); for (int i = 0; i < nE; i++) { i64 p = (i64)I(); int e = (int)I(); J.Ef.push_back({p, e}); }
        int nD = (int)I(); for (int i = 0; i < nD; i++) { i64 p = (i64)I(); int e = (int)I(); J.Df.push_back({p, e}); }
        int nx = (int)I(); for (int i = 0; i < nx; i++) { Extra e; e.p = (i64)I(); e.lo = (i64)I(); e.hi = (i64)I(); e.q = (i64)I();
            for (int k = 0; k < 6; k++) for (int t = 0; t < 3; t++) e.f[k][t] = (i64)I(); J.ex.push_back(e); }
        int ne = (int)I(); for (int i = 0; i < ne; i++) { Entry e; e.Hx = (i64)I(); int nw = (int)I();
            for (int k = 0; k < nw; k++) { i64 p = (i64)I(), v = (i64)I(); e.want.push_back({p, v}); }
            e.ux = (i64)I(); e.uy = (i64)I(); e.vx = (i64)I(); e.vy = (i64)I(); J.en.push_back(e); }
    } catch (int) { return false; }
    return true;
}

int main(int argc, char** argv) {
    if (argc < 2) { std::fprintf(stderr, "usage: lc_fast B [--triples] < jobs\n"); return 2; }
    B = p128(argv[1]); init_small();
    for (int i = 2; i < argc; i++) { if (!std::strcmp(argv[i], "--triples")) TRIPLES = true; if (!std::strcmp(argv[i], "--nocount")) NOCOUNT = true; if (!std::strcmp(argv[i], "--nocanon")) NOCANON = true; if (!std::strcmp(argv[i], "--checkg")) CHECKG = true; if (!std::strcmp(argv[i], "--debug")) { DS = atoll(argv[i + 1]); DR = atoll(argv[i + 2]); } }
    Job J;
    while (read_job(J)) {
        Stats st;
        try {
            i64 top1 = J.s_hi < 0 ? J.H1 : std::min(J.H1, J.s_hi);
            for (i64 s = J.s_lo; s <= top1; s++)
                for (i64 r = -J.H1; r <= J.H1; r++) { if ((s == 0 && r != 1) || gcd64(r, s) != 1) continue; process(J, s, r, st); }
            for (const Entry& e : J.en) {
                i64 S0 = J.s_lo, S1 = J.s_hi < 0 ? e.Hx : std::min(e.Hx, J.s_hi);
                if (S0 > S1) continue;
                box_points(J, e.ux, e.uy, e.vx, e.vy, S0, S1, -e.Hx, e.Hx, e.want, J.H1, st);
            }
            std::printf("C %lld;%lld;%lld;%s;%llu;%llu;%d\n", (long long)J.a, (long long)J.b, (long long)J.s_lo,
                        J.s_hi < 0 ? "None" : std::to_string(J.s_hi).c_str(), (unsigned long long)st.slopes, (unsigned long long)st.triples, st.kmax);
        } catch (Overflow&) {
            std::printf("F %lld %lld %lld %lld\n", (long long)J.a, (long long)J.b, (long long)J.s_lo, (long long)J.s_hi);
        }
        std::fflush(stdout);
    }
    return 0;
}
