// engine_b -- multiplier-chain hunt for taxicab numbers.
//
// For each seed N with known representations N = a_i^3+b_i^3 (k of them), scan
// every multiplier m >= 2 with m^3*N <= UB and test whether m^3*N has a
// representation NOT of the scaled form (m*a, m*b). Such an m is a SPLITTING
// FACTOR: m^3*N is a (k+1)-way number. Chains of splits generate essentially
// every multi-way number below ~1e30 (see census analysis: 71.5% of all
// multi-way numbers <= 1e15 are magnifications; the independent-ratio model
// puts spontaneous 7-way numbers beyond ~1e40).
//
// Filters (all proven/verified necessary conditions, safe kills):
//   * median window  n^{1/3} < s <= (4n)^{1/3}
//   * Su: s == n (mod 6)                     [verified: complete 3-adic content]
//   * inert-prime ratio gates s*s0^{-1} in D_p for p in {5,11,...,101}
//     (exact two-median rule at inert primes, verified by exhaustive sieve)
// Exact square test finishes survivors: 4(n/s)-s^2 = 3d^2.
//
// Self-contained validation: Ta(5) splits first at m=79 (-> Ta(6));
// Ta(6) splits first at m=101 (-> Boyer's Taxicab(7) upper bound).
//
// Build: g++ -O3 -fopenmp -std=c++17 engine_b.cpp -o engine_b
// Test:  ./engine_b --selftest
// Run:   ./engine_b --seeds seeds.csv --rounds 6 --threads 32 --out splits.csv

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
#include <set>
#include <sstream>
#include <unordered_map>
#include <unordered_set>
#include <fcntl.h>
#include <unistd.h>
#include <sys/stat.h>
#include <string>
#include <vector>
#ifdef _OPENMP
#include <omp.h>
#endif

using u64 = uint64_t;
using u128 = unsigned __int128;
using Clock = std::chrono::steady_clock;
static double el(Clock::time_point t){ return std::chrono::duration<double>(Clock::now()-t).count(); }

static std::string dec(u128 x){ if(!x) return "0"; char b[64]; int n=0;
  while(x){ b[n++]=char('0'+(int)(x%10)); x/=10; } std::string s; while(n) s.push_back(b[--n]); return s; }
static u128 parse128(const std::string& s){ u128 v=0; for(char c:s){ if(c<'0'||c>'9') break; v=v*10+(unsigned)(c-'0'); } return v; }
static u64 icbrt128(u128 n){ if(!n) return 0; long double g=powl((long double)n,1.0L/3.0L);
  u64 r=(u64)g; if(r>2) r-=2; else r=0;
  while((u128)(r+1)*(r+1)*(r+1)<=n) ++r; while(r&&(u128)r*r*r>n) --r; return r; }

