// engine_cf -- construct-and-sieve hunt for cubefree / squarefree taxicab numbers.
//
// Magnification (engine_b9) produces N = seed * m^3, so it can never emit a
// cubefree or squarefree hit. This engine enumerates those N directly:
//
//   1. Build candidates N = (product of split primes p≡1 mod 3) * extras
//      extras = 3^e * (inert primes ≡2 mod 3), exponents in {0,1} or {0,1,2}
//   2. Enumerate divisors s in the median window  N^{1/3} < s <= (4N)^{1/3}
//   3. Su: s ≡ N (mod 6)
//   4. Exact test: 4(N/s) - s^2 = 3d^2  with d perfect square, s≡d (mod 2)
//   5. Recover (a,b) = ((s-d)/2, (s+d)/2)
//
// Targets:
//   * A080642(5)  -- 5th cubefree taxicab number (open)
//   * squarefree taxicab sequence (no OEIS entry yet)
//
// Build: g++ -O3 -fopenmp -std=c++17 -march=native engine_cf.cpp -o engine_cf
// Test:  ./engine_cf --selftest
// Run:   ./engine_cf --ub 1e15 --pmax 500 --omega-min 3 --omega-max 7 --kmin 2

#include <algorithm>
#include <atomic>
#include <chrono>
#include <cmath>
#include <cstdint>
#include <cstdio>
#include <cstdlib>
#include <cstring>
#include <mutex>
#include <string>
#include <utility>
#include <vector>
#ifdef _OPENMP
#include <omp.h>
#endif

using u64 = uint64_t;
using u128 = unsigned __int128;
using Clock = std::chrono::steady_clock;
static double el(Clock::time_point t){
  return std::chrono::duration<double>(Clock::now()-t).count();
}

static std::string dec(u128 x){
  if(!x) return "0";
  char b[64]; int n=0;
  while(x){ b[n++]=char('0'+(int)(x%10)); x/=10; }
  std::string s; while(n) s.push_back(b[--n]);
  return s;
}
static u128 parse128(const std::string& s){
  u128 v=0;
  for(size_t i=0;i<s.size();++i){
    char c=s[i];
    if(c=='e'||c=='E'){
      int e=std::atoi(s.c_str()+i+1);
      while(e-- > 0) v*=10;
      break;
    }
    if(c<'0'||c>'9') continue;
    v=v*10+(unsigned)(c-'0');
  }
  return v;
}
static u64 icbrt128(u128 n){
  if(!n) return 0;
  long double g=powl((long double)n, 1.0L/3.0L);
  u64 r=(u64)g;
  if(r>2) r-=2; else r=0;
  while((u128)(r+1)*(r+1)*(r+1)<=n) ++r;
  while(r && (u128)r*r*r>n) --r;
  return r;
}
static u64 isqrt128(u128 n){
  if(!n) return 0;
  int bits=0; for(u128 t=n; t; t>>=1) ++bits;
  u64 r = bits<=2 ? 1 : (u64)1 << ((bits+1)/2);
  if(!r) r=1;
  for(;;){
    u64 q=(u64)(n/r);
    u64 nr=(r+q)>>1;
    if(nr>=r) break;
    r=nr;
    if(!r){ r=1; break; }
  }
  while((u128)r*r>n) --r;
  while(r<~0ULL && (u128)(r+1)*(r+1)<=n) ++r;
  return r;
}
static u64 gcd64(u64 a, u64 b){
  while(b){ u64 t=a%b; a=b; b=t; }
  return a;
}

// ---------------- primes ----------------
static std::vector<u64> split_primes;   // p ≡ 1 (mod 3)
static std::vector<u64> extra_primes;   // 3 and p ≡ 2 (mod 3)

static void sieve_primes(u64 pmax, u64 extra_pmax){
  u64 lim = pmax>extra_pmax ? pmax : extra_pmax;
  if(lim<3) lim=3;
  std::vector<uint8_t> is(lim+1, 1);
  is[0]=is[1]=0;
  for(u64 i=2;i*i<=lim;++i) if(is[i])
    for(u64 j=i*i;j<=lim;j+=i) is[j]=0;
  split_primes.clear(); extra_primes.clear();
  extra_primes.push_back(3);
  for(u64 p=2;p<=lim;++p) if(is[p]){
    if(p%3==1 && p<=pmax) split_primes.push_back(p);
    else if(p!=3 && p%3==2 && p<=extra_pmax) extra_primes.push_back(p);
  }
}

