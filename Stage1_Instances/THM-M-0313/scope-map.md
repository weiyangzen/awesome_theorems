# Scope map

## Included topic boundary

- Normal operators on a source-specified complex Hilbert space.
- The source-specified notion of spectral decomposition.
- All boundedness, domain, separability, and completeness hypotheses used by that representation.
- Existence, equality, support, uniqueness, and convergence clauses explicitly present in the
  selected theorem.

## Ambiguities to resolve at statement freeze

1. **Projection-valued measure:** existence of a PVM `E` supported on the spectrum with an operator
   integral formula such as `T = integral id dE`.
2. **Multiplication representation:** unitary equivalence of `T` to multiplication by a measurable
   function on an `L2` space.
3. **Functional calculus:** existence or properties of the unital star homomorphism from continuous
   functions on the spectrum to bounded operators, sending the identity function to `T`.
4. **Operator class:** bounded everywhere-defined operators versus closed densely defined unbounded
   normal operators; these require materially different statements.

The statement phase must inspect an immutable source and freeze one proposition, ordered binders,
normality predicate, topology/measurability structures, exact decomposition data, equality mode,
and uniqueness clause. It must decide the zero space, spectrum conventions, scalar field,
separability, boundedness, and integral/convergence interpretation.

## Explicit exclusions

- Hermitian or self-adjoint matrices and finite-dimensional unitary diagonalization as substitutes.
- The compact self-adjoint spectral theorem, which is separately tracked by `THM-M-0314`.
- A result only about spectral radius, eigenvalues, resolvents, or continuous functional calculus
  consequences when it does not construct the source-required decomposition.
- Replacing a normal operator by a self-adjoint operator unless the source states that restriction.
- Packaging the desired decomposition as a typeclass assumption and projecting it tautologically.
- Treating the repository label `已验证` or a nearby mathlib theorem as proof credit.

No canonical Lean target is frozen at intake because the repository record does not determine one.
