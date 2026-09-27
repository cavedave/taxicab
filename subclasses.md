1. Predicates for interesting subclasses: cubefree, squarefree, primitive representations, exactly/at-least \(k\) representations, and combinations of these.
Here is a good starting module.

from math import gcd, isqrt
from collections import Counter


# ------------------------------------------------------------
# Basic representation checks
# ------------------------------------------------------------

def canonical_pair(a, b):
    """Treat (a,b) and (b,a) as the same representation."""
    return tuple(sorted((int(a), int(b))))


def valid_cube_representation(n, pair):
    """True iff a^3 + b^3 == n."""
    a, b = pair
    return a > 0 and b > 0 and a**3 + b**3 == n


def distinct_pairs(pairs):
    """
    Return representations with (a,b) and (b,a) treated as identical.
    """
    return set(canonical_pair(a, b) for a, b in pairs)


def valid_taxicab_entry(n, pairs):
    """
    True iff all supplied pairs are distinct positive representations
    of n as a sum of two positive cubes.
    """
    canonical = [canonical_pair(a, b) for a, b in pairs]

    # Duplicate representations?
    if len(canonical) != len(set(canonical)):
        return False

    return all(valid_cube_representation(n, p) for p in canonical)


def representation_count(n, pairs):
    """
    Number of distinct VALID positive cube representations supplied.
    """
    reps = {
        canonical_pair(a, b)
        for a, b in pairs
        if valid_cube_representation(n, (a, b))
    }
    return len(reps)


# ------------------------------------------------------------
# Factorisation utilities
# ------------------------------------------------------------

def factorint_simple(n):
    """
    Simple pure-Python integer factorisation.

    Fine for moderate taxicab numbers.
    Later we can replace this with sympy.factorint() if the numbers
    get large.
    """
    n = abs(int(n))
    factors = Counter()

    while n % 2 == 0:
        factors[2] += 1
        n //= 2

    p = 3
    while p * p <= n:
        while n % p == 0:
            factors[p] += 1
            n //= p
        p += 2

    if n > 1:
        factors[n] += 1

    return dict(factors)


def is_squarefree(n):
    """
    True iff no p^2 divides n.
    """
    if n == 0:
        return False

    return all(e == 1 for e in factorint_simple(n).values())


def is_cubefree(n):
    """
    True iff no p^3 divides n.
    This is the property relevant to OEIS A080642.
    """
    if n == 0:
        return False

    return all(e < 3 for e in factorint_simple(n).values())


# ------------------------------------------------------------
# Properties of the representations
# ------------------------------------------------------------

def is_primitive_pair(a, b):
    """True iff gcd(a,b) == 1."""
    return gcd(a, b) == 1


def all_representations_primitive(pairs):
    """
    True iff every representation is primitive.
    """
    return all(is_primitive_pair(a, b) for a, b in pairs)


def has_nonprimitive_representation(pairs):
    return any(gcd(a, b) > 1 for a, b in pairs)


# ------------------------------------------------------------
# Useful taxicab subclasses
# ------------------------------------------------------------

def has_at_least_k_representations(n, pairs, k):
    return (
        valid_taxicab_entry(n, pairs)
        and representation_count(n, pairs) >= k
    )


def has_exactly_k_representations(n, pairs, k):
    """
    IMPORTANT: this means exactly k among the representations
    supplied to us.

    To establish mathematically that n has exactly k total
    representations, our search must have found ALL representations.
    """
    return (
        valid_taxicab_entry(n, pairs)
        and representation_count(n, pairs) == k
    )


def is_cubefree_taxicab(n, pairs, k=2):
    """
    Candidate for the A080642-style class:

        cubefree n having at least k representations
        as a sum of two positive cubes.
    """
    return (
        valid_taxicab_entry(n, pairs)
        and representation_count(n, pairs) >= k
        and is_cubefree(n)
    )


def is_squarefree_taxicab(n, pairs, k=2):
    return (
        valid_taxicab_entry(n, pairs)
        and representation_count(n, pairs) >= k
        and is_squarefree(n)
    )


