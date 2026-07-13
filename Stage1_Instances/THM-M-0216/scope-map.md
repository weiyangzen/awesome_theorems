# Scope map

## Included subject boundary

- A source-selected Gauss-Bonnet theorem for two-dimensional surfaces. The catalog says
  "surface" and does not authorize the higher-dimensional Chern-Gauss-Bonnet theorem.
- The source-selected geometric domain: an abstract Riemannian two-manifold or an embedded regular
  surface, with its exact compactness, connectedness, orientability, and regularity assumptions.
- The source-selected global curvature expression, including Gaussian curvature and area measure,
  plus boundary geodesic curvature and corner-angle terms if the selected theorem has a boundary.
- The exact meaning of "total curvature": signed Gaussian-curvature integral, absolute total
  curvature, scalar-curvature normalization, or an extrinsic/Gauss-map quantity. The title makes
  the signed intrinsic version a strong search lead but the catalog does not source-select it.
- The source-selected topological invariant, normally an explicitly normalized Euler
  characteristic of the same surface.
- Every convention-dependent sign, orientation, normalization, coercion, and degenerate or
  disconnected case actually stated by the selected source.

These bullets delimit the recognizable theorem family. They are not an accepted canonical
statement.

## Decisions required at statement freeze

1. Pin and independently inspect an immutable primary or authoritative source with exact edition,
   definition, theorem, page, assumption, proof-boundary, correction, and errata locators.
2. Decide whether the domain is a compact oriented boundaryless Riemannian two-manifold, a smooth
   compact surface with boundary, a piecewise-smooth region with corners, or another exact class.
3. Decide whether "surface" is intrinsic or embedded, and freeze all smoothness, Hausdorff,
   second-countability, finite-dimensionality, compactness, connectedness, and orientation data.
4. Select the exact formula. The closed identity, the smooth-boundary identity, and the
   corner-corrected identity have different binders, terms, and proof obligations.
5. Freeze Gaussian-curvature sign, area form or measure, boundary orientation, signed geodesic
   curvature, turning/exterior-angle convention, scalar-versus-Gaussian curvature convention, and
   the normalization of `2 * pi`.
6. Select a topological Euler-characteristic definition and prove any bridge from a triangulation,
   homology, cohomology, cell complex, or other representation to the same geometric surface.
7. Resolve disconnected surfaces, the empty and zero-dimensional cases if expressible, empty
   boundary, nonsmooth boundary points, nonorientable surfaces, singularities, and noncompact or
   finite-total-curvature variants.
8. Freeze ordered binders, universes, model-with-corners data, typeclass instances, coercions, all
   hypotheses, the exact conclusion, and every credited alternate encoding before proof search.
9. Reconcile separately cataloged Gauss/Chern-Gauss-Bonnet targets so no scope, state, or proof
   credit is transferred by title similarity.

## Explicit exclusions

- Replacing this surface theorem with higher-dimensional Chern-Gauss-Bonnet (`THM-M-0153`,
  `THM-M-0172`, or `THM-M-0569`).
- Substituting Gauss's Theorema Egregium (`THM-M-0152`), Bonnet-Myers, a local curvature identity,
  or a hyperbolic polygon area formula for the requested global surface theorem.
- Proving only the sphere, torus, constant-curvature, boundaryless, or triangulated special case
  before the root statement has selected that scope.
- Treating `HomologicalComplex.eulerChar` as the topological Euler characteristic of a manifold
  without a checked representation and invariance bridge.
- Storing or assuming the desired curvature integral, Euler characteristic, or final equality in a
  structure and then projecting it.
- Crediting a theorem name, uncited date or attribution, adjacent API elaboration, a bounded search,
  or the catalog label `已验证` as statement identity or proof evidence.

The manifest category "non-Euclidean geometry" is scheduling metadata. It does not restrict the
root to hyperbolic or constant-curvature surfaces; `THM-M-0220` separately owns the hyperbolic-area
formula, and no credit transfers from that special context.

## Formal boundary

No canonical Lean expression is frozen. At pinned mathlib revision
`8a178386ffc0f5fef0b77738bb5449d50efeea95`,
`Mathlib.Geometry.Manifold.Riemannian.Basic` supplies a real Riemannian-manifold context, while
`Mathlib.Algebra.Homology.EulerCharacteristic` supplies Euler characteristics for homological
complexes. A bounded exact-topic search found no Gauss-Bonnet declaration and no Gaussian or
geodesic curvature API composing these surfaces into the catalog claim. The generic homological
invariant is not definitionally a manifold's topological Euler characteristic. These are
feasibility surfaces only, not an anchor audit, global absence proof, target statement, transport,
or proof.
