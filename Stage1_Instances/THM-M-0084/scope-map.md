# Scope map

## Included subject

- A small indexing category `J`, a category `C`, and a diagram `F : J ⟶ C`.
- Cones and cocones over `F`, with limit and colimit understood through their universal properties.
- An existence conclusion only after the source supplies an explicit hypothesis such as
  `HasLimit F`, `HasLimitsOfShape J C`, completeness/cocompleteness, or a concrete construction.
- The duality between a limit statement in `C` and a colimit statement in `Cᵒᵖ`, if it is part
  of the selected source theorem.

## Statement-phase decisions

The primary-source audit must identify whether the intended result is a definition/uniqueness
theorem, a completeness criterion, a shape-specific construction (products, equalizers, pullbacks,
and their duals), or a preservation/creation theorem. It must then freeze universes, size
conditions, binder order, the exact category hypotheses, and whether the conclusion is existence,
an `IsLimit`/`IsColimit` witness, or uniqueness up to unique isomorphism.

## Explicit exclusions

- Unconditional existence of every limit or colimit in an arbitrary category.
- Replacing the target with the tautology that a limit exists under `HasLimit F` without source
  evidence that this is the intended formulation.
- A theorem about limits of sequences in analysis or topology.
- Adjunction, exactness, derived-category, spectral-sequence, or long-exact-sequence results merely
  suggested by the generic legacy profile.
- Treating mathlib typeclasses or a chosen `limit F` object as proof that the intended source theorem
  has been identified.
