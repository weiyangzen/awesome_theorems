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

## Statement-phase decisions

The exact source must fix whether "homology" means unreduced singular homology, reduced homology,
or a stated general homology theory; the coefficient ring/module; natural-number or integer grading;
and the category in which the group/module isomorphism lives. It must also settle universe and
topological-space binders, whether the result quantifies over a packaged `HomotopyEquiv`, and how
degree-zero, empty-space, and negative-degree cases are represented.

The preferred formal shape is a degreewise isomorphism induced by an actual homotopy equivalence,
not a bare existential isomorphism. Binder order, imports, and the precise expression remain open
until these decisions are source-checked and elaborated.

## Explicit exclusions

- Homotopy invariance of homotopy groups, cohomology, K-theory, or an arbitrary functor.
- The stronger claim that homotopy equivalent spaces are homeomorphic.
- Equality of homology types or cardinalities in place of a structured group/module isomorphism.
- Merely proving that homotopic maps induce equal maps without composing this fact into the
  homotopy-equivalence result.
- Assuming the desired homology isomorphism as a structure field or axiom.

No proof architecture or obligation denominator is frozen in this intake; that belongs to the
dependency-ordered obligation-tree phase after exact statement and anchor audit.
