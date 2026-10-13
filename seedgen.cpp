// seedgen -- exhaustive seed list for engine_b (fixes the missing-family bug)
//
// engine_b only ever finds numbers of the form N*m^3 with N a seed, so a
// family is invisible unless one of its members is in the seed file. The old
// seeds.csv had every 3-way <= ~1e15 but only a hand-picked ~4.8k 2-ways, so
// e.g. the 2-way 4513486310216 was absent, and with it its descendants
// T(5,6)=55634997032869710456 (= 231^3 * it) and Boyer's 6-way
// 869296828638589225875000.
//
// This enumerates EVERY pair a<=b with a^3+b^3 <= B, finds all n with >= 2
// representations, and keeps only the "roots": n such that no n/g^3 (g>1) is
// itself a >=2-way. Dropping the others loses nothing, since the engine scans
// every multiplier m of each root, so g^3*root is reached at m=g.
//
// Guarantee: with these seeds, every >=2-way n <= UB with some >=2-way
// cube-quotient n/g^3 <= B is reachable by engine_b in round 1 (modulo --mcap).
//
// Build: g++ -O3 -fopenmp -std=c++17 seedgen.cpp -o seedgen
// Run:   ./seedgen --max 1000000000000000 --out seeds_1e15.csv [--all multi_1e15.csv]

#include <algorithm>
#include <atomic>
#include <cmath>
#include <cstdint>
#include <cstdio>
#include <cstdlib>
#include <map>
#include <numeric>
#include <string>
#include <unordered_set>
#include <vector>
#ifdef _OPENMP
#include <omp.h>
#endif

using u64 = uint64_t;
using u128 = unsigned __int128;

static u64 icbrt(u64 n){ if(!n) return 0; u64 r=(u64)cbrtl((long double)n);
  while(r && (u128)r*r*r>n) --r; while((u128)(r+1)*(r+1)*(r+1)<=n) ++r; return r; }

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
  return true;                                   // deterministic for n < 3.3e24
}
static u64 rho(u64 n, u64 c){
  u64 x=2, y=2, d=1;
  while(d==1){
    x=((u128)x*x+c)%n; y=((u128)y*y+c)%n; y=((u128)y*y+c)%n;
    d=std::gcd(x>y?x-y:y-x,n);
  }
  return d;
}
static void factor(u64 n, std::map<u64,int>& F){
  for(u64 p=2;p<1000 && p*p<=n;++p) while(n%p==0){ ++F[p]; n/=p; }
  std::vector<u64> st; if(n>1) st.push_back(n);
  while(!st.empty()){
    u64 m=st.back(); st.pop_back();
    if(m==1) continue;
    if(is_prime(m)){ ++F[m]; continue; }
    u64 d=m; for(u64 c=1; d==m; ++c) d=rho(m,c);
    st.push_back(d); st.push_back(m/d);
  }
}

struct Multi { u64 n; std::vector<std::pair<u64,u64>> reps; };