// ---------------- extras: cubefree products of 3 and inert primes ----------
struct Extra {
  u128 m;
  std::vector<std::pair<u64,int>> fac;
};
static std::vector<Extra> extras;

static void rec_extras(size_t i, u128 cur, std::vector<std::pair<u64,int>>& fac,
                       u128 cap, bool squares_ok){
  if(cur>cap) return;
  if(cur>1) extras.push_back({cur, fac});
  for(size_t j=i;j<extra_primes.size();++j){
    u64 p=extra_primes[j];
    if(cur>cap/p) break;
    fac.push_back({p,1});
    rec_extras(j+1, cur*p, fac, cap, squares_ok);
    fac.pop_back();
    if(squares_ok && cur<=cap/p/p){
      fac.push_back({p,2});
      rec_extras(j+1, cur*p*p, fac, cap, squares_ok);
      fac.pop_back();
    }
  }
}
static void build_extras(u128 cap, bool squares_ok){
  extras.clear();
  extras.push_back({1, {}});
  if(extra_primes.empty() || cap<2) return;
  std::vector<std::pair<u64,int>> fac;
  rec_extras(0, 1, fac, cap, squares_ok);
  std::sort(extras.begin(), extras.end(),
            [](const Extra& a, const Extra& b){ return a.m<b.m; });
}

// ---------------- median sieve --------------------------------------------
struct Hit {
  u128 n;
  int k;
  bool squarefree;
  std::vector<std::pair<u64,int>> fac;
  std::vector<std::pair<u64,u64>> reps;
};

static void gen_divs(const std::vector<std::pair<u64,int>>& fac, size_t i,
                     u128 cur, u64 hi, u128 n, std::vector<u64>& out){
  if(cur>hi) return;
  if(i==fac.size()){
    u128 c3=cur*cur*cur;
    if(c3>n && c3<=4*n) out.push_back((u64)cur);
    return;
  }
  u128 v=cur;
  for(int j=0;j<=fac[i].second;++j){
    gen_divs(fac, i+1, v, hi, n, out);
    if(j==fac[i].second) break;
    if(v>hi/fac[i].first) break;
    v*=fac[i].first;
  }
}

static std::vector<std::pair<u64,u64>> sieve_n(u128 n, const std::vector<std::pair<u64,int>>& fac){
  std::vector<std::pair<u64,u64>> reps;
  if(!n) return reps;
  const u64 hi=icbrt128(4*n);
  std::vector<u64> divs;
  gen_divs(fac, 0, 1, hi, n, divs);
  const int nmod6=(int)(n%6);
  for(u64 s: divs){
    if((int)(s%6)!=nmod6) continue;                 // Su
    if(n%s) continue;
    u128 t=n/s;
    u128 v=4*t-(u128)s*s;
    if(v==0 || v%3) continue;
    u128 D=v/3;
    u64 d=isqrt128(D);
    if((u128)d*d!=D) continue;
    if(((s^d)&1)) continue;
    u64 a=(s-d)/2, b=(s+d)/2;
    if(a<1 || a>b) continue;
    if((u128)a*a*a+(u128)b*b*b!=n) continue;
    reps.push_back({a,b});
  }
  std::sort(reps.begin(), reps.end());
  reps.erase(std::unique(reps.begin(), reps.end()), reps.end());
  return reps;
}

