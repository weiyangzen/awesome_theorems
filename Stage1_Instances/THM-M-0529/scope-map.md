# Scope map

## Included claim family

- A topological space `X` and a degree `n`, with the eventual statement fixing all universe and
  category parameters.
- A concrete homology theory and coefficient object selected from the primary source; singular
  homology is the default candidate, not yet an accepted choice.
- Covariant functoriality: a continuous map induces a map on homology.
- Topological invariance in the precise minimal sense that a homeomorphism `X ≅ Y` induces an
  isomorphism between the degree-`n` homology objects, with inverse induced by the inverse
  homeomorphism.

## Decisions deferred to statement freeze

The source phrase does not specify singular, simplicial, cellular, Cech, or another homology theory;
integral or general coefficients; reduced or unreduced homology; absolute or relative groups; the
range of degrees; or whether "invariant" means equality, group isomorphism, a natural isomorphism,
or only equality of numerical invariants. The statement phase must choose an immutable primary
source and map every one of those decisions to ordered Lean binders, hypotheses, and a conclusion.
It must also define behavior for the empty space, degree zero, and coefficient degeneracies rather
than silently excluding them.

## Explicit exclusions

- The construction or computation of a particular space's homology as a substitute for invariance.
- Homotopy invariance, which is stronger and is separately represented by `THM-M-0535`.
- Cohomology, relative homology, excision, Kunneth, or universal-coefficient theorems.
- Equality of Betti numbers alone in place of an isomorphism of homology objects.
- An abstract structure that assumes the desired induced isomorphism as a field.
- The manifest's historical date, attribution, or `已验证` label as proof evidence.

No Lean declaration is canonical at intake. A later target must use concrete homology objects and
the map induced by the selected homeomorphism; it may not encode the conclusion as an assumption.
