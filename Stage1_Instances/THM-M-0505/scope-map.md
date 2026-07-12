# Scope map

## Included theorem family

- The Riemann zeta function and its nontrivial zeros, with multiplicity and the
  summation convention fixed by a pinpoint source.
- An admissible test function and its source-normalized Fourier or Mellin
  transform.
- A prime-power side, normally expressed using logarithmic prime weights or the
  von Mangoldt function.
- Every pole, trivial-zero, Gamma-factor, and archimedean contribution required
  by the selected identity.
- The analytic hypotheses and convergence/limiting claims that make both sides
  well-defined.

The root is an equality after pairing the zeta zero/prime distributions with a
test function. It is not the vague assertion that zeta "has an explicit
formula".

## Statement decisions still open

The statement phase must inspect an immutable source and freeze:

1. the exact displayed identity and its theorem or formula locator;
2. whether the test function lives on `Real`, `Complex`, or a multiplicative
   group, and all smoothness, holomorphy, compact-support, decay, and symmetry
   assumptions;
3. the Fourier/Mellin transform sign, scaling, and `2 * pi` normalization;
4. the zero collection, multiplicities, ordering, symmetric truncation, and
   convergence mode;
5. the prime-power indexing and weights, including the value at `1`;
6. the exact constants and allocation of the pole at `1`, trivial zeros, and
   logarithmic derivative of the Gamma factor;
7. whether the equality is distributional or an equality of independently
   defined sums/integrals, and the checked transport for any advertised form.

## Formal object boundary

Pinned mathlib exposes `riemannZeta`, `ArithmeticFunction.vonMangoldt`, real
Fourier integrals, interval integrals, complex Gamma, and infinite sums. These
are statement ingredients only. The intake did not identify a declaration of
the Weil explicit formula, construct a multiset of zeta zeros, or establish the
analytic convergence required by any variant.

## Explicit exclusions

- The Riemann-von Mangoldt zero-counting formula or a prime-counting explicit
  formula substituted without a checked source equivalence.
- The Euler product, functional equation, special zeta values, or prime number
  theorem alone.
- An identity for a different zeta or `L`-function unless the source-selected
  statement explicitly specializes to the Riemann zeta formula and the
  specialization is checked.
- A finite numerical sum over computed zeros or primes as evidence for the
  infinite identity.
- A tautological theorem that assumes the desired equality or packages it as a
  field of a structure.
- The repository label `已验证` as human-proof or machine-proof evidence.
