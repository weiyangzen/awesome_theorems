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

## Statement-phase decisions

The selected source must fix coefficients (`Z`, a commutative ring, or an abelian category), ordered
versus oriented simplices, finite versus locally finite chains, augmented/reduced versus unreduced
homology, whether the empty simplex is present, and the precise class of simplicial maps. It must
also fix universe parameters, degree indexing, signs, degenerate cases (empty complex and low
degrees), and whether functoriality and invariance under vertex-order choice belong to the root.

The Lean encoding must decide whether to build directly from
`AbstractSimplicialComplex`, pass through an associated simplicial object, or state the construction
for an already supplied simplicial object. Checked transports are required for any credited
alternate presentation.

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
