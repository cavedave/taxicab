// cabtaxi -- exhaustive search for numbers n <= B that are sums of two COPRIME cubes, signs allowed,
// in many ways (OEIS A047697: 1, 91, 3367, 16776487, 506433677359393; the 6-way term is unknown,
// none below 2.5e17 per Bernstein 1999). CPU reference for the GPU version.
//
// Representations of n > 0 as x^3 + y^3 with gcd(x, y) = 1, unordered:
//   sums         n = a^3 + b^3,  1 <= a <= b
//   differences  n = a^3 - c^3,  a > c >= 1   (a = c + d,  n = d^3 + 3 d c (c + d))
// (the zero case 1 = 1^3 + 0^3 is ignored; it only matters for the trivial term a(1) = 1).
//
// Method: split (0, B] into segments of roughly equal pair count, generate every coprime pair whose
// value falls in the segment, sort, and report each n with >= KMIN representations. Segments are
// independent (OpenMP here, one GPU each later). Every reported pair is re-checked exactly.
//
// Build: g++ -O3 -march=native -fopenmp -std=c++17 cabtaxi.cpp -o cabtaxi
// Run:   ./cabtaxi --max 1000000000000000 --kmin 4 --out cab_1e15.txt
//        ./cabtaxi --min 1e19-as-integer --max ... extends an earlier run without redoing it (and lets
//        several machines split a range); the idea of starting anywhere is from Bill Butler's Cabtaxi.c
// Output lines: n;k;x:y,x:y,...   (y negative for differences), then a per-k summary on stdout.

#include <algorithm>
#include <chrono>
#include <atomic>
#include <cmath>
#include <cstdint>
#include <cstdio>
#include <cstdlib>
#include <map>
#include <numeric>
#include <string>
#include <vector>
#ifdef _OPENMP
#include <omp.h>
#endif

using u32 = uint32_t; using u64 = uint64_t; using i64 = int64_t; using u128 = unsigned __int128;

static u64 icbrt(u64 n){ u64 r=(u64)cbrtl((long double)n); while(r&&(u128)r*r*r>n)--r; while((u128)(r+1)*(r+1)*(r+1)<=n)++r; return r; }
static u64 isqrt_(u64 n){ u64 r=(u64)sqrtl((long double)n); while(r&&(u128)r*r>n)--r; while((u128)(r+1)*(r+1)<=n)++r; return r; }

struct Rec { u64 n; u32 x; u32 y; u32 neg; };           // value, |x|, |y|, y negative?

// smallest c >= 1 with d^3 + 3 d c (c + d) >= v   (v >= 1)
static u64 cmin_for(u64 d, u64 v){
  u128 base=(u128)d*d*d;
  if(base+3*(u128)d*(1+d)>=v) return 1;
  // 3d c^2 + 3d^2 c + d^3 - v >= 0  ->  c >= (-3d^2 + sqrt(9d^4 - 12 d (d^3 - v))) / (6d)
  long double D=(long double)d;
  long double disc=9*D*D*D*D-12*D*(D*D*D-(long double)v);
  u64 c=(u64)((-3*D*D+sqrtl(disc))/(6*D)); if(c<1)c=1;
  while(c>1 && base+3*(u128)d*(c-1)*((c-1)+d)>=v) --c;
  while(base+3*(u128)d*c*(c+d)<v) ++c;
  return c;
}