static std::string fac_str(const std::vector<std::pair<u64,int>>& fac){
  std::string s;
  for(size_t i=0;i<fac.size();++i){
    if(i) s+=',';
    s+=std::to_string(fac[i].first)+":"+std::to_string(fac[i].second);
  }
  return s;
}
static std::string pairs_str(const std::vector<std::pair<u64,u64>>& r){
  std::string s;
  for(size_t i=0;i<r.size();++i){
    if(i) s+=',';
    s+=std::to_string(r[i].first)+":"+std::to_string(r[i].second);
  }
  return s;
}
static std::vector<std::pair<u64,int>> merge_fac(const std::vector<std::pair<u64,int>>& a,
                                                 const std::vector<std::pair<u64,int>>& b){
  std::vector<std::pair<u64,int>> o=a;
  o.insert(o.end(), b.begin(), b.end());
  std::sort(o.begin(), o.end());
  std::vector<std::pair<u64,int>> m;
  for(auto& pe: o){
    if(!m.empty() && m.back().first==pe.first) m.back().second+=pe.second;
    else m.push_back(pe);
  }
  return m;
}
static bool is_squarefree_fac(const std::vector<std::pair<u64,int>>& fac){
  for(auto& pe: fac) if(pe.second!=1) return false;
  return true;
}

// ---------------- search state --------------------------------------------
static u128 g_ub=0;
static int g_omin=3, g_omax=8, g_kmin=2, g_emax=1;
static std::atomic<u64> g_tested{0}, g_hits{0}, g_last_prog{0};
static std::mutex g_mu;
static FILE* g_out=nullptr;
static u128 g_best_cf[16];   // smallest cubefree with >= k ways; 0 = none
static u128 g_best_sf[16];
static Clock::time_point g_t0;

static void consider(u128 n, const std::vector<std::pair<u64,int>>& fac){
  auto reps=sieve_n(n, fac);
  int k=(int)reps.size();
  g_tested.fetch_add(1, std::memory_order_relaxed);
  if(k<g_kmin) return;
  bool sf=is_squarefree_fac(fac);
  bool all_coprime=true;
  for(auto& pr: reps) if(gcd64(pr.first, pr.second)!=1) all_coprime=false;

  std::lock_guard<std::mutex> lk(g_mu);
  bool record=false;
  if(k<16){
    if(!g_best_cf[k] || n<g_best_cf[k]){ g_best_cf[k]=n; record=true; }
    if(sf && (!g_best_sf[k] || n<g_best_sf[k])){ g_best_sf[k]=n; record=true; }
  }
  g_hits.fetch_add(1, std::memory_order_relaxed);
  if(g_out){
    std::string line=dec(n)+";"+std::to_string(k)+";"+(sf?"1":"0")+";"
                     +fac_str(fac)+";"+pairs_str(reps)+"\n";
    fputs(line.c_str(), g_out);
    fflush(g_out);
  }
  std::printf("  HIT k=%d %s N=%s  %s  pairs=%s%s\n",
              k, sf?"sqfree":"cubefree",
              dec(n).c_str(), fac_str(fac).c_str(), pairs_str(reps).c_str(),
              all_coprime?"":"  [non-coprime]");
  if(record){
    std::printf("    RECORD cubefree-k=%d  squarefree-k=%d\n",
                k, sf?k:0);
  }
  fflush(stdout);
  if(k>=5 && sf)
    std::printf("*** SQUAREFREE %d-WAY: %s ***\n", k, dec(n).c_str());
  if(k>=5)
    std::printf("*** CUBEFREE %d-WAY (A080642 candidate): %s ***\n", k, dec(n).c_str());
}

static void progress(){
  u64 t=g_tested.load(std::memory_order_relaxed);
  u64 prev=g_last_prog.load(std::memory_order_relaxed);
  if(t<prev+2000000) return;
  if(!g_last_prog.compare_exchange_strong(prev, t, std::memory_order_relaxed)) return;
  double sec=el(g_t0);
  std::printf("  ... tested %llu  hits %llu  %.0f/s  %.1fs\n",
              (unsigned long long)t, (unsigned long long)g_hits.load(),
              sec>0? t/sec : 0.0, sec);
  fflush(stdout);
}