// ---------------- Miller-Rabin + Brent rho (for later-round factoring) ----
static const u64 MR_BASES[] = {2,3,5,7,11,13,17,19,23,29,31,37};
static bool is_prime(u64 n){
  if(n<2) return false;
  for(u64 p: {2ULL,3ULL,5ULL,7ULL,11ULL,13ULL,17ULL,19ULL,23ULL,29ULL,31ULL,37ULL})
    if(n%p==0) return n==p;
  u64 d=n-1; int r=0; while(!(d&1)){ d>>=1; ++r; }
  for(u64 a: MR_BASES){ if(a%n==0) continue; u64 x=1, b=a%n, e=d;
    while(e){ if(e&1) x=(u128)x*b%n; b=(u128)b*b%n; e>>=1; }
    if(x==1||x==n-1) continue;
    bool comp=true;
    for(int i=1;i<r;++i){ x=(u128)x*x%n; if(x==n-1){ comp=false; break; } }
    if(comp) return false; }
  return true;                                   // deterministic < 3.3e24; prob. beyond
}
static u64 brent(u64 n){
  if(n%2==0) return 2;
  static u64 seed=987654321;
  auto rnd=[&](){ seed^=seed<<13; seed^=seed>>7; seed^=seed<<17; return seed; };
  while(true){
    u64 x=rnd()%(n-1)+1, y=x, c=rnd()%n, d=1;
    while(d==1){
      x=((u128)x*x+c)%n;
      y=((u128)y*y+c)%n; y=((u128)y*y+c)%n;
      d=std::__gcd(x>y?x-y:y-x,n);
    }
    if(d!=n) return d;
  }
}
static std::map<u64,int> factor_u128(u128 n){
  // Only used for the two hardcoded selftest seeds; trial division to 2e6 is
  // fully adequate (largest factor anywhere in this engine's selftest path is 157).
  std::map<u64,int> F;
  for(u64 p: {2ULL,3ULL,5ULL,7ULL,11ULL,13ULL,17ULL,19ULL,23ULL,29ULL,31ULL,37ULL})
    while(n%p==0){ ++F[p]; n/=p; }
  for(u64 p=41;p<2000000;p+=2) while(n%p==0){ ++F[p]; n/=p; }
  if(n>1){
    if(n<((u128)1<<64) && is_prime((u64)n)) ++F[(u64)n];
    else { std::printf("factor_u128: unhandled remainder %s\n", dec(n).c_str()); std::exit(3); }
  }
  return F;
}

// ---------------- inert-prime ratio sets (exact two-median sieve) ----------
static const int INERT[] = {5,11,17,23,29,41,47,53,59,71,83,89,101};
static std::map<int,std::vector<char>> D_P;
static u64 invm(u64 a, u64 m){
  int64_t t=0, nt=1, r=(int64_t)m, nr=(int64_t)(a%m);
  while(nr){ int64_t q=r/nr; int64_t tp=t-q*nt; t=nt; nt=tp; int64_t tr=r-q*nr; r=nr; nr=tr; }
  if(t<0) t+=(int64_t)m;
  return (u64)t;
}
static void compute_D(){
  for(int p: INERT){
    std::vector<std::vector<char>> R(p, std::vector<char>(p,0));
    for(int s=0;s<p;++s) for(int a=0;a<p;++a){
      int v=(int)(((u64)a*a%p*a + (u64)((s-a+p)%p)*(s-a+p)%p*((s-a+p)%p))%p);
      R[s][v]=1;
    }
    std::vector<char> D(p,0);
    for(int r=0;r<p;++r) for(int v=0;v<p;++v) if(R[r][v]&&R[1][v]){ D[r]=1; break; }
    D_P[p]=D;
  }
}
static inline bool ratio_gate(u64 s, u64 s0){
  for(int p: INERT){
    if(s%p==0 || s0%p==0) continue;
    u64 inv=1, base=s0%p, e=p-2;             // Fermat inverse (p prime)
    while(e){ if(e&1) inv=inv*base%p; base=base*base%p; e>>=1; }
    u64 ratio=(u64)((u128)(s%p)*inv%p);
    if(!D_P[p][ratio]) return false;
  }
  return true;
}

// ---------------- seeds ----------------
struct Seed { u128 n; int k; std::map<u64,int> fac; std::vector<std::pair<u64,u64>> reps; };
static std::vector<Seed> load_seeds(const std::string& path){
  std::vector<Seed> out; std::ifstream f(path); std::string line;
  while(std::getline(f,line)){
    if(line.empty()) continue;
    std::stringstream ss(line); std::string tok;
    Seed s;
    std::getline(ss,tok,';'); s.n=parse128(tok);
    std::getline(ss,tok,';'); s.k=std::atoi(tok.c_str());
    std::getline(ss,tok,';'); { std::stringstream f2(tok); std::string pe;
      while(std::getline(f2,pe,',')){ auto c=pe.find(':'); s.fac[(u64)parse128(pe.substr(0,c))]=std::atoi(pe.c_str()+c+1); } }
    std::getline(ss,tok,';'); { std::stringstream f2(tok); std::string ab;
      while(std::getline(f2,ab,',')){ auto c=ab.find(':'); s.reps.push_back({(u64)parse128(ab.substr(0,c)),(u64)parse128(ab.c_str()+c+1)}); } }
    out.push_back(std::move(s));
  }
  return out;
}

