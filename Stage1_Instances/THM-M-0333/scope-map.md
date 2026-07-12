# Scope map

## Included topic boundary

- A complex Hilbert space and its algebra of bounded complex-linear operators.
- A source-specified unital adjoint-closed operator algebra, or a source-specified generating set
  together with the precise algebra it generates.
- The commutant and bicommutant taken inside all bounded operators on that Hilbert space.
- The exact strong-operator or weak-operator topology and the corresponding closure predicate.
- The source-selected equality or equivalence among algebra closure, bicommutant, and topological
  closedness.

## Ambiguities to resolve at statement freeze

The short repository gloss is compatible with several non-identical formulations:

1. A unital star subalgebra equals its bicommutant if and only if it is weak-operator closed.
2. The analogous equivalence using the strong operator topology.
3. The bicommutant of a unital self-adjoint algebra or generating set equals its weak closure.
4. The bicommutant equals its strong closure, with weak and strong closures identified as a
   consequence.
5. The definitional fact that an already bundled `VonNeumannAlgebra` equals its bicommutant.

Item 5 is not a proof of items 1-4: pinned mathlib builds bicommutant equality into the bundled
structure. The statement phase must choose a source, preserve its direction and hypotheses, and
freeze universes, scalar field, identity and adjoint assumptions, topology, closure operation,
ordered binders, conclusion, and all boundary cases.

## Explicit exclusions

- `VonNeumannAlgebra.commutant_commutant` as a substitute for the characterization theorem; it
  unfolds a property required by the bundled input.
- The algebraic identity that a centralizer is triple-centralizer stable.
- Sakai's abstract predual characterization or other representation/classification theorems.
- A theorem about only finite-dimensional operator algebras.
- Omitting unitality or adjoint closure without a source-supported reformulation.
- Treating weak, weak-star, strong, strong-star, or norm topology as interchangeable.
- Treating the repository label `已验证` as human-source or kernel evidence.

No canonical Lean target is frozen in this intake because the source record does not determine one.
