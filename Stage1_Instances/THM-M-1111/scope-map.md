# Scope map

## Included claim

- Two dimension-indexed Wigner Hermitian random matrices, with independent upper-triangular atom
  variables subject to the selected source's normalization and tail/regularity condition.
- Off-diagonal atom distributions matching moments through total order four, and diagonal atom
  distributions matching through order two, using the source's complex-moment convention.
- Comparison of expectations of a smooth test function applied to a fixed finite tuple of ordered,
  normalized eigenvalues.
- The exact index range, derivative bounds on the test function, convergence/error rate, and order
  of quantifiers stated by the selected immutable Tao-Vu theorem.

## Decisions reserved for the statement phase

The Tao-Vu paper family contains a basic four moment theorem, a truncated version, and later
variants near the spectral edge. The next phase must select one version and freeze its theorem
number and text. It must then decide from that text: real symmetric versus complex Hermitian
scope, the normalization of matrix entries and eigenvalues, Condition C0 or its replacement, how
complex moments are matched, whether indices are bulk-only or may approach the edge, the allowed
number of eigenvalues, smoothness/derivative exponents for the test function, and the quantitative
comparison bound. These details may not be inferred from the repository's one-line description.

## Explicit exclusions

- The assertion that four matching scalar moments imply identical distributions.
- A central limit theorem, the Wigner semicircle law, or universality of only the empirical spectral
  distribution.
- A qualitative slogan that all random matrices have universal local statistics.
- The replacement principle, Lindeberg exchange, or eigenvalue-stability estimates alone; these
  may later be proof obligations but are not substitutes for the root comparison theorem.
- A proposition made tautological by assuming the desired eigenvalue-statistics comparison.

Degenerate dimensions, repeated eigenvalues, eigenvalue ordering, measurability, integrability, and
empty/out-of-range index cases must be represented according to the chosen source rather than
hidden in Lean definitions.
