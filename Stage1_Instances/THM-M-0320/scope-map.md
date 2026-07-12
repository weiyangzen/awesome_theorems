# Scope map

## Included theorem family

- A nonempty compact convex domain `K` in a finite-dimensional real vector space (equivalently,
  after a checked transport, the source's closed bounded convex Euclidean domain).
- A correspondence `F : K -> Set K`, so every value lies in the domain.
- Every `F x` is nonempty and convex, with the source-required closedness or compactness.
- `F` is upper hemicontinuous on `K`, in the precise sense selected from the primary source.
- The conclusion is `Exists x : K, x in F x`.

## Decisions required at statement freeze

The statement phase must inspect and select the exact primary statement and freeze: Euclidean
space versus an abstract finite-dimensional real topological vector space; whether the domain is
given as compact or as closed and bounded; whether values are closed or compact; the definition of
upper semicontinuity used by Kakutani and the hypotheses needed to identify it with mathlib's
`UpperHemicontinuousOn`; the subtype versus ambient-set encoding; and the order of all binders and
typeclass assumptions. It must explicitly handle empty domains, empty values, zero-dimensional
spaces, singleton domains, boundary points, and values that escape `K`.

Common graph-closed formulations may be equivalent only under compactness/Hausdorff hypotheses.
They require checked transports and may not silently replace upper hemicontinuity.

## Explicit exclusions

- Brouwer's single-valued fixed-point theorem, Schauder's theorem, or Markov-Kakutani's theorem for
  commuting affine maps as the root result.
- Infinite-dimensional locally convex generalizations unless the selected source statement says so.
- Approximate fixed points, fixed points for one continuous selection, or a conclusion in the
  convex hull of `F x`.
- A structure or hypothesis that contains `x in F x`, a chosen fixed point, or the theorem itself.
- Riesz-Markov-Kakutani representation results, which share a name but are unrelated.
- Reusing the separately scheduled duplicate-title record `THM-M-0639` for proof or status credit.

No formal target is frozen at intake. A later target must expose domain compactness and convexity,
value containment/nonemptiness/convexity/closedness, hemicontinuity, and membership in the
conclusion as genuine propositions.