// kernel DFS: products of split primes, then multiply by each extra
static void rec_kernel(int start, u128 prod, int taken,
                       std::vector<std::pair<u64,int>>& kfac){
  if(taken>=g_omin){
    for(const Extra& e: extras){
      if(e.m!=1 && prod>g_ub/e.m) continue;
      u128 n=prod*e.m;
      if(n>g_ub || n<2) continue;
      auto fac=merge_fac(kfac, e.fac);
      consider(n, fac);
    }
    progress();
  }
  if(taken>=g_omax) return;
  for(int i=start;i<(int)split_primes.size();++i){
    u64 p=split_primes[i];
    if(prod>g_ub/p) break;
    kfac.push_back({p,1});
    rec_kernel(i+1, prod*p, taken+1, kfac);
    kfac.pop_back();
    if(g_emax>=2){
      if(prod>g_ub/p/p) continue;
      kfac.push_back({p,2});
      rec_kernel(i+1, prod*p*p, taken+1, kfac);
      kfac.pop_back();
    }
  }
}

static void search(int threads){
  g_t0=Clock::now();
  g_tested=0; g_hits=0;
  std::memset(g_best_cf, 0, sizeof g_best_cf);
  std::memset(g_best_sf, 0, sizeof g_best_sf);

  std::printf("=== engine_cf ===\n");
  std::printf("  UB=%s  split_primes=%zu (<=%llu)  extras=%zu  omega=%d..%d  exp<=%d  kmin=%d  threads=%d\n",
              dec(g_ub).c_str(), split_primes.size(),
              split_primes.empty()?0ULL:(unsigned long long)split_primes.back(),
              extras.size(), g_omin, g_omax, g_emax, g_kmin, threads);

#ifdef _OPENMP
  omp_set_num_threads(threads);
#pragma omp parallel for schedule(dynamic,1)
  for(int i=0;i<(int)split_primes.size();++i){
    std::vector<std::pair<u64,int>> fac;
    u64 p=split_primes[i];
    if((u128)p>g_ub) continue;
    fac.push_back({p,1});
    rec_kernel(i+1, p, 1, fac);
    fac.pop_back();
    if(g_emax>=2 && (u128)p*p<=g_ub){
      fac.push_back({p,2});
      rec_kernel(i+1, (u128)p*p, 1, fac);
    }
  }
#else
  (void)threads;
  std::vector<std::pair<u64,int>> fac;
  rec_kernel(0, 1, 0, fac);
#endif

  // omega=0 kernels are only extras; skip (N=2 is the trivial 1-way)
  std::printf("done: tested %llu  hits %llu  %.2fs\n",
              (unsigned long long)g_tested.load(),
              (unsigned long long)g_hits.load(), el(g_t0));
  std::printf("records (smallest N with exactly-or-at-least k ways found this run):\n");
  for(int k=g_kmin;k<=15;++k){
    if(!g_best_cf[k] && !g_best_sf[k]) continue;
    std::printf("  k=%d  cubefree=%s  squarefree=%s\n", k,
                g_best_cf[k]?dec(g_best_cf[k]).c_str():"—",
                g_best_sf[k]?dec(g_best_sf[k]).c_str():"—");
  }
}

// ---------------- factor + single sieve -----------------------------------
static const u64 MR_BASES[]={2,3,5,7,11,13,17,19,23,29,31,37};
static bool is_prime(u64 n){
  if(n<2) return false;
  for(u64 p:{2ULL,3ULL,5ULL,7ULL,11ULL,13ULL,17ULL,19ULL,23ULL,29ULL,31ULL,37ULL})
    if(n%p==0) return n==p;
  u64 d=n-1; int r=0; while(!(d&1)){ d>>=1; ++r; }
  for(u64 a: MR_BASES){
    if(a%n==0) continue;
    u64 x=1,b=a%n,e=d;
    while(e){ if(e&1) x=(u128)x*b%n; b=(u128)b*b%n; e>>=1; }
    if(x==1||x==n-1) continue;
    bool comp=true;
    for(int i=1;i<r;++i){ x=(u128)x*x%n; if(x==n-1){ comp=false; break; } }
    if(comp) return false;
  }
  return true;
}
static u64 brent(u64 n){
  if(n%2==0) return 2;
  static u64 seed=123456789;
  auto rnd=[&](){ seed^=seed<<13; seed^=seed>>7; seed^=seed<<17; return seed; };
  while(true){
    u64 x=rnd()%(n-1)+1, y=x, c=rnd()%n, d=1;
    while(d==1){
      x=((u128)x*x+c)%n;
      y=((u128)y*y+c)%n; y=((u128)y*y+c)%n;
      u64 z=x>y?x-y:y-x;
      d=gcd64(z,n);
    }
    if(d!=n) return d;
  }
}
static void factor_push(u64 n, std::vector<std::pair<u64,int>>& fac){
  if(n<2) return;
  if(is_prime(n)){ fac.push_back({n,1}); return; }
  u64 d=brent(n);
  factor_push(d, fac);
  factor_push(n/d, fac);
}
static std::vector<std::pair<u64,int>> factor_u128(u128 n){
  std::vector<std::pair<u64,int>> raw, out;
  for(u64 p:{2ULL,3ULL,5ULL,7ULL,11ULL,13ULL,17ULL,19ULL,23ULL,29ULL,31ULL,37ULL})
    while(n%p==0){ raw.push_back({p,1}); n/=p; }
  for(u64 p=41; p<2000000 && (u128)p*p<=n; p+=2)
    while(n%p==0){ raw.push_back({p,1}); n/=p; }
  if(n>1){
    if(n<((u128)1<<64)) factor_push((u64)n, raw);
    else{
      std::printf("factor: unhandled remainder %s\n", dec(n).c_str());
      std::exit(3);
    }
  }
  std::sort(raw.begin(), raw.end());
  for(auto& pe: raw){
    if(!out.empty() && out.back().first==pe.first) out.back().second+=pe.second;
    else out.push_back(pe);
  }
  return out;
}