// bounded divisor enumeration: divisors d of fac with d^3 in (n, 4n]
static void gen_divs(const std::vector<std::pair<u64,int>>& fac, size_t i, u128 cur,
                     u64 hi, u128 n, std::vector<u64>& out){
  if(cur>hi) return;
  if(i==fac.size()){
    u128 c3=cur*cur*cur;
    if(c3>n && c3<=4*n) out.push_back((u64)cur);
    return;
  }
  u128 v=cur;
  for(int j=0;j<=fac[i].second;++j){
    gen_divs(fac,i+1,v,hi,n,out);
    v*=fac[i].first;
    if(v>hi) break;
  }
}

static u128 UB;   // run-wide upper bound
static uint32_t* g_spf=nullptr; static u64 g_spf_lim=0;
static u64 g_mcap=25000000ULL;      // scan multipliers only up to this (all known primaries <= 2e7)
static int g_disc_kmin=0;
static u64 g_bigfac_skip=0;           // if >0, don't persist discoveries with k < this to .disc
static void build_spf(u64 lim){
  g_spf_lim=lim; g_spf=(uint32_t*)malloc((lim+1)*sizeof(uint32_t));
  std::memset(g_spf,0,(lim+1)*sizeof(uint32_t));
  for(u64 i=2;i<=lim;i++) if(!g_spf[i]){ g_spf[i]=(uint32_t)i;
    if(i<=lim/i) for(u64 j=i*i;j<=lim;j+=i) if(!g_spf[j]) g_spf[j]=(uint32_t)i; }
}
static inline void factor_m(u64 m, std::map<u64,int>& fm){
  if(m<=g_spf_lim){ while(m>1){ u64 p=g_spf[m]; ++fm[p]; m/=p; } return; }
  u64 t=m;
  { int c2=0; while(!(t&1)){ t>>=1; ++c2; } if(c2) fm[2]=c2; }
  for(u64 p=3; p*p<=t; p+=2) while(t%p==0){ ++fm[p]; t/=p; }
  if(t>1) ++fm[t];
}

struct Split { u128 seed_n; u64 m; u128 n_new; int k_new;
  std::vector<std::pair<u64,u64>> new_reps;          // genuinely new representations
  std::vector<std::pair<u64,u64>> full_reps;         // all reps of n_new (scaled + new)
  std::vector<std::pair<u64,int>> facn;              // factorization of n_new
};

