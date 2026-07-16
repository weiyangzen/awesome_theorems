# Scope map

## Included claim

The selected target is the reduced, set-theoretic projective
analytic-to-algebraic theorem. For every `n : Nat`, the ambient carrier is
`Projectivization Complex (Fin (n + 1) -> Complex)`. A subset `Z` is required
to have a closed quotient preimage and, near each of its points, that preimage
must be the common zero locus of finitely many `AnalyticOnNhd Complex`
functions on the homogeneous-coordinate vector space.

The conclusion supplies one set of complex multivariate polynomials, each
homogeneous of some degree, whose simultaneous zeros on every nonzero
representative are exactly `Z`. Quantifying over every representative avoids
postulating an unproved quotient-evaluation function. This formulation
includes reducible subsets, the empty and full subsets, and `n = 0`.

## Exclusions

- Chow's lemma, Chow varieties, Chow groups, and Chow rings.
- The converse direction that algebraic projective subvarieties are analytic.
- GAGA equivalences stronger than the target unless a checked specialization
  produces this exact conclusion.
- Compact analytic spaces not already embedded as closed subvarieties of a
  projective space.
- Abstract predicates with no native mathematical data. The local analytic
  functions and homogeneous polynomial family in `Statement.lean` are data,
  not uninterpreted placeholders.
- Merely showing that the ambient projective scheme is proper.

## Required transports

Nonreduced analytic subspaces, algebraic closed subschemes, and structured
analytification/GAGA formulations are not credited alternate encodings. Any
later use of one must bind both statement fingerprints and provide a checked
transport accounting for nilpotent structure, not merely equality of carriers.

## Statement mutation obligations

The executable mutation suite removes closedness, changes the projective domain
to an affine coordinate space, moves the equation family outside the subset
binder, and excludes `n = 0`. Lean rejects exact-type equality for each mutant,
and the validator requires a distinct fully explicit expression fingerprint.