int main(int argc, char** argv){
  u64 B=1000000000000ULL; std::string out="seeds_gen.csv", all; int segs=0;
  for(int i=1;i<argc;++i){ std::string a=argv[i];
    auto nx=[&]()->const char*{ if(i+1>=argc){ std::printf("bad args\n"); std::exit(1);} return argv[++i]; };
    if(a=="--max") B=strtoull(nx(),0,10);
    else if(a=="--out") out=nx();
    else if(a=="--all") all=nx();
    else if(a=="--segments") segs=atoi(nx());
    else { std::printf("usage: seedgen --max B [--out seeds.csv] [--all multi.csv] [--segments S]\n"); return 1; }
  }
  if(B>(u64)4e18){ std::printf("--max too large for u64 sums\n"); return 1; }
  // pairs below t grow like t^{2/3}: equal-count segments are B*(i/S)^{3/2}
  if(!segs){ double pairs=0.45*pow((double)B,2.0/3.0); segs=std::max(64,(int)(pairs/4e6)); }
  std::vector<u64> edge(segs+1);
  for(int i=0;i<=segs;++i) edge[i]=(u64)((long double)B*powl((long double)i/segs,1.5L));
  edge[0]=1; edge[segs]=B+1;

  std::vector<std::vector<Multi>> found(segs);
  std::atomic<u64> npairs{0}; std::atomic<int> done{0};
#pragma omp parallel for schedule(dynamic,1)
  for(int sg=0; sg<segs; ++sg){
    const u64 lo=edge[sg], hi=edge[sg+1];          // sums in [lo,hi)
    if(lo>=hi) continue;
    std::vector<std::pair<u64,uint32_t>> v;
    for(u64 a=1; 2*a*a*a<hi; ++a){
      const u64 a3=a*a*a;
      u64 b = lo>a3 ? icbrt(lo-a3-1)+1 : a;          // smallest b with a3+b^3 >= lo
      if(b<a) b=a;
      for(; a3+b*b*b<hi; ++b) v.push_back({a3+b*b*b,(uint32_t)a});
    }
    npairs+=v.size();
    std::sort(v.begin(),v.end());
    for(size_t i=0;i<v.size();){
      size_t j=i; while(j<v.size() && v[j].first==v[i].first) ++j;
      if(j-i>=2){ Multi M; M.n=v[i].first;
        for(size_t t=i;t<j;++t){ u64 a=v[t].second, b=icbrt(M.n-a*a*a);
          if(a*a*a+b*b*b!=M.n){ std::printf("FATAL: bad pair\n"); std::exit(3); }
          M.reps.push_back({a,b}); }
        found[sg].push_back(std::move(M)); }
      i=j;
    }
    int d=++done; if(d%64==0 || d==segs){
#pragma omp critical
      { std::printf("  segments %d/%d, %llu pairs\n",d,segs,(unsigned long long)npairs.load()); fflush(stdout); } }
  }
  std::vector<Multi> M; for(auto& f: found) for(auto& m: f) M.push_back(std::move(m));
  std::sort(M.begin(),M.end(),[](const Multi& x,const Multi& y){ return x.n<y.n; });
  std::unordered_set<u64> multiset; multiset.reserve(M.size()*2);
  for(auto& m: M) multiset.insert(m.n);

  std::vector<std::map<u64,int>> fac(M.size()); std::vector<char> root(M.size(),0);
#pragma omp parallel for schedule(dynamic,256)
  for(size_t i=0;i<M.size();++i){
    factor(M[i].n, fac[i]);
    // enumerate cube divisors g^3 | n, g>1; n is a root iff no n/g^3 is multi
    std::vector<u64> gs{1};
    for(auto& pe: fac[i]){ size_t sz=gs.size(); u64 pw=1;
      for(int e=3;e<=pe.second;e+=3){ pw*=pe.first;
        for(size_t t=0;t<sz;++t) gs.push_back(gs[t]*pw); } }
    bool r=true;
    for(u64 g: gs) if(g>1 && multiset.count(M[i].n/(g*g*g))){ r=false; break; }
    root[i]=r;
  }
  std::map<int,u64> hist, rhist;
  FILE* fo=fopen(out.c_str(),"w"); FILE* fa=all.empty()?nullptr:fopen(all.c_str(),"w");
  for(size_t i=0;i<M.size();++i){
    int k=(int)M[i].reps.size(); ++hist[k];
    std::string line=std::to_string(M[i].n)+";"+std::to_string(k)+";";
    bool first=true;
    for(auto& pe: fac[i]){ line+=(first?"":",")+std::to_string(pe.first)+":"+std::to_string(pe.second); first=false; }
    line+=";"; first=true;
    for(auto& pr: M[i].reps){ line+=(first?"":",")+std::to_string(pr.first)+":"+std::to_string(pr.second); first=false; }
    line+="\n";
    if(fa) fputs(line.c_str(),fa);
    if(root[i]){ ++rhist[k]; fputs(line.c_str(),fo); }
  }
  fclose(fo); if(fa) fclose(fa);
  std::printf("B=%llu pairs=%llu multi-ways=%zu\n",(unsigned long long)B,(unsigned long long)npairs.load(),M.size());
  for(auto& kv: hist) std::printf("  k=%d: %llu total, %llu roots\n",kv.first,(unsigned long long)kv.second,(unsigned long long)rhist[kv.first]);
  return 0;
}
