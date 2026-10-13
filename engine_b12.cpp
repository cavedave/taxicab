// engine_b12 -- magnification hunt for taxicab numbers
//
// For each seed N (a sum of two cubes in k>=2 ways) scan every multiplier
// m = 2..mmax with N*m^3 <= UB and compute the COMPLETE representation set of
// n = N*m^3. If n has a representation that is not m*(a seed pair), m is a
// splitting factor and n is reported with its exact way count.
//
// Use with seeds from seedgen (all "root" multi-ways <= B). Then one pass
// finds every multi-way n <= UB that has a multi-way cube-quotient <= B. No
// further rounds are needed: the full rep set of every N*m^3 is computed
// directly, so chains of splits add nothing.
//
// CHANGES b11 -> b12
//   Speed (about 6x faster than b11):
//   * Seed divisors are enumerated ONCE per seed (sorted). For each m only the
//     divisors e of m^3 are generated; candidate sums s = d*e are pulled from
//     the seed list by binary search on [lo/e, hi/e]. b11 rebuilt a std::map
//     and walked every divisor of N*m^3 for every m.
//   * n/s is formed as (N/d)*(m^3/e): no 128-bit division in the hot loop.
//   * Square test on w = 3(4t - s^2) = 9D with a mod-64/63/65/11 residue
//     filter (~99% rejected before any sqrt). This also subsumes the v%3 test.
//   * Redundancy filter looks up the divisors of m in a hash map instead of
//     scanning the list of accepted splits (was O(splits^2) on small seeds).
//   Correctness:
//   * Inert-prime ratio gates removed: D square => D is a QR mod every p, so
//     the exact square test already implies them; they only added risk.
//   * Global g_seen set and the multi-round BFS removed. Each n is reported by
//     exactly one seed, deterministically: the SMALLEST seed N' with n/N' a
//     cube (and n/N' <= mcap^3). No RAM growth, no thread races, no duplicates
//     across seeds (e.g. T(5,6) = 231^3*4513486310216 = 66^3*193515725550511).
//   * --mcap now defaults to 0 (no cap). b9-b11's 25M cap silently truncated
//     the smallest seeds; b11's "--mcap 0" also built an empty SPF sieve.
//   * Seeds are verified at load: factorization multiplies back to N with all
//     factors prime, and the stored pairs equal the recomputed full rep set.
//   * Every split re-finds all k(seed) scaled pairs or the run aborts (FATAL):
//     a live check that the divisor enumeration is complete.
//   * Every reported pair satisfies a^3+b^3 == n exactly (FATAL otherwise).
//   * Compiles with clang (macOS) and GCC: std::gcd instead of std::__gcd.
//   * The b11 "race" comment was wrong: b10's count+insert were already in one
//     critical section. The duplicate BTa(7) came from two seeds
//     (5289780723136 and 27x it) across separate runs sharing FOUND7.txt.
//
// Filters (all exact or proven necessary):
//   * window  n^{1/3} < s <= (4n)^{1/3}, s = a+b, s | n
//   * s == n (mod 6)          (x^3 == x mod 6)
//   * 4(n/s) - s^2 = 3D, D = (b-a)^2 a perfect square
//
// Counting convention: a split m is suppressed when an accepted split m' | m of
// the same seed has k(m') >= k(m): then n is a pure cube multiple of n' and
// carries no new information. Histograms count reported (non-redundant) splits.
//
// Outputs (all appended; resumable):
//   <out>          seed;m;n;k;new pairs        for k >= --kmin  (default 4)
//   <out>.full     n;k;seed;m;all pairs        for k >= --fullk (default 6)
//   <out>.ckpt     seed;m_scanned;h3,h4,...    one line per finished seed
//   FOUND7.full    same as .full, for k >= 7
//
// Build: g++ -O3 -march=native -fopenmp -std=c++17 engine_b12.cpp -o engine_b12
// Test:  ./engine_b12 --selftest
// Run:   ./engine_b12 --seeds seeds_1e15.csv --threads 32 --out splits.csv

#include <algorithm>
#include <atomic>
#include <chrono>
#include <cmath>
#include <cstdint>
#include <cstdio>
#include <cstdlib>
#include <cstring>
#include <fstream>
#include <map>
#include <numeric>
#include <set>
#include <sstream>
#include <string>
#include <unordered_map>
#include <unordered_set>
#include <vector>
#include <fcntl.h>
#include <unistd.h>
#ifdef _OPENMP
#include <omp.h>
#endif

using u32 = uint32_t;
using u64 = uint64_t;
using u128 = unsigned __int128;
using Clock = std::chrono::steady_clock;
static double el(Clock::time_point t){ return std::chrono::duration<double>(Clock::now()-t).count(); }

[[noreturn]] static void fatal(const std::string& msg){ std::printf("FATAL: %s\n", msg.c_str()); std::fflush(stdout); std::exit(3); }

static std::string dec(u128 x){ if(!x) return "0"; char b[64]; int n=0;
  while(x){ b[n++]=char('0'+(int)(x%10)); x/=10; } std::string s; while(n) s.push_back(b[--n]); return s; }
