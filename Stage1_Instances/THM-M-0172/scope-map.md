# Scope map

## Included claim

- A smooth compact Riemannian manifold `M` of finite even dimension `2n`.
- A chosen orientation and no boundary.
- The Levi-Civita connection and its curvature two-form.
- The Euler form defined by the source-convention-normalized Pfaffian of that curvature.
- Equality of the oriented integral of this top-degree form with the topological Euler
  characteristic `chi(M)`.

This is the classical global Chern-Gauss-Bonnet formula intended by the repository phrase "an
intrinsic representation of the Euler characteristic." The statement phase must freeze the source
formula, binder order, universes, smoothness class, scalar codomain, orientation convention,
curvature sign, Pfaffian convention, and powers of `2*pi` in an exact Lean expression.

## Boundary decisions

- Dimension zero is included in intent. The statement gate must explicitly test its Pfaffian and
  orientation conventions.
- Disconnected compact manifolds are intended to be included if the selected source theorem and
  formal interfaces make both sides componentwise additive. Otherwise connectedness must be an
  explicit source-justified hypothesis.
- Odd dimension is outside the binder domain. Vanishing of Euler characteristic in the oriented
  closed odd-dimensional case is a related corollary, not this theorem.
- Manifolds with boundary are excluded because they require a boundary correction term.

## Explicit exclusions

- The two-dimensional Gauss-Bonnet theorem alone.
- A local curvature-density identity without the global integral and Euler-characteristic bridge.
- An Euler-class/fundamental-class pairing statement without a checked bridge identifying that
  class with the normalized Pfaffian curvature form.
- Any statement taking the desired equality, Euler characteristic, curvature integral, or bridge
  theorem as a hypothesis or uninterpreted parameter.
- Noncompact, orbifold, singular-space, and boundary-correction variants.
- A theorem about a caller-supplied finite complex that is not checked to compute the manifold's
  Euler characteristic.

## Formal surface still to freeze

Concrete Lean interfaces are required for the oriented Riemannian manifold, Levi-Civita curvature,
Pfaffian/Euler form, integration of top forms, topological Euler characteristic, and their
analytic-topological bridge. At intake none is replaced by a broadened or abstract substitute.
Exact Lean elaboration belongs to the dependent statement phase and remains open.