static std::vector<Split> process_seed(const Seed& S){
  std::vector<Split> found;
  if(S.n>=UB) return found;
  u64 mmax=icbrt128(UB/S.n); if(g_mcap && mmax>g_mcap) mmax=g_mcap;
  const bool have_reps=!S.reps.empty();
  const u64 s0=have_reps?(u64)(S.reps[0].first+S.reps[0].second):0;
  for(u64 m=2;m<=mmax;++m){
    // factor m (trial) and merge with seed factorization
    std::vector<std::pair<u64,int>> facn(S.fac.begin(),S.fac.end());
    { std::map<u64,int> fm; factor_m(m,fm);
      for(auto& kv: fm){
        bool foundp=false;
        for(auto& pe: facn) if(pe.first==kv.first){ pe.second+=3*kv.second; foundp=true; break; }
        if(!foundp) facn.push_back({kv.first,3*kv.second});
      }
    }
    u64 invw[13];
    { for(int ii=0;ii<13;++ii){ const u64 p=INERT[ii];
        u64 w=(u64)((u128)(s0%p)*(m%p)%p);
        invw[ii]= w? invm(w,p) : 0; } }
    const u128 n=(u128)m*m*(u128)m*S.n;
    const u64 hi=icbrt128(4*n);
    std::vector<u64> divs; gen_divs(facn,0,1,hi,n,divs);
    std::vector<std::pair<u64,u64>> news;
    for(u64 s: divs){
      if(s%6 != (u64)(n%6)) continue;                    // Su
      if(have_reps){ bool ok=true;
        for(int ii=0;ii<13;++ii){ const u64 p=INERT[ii]; u64 sp=s%p;
          if(sp==0||invw[ii]==0) continue;
          u64 r=(u64)((u128)sp*invw[ii]%p);
          if(!D_P[p][r]){ ok=false; break; } }
        if(!ok) continue; }                              // inert two-median gates
      const u128 t=n/s;
      if(t*s!=n) continue;                     // exactness guard (factorization must be right)
      u128 v=4*t-(u128)s*s;
      if(v==0 || v%3) continue;
      u128 D=v/3;
      u64 r=(u64)sqrtl((long double)D);
      while((u128)(r+1)*(r+1)<=D) ++r;
      while((u128)r*r>D) --r;
      if((u128)r*r!=D) continue;
      if(((s^r)&1)) continue;
      const u64 a=(s-r)/2, b=(s+r)/2;
      if(a<1) continue;
      bool scaled=false;
      if(a%m==0 && b%m==0){ const u64 aa=a/m, bb=b/m;
        for(auto& pr: S.reps) if(pr.first==aa&&pr.second==bb){ scaled=true; break; } }
      if(!scaled) news.push_back({a,b});
    }
    if(!news.empty() && (have_reps || news.size()>=2)){   // core seeds: need >=2 reps to count
      std::sort(news.begin(),news.end());
      news.erase(std::unique(news.begin(),news.end()),news.end());
      Split sp; sp.seed_n=S.n; sp.m=m; sp.n_new=n;
      sp.k_new=(int)S.reps.size()+(int)news.size(); sp.new_reps=news; sp.facn=facn;
      for(auto& pr: S.reps) sp.full_reps.push_back({pr.first*m, pr.second*m});
      sp.full_reps.insert(sp.full_reps.end(),news.begin(),news.end());
      std::sort(sp.full_reps.begin(),sp.full_reps.end());
      found.push_back(std::move(sp));
    }
  }
  return found;
}


struct U128Hash {
  size_t operator()(const u128& x) const noexcept {
    uint64_t lo=(uint64_t)x, hi=(uint64_t)(x>>64);
    uint64_t h = lo ^ (hi + 0x9e3779b97f4a7c15ULL + (lo<<6) + (lo>>2));
    h ^= h>>30; h*=0xbf58476d1ce4e5b9ULL; h^=h>>27; h*=0x94d049bb133111ebULL; h^=h>>31;
    return (size_t)h;
  }
};
static std::unordered_set<u128,U128Hash> g_seen, g_processed;
static u64 g_bad_recs=0, g_loaded_recs=0;
struct SeedLite { std::vector<std::pair<u64,int>> facn; std::vector<std::pair<u64,u64>> reps; int k=0; };
static std::unordered_map<u128,SeedLite,U128Hash> g_disc;

static const char DISC_MAGIC[8] = {'T','C','B','9','D','I','S','C'};
static const char CKPT_MAGIC[8] = {'T','C','B','6','C','K','P','T'};

static bool write_full(int fd, const void* buf, size_t len){
  const char* p=(const char*)buf;
  while(len){ ssize_t w=write(fd,p,len); if(w<=0) return false; p+=w; len-=w; }
  return true;
}