def is_primitive_taxicab(n, pairs, k=2):
    """
    Every supplied representation is primitive.
    """
    return (
        valid_taxicab_entry(n, pairs)
        and representation_count(n, pairs) >= k
        and all_representations_primitive(pairs)
    )


def is_cubefree_primitive_taxicab(n, pairs, k=2):
    return (
        is_cubefree_taxicab(n, pairs, k)
        and all_representations_primitive(pairs)
    )


# ------------------------------------------------------------
# One function returning all interesting flags
# ------------------------------------------------------------

def classify_taxicab(n, pairs):
    """
    Produce a useful set of properties for one candidate.
    """
    reps = representation_count(n, pairs)

    return {
        "n": n,
        "representations": reps,

        "valid": valid_taxicab_entry(n, pairs),

        "cubefree": is_cubefree(n),
        "squarefree": is_squarefree(n),

        "all_primitive": all_representations_primitive(pairs),
        "has_nonprimitive": has_nonprimitive_representation(pairs),

        "taxicab_2+": reps >= 2,
        "taxicab_3+": reps >= 3,
        "taxicab_4+": reps >= 4,
        "taxicab_5+": reps >= 5,
        "taxicab_6+": reps >= 6,
        "taxicab_7+": reps >= 7,

        "cubefree_5+": is_cubefree_taxicab(n, pairs, 5),
        "cubefree_6+": is_cubefree_taxicab(n, pairs, 6),
        "cubefree_7+": is_cubefree_taxicab(n, pairs, 7),

        "squarefree_5+": is_squarefree_taxicab(n, pairs, 5),
        "squarefree_6+": is_squarefree_taxicab(n, pairs, 6),
        "squarefree_7+": is_squarefree_taxicab(n, pairs, 7),
    }

    n = 1729
pairs = [
    (1, 12),
    (9, 10),
]

print(valid_taxicab_entry(n, pairs))
# True

print(is_cubefree_taxicab(n, pairs, 2))
# True

print(classify_taxicab(n, pairs))

if is_cubefree_taxicab(n, pairs, 5):
    print("Possible A080642(5) candidate:", n)

    if is_cubefree_taxicab(n, pairs, 6):
    print("cubefree 6-way:", n)

if is_squarefree_taxicab(n, pairs, 5):
    print("squarefree 5-way:", n)

    def could_be_cubefree(pairs):
    """
    Very cheap rejection test.

    If gcd(a,b) > 1 for any representation, then
    gcd(a,b)^3 divides a^3+b^3, so n cannot be cubefree.
    """
    return all(gcd(a, b) == 1 for a, b in pairs)

    def is_cubefree_taxicab_fast(n, pairs, k=2):
    if len(distinct_pairs(pairs)) < k:
        return False

    if not valid_taxicab_entry(n, pairs):
        return False

    # Cheap rejection before factorisation
    if not could_be_cubefree(pairs):
        return False

    return is_cubefree(n)

    - A001235 — numbers with at least two positive-cube representations.
- A018787 — at least three ways.
- A023051 — at least four ways.
- A051167 — at least five ways.
- A018850 — primitive taxicab numbers, i.e. numbers with more than one cube-sum representation satisfying the primitive condition. OEIS
So I would make the miner calculate at least these properties for every \(N\):
N
number_of_representations

cubefree
squarefree

all_pairs_coprime
global_gcd_of_all_bases

omega(N)          # distinct prime factors
Omega(N)          # prime factors with multiplicity
factorization

is_perfect_square
is_perfect_cube
is_perfect_power


features = classify(n, pairs)

if features["ways"] >= 6:
    report("6-way", n)

if features["ways"] >= 6 and features["cubefree"]:
    report("cubefree 6-way", n)

if features["ways"] >= 6 and features["primitive_global"]:
    report("primitive 6-way", n)

if features["ways"] >= 7 and features["squarefree"]:
    report("squarefree 7-way", n)

if features["ways"] >= 5 and features["perfect_square"]:
    report("square 5-way", n)