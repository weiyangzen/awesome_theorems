# Scope map

## Included claim

- A smooth compact Riemannian manifold `M` of even dimension `2n`.
- A chosen orientation and no boundary.
- The Levi-Civita connection and its curvature two-form.
- The Euler form obtained from the appropriately normalized Pfaffian of that curvature.
- Equality of the integral of this top-degree form with the topological Euler characteristic
  `chi(M)`.

This freezes the classical closed, even-dimensional global formula as the intended human claim.
The statement phase must freeze all binder order, universe, smoothness, connectedness, integration,
orientation, Pfaffian, curvature-sign, and `(2 pi)` normalization conventions in an exact Lean
expression. It must also decide how Euler characteristic is represented and prove checked
transports for any credited cohomological or characteristic-class encoding.

## Boundary decisions

- Disconnected compact manifolds are intended to be allowed if the chosen primary theorem and Lean
  interfaces make both sides additive componentwise; otherwise this must become an explicit
  hypothesis, not an implicit simplification.
- The zero-dimensional case is included in intent, but must receive an explicit mutation/boundary
  test because conventions for the Pfaffian of a zero-rank bundle matter.
- Odd-dimensional manifolds are outside the canonical binder domain. Their vanishing Euler
  characteristic is a related corollary, not a replacement for the curvature formula.
- Manifolds with boundary are excluded. Gauss-Bonnet-Chern boundary correction terms require a
  separate target or a checked strengthening with the closed case transported back.

## Explicit exclusions

- The two-dimensional Gauss-Bonnet formula alone.
- A statement merely asserting that the Euler class pairs with the fundamental class to give the
  Euler characteristic, unless a checked bridge identifies that Euler class with the normalized
  Pfaffian curvature form.
- A theorem for a tangent bundle with Euler characteristic supplied as an assumption or structure
  field.
- A local density identity, an index-theorem specialization, or a finite triangulation formula
  without checked composition to the canonical global equality.
- Noncompact variants, orbifolds, singular spaces, and boundary formulas.

## Expected formal surface

The exact target is currently blocked on concrete Lean interfaces for smooth oriented Riemannian
manifolds, Levi-Civita curvature, alternating forms/Pfaffians, integration of top forms, Euler
characteristic, and the analytic-topological bridge. No abstract substitute may be introduced to
make elaboration artificially easy.
