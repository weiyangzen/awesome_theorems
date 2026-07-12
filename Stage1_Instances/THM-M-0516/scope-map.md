# Scope map

## Included topic boundary

- A source-specified theorem about p-adic L-functions in the cyclotomic setting.
- The exact prime, coefficient field, character and parity/conductor restrictions selected by that
  source.
- The exact construction or existence/uniqueness claim, interpolation values, Euler factors,
  normalization, and exceptional cases belonging to the selected theorem.
- Any cyclotomic tower, Galois group, measure, power-series, class-group, or Iwasawa-module objects
  actually required by that exact claim.

## Ambiguities to resolve at statement freeze

The repository record does not decide among these non-interchangeable readings:

1. existence of the Kubota-Leopoldt p-adic L-function for a Dirichlet character;
2. its interpolation formula at negative integers, including conventions for Euler factors and
   generalized Bernoulli numbers;
3. a uniqueness, analyticity, measure, or power-series formulation of the same construction;
4. an arithmetic theorem about class groups or Iwasawa modules in a cyclotomic tower.

The statement phase must freeze an immutable source passage and one proposition with ordered
binders. It must decide whether the prime is odd, which characters and conductors are allowed,
whether the trivial character or exceptional zero is included, the value field and embeddings,
the cyclotomic layer/tower, normalization of the complex and p-adic L-values, and every boundary
case.

## Explicit exclusions

- The Iwasawa main conjecture as a substitute; it is separately listed as `THM-M-0517` in the
  repository source inventory.
- The unrelated Iwasawa criterion for simplicity of groups found in mathlib.
- A theorem merely about finite cyclotomic fields, complex Dirichlet L-series, p-adic valuations,
  or p-adic completeness.
- A definition packaged as assumed data followed by a tautological property.
- Any convenient special case without an exact checked transport from the selected source claim.
- The inventory label `已验证` as human-proof or kernel-proof evidence.

No canonical Lean target is frozen at intake because the source record does not identify a unique
proposition.
