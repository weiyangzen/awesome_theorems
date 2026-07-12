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

## Statement freeze decisions

The canonical target selects ordinary, unreduced, absolute singular homology with integral
coefficients, degrees `n : ℕ`, and invariance as invertibility of the functorial induced morphism in
`AddCommGrpCat`. Its ordered binders are `n`, `X`, `Y`, then the homeomorphism `e`. It makes no
connectedness, nonemptiness, or positive-degree assumption. The primary-source pinpoint and its
historical-to-modern crosswalk remain an anchor-audit responsibility and receive no H credit here.

## Explicit exclusions

- The construction or computation of a particular space's homology as a substitute for invariance.
- Homotopy invariance, which is stronger and is separately represented by `THM-M-0535`.
- Cohomology, relative homology, excision, Kunneth, or universal-coefficient theorems.
- Equality of Betti numbers alone in place of an isomorphism of homology objects.
- An abstract structure that assumes the desired induced isomorphism as a field.
- The manifest's historical date, attribution, or `已验证` label as proof evidence.

The canonical Lean declaration is `AwesomeTheorems.THM_M_0529.CanonicalTarget` in `Statement.lean`.
It uses concrete homology objects and the map induced by the selected homeomorphism; the conclusion
is not encoded as an assumption.