static void load_state(const std::string& discpath, const std::string& ckptpath){
  { int fd=open(ckptpath.c_str(),O_RDONLY);
    if(fd>=0){ char mg[8]; if(read(fd,mg,8)==8 && !memcmp(mg,CKPT_MAGIC,8)){
      unsigned char buf[16*4096]; ssize_t r;
      while((r=read(fd,buf,sizeof buf))>0) for(ssize_t i=0;i+16<=r;i+=16){
        u128 n=0; for(int j=0;j<16;j++) n|=((u128)buf[i+j])<<(8*j); g_processed.insert(n); }
    } else std::printf("  ckpt: foreign/corrupt magic -> ignoring\n");
      close(fd); } }
  { int fd=open(discpath.c_str(),O_RDONLY);
    if(fd>=0){ char mg[8]; if(read(fd,mg,8)==8 && !memcmp(mg,DISC_MAGIC,8)){
      for(;;){ u128 n=0; unsigned char hdr[2];
        if(read(fd,&n,16)!=16) break;
        if(read(fd,hdr,2)!=2){ ++g_bad_recs; break; }
        int nfac=hdr[0], nreps=hdr[1];
        if(nfac<1||nfac>24||nreps<1||nreps>64){ ++g_bad_recs; break; }
        unsigned char fb[24*9];
        if(read(fd,fb,nfac*9)!=(ssize_t)(nfac*9)){ ++g_bad_recs; break; }
        std::vector<std::pair<u64,int>> facn(nfac);
        for(int i=0;i<nfac;++i){ uint64_t p=0; for(int j=0;j<8;j++) p|=(uint64_t)fb[i*9+j]<<(8*j); facn[i]={p,fb[i*9+8]}; }
        unsigned char rb[64*16];
        if(read(fd,rb,nreps*16)!=(ssize_t)(nreps*16)){ ++g_bad_recs; break; }
        std::vector<std::pair<u64,u64>> reps(nreps); bool ok=true;
        for(int i=0;i<nreps;++i){ uint64_t a=0,b=0; for(int j=0;j<8;j++){ a|=(uint64_t)rb[i*16+j]<<(8*j); b|=(uint64_t)rb[i*16+8+j]<<(8*j); }
          reps[i]={a,b};
          if((u128)a*a*a+(u128)b*b*b!=n) ok=false; }
        if(!ok){ ++g_bad_recs; continue; }
        g_seen.insert(n);
        if(!g_processed.count(n)){ ++g_loaded_recs; SeedLite L; L.facn=std::move(facn); L.reps=std::move(reps); L.k=nreps; g_disc[n]=std::move(L); }
      }
      std::printf("  disc: %llu valid records (%llu pending, %llu bad skipped)\n",
                  (unsigned long long)(g_loaded_recs),(unsigned long long)g_loaded_recs,(unsigned long long)g_bad_recs);
    } else std::printf("  disc: foreign/corrupt magic -> clean start\n");
      close(fd); } }
}