static bool parse128(const std::string& s, u128& v){
  v=0; if(s.empty()) return false;
  for(char c: s){ if(c<'0'||c>'9') return false; u128 nv=v*10+(unsigned)(c-'0'); if(nv/10!=v) return false; v=nv; }
  return true;
}
static u64 icbrt128(u128 n){ if(!n) return 0; long double g=cbrtl((long double)n);
  u64 r=(u64)g; if(r>2) r-=2; else r=0;
  while((u128)(r+1)*(r+1)*(r+1)<=n) ++r; while(r&&(u128)r*r*r>n) --r; return r; }
// floor(cbrt(n)) given a close floating estimate
static inline u64 cbrt_fix(u128 n, long double est){
  u64 r=(u64)est;
  while(r && (u128)r*r*r>n) --r;
  while((u128)(r+1)*(r+1)*(r+1)<=n) ++r;
  return r;
}

static bool is_prime(u64 n){
  if(n<2) return false;
  for(u64 p: {2ULL,3ULL,5ULL,7ULL,11ULL,13ULL,17ULL,19ULL,23ULL,29ULL,31ULL,37ULL})
    if(n%p==0) return n==p;
  u64 d=n-1; int r=0; while(!(d&1)){ d>>=1; ++r; }
  for(u64 a: {2ULL,3ULL,5ULL,7ULL,11ULL,13ULL,17ULL,19ULL,23ULL,29ULL,31ULL,37ULL}){
    u64 x=1, b=a%n, e=d;
    while(e){ if(e&1) x=(u128)x*b%n; b=(u128)b*b%n; e>>=1; }
    if(x==1||x==n-1) continue;
    bool comp=true;
    for(int i=1;i<r;++i){ x=(u128)x*x%n; if(x==n-1){ comp=false; break; } }
    if(comp) return false; }
  return true;                                   // deterministic for all u64
}

// ---------------- perfect-square test ----------------
static bool QR64[64], QR63[63], QR65[65], QR11[11];
static void init_qr(){
  for(int i=0;i<64;++i) QR64[(i*i)%64]=true;
  for(int i=0;i<63;++i) QR63[(i*i)%63]=true;
  for(int i=0;i<65;++i) QR65[(i*i)%65]=true;
  for(int i=0;i<11;++i) QR11[(i*i)%11]=true;
}
static inline bool square_root(u128 w, u64& r){
  const u64 lo=(u64)w, hi=(u64)(w>>64);
  if(!QR64[lo&63]) return false;
  const u64 M=45045;                              // 63*65*11
  const u64 R64=(u64)((((u128)1)<<64)%M);         // 2^64 mod M (constant-folded)
  const u64 t = ((hi%M)*R64 + lo%M) % M;          // all-u64: no __umodti3 call
  if(!QR63[t%63] || !QR65[t%65] || !QR11[t%11]) return false;
  u64 g=(u64)sqrtl((long double)w);
  while(g && (u128)g*g>w) --g;
  while((u128)(g+1)*(g+1)<=w) ++g;
  r=g; return (u128)g*g==w;
}

// ---------------- smallest-prime-factor sieve for m ----------------
static std::vector<u32> g_spf; static u64 g_spf_lim=0;
static void build_spf(u64 lim){
  g_spf_lim=lim; g_spf.assign(lim+1,0);
  for(u64 i=2;i<=lim;++i) if(!g_spf[i]){ g_spf[i]=(u32)i;
    if(i<=lim/i) for(u64 j=i*i;j<=lim;j+=i) if(!g_spf[j]) g_spf[j]=(u32)i; }
}
struct MFac { int np=0; u64 p[16]; int e[16]; };
static inline void factor_m(u64 m, MFac& F){
  F.np=0;
  if(m<=g_spf_lim){
    while(m>1){ u64 p=g_spf[m]; int c=0; while(m%p==0){ m/=p; ++c; } F.p[F.np]=p; F.e[F.np]=c; ++F.np; }
    return;
  }
  for(u64 p=2; p*p<=m; p+=(p==2?1:2)) if(m%p==0){ int c=0; while(m%p==0){ m/=p; ++c; } F.p[F.np]=p; F.e[F.np]=c; ++F.np; }
  if(m>1){ F.p[F.np]=m; F.e[F.np]=1; ++F.np; }
}

