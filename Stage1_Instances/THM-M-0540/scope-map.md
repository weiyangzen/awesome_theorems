# Scope map

## Included claim

- Ordinary, unreduced singular homology of a topological space `X`.
- Singular `q`-simplices as continuous maps from the standard topological `q`-simplex to `X`.
- Chains with fixed coefficients, with boundary given by the alternating sum of face restrictions.
- The chain-complex identity and degree-`n` homology as cycles modulo boundaries.
- Functoriality for continuous maps, including the induced morphism on degree-`n` homology.

This is a construction-level target because the repository phrase "the singular homology of a
topological space" does not state a numerical calculation, invariance theorem, or comparison
theorem. The statement phase must turn this scope into one exact theorem-shaped Lean proposition,
rather than silently replacing it by a nearby theorem.

## Decisions reserved for the statement phase

The exact source formulation must decide integral coefficients versus a general coefficient ring
or an object in a suitable preadditive category; reduced versus unreduced conventions; the precise
standard-simplex model; universes; grading; and whether the canonical target asserts construction,
the boundary-square-zero law, a natural isomorphism, or the complete functor package. Binder order,
typeclasses, foundation profile, and degenerate cases must then be frozen and mutation-tested.

Degree zero and the empty space must be addressed explicitly. Negative grading is outside
mathlib's current `n : Nat` singular-homology API unless the chosen source target requires an
extension. A general coefficient-category target may not be substituted for a source claim whose
assumptions support only ordinary integral homology.

## Explicit exclusions

- Homotopy invariance, excision, Mayer-Vietoris, the Eilenberg-Steenrod axioms, or a homology
  computation as a substitute for the construction itself.
- Simplicial, cellular, sheaf, de Rham, or reduced homology without a checked comparison map.
- A bare declaration named `SingularHomology` or a structure that assumes the desired construction.
- Treating the existence of mathlib definitions, the Stage0 label `已验证`, or the intake API probe
  as proof of a not-yet-selected canonical proposition.

No obligation denominator or theorem tree is frozen at intake. Those belong to the ordered anchor
audit and obligation-tree phases after exact statement identity is established.
