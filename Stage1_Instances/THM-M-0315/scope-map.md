# Scope map

## Included theorem-family boundary

- Compact linear operators on a source-specified Banach or Hilbert space.
- An equation involving the identity and a compact operator, or equivalently a nonzero spectral
  parameter for a compact endomorphism.
- The exact alternative selected by a primary source: spectral membership, bijectivity, or
  solvability subject to an adjoint-kernel condition.
- All source-required scalar-field, completeness, topology, adjoint, and nonzero-parameter
  hypotheses.

## Ambiguities to resolve at statement freeze

1. **Spectral form:** for compact `T` and nonzero `mu`, either `mu` is an eigenvalue or lies in the
   resolvent set.
2. **Identity-minus-compact form:** `I - T` is injective exactly when it is surjective, often
   accompanied by finite-dimensional kernel/cokernel claims.
3. **Adjoint solvability form:** `(I - T)x = y` is solvable exactly when `y` is orthogonal to the
   nullspace of the adjoint equation.

These forms require nontrivial transports and different structures. The statement phase must
inspect an immutable source, choose one proposition, and freeze ordered binders, hypotheses,
conclusion, and whether the alternative is exclusive or merely a disjunction.

## Explicit exclusions

- A general theorem about arbitrary Fredholm operators as a substitute for compact perturbations
  of the identity.
- The Fredholm integral equation without a specified function space, kernel regularity, measure,
  and induced compact operator.
- The analytic Fredholm theorem for holomorphic operator families.
- The Fredholm index-zero assertion alone, or the compact-operator spectral theorem as a whole.
- A tautological restatement that assumes invertibility, solvability, or the desired alternative.
- The repository `已验证` label or a theorem-name match as proof or exact-statement evidence.

No canonical Lean target is frozen at intake because the source record does not distinguish the
three formulations above.