// ---------------- seeds ----------------
using Pair = std::pair<u64,u64>;
struct Seed { u128 n=0; std::vector<std::pair<u64,int>> fac; std::vector<Pair> reps; };
// A sum s=a+b of n gives t = n/s = a^2-ab+b^2, a norm from Z[w]. So every
// prime q == 2 (mod 3) (2, 5, 11, ...) divides t to an EVEN power. This prunes
// whole branches of the divisor enumeration: per inert prime, half the
// exponent choices for s are impossible.
static const int MAXBITS=24;                     // inert primes of N tracked in masks
struct SeedCtx {
  const Seed* S=nullptr;
  // divisors d of N, grouped by parity mask over N's inert primes, sorted by d
  std::vector<u64> d; std::vector<u128> cof;      // d and N/d, group-contiguous
  std::vector<std::pair<u32,std::pair<u32,u32>>> grp;   // mask -> [begin,end), sorted by mask
  std::vector<u64> pr; std::vector<int> bit;      // seed primes; mask bit (-1: none)
  u32 maskN=0;                                    // parity of v_q(N) for tracked q
  std::vector<int32_t> gidx;                      // mask -> group index (-1 none), when nb small
  long double cbN=0, cb4N=0; unsigned n6=0;
};
static inline bool inert(u64 p){ return p%3==2; }
static void build_ctx(const Seed& S, u64 dlim, SeedCtx& C){
  C.S=&S; C.cbN=cbrtl((long double)S.n); C.cb4N=cbrtl(4.0L*(long double)S.n); C.n6=(unsigned)(S.n%6);
  int nb=0;
  for(auto& pe: S.fac){
    C.pr.push_back(pe.first);
    int b=(inert(pe.first) && nb<MAXBITS) ? nb++ : -1;
    C.bit.push_back(b);
    if(b>=0 && (pe.second&1)) C.maskN|=1u<<b;
  }
  std::vector<std::pair<u64,u32>> ds{{1,0}};      // (d, parity mask of d)
  for(size_t i=0;i<S.fac.size();++i){ const u64 p=S.fac[i].first; const int b=C.bit[i];
    size_t sz=ds.size();
    for(size_t t=0;t<sz;++t){ u128 v=ds[t].first; u32 mk=ds[t].second;
      for(int j=1;j<=S.fac[i].second;++j){ v*=p; if(v>dlim) break;
        ds.push_back({(u64)v, (b>=0 && (j&1)) ? (mk|(1u<<b)) : mk}); } } }
  std::sort(ds.begin(),ds.end(),[](const std::pair<u64,u32>& x,const std::pair<u64,u32>& y){
    return x.second!=y.second ? x.second<y.second : x.first<y.first; });
  C.d.resize(ds.size()); C.cof.resize(ds.size());
  for(size_t i=0;i<ds.size();++i){ C.d[i]=ds[i].first; C.cof[i]=S.n/ds[i].first; }
  for(size_t i=0;i<ds.size();){ size_t j=i; while(j<ds.size() && ds[j].second==ds[i].second) ++j;
    C.grp.push_back({ds[i].second,{(u32)i,(u32)j}}); i=j; }
  if(nb<=16){ C.gidx.assign(1u<<nb,-1); for(size_t g=0;g<C.grp.size();++g) C.gidx[C.grp[g].first]=(int32_t)g; }
}

struct ME { u64 e; u128 ce; u32 mask; };
struct Scratch { std::vector<ME> me, me2; std::vector<Pair> found; };

// Complete rep set of n = N*m^3 (m=1 allowed), sorted, into W.found.
static u128 reps_at(const SeedCtx& C, u64 m, const MFac& F, Scratch& W){
  const u128 m3=(u128)m*m*m, n=C.S->n*m3;
  const u64 lo=cbrt_fix(n, (long double)m*C.cbN)+1;          // s^3 > n
  const u64 hi=cbrt_fix(4*n, (long double)m*C.cb4N);         // s^3 <= 4n
  W.found.clear();
  if(lo>hi) return n;
  // divisors e of m^3 with e <= hi, paired with m^3/e; parity-pruned
  u32 target0=C.maskN;
  W.me.clear(); W.me.push_back({1,1,0});
  for(int i=0;i<F.np;++i){
    const u64 p=F.p[i]; const int E=3*F.e[i];
    int b=-1; bool inN=false;
    for(size_t k=0;k<C.pr.size();++k) if(C.pr[k]==p){ inN=true; b=C.bit[k]; break; }
    int jstep=1, jstart=0;
    if(inert(p)){
      if(!inN){ jstep=2; jstart=E&1; }            // v_p(t)=E-j must be even
      else if(b>=0 && (F.e[i]&1)) target0^=1u<<b; // v_p(n)=v_p(N)+3e: parity flips by e
    }
    u128 pw[3*64+1]; pw[0]=1; for(int j=1;j<=E;++j) pw[j]=pw[j-1]*p;   // E = 3*v_p(m) <= 189
    W.me2.clear();
    for(auto& x: W.me){
      for(int j=jstart;j<=E;j+=jstep){
        const u128 e=(u128)x.e*pw[j];
        if(e>hi) break;
        W.me2.push_back({(u64)e, x.ce*pw[E-j], (b>=0 && (j&1)) ? (x.mask^(1u<<b)) : x.mask});
      }
    }
    W.me.swap(W.me2);
  }
  const unsigned n6=(unsigned)(((u64)C.n6*(unsigned)(m3%6))%6);
  const u64* dB=C.d.data();
  const size_t ng=C.grp.size();
  for(auto& x: W.me){
    const u32 want=target0^x.mask;                // parity mask d must have
    size_t g0;
    if(!C.gidx.empty()){ int32_t g=C.gidx[want]; if(g<0) continue; g0=(size_t)g; }
    else { size_t L=0,R=ng; while(L<R){ size_t M=(L+R)/2; if(C.grp[M].first<want) L=M+1; else R=M; }
      if(L==ng || C.grp[L].first!=want) continue; g0=L; }
    const u64 e=x.e; const u128 ce=x.ce;
    // d in [lo/e, hi/e]: float start point, exact integer bounds below
    const double inv=1.0/(double)e;
    const u64 dl0=(u64)((double)lo*inv*(1-1e-12));
    const u64* gB=dB+C.grp[g0].second.first; const u64* gE=dB+C.grp[g0].second.second;
    if((u128)gE[-1]*e<lo || (u128)gB[0]*e>hi) continue;   // no d of this group fits
    for(const u64* it=std::lower_bound(gB,gE,dl0); it!=gE; ++it){
      const u128 sw=(u128)*it*e;
      if(sw<lo) continue;
      if(sw>hi) break;
      const u64 s=(u64)sw;
      if(s%6!=n6) continue;
      const u128 t=C.cof[it-dB]*ce;                // n/s exactly
      const u128 s2=(u128)s*s, t4=4*t;
      if(t4<=s2) continue;
      u64 R; if(!square_root(3*(t4-s2),R)) continue; // 9D = R^2
      const u64 r=R/3;
      if((s^r)&1) continue;
      if(r>=s) continue;
      W.found.push_back({(s-r)/2,(s+r)/2});
    }
  }
  if(W.found.size()>1){ std::sort(W.found.begin(),W.found.end());
    W.found.erase(std::unique(W.found.begin(),W.found.end()),W.found.end()); }
  return n;
}