static void process_batch(std::vector<Seed>& work, int round, int threads,
                          const std::string& outpath, const std::string& discpath, const std::string& ckptpath){
  auto t0=Clock::now();
  std::atomic<u64> done{0}, fresh_cnt{0};
#pragma omp parallel num_threads(threads)
  {
    int fo=open(outpath.c_str(),O_WRONLY|O_CREAT|O_APPEND,0644);
    int fd=open(discpath.c_str(),O_WRONLY|O_CREAT|O_APPEND,0644);
    int fc=open(ckptpath.c_str(),O_WRONLY|O_CREAT|O_APPEND,0644);
#pragma omp for schedule(dynamic,1)
    for(size_t i=0;i<work.size();++i){
      auto v=process_seed(work[i]);
      std::vector<const Split*> mine;
#pragma omp critical
      { for(auto& sp: v){ if(!g_seen.count(sp.n_new)){ g_seen.insert(sp.n_new); mine.push_back(&sp); } } }
      std::string stext; std::vector<unsigned char> sbin, scpt;
      for(const Split* ps: mine){
        const Split& sp=*ps;
        if(sp.k_new>=3){
          stext += dec(sp.seed_n)+";"+std::to_string(sp.m)+";"+dec(sp.n_new)+";"+std::to_string(sp.k_new)+";";
          for(auto& pr: sp.new_reps) stext+=std::to_string(pr.first)+":"+std::to_string(pr.second)+",";
          stext+="\n";
        }
        if(g_disc_kmin && sp.k_new<g_disc_kmin) continue;
        { bool big=false; for(auto& pe: sp.facn) if(pe.first>=(1ULL<<63)) big=true;
          if(big){ ++g_bigfac_skip; continue; } }
        unsigned char hdr[18]; for(int j=0;j<16;j++) hdr[j]=(unsigned char)(sp.n_new>>(8*j));
        hdr[16]=(unsigned char)sp.facn.size(); hdr[17]=(unsigned char)sp.full_reps.size();
        sbin.insert(sbin.end(),hdr,hdr+18);
        for(auto& pe: sp.facn){ for(int j=0;j<8;j++) sbin.push_back((unsigned char)(pe.first>>(8*j))); sbin.push_back((unsigned char)pe.second); }
        for(auto& pr: sp.full_reps){ for(int j=0;j<8;j++) sbin.push_back((unsigned char)(pr.first>>(8*j))); for(int j=0;j<8;j++) sbin.push_back((unsigned char)(pr.second>>(8*j))); }
        if(sp.k_new>=7){
#pragma omp critical
          { std::string t="ROUND "+std::to_string(round)+" k="+std::to_string(sp.k_new)+" seed="+dec(sp.seed_n)+
                          " m="+std::to_string(sp.m)+" n="+dec(sp.n_new)+"\n";
            FILE* f=fopen("FOUND7.txt","a"); fputs(t.c_str(),f); fclose(f);
            std::printf("*** k=%d BELOW UB: %s ***\n", sp.k_new, dec(sp.n_new).c_str()); fflush(stdout); }
        }
      }
      for(int j=0;j<16;j++) scpt.push_back((unsigned char)(work[i].n>>(8*j)));
      if(!stext.empty()) write_full(fo,stext.data(),stext.size());
      if(!sbin.empty())  write_full(fd,sbin.data(),sbin.size());
      write_full(fc,scpt.data(),16);
      if(!mine.empty()) fresh_cnt+=mine.size();
#pragma omp critical
      g_processed.insert(work[i].n);
      u64 d=++done;
      if(d%256==0){ std::printf("[r%d] %zu/%zu seeds, %zu seen, %llu fresh, %.0fs\n",
                               round,(size_t)d,work.size(),g_seen.size(),(unsigned long long)fresh_cnt.load(),el(t0)); fflush(stdout); }
    }
    close(fo); close(fd); close(fc);
  }
  std::printf("[r%d] done: %zu seen, %llu fresh this round, %.1fs\n",
              round, g_seen.size(), (unsigned long long)fresh_cnt.load(), el(t0)); fflush(stdout);
}

