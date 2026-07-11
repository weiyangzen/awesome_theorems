# Scope map

## Included subject boundary

- A distribution is a continuous linear functional on compactly supported smooth test functions
  on an open domain `Omega` in a finite-dimensional real vector space (classically `R^n`).
- Restriction to an open subset is determined by evaluating on test functions supported there.
- The zero locus is the union of open subsets on which the restriction is zero; support is its
  complement, hence closed relative to `Omega`.
- The candidate localization result relates vanishing of the restriction, disjointness from the
  support, and vanishing on supported test functions.

## Decisions deferred to statement phase

An inspected source must fix the ambient domain, scalar field, topology on the test-function space,
the exact definition of restriction and support, and which implication/equivalence is the root.
It must also fix relative versus ambient support, the empty domain, the zero distribution,
disconnected domains, and whether support containment uses ordinary or compact support.

The formal phase must then freeze universes and ordered binders and identify concrete mathlib APIs.
The Stage0 title alone is insufficient to choose these details.

## Explicit exclusions

- Support of a function, measure, Fourier transform, or distributional derivative as a substitute.
- A theorem merely asserting that support is closed unless the source root is shown to be exactly it.
- A localization principle for PDE solutions or sheaves without a checked equivalence to the source.
- An abstract structure that assumes restriction, support, or the desired equivalence as a field.
- Any appeal to the untrusted Stage0 label `已验证` as source or kernel evidence.