// ---------------- run configuration ----------------
static u128 UB;
static u64 g_mcap=0;
static int g_kmin=4, g_fullk=6;
struct U128Hash { size_t operator()(const u128& x) const noexcept {
  u64 h=(u64)x ^ ((u64)(x>>64)*0x9e3779b97f4a7c15ULL);
  h^=h>>30; h*=0xbf58476d1ce4e5b9ULL; h^=h>>27; h*=0x94d049bb133111ebULL; h^=h>>31; return (size_t)h; } };
static std::unordered_set<u128,U128Hash> g_seedset;
static std::atomic<u64> g_redundant{0}, g_deferred{0};

static u64 mmax_of(u128 N){
  if(N>=UB) return 0;
  u64 mm=icbrt128(UB/N);
  if(g_mcap && mm>g_mcap) mm=g_mcap;
  return mm;
}

// n is reported by the smallest seed N' with n = N'*g^3. Here N = n/m^3; a
// smaller owner needs g > m, g^3 | n, n/g^3 a seed, and g within its scan.
static bool is_owner(const Seed& S, u64 m, const MFac& F, u128 n){
  if(g_seedset.empty()) return true;
  std::vector<std::pair<u64,int>> ex;                 // exponent of each prime in n
  for(auto& pe: S.fac) ex.push_back(pe);
  for(int i=0;i<F.np;++i){ bool hit=false;
    for(auto& pe: ex) if(pe.first==F.p[i]){ pe.second+=3*F.e[i]; hit=true; break; }
    if(!hit) ex.push_back({F.p[i],3*F.e[i]}); }
  const u64 gmax=icbrt128(n);
  std::vector<u64> gs{1};
  for(auto& pe: ex){ size_t sz=gs.size();
    for(size_t t=0;t<sz;++t){ u128 g=gs[t];
      for(int j=3;j<=pe.second;j+=3){ g*=pe.first; if(g>gmax) break; gs.push_back((u64)g); } } }
  for(u64 g: gs){
    if(g<=m) continue;
    if(g_mcap && g>g_mcap) continue;
    if(g_seedset.count(n/((u128)g*g*g))) return false;
  }
  return true;
}

struct Split { u64 m; u128 n; int k; std::vector<Pair> full, news; };
struct Sink { virtual void put(const Seed&, const Split&)=0; virtual ~Sink(){} };

