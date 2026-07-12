# Scope map

## Included claim

- A locally convex topological real vector space `E`.
- A nonempty compact convex subset `K : Set E`.
- A continuous map `f : E -> E` that maps `K` into itself, or equivalently a continuous
  endomorphism of the subtype `K`; the statement phase must select one encoding.
- Existence of `x` in `K` with `f x = x`.

## Decisions reserved for the statement phase

The selected source text must determine whether the ambient space is required to be Hausdorff or
otherwise separated, whether local convexity is formulated over `R` or a more general topological
field, and whether compactness belongs to the subset or to a standalone convex space. It must also
fix binder order, typeclass assumptions, and the exact treatment of an empty set. These choices
cannot be inferred from the repository's one-line description.

The anticipated Lean vocabulary at pinned mathlib revision
`8a178386ffc0f5fef0b77738bb5449d50efeea95` includes `LocallyConvexSpace`, `Convex`, `IsCompact`,
`Continuous`, `Set.MapsTo`, and `Function.IsFixedPt`. API availability does not establish that the combined
theorem is present or provable from the eventual assumptions.

## Explicit exclusions

- Tychonoff's product theorem for compact spaces (`THM-M-0620`).
- Schauder, Brouwer, Kakutani, Markov-Kakutani, or Banach fixed-point theorems as substitutes.
- A finite-dimensional, normed-space, contraction, affine-map, or set-valued-map specialization.
- A statement that assumes a fixed point or packages it as structure data.
- Mere existence of an `x : E` with `f x = x` without also establishing `x in K`.

## Boundary cases and mutations to test later

- Remove nonemptiness: the empty compact convex set refutes the conclusion.
- Remove `MapsTo f K K`: a translation of a compact interval need not have a fixed point in it.
- Change continuity or local convexity assumptions and verify that this is not silently accepted as
  the canonical target.
- Compare the ambient-map and subtype-self-map encodings with a checked transport.
