# Scope map

## Included claim

- Topological spaces `X` and `Y` related by a homotopy equivalence.
- Homology groups of `X` and `Y` in each degree.
- Isomorphisms induced by the forward map of the chosen homotopy equivalence, with inverse induced
  by its homotopy inverse.
- The two underlying facts needed for that conclusion: functoriality of homology and equality of
  induced homology maps for homotopic continuous maps.

This is the narrow reading fixed by the Stage0 text: "homotopy equivalent spaces have the same
homology groups." Here "same" means isomorphic, not definitionally equal.

## Frozen statement conventions

`Target.lean` fixes unreduced singular homology with integral coefficients, valued in
`ModuleCat ℤ`, and indexed by `n : ℕ`. It quantifies over base-universe types with topologies and a
packaged `ContinuousMap.HomotopyEquiv`; the asserted morphism is the image of `e.toFun` under the
degree-`n` singular homology functor and the conclusion is `IsIso` for that exact morphism.

Degree zero and empty spaces are included without side conditions. Negative degrees are excluded by
the natural-number grading. This induced-map formulation is stronger and more informative than a
bare existential isomorphism while matching the repository phrase "have the same homology groups."

## Explicit exclusions

- Homotopy invariance of homotopy groups, cohomology, K-theory, or an arbitrary functor.
- The stronger claim that homotopy equivalent spaces are homeomorphic.
- Equality of homology types or cardinalities in place of a structured group/module isomorphism.
- Merely proving that homotopic maps induce equal maps without composing this fact into the
  homotopy-equivalence result.
- Assuming the desired homology isomorphism as a structure field or axiom.

No proof architecture or obligation denominator is frozen in this intake; that belongs to the
dependency-ordered obligation-tree phase after exact statement and anchor audit.
