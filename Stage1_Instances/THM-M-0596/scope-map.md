# Scope map

## Included claim

- Smooth manifolds `M` and `N`, with their category, dimensions, countability assumptions, and
  possible boundaries fixed from the selected theorem rather than inferred.
- A smooth embedded submanifold `S` of `N`.
- Smooth maps `f : M -> N` satisfying pointwise transversality: whenever `f(x)` lies in `S`, the
  image of `d f_x` together with `T_(f x) S` spans `T_(f x) N`.
- A genericity conclusion for such maps in an explicitly named topology on `C^infty(M, N)`.
- Residuality, density, openness, approximation, and relative control only to the extent actually
  supplied by the selected source theorem and its hypotheses.

## Decisions reserved for the statement phase

The source phrase "transverse maps are generic" does not uniquely determine a proposition. A
primary-source inspection must select ordinary versus parametric transversality, differentiability
class (`C^r` or smooth), weak versus strong Whitney topology, and the meaning of generic. It must
also settle compactness or closedness assumptions, manifolds with boundary or corners, whether
`S` is closed or properly embedded, and relative constraints on a closed subset. These choices
control whether the result is merely residual/dense or also open.

The formal statement must freeze universes, binder order, the tangent-map transversality predicate,
the mapping-space topology, and all typeclass assumptions. Empty manifolds, empty `S`, zero
dimensions, `S = N`, maps avoiding `S`, and boundary points require explicit treatment rather than
being discarded as informal edge cases.

## Explicit exclusions

- Sard's theorem, the regular value theorem, or a preimage-submanifold theorem alone.
- Only the existence of one transverse perturbation when the selected root asserts residuality.
- Jet or multijet transversality substituted for ordinary transversality without a checked bridge.
- A finite-dimensional parameter-family theorem presented as the full mapping-space theorem.
- Openness without the additional topology, compactness, and closed-submanifold hypotheses it may
  require.
- An abstract structure that assumes transversality or genericity as a field.

The future Lean encoding must expose concrete smooth-manifold, tangent-map, submanifold, and
mapping-space-topology interfaces, or record a precise missing-API blocker.
