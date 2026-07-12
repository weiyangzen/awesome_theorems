# Scope map

## Included mathematical claim

- `M` is a smooth finite-dimensional Riemannian manifold with a chosen orientation.
- `M` is compact, has no boundary, and has even dimension `2n`.
- The metric determines the Levi-Civita connection and its curvature two-form.
- The convention-normalized Pfaffian of that curvature defines the Euler form.
- The oriented integral of the Euler form over `M` equals the topological Euler characteristic
  `chi(M)`.

This is a human-scope freeze, not a frozen Lean proposition. The statement phase must select exact
definitions and binders, inspect the primary formula, and record the normalization and sign
conventions before expression fingerprinting.

## Boundary decisions

- Disconnected compact manifolds are intended to be included because both sides should be additive,
  but this must be checked against the selected source and formal interfaces.
- The zero-dimensional closed case is intended to be included and requires an explicit convention
  test for the Pfaffian of a rank-zero bundle.
- Odd-dimensional manifolds are outside the canonical domain; their Euler-characteristic vanishing
  is a related result rather than this curvature formula.
- Manifolds with boundary are excluded because the corresponding theorem needs boundary correction
  terms.

## Explicit non-substitutions

- the surface Gauss-Bonnet theorem alone;
- a caller-supplied curvature integral or Euler characteristic with the desired equality assumed;
- an Euler-class pairing without a checked differential-geometric representative bridge;
- a local density identity, an index-theorem slogan, or a finite triangulation formula without
  checked composition to the canonical equality;
- noncompact, singular, or orbifold variants.

## Anticipated formal architecture

The later obligation registry is expected to separate the Riemannian and orientation context,
Levi-Civita curvature construction, invariant Pfaffian polynomial and normalization, global Euler
form, oriented integration, Euler-class identification, evaluation on the fundamental class, and
identification with Euler characteristic. This list is planning scope only and carries no proof or
coverage credit.
