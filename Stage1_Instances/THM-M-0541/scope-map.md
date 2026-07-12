# Scope map

## Included result family

- An abstract simplicial complex `K` on a vertex type, with finite simplices and downward closure.
- Degree-`n` oriented simplicial chains with coefficients fixed by the selected source statement.
- The alternating face boundary and the identity `boundary (boundary c) = 0` needed to obtain a
  chain complex.
- Degreewise homology, defined as cycles modulo boundaries or by the equivalent categorical
  homology object.
- Functoriality: an admissible simplicial map induces a chain map and hence maps on homology.

This is a result family because the Stage0 phrase is not itself a closed proposition. The statement
phase must select one root proposition (or an explicitly composed finite family) without silently
turning the existence of definitions into theorem completion.

## Frozen statement choices

`Statement.lean` fixes integral finite-support chains on ordered simplices, with the increasing
vertex enumeration supplying orientation. It uses unreduced degrees in `Nat`, excludes the empty
simplex and degree `-1`, and includes empty vertex types and infinite complexes. The root is the
existence of the basis-level alternating boundary and its square-zero law.

The encoding builds directly from `AbstractSimplicialComplex`; no alternate presentation is
credited. Functoriality and independence of vertex order are deferred to explicit downstream
bridges rather than assumed as part of this construction root.

## Explicit exclusions

- Singular homology, cellular homology, or Cech homology as a substitute.
- The comparison theorem between simplicial and singular homology of a realization.
- Homotopy invariance, excision, Mayer-Vietoris, the Eilenberg-Steenrod axioms, or homology of one
  particular complex unless explicitly made a downstream obligation.
- Dold-Kan equivalence as a substitute for constructing the simplicial chain complex of `K`.
- A structure that assumes the boundary-square or homology result as a field.

The pinned mathlib modules expose abstract simplicial complexes, alternating face-map complexes,
and a general homology functor. Intake has not established the concrete bridge from a complex `K`
to the coefficient-valued simplicial object required by the intended result family.