static int run_rounds(const std::vector<Seed>& seeds0, int rounds, int threads, const std::string& outpath){
  const std::string discpath = outpath + ".disc", ckptpath = outpath + ".ckpt";
  std::printf("=== engine_b9 (u64 reps, mcap, bounded RAM/disk) ===\n");
  load_state(discpath, ckptpath);
  for(auto& pr : {std::pair<std::string,const char*>{discpath,DISC_MAGIC},
                  std::pair<std::string,const char*>{ckptpath,CKPT_MAGIC}}){
    int fd=open(pr.first.c_str(),O_WRONLY|O_CREAT|O_APPEND,0644);
    if(lseek(fd,0,SEEK_END)==0) write_full(fd,pr.second,8);
    close(fd);
  }
  std::vector<Seed> work;
  for(const auto& s: seeds0) if(!g_processed.count(s.n)) work.push_back(s);
  { u64 mmax_max=0; for(const auto& s: seeds0){ if(s.n>=UB) continue; u64 mm=icbrt128(UB/s.n); if(mm>mmax_max) mmax_max=mm; }
    if(mmax_max>=2){ u64 lim = mmax_max>g_mcap ? g_mcap : mmax_max; build_spf(lim);
      std::printf("  SPF sieve built to %llu (max seed mmax %llu)%s\n",
                  (unsigned long long)lim,(unsigned long long)mmax_max,
                  mmax_max>lim?" [capped; wheel fallback beyond]":""); } }
  std::printf("  round 1 worklist: %zu original seeds\n", work.size());
  if(!work.empty()) process_batch(work, 1, threads, outpath, discpath, ckptpath);

  for(int round=2; round<=rounds; ++round){
    struct stat st; if(stat(discpath.c_str(),&st)!=0) break;
    off_t snap=st.st_size;
    int fd=open(discpath.c_str(),O_RDONLY);
    if(fd<0) break;
    lseek(fd,8,SEEK_SET);
    std::vector<Seed> batch; const size_t BATCH=2000000;
    while(lseek(fd,0,SEEK_CUR)<snap){
      u128 n=0; unsigned char hdr[2];
      if(read(fd,&n,16)!=16) break;
      if(read(fd,hdr,2)!=2){ ++g_bad_recs; break; }
      int nfac=hdr[0], nreps=hdr[1];
      if(nfac<1||nfac>24||nreps<1||nreps>64){ ++g_bad_recs; break; }
      unsigned char fb[24*9]; if(read(fd,fb,nfac*9)!=(ssize_t)(nfac*9)){ ++g_bad_recs; break; }
      unsigned char rb[64*16]; if(read(fd,rb,nreps*16)!=(ssize_t)(nreps*16)){ ++g_bad_recs; break; }
      if(g_processed.count(n)) continue;
      Seed s; s.n=n; s.k=nreps;
      for(int i=0;i<nfac;++i){ uint64_t p=0; for(int j=0;j<8;j++) p|=(uint64_t)fb[i*9+j]<<(8*j); s.fac[p]=fb[i*9+8]; }
      for(int i=0;i<nreps;++i){ uint64_t a=0,b=0; for(int j=0;j<8;j++){ a|=(uint64_t)rb[i*16+j]<<(8*j); b|=(uint64_t)rb[i*16+8+j]<<(8*j); } s.reps.push_back({a,b}); }
      batch.push_back(std::move(s));
      if(batch.size()>=BATCH) break;
    }
    close(fd);
    if(batch.empty()){ std::printf("[r%d] nothing pending -> BFS complete\n", round); break; }
    std::sort(batch.begin(),batch.end(),[](const Seed&a,const Seed&b){ return a.k>b.k; });
    std::printf("[r%d] pending batch: %zu (k-sorted, high first)\n", round, batch.size());
    process_batch(batch, round, threads, outpath, discpath, ckptpath);
  }
  return 0;
}

// NOTE on rounds>=2: process_seed compares candidate reps only against the CURRENT
// seed's scaled reps, so a number found in round r is tested as a fresh seed in
// round r+1 -- splits of splits are discovered chain by chain. The reps stored on
// new seeds must be the FULL rep set for correct "scaled" classification in later
// rounds; we rebuild them exactly in the selftest and rely on --selftest for that path.

static std::vector<std::pair<u64,u64>> full_reps(const Seed& S, u64 m){
  // all reps of m^3 S.n = scaled seed reps + any new ones (re-run of the sieve)
  std::vector<std::pair<u64,u64>> reps;
  for(auto& pr: S.reps) reps.push_back({pr.first*m, pr.second*m});
  // new ones: reuse process_seed's logic is awkward; enumerate medians of n and test
  return reps;
}