// Scan one seed. Returns number of multipliers scanned; fills hist[k].
static u64 process_seed(const Seed& S, u64 dlim, Sink& sink, std::vector<u64>& hist){
  const u64 mmax=mmax_of(S.n);
  if(mmax<2) return 0;
  SeedCtx C; build_ctx(S,dlim,C);
  Scratch W; MFac F;
  std::unordered_map<u64,int> accepted;              // m -> k for accepted splits
  std::vector<u64> mdivs;
  const size_t k0=S.reps.size();
  for(u64 m=2;m<=mmax;++m){
    factor_m(m,F);
    const u128 n=reps_at(C,m,F,W);
    const size_t k=W.found.size();
    size_t scaled=0;
    Split sp; sp.m=m; sp.n=n; sp.k=(int)k;
    if(k==k0){                                      // fast path: must be exactly the scaled pairs
      for(size_t i=0;i<k0;++i) if(W.found[i].first!=S.reps[i].first*m || W.found[i].second!=S.reps[i].second*m)
        fatal("seed "+dec(S.n)+" m="+std::to_string(m)+": rep set is not m*(seed pairs)");
      continue;
    }
    for(auto& pr: W.found){
      if(pr.first%m==0 && pr.second%m==0 &&
         std::binary_search(S.reps.begin(),S.reps.end(),Pair{pr.first/m,pr.second/m})) ++scaled;
      else sp.news.push_back(pr);
    }
    if(scaled!=k0) fatal("seed "+dec(S.n)+" m="+std::to_string(m)+": found "+std::to_string(scaled)+
                         " of "+std::to_string(k0)+" scaled seed pairs (divisor enumeration incomplete)");
    if(sp.news.empty()) continue;                   // only m*(seed pairs)
    // redundancy: an accepted m' | m with k(m') >= k
    mdivs.assign(1,1);
    for(int i=0;i<F.np;++i){ size_t sz=mdivs.size(); u64 pw=1;
      for(int j=1;j<=F.e[i];++j){ pw*=F.p[i]; for(size_t t=0;t<sz;++t) mdivs.push_back(mdivs[t]*pw); } }
    bool redundant=false;
    for(u64 d: mdivs){ if(d<2||d==m) continue;
      auto it=accepted.find(d); if(it!=accepted.end() && it->second>=(int)k){ redundant=true; break; } }
    if(redundant){ ++g_redundant; continue; }
    accepted[m]=(int)k;
    if(!is_owner(S,m,F,n)){ ++g_deferred; continue; }
    for(auto& pr: W.found)
      if((u128)pr.first*pr.first*pr.first+(u128)pr.second*pr.second*pr.second!=n)
        fatal("pair "+std::to_string(pr.first)+":"+std::to_string(pr.second)+" fails a^3+b^3==n="+dec(n));
    sp.full=W.found;
    if(hist.size()<=k) hist.resize(k+1,0);
    ++hist[k];
    sink.put(S,sp);
  }
  return mmax-1;
}

// ---------------- seed loading ----------------
static std::vector<std::string> split(const std::string& s, char c){
  std::vector<std::string> out; std::string cur; std::stringstream ss(s);
  while(std::getline(ss,cur,c)) if(!cur.empty()) out.push_back(cur);
  return out;
}
static std::vector<Seed> load_seeds(const std::string& path){
  std::ifstream f(path); if(!f) fatal("cannot open seeds file "+path);
  std::vector<Seed> out; std::string line; size_t ln=0;
  while(std::getline(f,line)){
    ++ln; if(line.empty()) continue;
    std::vector<std::string> fld; { std::string cur; std::stringstream ss(line); while(std::getline(ss,cur,';')) fld.push_back(cur); }
    const std::string where=path+":"+std::to_string(ln)+": ";
    if(fld.size()<4) fatal(where+"expected N;k;p:e,...;a:b,...");
    Seed S; if(!parse128(fld[0],S.n)) fatal(where+"bad N");
    u128 prod=1;
    for(auto& pe: split(fld[2],',')){
      auto c=pe.find(':'); u128 p; if(c==std::string::npos || !parse128(pe.substr(0,c),p)) fatal(where+"bad factor "+pe);
      int e=std::atoi(pe.c_str()+c+1);
      if(p>>64 || !is_prime((u64)p) || e<1) fatal(where+"factor "+pe+" is not a prime power");
      S.fac.push_back({(u64)p,e});
      for(int j=0;j<e;++j){ prod*=p; if(prod>S.n) fatal(where+"factorization exceeds N"); }
    }
    if(prod!=S.n) fatal(where+"factorization does not multiply to N");
    for(auto& ab: split(fld[3],',')){
      auto c=ab.find(':'); u128 a,b; if(c==std::string::npos || !parse128(ab.substr(0,c),a) || !parse128(ab.substr(c+1),b)) fatal(where+"bad pair "+ab);
      if(a>b) std::swap(a,b);
      if(a*a*a+b*b*b!=S.n) fatal(where+"pair "+ab+" fails a^3+b^3==N");
      S.reps.push_back({(u64)a,(u64)b});
    }
    std::sort(S.reps.begin(),S.reps.end());
    if(S.reps.size()<2) fatal(where+"seed needs >= 2 pairs");
    out.push_back(std::move(S));
  }
  return out;
}
// Stored pairs must be the complete rep set (else "scaled" classification breaks)
static void verify_seed_reps(const std::vector<Seed>& seeds){
  std::atomic<u64> bad{0};
#pragma omp parallel for schedule(dynamic,256)
  for(size_t i=0;i<seeds.size();++i){
    SeedCtx C; build_ctx(seeds[i], icbrt128(4*seeds[i].n), C);
    Scratch W; MFac F; F.np=0;
    reps_at(C,1,F,W);
    if(W.found!=seeds[i].reps){
#pragma omp critical
      { if(bad<10) std::printf("  seed %s: stored %zu pairs, full rep set has %zu\n",
          dec(seeds[i].n).c_str(), seeds[i].reps.size(), W.found.size()); }
      ++bad;
    }
  }
  if(bad) fatal(std::to_string(bad.load())+" seeds have incomplete or wrong pair lists");
}

