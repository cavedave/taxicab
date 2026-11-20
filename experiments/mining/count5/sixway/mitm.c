/* mitm.c -- six-way search for one fully factored n (see sixway.py): s = product of a subset of the prime powers of n
   (half A x half B), s <= (4n)^(1/3), and (4n/s - s^2)/3 a quadratic residue mod K small primes (tests via discrete
   logs: allowed tables indexed by dlog(s mod q)). Prints the surviving (maskA, maskB) pairs; sixway.py checks them exactly.
   Input (stdin): nA nB K Lbound / K lines "q t_0..t_{q-2}" / nA+nB lines "log d_1..d_K".  Args: a_start a_end */
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <string.h>
typedef struct { double lg; uint32_t mask; } Bx;
static int K; static int qm1[64]; static uint8_t *tab[64];
static int nA, nB; static double LB;
static double *plg; static int *pd;  /* per prime power: log, K dlogs */
static uint16_t *dB; static Bx *B;
static int cmpb(const void *x, const void *y) { double a = ((Bx*)x)->lg, b = ((Bx*)y)->lg; return a < b ? -1 : a > b; }
int main(int argc, char **argv) {
  long a0 = atol(argv[1]), a1 = atol(argv[2]);
  if (scanf("%d %d %d %lf", &nA, &nB, &K, &LB) != 4) return 1;
  for (int k = 0; k < K; k++) { int q; scanf("%d", &q); qm1[k] = q - 1; tab[k] = malloc(q);
    for (int i = 0; i < q - 1; i++) { int t; scanf("%d", &t); tab[k][i] = t; } }
  int np = nA + nB; plg = malloc(sizeof(double) * np); pd = malloc(sizeof(int) * np * K);
  for (int i = 0; i < np; i++) { scanf("%lf", &plg[i]); for (int k = 0; k < K; k++) scanf("%d", &pd[i * K + k]); }
  long NB = 1L << nB; B = malloc(sizeof(Bx) * NB);
  for (long m = 0; m < NB; m++) { double l = 0; for (int i = 0; i < nB; i++) if (m >> i & 1) l += plg[nA + i]; B[m].lg = l; B[m].mask = m; }
  qsort(B, NB, sizeof(Bx), cmpb);
  dB = malloc(sizeof(uint16_t) * NB * K);
  for (long j = 0; j < NB; j++) for (int k = 0; k < K; k++) { long d = 0;
      for (int i = 0; i < nB; i++) if (B[j].mask >> i & 1) d += pd[(nA + i) * K + k];
      dB[j * K + k] = d % qm1[k]; }
  int dA[64]; long surv = 0, pairs = 0;
  for (long ma = a0; ma < a1; ma++) {
    double la = 0; for (int i = 0; i < nA; i++) if (ma >> i & 1) la += plg[i];
    if (la > LB) continue;
    for (int k = 0; k < K; k++) { long d = 0; for (int i = 0; i < nA; i++) if (ma >> i & 1) d += pd[i * K + k]; dA[k] = d % qm1[k]; }
    long lo = 0, hi = NB; double rem = LB - la;           /* B entries with lg <= rem */
    while (lo < hi) { long mid = (lo + hi) / 2; if (B[mid].lg <= rem) lo = mid + 1; else hi = mid; }
    pairs += lo;
    for (long j = 0; j < lo; j++) {
      const uint16_t *db = dB + j * K; int k;
      for (k = 0; k < K; k++) { int d = dA[k] + db[k]; if (d >= qm1[k]) d -= qm1[k]; if (!tab[k][d]) break; }
      if (k == K) { printf("%ld %u\n", ma, B[j].mask); surv++; }
    }
  }
  fprintf(stderr, "range %ld-%ld: %ld pairs under the size bound, %ld survivors\n", a0, a1, pairs, surv);
  return 0;
}
