# Scope map

## Preserved theorem family

The intake preserves the classical complex-analytic Weierstrass factorization family named by the
catalog: zeros of entire functions are represented through a convergent product of suitable
primary factors, with a zero-free entire factor in the given-function formulation. This sentence
is a family boundary, not a frozen canonical statement.

Two standard roots must not be conflated before an accepted source selects one:

1. Given a discrete zero divisor in the complex plane, construct an entire function having exactly
   those zeros with those multiplicities.
2. Given a nonzero entire function, represent it by a power at zero, an exponential of an entire
   function, and a canonical product over its nonzero zeros.

The second is often expressed schematically as
`f(z) = z^m * exp(g(z)) * product_n E_(p_n)(z / a_n)`. This is an uncredited candidate shape only;
the repository wording does not select it.

## Decisions required at statement freeze

1. Select an immutable primary or authoritative source edition, exact theorem and definition
   locators, incorporated premises, corrections and errata, and an independent source reviewer.
2. Choose the prescribed-zero construction, the factorization of a given function, an explicitly
   checked equivalence of both, or another source-selected root.
3. Fix the entire-function predicate and whether the scalar and domain are exactly `Complex`.
4. Decide whether the input function is required to be nonzero and how the identically-zero case is
   classified rather than hidden behind an impossible zero enumeration.
5. Represent zeros as a sequence, multiset, locally finite divisor, or another structure; fix
   multiplicities, enumeration invariance, nonzero entries, and absence of finite accumulation.
6. Separate the zero at the origin and fix its finite multiplicity `m`, including the case `m = 0`.
7. Define the Weierstrass primary factors
   `E_p(w) = (1 - w) * exp(w + w^2/2 + ... + w^p/p)`, including the `p = 0` convention.
8. State the genus sequence `p_n`, its existence or explicit growth condition, and the exact
   local-uniform convergence and infinite-product semantics.
9. Fix the residual zero-free factor, ordinarily `exp(g)` for an entire `g`, and state any use of a
   holomorphic logarithm or simple-connectedness bridge.
10. Decide whether the conclusion asserts existence only, equality at every point, preservation of
    the zero divisor, a converse, uniqueness up to a zero-free factor, or any normalization.

## Degenerate and boundary cases

Statement review must explicitly cover the identically-zero function; a nonzero constant; no
nonzero zeros; finitely many zeros and polynomial cases; a zero only at the origin; repeated zeros;
arbitrary enumerations of the same divisor; sequences with a finite accumulation point; invalid
zero entries among the `a_n`; empty and finite products; `p_n = 0`; and pointwise versus locally
uniform product convergence. No case is excluded at intake because no proposition has been frozen.

## Excluded substitutions

- Hadamard factorization for finite-order entire functions is a stronger growth-controlled result.
- The Mittag-Leffler theorem (`THM-M-0231`) concerns prescribed principal parts of meromorphic
  functions, not entire-function zero factorization.
- Inner-outer factorization (`THM-M-0251`) concerns a different function-space boundary.
- Weierstrass preparation and mathlib's power-series `IsWeierstrassFactorization` are local
  algebraic factorizations, not an infinite product over the zeros of an entire function.
- Weierstrass approximation, Stone-Weierstrass, Bolzano-Weierstrass, elliptic Weierstrass functions,
  and unrelated uses of "canonical product" share terminology only.
- Euler's infinite product for sine is one special function, not the universal theorem.
- `MeromorphicOn.extract_zeros_poles` assumes finite divisor support and uses a finite product;
  `Complex.canonicalFactor` is a disk/Blaschke factor rather than the primary factor `E_p`.
- A generic infinite-product convergence theorem, a structure storing the requested equality, a
  theorem name, `#check`, or the untrusted `已验证` label supplies no target proof.

## Formal boundary

No canonical Lean expression is frozen at intake. At pinned mathlib revision
`8a178386ffc0f5fef0b77738bb5449d50efeea95`, the probe checks analytic order, isolated-zero,
locally uniform product, holomorphic-limit, finite-support meromorphic factorization, disk factor,
and sine-product interfaces. The bounded exact-topic search found only the unrelated power-series
Weierstrass preparation namesake and no terminal universal entire-function factorization
declaration in pinned mathlib or repo-local Lean. This is scoped intake discovery, not an exhaustive
anchor audit or a proof of global absence.
