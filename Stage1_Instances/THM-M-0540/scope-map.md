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

## Statement decisions

The canonical target uses integral coefficients (`ModuleCat.of ℤ ℤ`), ordinary unreduced homology,
mathlib's singular-set model, small spaces `X : Type`, and natural grading. It asserts the central
construction identity: singular homology is homology of the singular chain complex. This is the
narrow theorem-shaped reading of the source phrase, not a claim that every theorem about singular
homology has been formalized.

Degree zero and the empty space are included by a checked boundary fixture. Negative grading,
higher-universe spaces, reduced homology, and nonintegral coefficients are explicit exclusions.

## Explicit exclusions

- Homotopy invariance, excision, Mayer-Vietoris, the Eilenberg-Steenrod axioms, or a homology
  computation as a substitute for the construction itself.
- Simplicial, cellular, sheaf, de Rham, or reduced homology without a checked comparison map.
- A bare declaration named `SingularHomology` or a structure that assumes the desired construction.
- Treating the existence of mathlib definitions, the Stage0 label `已验证`, or the intake API probe
  as proof of a not-yet-selected canonical proposition.

No obligation denominator or theorem tree is frozen at intake. Those belong to the ordered anchor
audit and obligation-tree phases after exact statement identity is established.
