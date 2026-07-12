# Scope map

## Included topic boundary

- Compact continuous linear endomorphisms of a source-specified real or complex Hilbert space.
- The source-specified self-adjointness condition.
- A source-specified spectral decomposition into mutually orthogonal eigenspaces or eigenvectors.
- The role of the zero eigenspace and finite-dimensionality of nonzero eigenspaces.
- Any separability, completeness, convergence, ordering, or multiplicity hypotheses required by the
  selected formulation.

## Ambiguities to resolve at statement freeze

The repository gloss does not choose among several related but nonidentical conclusions:

1. The closed span of all eigenspaces is the entire Hilbert space, equivalently its orthogonal
   complement is trivial.
2. There exists an orthonormal basis consisting of eigenvectors.
3. Every vector admits a norm-convergent expansion in eigenvectors, with an explicit formula for
   the action of the operator.
4. The nonzero spectrum is a finite or countable set of real eigenvalues, of finite multiplicity,
   with zero as its only possible accumulation point.

The statement phase must select one exact proposition from an immutable source and freeze its
ordered binders, field, universe parameters, completeness and self-adjointness predicates,
decomposition encoding, topology of convergence, and zero/operator boundary cases. Related
consequences may become child obligations but cannot silently replace the root.

## Explicit exclusions

- The finite-dimensional spectral theorem without compact-operator content.
- The spectral theorem for arbitrary bounded normal or self-adjoint operators using projection-
  valued measures or functional calculus.
- The Riesz-Schauder or Fredholm alternative alone; nonzero spectral points being eigenvalues is
  not by itself a decomposition theorem.
- Singular-value decomposition for a non-self-adjoint compact operator.
- Compact-resolvent differential operators as substitutes for a compact operator.
- A structure that assumes an eigenbasis or decomposition and then projects it as the conclusion.
- The metadata label `已验证` or a matching mathlib docstring as proof/source acceptance.

No canonical Lean target is frozen at intake because the source record does not distinguish these
formal variants.