// ---------------- production run ----------------
static bool write_full(int fd, const std::string& s){
  const char* p=s.data(); size_t len=s.size();
  while(len){ ssize_t w=write(fd,p,len); if(w<=0) return false; p+=w; len-=(size_t)w; }
  return true;
}
static std::string pairs_str(const std::vector<Pair>& v){
  std::string s; for(size_t i=0;i<v.size();++i){ if(i) s+=","; s+=std::to_string(v[i].first)+":"+std::to_string(v[i].second); } return s;
}
struct FileSink : Sink {
  int fo, ff; std::string bo, bf;
  FileSink(int a,int b):fo(a),ff(b){}
  void put(const Seed& S, const Split& sp) override {
    if(sp.k>=g_kmin) bo+=dec(S.n)+";"+std::to_string(sp.m)+";"+dec(sp.n)+";"+std::to_string(sp.k)+";"+pairs_str(sp.news)+"\n";
    if(sp.k>=g_fullk || sp.k>=7){
      std::string line=dec(sp.n)+";"+std::to_string(sp.k)+";"+dec(S.n)+";"+std::to_string(sp.m)+";"+pairs_str(sp.full)+"\n";
      if(sp.k>=g_fullk) bf+=line;
      if(sp.k>=7){
#pragma omp critical(found7)
        { FILE* f=fopen("FOUND7.full","a"); if(f){ fputs(line.c_str(),f); fclose(f); }
          std::printf("*** k=%d: %s (seed %s, m=%llu) ***\n", sp.k, dec(sp.n).c_str(), dec(S.n).c_str(), (unsigned long long)sp.m);
          std::fflush(stdout); }
      }
    }
    if(bo.size()>(1<<20)) flush();
  }
  void flush(){ if(!bo.empty()){ write_full(fo,bo); bo.clear(); } if(!bf.empty()){ write_full(ff,bf); bf.clear(); } }
};

static int run(const std::string& seedpath, const std::string& out, int threads){
  auto t0=Clock::now();
  auto seeds=load_seeds(seedpath);
  std::sort(seeds.begin(),seeds.end(),[](const Seed& a,const Seed& b){ return a.n<b.n; });
  seeds.erase(std::unique(seeds.begin(),seeds.end(),[](const Seed& a,const Seed& b){ return a.n==b.n; }),seeds.end());
  std::printf("=== engine_b12 ===\n  seeds=%zu  UB=%s  mcap=%llu  kmin=%d  fullk=%d  threads=%d\n",
              seeds.size(), dec(UB).c_str(), (unsigned long long)g_mcap, g_kmin, g_fullk, threads);
  verify_seed_reps(seeds);
  std::printf("  seeds verified (factorizations prime, pair lists complete) %.1fs\n", el(t0));
  for(auto& s: seeds) if(s.n<UB) g_seedset.insert(s.n);

  // resume
  const std::string ckpt=out+".ckpt";
  std::unordered_set<u128,U128Hash> done; std::vector<u64> hist;
  { std::ifstream f(ckpt); std::string line;
    while(std::getline(f,line)){
      auto fld=split(line,';'); if(fld.size()<2) continue;
      u128 n; if(!parse128(fld[0],n)) continue;
      done.insert(n);
      if(fld.size()>=3){ auto h=split(fld[2],','); for(size_t i=0;i<h.size();++i){
        if(hist.size()<=i+3) hist.resize(i+4,0); hist[i+3]+=strtoull(h[i].c_str(),0,10); } }
    } }
  std::vector<const Seed*> work; long double total=0, todo=0;
  u64 mmax_all=0;
  for(auto& s: seeds){ u64 mm=mmax_of(s.n); total+=mm; if(mm<2 || done.count(s.n)) continue;
    work.push_back(&s); todo+=mm; mmax_all=std::max(mmax_all,mm); }
  std::printf("  resume: %zu seeds already done, %zu to scan, %.3Le of %.3Le multipliers left\n",
              done.size(), work.size(), todo, total);
  if(work.empty()){ std::printf("  nothing to do\n"); return 0; }
  build_spf(mmax_all);
  std::printf("  SPF sieve to %llu (%.2f GB)\n", (unsigned long long)mmax_all, mmax_all*4.0/1e9);
  const u64 dlim=icbrt128(4*UB);

  std::atomic<u64> nseeds{0}; std::atomic<u64> mdone{0};
  auto tr=Clock::now(); double last=0;
#pragma omp parallel num_threads(threads)
  {
    int fo=open(out.c_str(),O_WRONLY|O_CREAT|O_APPEND,0644);
    int ff=open((out+".full").c_str(),O_WRONLY|O_CREAT|O_APPEND,0644);
    int fc=open(ckpt.c_str(),O_WRONLY|O_CREAT|O_APPEND,0644);
    if(fo<0||ff<0||fc<0) fatal("cannot open output files");
    FileSink sink(fo,ff);
#pragma omp for schedule(dynamic,1)
    for(size_t i=0;i<work.size();++i){
      std::vector<u64> h;
      u64 ms=process_seed(*work[i],dlim,sink,h);
      sink.flush();
      std::string c=dec(work[i]->n)+";"+std::to_string(ms)+";";
      for(size_t k=3;k<h.size();++k){ if(k>3) c+=","; c+=std::to_string(h[k]); }
      c+="\n"; write_full(fc,c);
#pragma omp critical(hist)
      { for(size_t k=0;k<h.size();++k){ if(hist.size()<=k) hist.resize(k+1,0); hist[k]+=h[k]; }
        u64 d=++nseeds; mdone+=ms; double t=el(tr);
        if(t-last>60 || d==work.size()){ last=t;
          double frac=(double)mdone.load()/(double)todo;
          std::printf("[%6.0fs] %llu/%zu seeds, %.1f%% of multipliers, ETA %.0fs | k>=5: ",
                      t,(unsigned long long)d,work.size(),100*frac, frac>0? t/frac-t : 0.0);
          for(size_t k=5;k<hist.size();++k) std::printf("k%zu=%llu ",k,(unsigned long long)hist[k]);
          std::printf("\n"); std::fflush(stdout); } }
    }
    sink.flush(); close(fo); close(ff); close(fc);
  }
  std::printf("done %.1fs; %llu redundant scaled copies suppressed, %llu reported by a smaller seed\n",
              el(t0),(unsigned long long)g_redundant.load(),(unsigned long long)g_deferred.load());
  std::printf("histogram (all seeds incl. resumed):\n");
  for(size_t k=3;k<hist.size();++k) std::printf("  k=%zu %llu\n",k,(unsigned long long)hist[k]);
  return 0;
}

