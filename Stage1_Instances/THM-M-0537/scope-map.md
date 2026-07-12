# Scope map

## Included mathematical subject

- The classical ordinary-homology axiomatic framework associated with Eilenberg and Steenrod.
- A category of topological pairs and maps of pairs.
- Graded homology objects, induced morphisms, and connecting morphisms for pairs.
- Homotopy invariance, exactness of a pair, excision, and the dimension axiom.
- Additivity only if the selected source/version includes it in the credited axiom package.

This identifies the subject without pretending that an axiom system is already a theorem. A Lean
structure can encode the package but proves only that the definition is well formed. A model
theorem for singular homology would assert that concrete data satisfies every field; a uniqueness
theorem would be a different and stronger root.

## Decisions required by the statement phase

The next phase must select the root kind and preserve that choice in both human and formal forms.
It must also fix reduced versus unreduced homology, integer or general coefficients, nonnegative or
integer grading, all pairs versus an admissible category, the exact form of excision, the point
normalization, additivity, naturality laws, binder order, universes, and equality versus natural
isomorphism. Empty spaces, point spaces, empty subspaces, and negative degrees must be explicit.

## Explicit exclusions

- The bare existence of a structure whose fields assume all axioms.
- Any one axiom, such as homotopy invariance or exactness, substituted for the full package.
- Homological-complex axioms alone, without the topological-pair functor and source crosswalk.
- A generalized homology theory obtained merely by dropping the dimension axiom.
- The uniqueness theorem for homology theories on CW complexes unless chosen and sourced as the
  canonical root.
- `THM-M-0538` or its future artifacts as proof credit; the adjacent metadata label is a separate
  target and the overlap must be resolved, not silently shared.

## Initial formal boundary

The repository has a pinned Lean 4/mathlib environment but no target-specific legacy module for
rank 594. Existing mathlib homological-algebra and singular-homology APIs are discovery substrate,
not evidence that the full Eilenberg-Steenrod package is encoded or satisfied. The statement and
anchor-audit phases must establish that boundary at the pinned revision.
