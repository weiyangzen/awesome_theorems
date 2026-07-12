# Scope map

## Included theorem family

- A finite-rank real vector bundle, or the source-selected generalization, over a suitably regular
  base space.
- An orientation over a fixed coefficient ring, expressed by a Thom class restricting to a
  generator on every fibre.
- The degree-shifting map given by pullback followed by cup product with that Thom class.
- An isomorphism between base cohomology and relative cohomology of the disk/sphere-bundle pair;
  the equivalent reduced-cohomology formulation for the Thom space is included only through a
  checked transport.

## Decisions required at statement freeze

The statement phase must select and inspect one exact source theorem and freeze: real, complex, or
general vector bundles; rank and universe binders; paracompactness, compactness, CW, or other base
hypotheses; ordinary versus compactly supported cohomology; singular, Cech, or generalized
cohomology; the coefficient ring and any local coefficient orientation system; the definition of
orientation and normalization of the Thom class; disk/sphere bundles versus zero-section
complements versus the Thom-space quotient; the map direction and degree indexing; and naturality
claims. It must explicitly handle rank zero, empty or disconnected bases, nonorientable bundles,
boundary degrees, and whether an orientation is data or an existence hypothesis.

These are proposition-changing choices, not notational details. Ordered Lean binders, typeclass
assumptions, universes, foundations, and imports must be derived from the selected variant.

## Explicit exclusions

- The Thom space construction or existence of a Thom class without the isomorphism conclusion.
- The Gysin sequence, Euler-class identities, Poincare duality, or the tubular-neighborhood theorem
  as a substitute for the root theorem.
- A trivial-bundle suspension isomorphism or a single-rank special case in place of the selected
  bundle theorem.
- A structure, hypothesis, or abstract equivalence field that assumes the desired isomorphism.
- Homological or generalized-cohomology variants unless the selected source and checked transports
  make them the canonical claim.
- The repository metadata value `已验证` as human-source or kernel evidence.

No Lean proposition is frozen at intake. A later statement must expose the actual bundle,
orientation, Thom class, cohomology theory, cup-product map, and isomorphism rather than package the
conclusion as input data.