int main(int argc,char**argv){
  u64 B=1000000000000000ULL, A=0; int kmin=4; std::string out="cabtaxi_out.txt"; int segs=0;
  for(int i=1;i<argc;++i){ std::string a=argv[i];
    auto nx=[&]()->const char*{ if(i+1>=argc){ std::printf("missing value for %s\n",a.c_str()); std::exit(1);} return argv[++i]; };
    if(a=="--max") B=strtoull(nx(),0,10);
    else if(a=="--min") A=strtoull(nx(),0,10);
    else if(a=="--kmin") kmin=atoi(nx());
    else if(a=="--out") out=nx();
    else if(a=="--segments") segs=atoi(nx());
    else { std::printf("usage: cabtaxi --max B [--min A] [--kmin K] [--out file] [--segments S]\n"); return 1; }
  }
  const auto T0=std::chrono::steady_clock::now();
  std::printf("cabtaxi v2 (coprime signed two-cube search): %llu < n <= %llu, kmin=%d\n",
              (unsigned long long)A,(unsigned long long)B,kmin);
  if(B>(u64)1.8e19){ std::printf("--max must fit in 64 bits\n"); return 1; }
  if(isqrt_(B/3)+cbrtl((long double)B)>4.0e9){ std::printf("--max too large for 32-bit pair storage\n"); return 1; }
  // pair count ~ 1.6 B^(2/3); density ~ n^(-1/3): equal-count edges B*(i/S)^1.5
  if(A>=B){ std::printf("--min must be below --max\n"); return 1; }
  // pairs below x ~ 1.6 x^(2/3): equal-count segments of (A, B] are equally spaced in x^(2/3)
  const long double A23=powl((long double)A,2.0L/3), B23=powl((long double)B,2.0L/3);
  if(!segs){ double pairs=1.6*(double)(B23-A23); segs=std::max(64,(int)(pairs/4e6)); }
  std::vector<u64> edge(segs+1);
  for(int i=0;i<=segs;++i) edge[i]=(u64)powl(A23+(B23-A23)*i/segs,1.5L);
  edge[0]=A+1; edge[segs]=B+1;                          // values in [A+1, B]
  for(int i=1;i<segs;++i) edge[i]=std::min(std::max(edge[i],edge[i-1]),B+1);
  const u64 dmax=icbrt(B);

  // Work is split into contiguous blocks of segments. Inside a block every a (sums) and d
  // (differences) sits in the bucket of the segment holding its next value, so a segment only
  // touches the a, d that actually have pairs in it: cost ~ pairs, not segments x range.
  const int nblocks=std::min(segs, std::max(1,
#ifdef _OPENMP
      omp_get_max_threads()
#else
      1
#endif
      *16));
  std::vector<int> bstart(nblocks+1);
  for(int i=0;i<=nblocks;++i) bstart[i]=(int)((long long)segs*i/nblocks);
  std::vector<std::vector<std::pair<u64,std::vector<Rec>>>> hits(nblocks);
  std::atomic<u64> npairs{0}; std::atomic<int> done{0};
#pragma omp parallel for schedule(dynamic,1)
  for(int blk=0;blk<nblocks;++blk){
    const int s0=bstart[blk], s1=bstart[blk+1];
    if(s0>=s1) continue;
    const u64 lo0=edge[s0], hiEnd=edge[s1];
    auto seg_of=[&](u64 v){ return (int)(std::upper_bound(edge.begin()+s0, edge.begin()+s1, v)-edge.begin())-1; };
    // Bucket queues as intrusive linked lists in flat arrays: no allocation per move.
    // (v1 of this used vector<vector<u32>>; on Linux with 64 threads the constant small
    //  allocations fragmented malloc arenas until the OOM killer stopped a 1e19 run at 258 GB.)
    static thread_local std::vector<int32_t> headS, headD, linkS, linkD;
    static thread_local std::vector<u32> nextB, nextC;   // next b for each a; next c for each d
    static thread_local std::vector<Rec> v;
    const int ns=s1-s0;
    headS.assign(ns,-1); headD.assign(ns,-1);
    const u64 amax=icbrt(hiEnd/2)+2;
    nextB.assign(amax+1,0); linkS.assign(amax+1,-1);
    nextC.assign(dmax+2,0); linkD.assign(dmax+2,-1);
    auto pushS=[&](int sg,u32 a){ linkS[a]=headS[sg]; headS[sg]=(int32_t)a; };
    auto pushD=[&](int sg,u32 d){ linkD[d]=headD[sg]; headD[sg]=(int32_t)d; };
    for(u64 a=1; 2*(u128)a*a*a<hiEnd; ++a){
      const u64 a3=a*a*a;
      u64 b = lo0>a3 ? icbrt(lo0-a3-1)+1 : a; if(b<a) b=a;
      nextB[a]=(u32)b;
      const u128 val=(u128)a3+(u128)b*b*b;
      if(val<hiEnd) pushS(seg_of((u64)val)-s0,(u32)a);
    }
    for(u64 d=1; d<=dmax; ++d){
      const u128 d3=(u128)d*d*d;
      if(d3+3*(u128)d*(1+d)>=hiEnd) break;
      const u64 c=cmin_for(d,lo0);
      nextC[d]=(u32)c;
      const u128 val=d3+3*(u128)d*c*(c+d);
      if(val<hiEnd) pushD(seg_of((u64)val)-s0,(u32)d);
    }
    for(int sg=s0; sg<s1; ++sg){
      const u64 hi=edge[sg+1];
      v.clear();
      for(int32_t a32=headS[sg-s0]; a32>=0; ){
        const int32_t nxt=linkS[a32];
        const u64 a=(u64)a32, a3=a*a*a; u64 b=nextB[a]; u128 val;
        while((val=(u128)a3+(u128)b*b*b)<hi){ if(std::gcd(a,b)==1) v.push_back({(u64)val,(u32)a,(u32)b,0}); ++b; }
        nextB[a]=(u32)b;
        if(val<hiEnd) pushS(seg_of((u64)val)-s0,(u32)a);
        a32=nxt;
      }
      headS[sg-s0]=-1;
      for(int32_t d32=headD[sg-s0]; d32>=0; ){
        const int32_t nxt=linkD[d32];
        const u64 d=(u64)d32; const u128 d3=(u128)d*d*d; u64 c=nextC[d]; u128 val;
        while((val=d3+3*(u128)d*c*(c+d))<hi){ if(std::gcd(c,d)==1) v.push_back({(u64)val,(u32)(c+d),(u32)c,1}); ++c; }
        nextC[d]=(u32)c;
        if(val<hiEnd) pushD(seg_of((u64)val)-s0,(u32)d);
        d32=nxt;
      }
      headD[sg-s0]=-1;
      npairs+=v.size();
      std::sort(v.begin(),v.end(),[](const Rec& p,const Rec& q){ return p.n<q.n; });
      for(size_t i=0;i<v.size();){
        size_t j=i; while(j<v.size() && v[j].n==v[i].n) ++j;
        if((int)(j-i)>=kmin){
          std::vector<Rec> r(v.begin()+i,v.begin()+j);
          for(auto& x: r){                                // exact re-check
            u128 X=(u128)x.x*x.x*x.x, Y=(u128)x.y*x.y*x.y;
            if((x.neg ? X-Y : X+Y)!=(u128)x.n || std::gcd((u64)x.x,(u64)x.y)!=1){ std::printf("FATAL: bad pair\n"); std::exit(3); }
          }
          hits[blk].push_back({v[i].n,r});
        }
        i=j;
      }
    }
    int dn=++done;
#pragma omp critical
    { std::printf("  blocks %d/%d, %llu pairs\n",dn,nblocks,(unsigned long long)npairs.load()); std::fflush(stdout); }
  }
  // deterministic output: numbers ascending, pairs within a number sorted
  std::vector<std::pair<u64,std::vector<Rec>>> all;
  for(auto& h: hits) for(auto& e: h) all.push_back(e);
  std::sort(all.begin(),all.end(),[](const auto& p,const auto& q){ return p.first<q.first; });
  for(auto& e: all) std::sort(e.second.begin(),e.second.end(),[](const Rec& p,const Rec& q){
    return p.neg!=q.neg ? p.neg<q.neg : p.x!=q.x ? p.x<q.x : p.y<q.y; });
  FILE* f=fopen(out.c_str(),"w");
  std::fprintf(f,"# cabtaxi v2: n = x^3 + y^3, gcd(x,y)=1, signs allowed; all %llu < n <= %llu with >= %d representations\n",
               (unsigned long long)A,(unsigned long long)B,kmin);
  std::map<int,std::vector<u64>> byk;
  for(auto& e: all){
    int k=(int)e.second.size(); byk[k].push_back(e.first);
    std::fprintf(f,"%llu;%d;",(unsigned long long)e.first,k);
    for(size_t t=0;t<e.second.size();++t){ auto& x=e.second[t];
      std::fprintf(f,"%s%u:%s%u",t?",":"",x.x,x.neg?"-":"",x.y); }
    std::fprintf(f,"\n");
  }
  fclose(f);
  std::printf("B=%llu coprime signed pairs=%llu kmin=%d time=%.0fs\n",(unsigned long long)B,
              (unsigned long long)npairs.load(),kmin,std::chrono::duration<double>(std::chrono::steady_clock::now()-T0).count());
  for(auto it=byk.rbegin(); it!=byk.rend(); ++it){
    auto& L=it->second; std::sort(L.begin(),L.end());
    std::printf("  k=%d: %zu numbers, smallest:",it->first,L.size());
    for(size_t i=0;i<L.size() && i<4;++i) std::printf(" %llu",(unsigned long long)L[i]);
    std::printf("\n");
  }
  return 0;
}