// ---------------- selftest ----------------
struct VecSink : Sink { std::vector<Split> v; void put(const Seed&, const Split& sp) override { v.push_back(sp); } };
static Seed make_seed(const char* n, std::vector<Pair> reps){
  Seed S; parse128(n,S.n); S.reps=reps; std::sort(S.reps.begin(),S.reps.end());
  u128 x=S.n;
  for(u64 p=2;p<2000000 && (u128)p*p<=x;++p){ int e=0; while(x%p==0){ x/=p; ++e; } if(e) S.fac.push_back({p,e}); }
  if(x>1){ if(x>>64 || !is_prime((u64)x)) fatal("selftest factor"); S.fac.push_back({(u64)x,1}); }
  return S;
}
static std::vector<Pair> brute(u128 n){
  std::vector<Pair> r;
  for(u64 a=1; 2*(u128)a*a*a<=n; ++a){ u128 rest=n-(u128)a*a*a; u64 b=icbrt128(rest);
    if((u128)b*b*b==rest && b>=a) r.push_back({a,b}); }
  return r;
}
static int selftest(){
  bool ok=true;
  auto expect=[&](bool c, const std::string& what){ std::printf("[selftest] %s %s\n", c?"ok  ":"FAIL", what.c_str()); if(!c) ok=false; };
  build_spf(1000000);
  // 1. brute-force cross-check of the complete rep set at every m
  {
    std::vector<Seed> ss={ make_seed("1729",{{1,12},{9,10}}), make_seed("4104",{{2,16},{9,15}}),
      make_seed("13832",{{2,24},{18,20}}), make_seed("87539319",{{167,436},{228,423},{255,414}}),
      make_seed("6963472309248",{{2421,19083},{5436,18948},{10200,18072},{13322,16630}}) };
    u64 checked=0, mism=0;
    for(auto& S: ss){
      UB=(u128)200000000000000ULL;                    // 2e14
      SeedCtx C; build_ctx(S,icbrt128(4*UB),C); Scratch W; MFac F;
      for(u64 m=1; S.n*(u128)m*m*m<=UB; ++m){
        factor_m(m,F); u128 n=reps_at(C,m,F,W);
        if(W.found!=brute(n)){ ++mism; std::printf("  mismatch N=%s m=%llu\n",dec(S.n).c_str(),(unsigned long long)m); }
        ++checked; }
    }
    expect(mism==0, "complete rep sets match brute force at "+std::to_string(checked)+" (seed,m) points <= 2e14");
  }
  // 1b. high prime powers in m (E = 3*v_p(m) up to 84; b12-dev overflowed pw[64] at v_2(m) >= 22)
  { Seed S=make_seed("1729",{{1,12},{9,10}});
    bool good=true;
    for(u64 m: {1ULL<<21, 1ULL<<22, 1ULL<<28, 3486784401ULL /*3^20*/, 2ULL*3*5*7*11*13*17*19*23}){
      u128 n=S.n*(u128)m*m*m; SeedCtx C; build_ctx(S,icbrt128(4*n),C); Scratch W; MFac F; factor_m(m,F);
      reps_at(C,m,F,W);
      for(auto& pr: S.reps) if(!std::binary_search(W.found.begin(),W.found.end(),Pair{pr.first*m,pr.second*m})) good=false;
      for(auto& pr: W.found) if((u128)pr.first*pr.first*pr.first+(u128)pr.second*pr.second*pr.second!=n) good=false;
    }
    expect(good, "m = 2^21, 2^22, 2^28, 3^20, 23#: scaled pairs found, all pairs exact"); }
  auto first_split=[&](const Seed& S, const char* ub){ parse128(ub,UB); VecSink vs; std::vector<u64> h;
    process_seed(S,icbrt128(4*UB),vs,h); return vs.v; };
  // 2. Ta(5) -> Ta(6) at m=79, nothing earlier
  { Seed ta5=make_seed("48988659276962496",{{38787,365757},{107839,362753},{205292,342952},{221424,336588},{231518,331954}});
    auto v=first_split(ta5,"24885189317885898975235988544");
    expect(!v.empty() && v[0].m==79 && v[0].k==6 && dec(v[0].n)=="24153319581254312065344", "Ta(5) first splits at m=79 -> Ta(6)");
    bool r127=false; for(auto& s: v) if(s.m==127 && s.k==6 && dec(s.n)=="100347536855722268443968") r127=true;
    expect(r127, "Ta(5) m=127 -> Boyer T'(6,2)");
    std::set<u64> ms; for(auto& s: v) if(s.m<10000 && s.k==6) ms.insert(s.m);
    expect(ms==std::set<u64>({79,127,139,727,4622}), "Ta(5) splitting factors < 10000 = {79,127,139,727,4622} (Boyer Fig. A3)"); }
  { Seed t52=make_seed("490593422681271000",{{48369,788631},{233775,781785},{285120,776070},{543145,691295},{579240,666630}});
    auto v=first_split(t52,"1000000000000000000000000000000");
    std::set<u64> ms; for(auto& s: v) if(s.m<10000 && s.k==6) ms.insert(s.m);
    expect(ms==std::set<u64>({139,377,1139,1297}), "T(5,2) splitting factors < 10000 = {139,377,1139,1297} (Boyer Fig. A3)"); }
  // 3. Ta(6) -> Boyer's BTa(7) at m=101, nothing earlier
  { Seed ta6=make_seed("24153319581254312065344",{{582162,28906206},{3064173,28894803},{8519281,28657487},{16218068,27093208},{17492496,26590452},{18289922,26224366}});
    auto v=first_split(ta6,"24885189317885898975235988544");
    expect(!v.empty() && v[0].m==101 && v[0].k==7 && dec(v[0].n)=="24885189317885898975235988544", "Ta(6) first splits at m=101 -> BTa(7)"); }
  // 4. the family missing from the old seeds.csv
  { Seed r=make_seed("4513486310216",{{5756,16290},{9843,15269}});
    auto v=first_split(r,"1000000000000000000000000");
    std::map<u64,std::pair<int,std::string>> by; for(auto& s: v) by[s.m]={s.k,dec(s.n)};
    expect(by.count(231) && by[231].first==5 && by[231].second=="55634997032869710456", "root 4513486310216 m=231 -> T(5,6)");
    expect(by.count(525) && by[525].first==5 && by[525].second=="653115573732974625000", "root 4513486310216 m=525 -> T(5,14)");
    expect(by.count(5775) && by[5775].first==6 && by[5775].second=="869296828638589225875000", "root 4513486310216 m=5775 -> Boyer T'(6,4)"); }
  // 5. ownership: the same 6-way from two roots is reported once
  { Seed r1=make_seed("4513486310216",{{5756,16290},{9843,15269}});
    Seed r2=make_seed("193515725550511",{{20146,57015},{29424,55183}});
    parse128("1000000000000000000000000",UB);
    g_seedset={r1.n,r2.n};
    VecSink a,b; std::vector<u64> h;
    process_seed(r1,icbrt128(4*UB),a,h); process_seed(r2,icbrt128(4*UB),b,h);
    int c=0; for(auto& s: a.v) if(dec(s.n)=="55634997032869710456") ++c;
    for(auto& s: b.v) if(dec(s.n)=="55634997032869710456") ++c;
    expect(c==1, "T(5,6) reported by exactly one of its two roots");
    g_seedset.clear(); }
  std::printf("[selftest] %s\n", ok?"PASSED":"FAILED");
  return ok?0:1;
}