static int sieve_one(const std::string& ns){
  u128 n=parse128(ns);
  auto fac=factor_u128(n);
  auto reps=sieve_n(n, fac);
  bool sf=is_squarefree_fac(fac);
  bool cf=true; for(auto& pe: fac) if(pe.second>=3) cf=false;
  std::printf("N=%s\n  fac=%s\n  cubefree=%d squarefree=%d\n  k=%zu\n",
              dec(n).c_str(), fac_str(fac).c_str(), (int)cf, (int)sf, reps.size());
  for(auto& pr: reps)
    std::printf("    %llu^3 + %llu^3   gcd=%llu\n",
                (unsigned long long)pr.first, (unsigned long long)pr.second,
                (unsigned long long)gcd64(pr.first,pr.second));
  return 0;
}

// ---------------- selftest ------------------------------------------------
static int expect_k(u128 n, int want, const char* label){
  auto fac=factor_u128(n);
  auto reps=sieve_n(n, fac);
  if((int)reps.size()!=want){
    std::printf("[selftest] FAIL %s: got k=%zu want %d  N=%s fac=%s\n",
                label, reps.size(), want, dec(n).c_str(), fac_str(fac).c_str());
    for(auto& pr: reps)
      std::printf("    %llu %llu\n", (unsigned long long)pr.first, (unsigned long long)pr.second);
    return 1;
  }
  for(auto& pr: reps)
    if((u128)pr.first*pr.first*pr.first+(u128)pr.second*pr.second*pr.second!=n){
      std::printf("[selftest] FAIL %s: pair does not sum to N\n", label); return 1;
    }
  std::printf("[selftest] %s  k=%d  fac=%s  OK\n", label, want, fac_str(fac).c_str());
  return 0;
}

static int selftest(){
  int rc=0;
  rc|=expect_k(1729, 2, "A080642(2)=1729");
  rc|=expect_k(parse128("15170835645"), 3, "A080642(3)=15170835645");
  rc|=expect_k(parse128("1801049058342701083"), 4, "A080642(4)");
  rc|=expect_k(parse128("208438080643"), 3, "sqfree 3-way seed 208438080643");
  {
    auto fac=factor_u128(parse128("15170835645"));
    if(is_squarefree_fac(fac)){
      std::printf("[selftest] FAIL: A080642(3) should not be squarefree\n"); rc=1;
    }
    auto fac4=factor_u128(parse128("1801049058342701083"));
    if(!is_squarefree_fac(fac4)){
      std::printf("[selftest] FAIL: A080642(4) should be squarefree\n"); rc=1;
    }
  }
  if(rc){ std::printf("[selftest] FAILED\n"); return 1; }
  std::printf("[selftest] PASSED\n");
  return 0;
}

