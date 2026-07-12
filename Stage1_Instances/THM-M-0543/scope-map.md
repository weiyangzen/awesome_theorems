# Scope map

## Included human claim

- A smooth manifold `M` and a degree `k`.
- The de Rham cohomology group of smooth real-valued differential forms: closed `k`-forms modulo
  exact `k`-forms.
- Singular cohomology of the underlying topological space with real coefficients, using a concrete
  singular or smooth-singular cochain model.
- The comparison induced by integration of forms over smooth singular chains, including the
  Stokes compatibility needed for it to descend to cohomology.
- A degreewise natural real-linear isomorphism, with ring compatibility included only if the
  selected source theorem states and proves it.

## Decisions required at statement freeze

The statement phase must select and inspect an exact source theorem, then freeze whether manifolds
are finite-dimensional, Hausdorff, second countable/paracompact, with or without boundary, and
whether disconnected or empty manifolds are admitted. It must fix the degree range, ordinary
versus compact-support cohomology, real versus other characteristic-zero coefficients, smooth
singular versus ordinary singular chains, reduced versus unreduced degree-zero conventions, and
the direction and normalization of the integration comparison.

Binder order, universes, the smoothness model, scalar fields, cochain signs, quotient encodings,
and any naturality or graded-ring conclusion must follow those choices. Boundary cases requiring
explicit treatment include negative/out-of-range degrees in the chosen grading, the empty
manifold, zero-dimensional and noncompact manifolds, manifolds with boundary, and degree zero.

## Explicit exclusions

- De Rham cohomology alone, singular cohomology alone, or merely `d \u2218 d = 0`.
- The Poincare lemma, Stokes' theorem, Hodge theorem, or de Rham homology as a substitute for the
  global comparison isomorphism.
- Equality only of Betti numbers or finite-dimensional vector-space dimensions.
- Compact-support de Rham theory, relative cohomology, or a complex-analytic comparison unless an
  exact checked transport to the selected ordinary real theorem is supplied.
- An abstract structure that contains the comparison isomorphism or its inverse as assumed data.

No Lean target is frozen in this intake. A later target must expose concrete complexes,
cohomologies, integration map, and induced isomorphism rather than restating the desired result as
a field or hypothesis.