int main(int argc,char**argv){
  setvbuf(stdout,nullptr,_IOLBF,0);               // logs survive a crash when redirected
  init_qr();
  std::string seeds="seeds.csv", out="splits.csv"; int threads=0; bool st=false;
  std::string ubstr="24885189317885898975235988544";
  for(int i=1;i<argc;++i){ std::string a=argv[i];
    auto nx=[&]()->const char*{ if(i+1>=argc){ std::printf("missing value for %s\n",a.c_str()); std::exit(1);} return argv[++i]; };
    if(a=="--seeds") seeds=nx();
    else if(a=="--out") out=nx();
    else if(a=="--threads") threads=atoi(nx());
    else if(a=="--ub") ubstr=nx();
    else if(a=="--mcap") g_mcap=strtoull(nx(),0,10);
    else if(a=="--kmin") g_kmin=atoi(nx());
    else if(a=="--fullk") g_fullk=atoi(nx());
    else if(a=="--selftest") st=true;
    else if(a=="--rounds"){ if(atoi(nx())!=1) std::printf("note: b12 is single-pass; --rounds ignored\n"); }
    else { std::printf("usage: engine_b12 [--seeds f] [--out f] [--ub decimal] [--threads n] [--mcap m] [--kmin k] [--fullk k] [--selftest]\n"); return 1; }
  }
  if(st) return selftest();
  if(!parse128(ubstr,UB) || UB==0) fatal("bad --ub");
  if(UB>((u128)1<<100)) fatal("--ub too large (pairs must fit u64; keep UB < 2^100)");
#ifdef _OPENMP
  if(threads<=0) threads=omp_get_max_threads();
#else
  threads=1;
#endif
  return run(seeds,out,threads);
}