static void usage(){
  std::printf(
    "engine_cf -- construct-and-sieve cubefree / squarefree taxicab search\n"
    "\n"
    "  --selftest              verify known A080642 / squarefree seeds\n"
    "  --sieve N               factor N and list all a^3+b^3 representations\n"
    "  --ub N                  search N <= UB  (accepts 1e15 style)\n"
    "  --pmax P                split primes p≡1 (mod 3) up to P  [default 500]\n"
    "  --omega-min A           min distinct split primes         [default 3]\n"
    "  --omega-max B           max distinct split primes         [default 8]\n"
    "  --squarefree            exponents = 1 only (faster; default)\n"
    "  --cubefree              allow p^2 (still cubefree)\n"
    "  --extras                also multiply by 3^e and inert primes\n"
    "  --extra-pmax P          inert/3 primes for extras         [default 50]\n"
    "  --extra-max M           extra-factor product cap          [default 10000]\n"
    "  --kmin K                report only k >= K                [default 2]\n"
    "  --threads N             OpenMP threads                    [default max]\n"
    "  --out FILE              append hits as N;k;sqfree;fac;pairs\n"
    "\n"
    "Examples:\n"
    "  ./engine_cf --selftest\n"
    "  ./engine_cf --ub 1e12 --pmax 300 --omega-min 3 --omega-max 7 --kmin 2 --out cf_hits.csv\n"
    "  ./engine_cf --ub 1e18 --pmax 2000 --cubefree --extras --kmin 3 --out cf_k3.csv\n"
  );
}

int main(int argc, char** argv){
  std::string ubstr="1000000000000";
  std::string outpath;
  u64 pmax=500, extra_pmax=50;
  u128 extra_cap=10000;
  bool st=false, do_extras=false, squares=false;
  int threads=0;
  std::string sieve_arg;

  for(int i=1;i<argc;++i){
    std::string a=argv[i];
    auto nx=[&]()->const char*{
      if(i+1>=argc){ std::printf("missing value after %s\n", a.c_str()); std::exit(1); }
      return argv[++i];
    };
    if(a=="--selftest") st=true;
    else if(a=="--sieve") sieve_arg=nx();
    else if(a=="--ub") ubstr=nx();
    else if(a=="--pmax") pmax=strtoull(nx(),0,10);
    else if(a=="--omega-min") g_omin=atoi(nx());
    else if(a=="--omega-max") g_omax=atoi(nx());
    else if(a=="--squarefree") squares=false;
    else if(a=="--cubefree") squares=true;
    else if(a=="--extras") do_extras=true;
    else if(a=="--extra-pmax") extra_pmax=strtoull(nx(),0,10);
    else if(a=="--extra-max") extra_cap=parse128(nx());
    else if(a=="--kmin") g_kmin=atoi(nx());
    else if(a=="--threads") threads=atoi(nx());
    else if(a=="--out") outpath=nx();
    else if(a=="-h"||a=="--help"){ usage(); return 0; }
    else { std::printf("unknown arg: %s\n", a.c_str()); usage(); return 1; }
  }

  if(st) return selftest();
  if(!sieve_arg.empty()) return sieve_one(sieve_arg);

  g_emax = squares ? 2 : 1;
  g_ub=parse128(ubstr);
  if(g_ub > ((u128)-1)/4){
    g_ub=((u128)-1)/4;
    std::printf("UB capped at %s to keep 4N inside 128 bits\n", dec(g_ub).c_str());
  }
  if(g_omin<1) g_omin=1;
  if(g_omax<g_omin) g_omax=g_omin;
  if(g_kmin<1) g_kmin=1;

#ifdef _OPENMP
  if(threads<=0) threads=omp_get_max_threads();
#else
  threads=1;
#endif

  sieve_primes(pmax, do_extras?extra_pmax:0);
  if(!do_extras) extra_primes.clear();
  build_extras(do_extras?extra_cap:1, squares);

  if(!outpath.empty()){
    g_out=fopen(outpath.c_str(), "a");
    if(!g_out){ std::printf("cannot open %s\n", outpath.c_str()); return 1; }
  }
  search(threads);
  if(g_out) fclose(g_out);
  return 0;
}