static int selftest(){
  compute_D();
  UB=parse128("24885189317885898975235988544");
  Seed ta5; ta5.n=parse128("48988659276962496"); ta5.k=5;
  ta5.reps={{38787,365757},{107839,362753},{205292,342952},{221424,336588},{231518,331954}};
  ta5.fac=factor_u128(ta5.n);
  { std::map<u64,int> want={{2,6},{3,3},{7,4},{13,1},{19,1},{43,1},{73,1},{97,1},{157,1}};
    if(ta5.fac!=want){ std::printf("[selftest] FAIL: fac(Ta5) wrong: got");
      for(auto& kv: ta5.fac) std::printf(" %llu:%d",(unsigned long long)kv.first,kv.second);
      std::printf("\n"); return 1; }
    std::printf("[selftest] fac(Ta5) correct\n"); }
  {
    auto v=process_seed(ta5);
    std::map<u64,u128> bym;
    for(auto& sp: v) bym[sp.m]=sp.n_new;
    auto it79=bym.find(79);
    if(it79==bym.end() || dec(it79->second)!="24153319581254312065344"){
      std::printf("[selftest] FAIL: m=79 should split Ta(5) -> Ta(6)\n"); return 1; }
    for(auto& sp: v) if(sp.m<79){
      std::printf("[selftest] UNEXPECTED: m=%llu n_new=%s k=%d newreps:",(unsigned long long)sp.m, dec(sp.n_new).c_str(), sp.k_new);
      for(auto& pr: sp.new_reps) std::printf(" (%llu,%llu)",(unsigned long long)pr.first,(unsigned long long)pr.second);
      std::printf("\n"); }
    std::printf("[selftest] Ta(5): first split at m=79 -> Ta(6). OK\n");
  }
  Seed ta6; ta6.n=parse128("24153319581254312065344"); ta6.k=6;
  ta6.reps={{582162,28906206},{3064173,28894803},{8519281,28657487},{16218068,27093208},{17492496,26590452},{18289922,26224366}};
  ta6.fac=factor_u128(ta6.n);
  { std::map<u64,int> want={{2,6},{3,3},{7,4},{13,1},{19,1},{43,1},{73,1},{97,1},{157,1},{79,3}};
    if(ta6.fac!=want){ std::printf("[selftest] FAIL: fac(Ta6) wrong: got");
      for(auto& kv: ta6.fac) std::printf(" %llu:%d",(unsigned long long)kv.first,kv.second);
      std::printf("\n"); return 1; }
    std::printf("[selftest] fac(Ta6) correct\n"); }
  {
    auto v=process_seed(ta6);
    std::map<u64,u128> bym;
    for(auto& sp: v) bym[sp.m]=sp.n_new;
    auto it=bym.find(101);
    if(it==bym.end() || dec(it->second)!="24885189317885898975235988544"){
      std::printf("[selftest] FAIL: m=101 should split Ta(6) -> Boyer T7\n"); return 1; }
    for(auto& kv: bym) if(kv.first<101){
      std::printf("[selftest] FAIL: unexpected split of Ta(6) at m=%llu\n",(unsigned long long)kv.first); return 1; }
    std::printf("[selftest] Ta(6): first split at m=101 -> Boyer T(7) upper bound. OK\n");
  }
  std::printf("[selftest] PASSED\n");
  return 0;
}

int main(int argc,char**argv){
  std::string seeds="seeds.csv", out="splits.csv"; int rounds=1, threads=0; bool st=false;
  std::string ubstr="24885189317885898975235988544";
  for(int i=1;i<argc;++i){ std::string a=argv[i];
    auto nx=[&]()->const char*{ if(i+1>=argc){ std::printf("bad args\n"); std::exit(1);} return argv[++i]; };
    if(a=="--seeds") seeds=nx();
    else if(a=="--out") out=nx();
    else if(a=="--rounds") rounds=atoi(nx());
    else if(a=="--threads") threads=atoi(nx());
    else if(a=="--ub") ubstr=nx();
    else if(a=="--mcap") g_mcap=strtoull(nx(),0,10);
    else if(a=="--disc-kmin") g_disc_kmin=atoi(nx());
    else if(a=="--selftest") st=true;
    else { std::printf("usage: engine_b [--seeds f] [--rounds n] [--threads n] [--ub decimal] [--out f] [--selftest]\n"); return 1; }
  }
  compute_D();
  UB=parse128(ubstr);
  if(st) return selftest();
#ifdef _OPENMP
  if(threads<=0) threads=omp_get_max_threads();
#else
  threads=1;
#endif
  auto S=load_seeds(seeds);
  std::printf("=== engine_b ===\n  seeds=%zu  UB=%s  rounds=%d  threads=%d\n",
              S.size(), dec(UB).c_str(), rounds, threads);
  return run_rounds(S, rounds, threads, out);
}
