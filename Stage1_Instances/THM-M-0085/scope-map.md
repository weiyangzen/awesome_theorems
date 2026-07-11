# Scope map

## Included claim

- Categories `C` and `D`, functors `F : C ⥤ D` and `G : D ⥤ C`, and an adjunction `F ⊣ G`.
- The monad `G F` induced on `C` and the comparison functor from `D` to its Eilenberg-Moore category.
- A standard Beck hypothesis expressed using `G`-split parallel pairs and their coequalizers.
- The conclusion that the comparison functor is an equivalence, equivalently that `G` is monadic.

## Decisions deferred to statement phase

The selected primary theorem must determine whether the exact criterion uses creation of
coequalizers, or existence plus preservation and reflection, and whether reflection of
isomorphisms is separate. Universe levels, local smallness, the direction of composition, and the
precise definition of a `G`-split pair must be frozen against that source and mathlib's encoding.

## Explicit exclusions

- Comonadicity, despite its dual relationship.
- Merely asserting that an adjunction induces a monad.
- Replacing the comparison equivalence by full faithfulness or essential surjectivity alone.
- Treating one sufficient variant as though it represented every theorem called "Beck's theorem".
- Crediting the legacy wrappers before exact-statement, provenance, trust, and replay gates.

Degenerate categories and identity adjunctions remain included unless the selected source excludes
them. No finiteness, abelian, exactness, spectral-sequence, or homological hypothesis is intended.
