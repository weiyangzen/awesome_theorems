# Scope map

## Included claim

- An `n`-dimensional oriented topological manifold `M`, possibly with boundary `∂M`.
- Cohomology with compact supports on `M` and relative homology of the pair `(M, ∂M)`.
- Degree reversal `q` to `n - q`, induced by cap product with the orientation/fundamental class.
- Naturality and coefficient hypotheses only where they occur in the selected primary theorem.

## Boundary decisions for the statement phase

The primary-source edition must decide whether `M` is compact, paracompact, connected, or merely
locally compact; whether orientations are over `Z` or a coefficient ring/local system; whether the
theorem is stated as an isomorphism or a cap-product map; and the behavior for `q > n`, empty
boundary, disconnected spaces, and noncompact manifolds. Binder order and universes must follow
those decisions rather than the legacy wrapper.

## Explicit exclusions

- Poincare duality only for closed manifolds as a substitute for the boundary theorem.
- Alexander duality, the Lefschetz fixed-point theorem, or a finite-dimensional vector-space
  dimension equality.
- An abstract structure containing the desired isomorphism as a field.
- The checked adjacent API in `S1_M_119.lean` as proof of the terminal result.

The later formal statement must provide concrete pair, relative singular homology, compact-support
cohomology, cap product, and orientation-class interfaces, or record a precise API blocker.
