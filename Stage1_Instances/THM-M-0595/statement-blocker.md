# Exact-statement gate: blocked

Item: `S56-M-0595-STATEMENT`

## Decision

The exact Lean 4 target cannot be truthfully elaborated from the repository source record. Its
complete mathematical wording is `连续函数可用光滑函数逼近` ("continuous functions can be
approximated by smooth functions"). As already frozen by the accepted predecessor intake, this
does not determine one proposition. It leaves open:

- the source space (Euclidean space, an open subset, or a smooth manifold, with which compactness,
  boundary, countability, and model-space hypotheses);
- the target (real numbers, a normed vector space, or another smooth manifold);
- the differentiability order;
- the approximation relation (one uniform constant, a point-dependent positive tolerance,
  compact-open density, or strong/Whitney topology);
- whether equality near/on a closed set, support preservation, or a homotopy is part of the result.

These alternatives are not definitionally or logically interchangeable without additional
hypotheses and checked transports. Selecting any one as the root solely because it is convenient
in pinned mathlib would broaden or narrow the underspecified source claim. That is forbidden by
sections 0.1 and 5 of the rev-5.6 standard.

## Pinned Lean boundary checked

`StatementProbe.lean` imports only `Mathlib.Geometry.Manifold.SmoothApprox` and checks the two
closest pinned declarations:

- `Continuous.exists_contMDiff_approx`, for maps from a real sigma-compact finite-dimensional
  manifold to a real normed space, with a continuous pointwise-positive tolerance and support
  containment; and
- `Continuous.exists_contDiff_approx`, its finite-dimensional normed-space specialization.

Both declarations elaborate in the existing pinned environment. Their presence proves only that
two candidate formulations are available. It does not decide that either is the source's exact
claim, and neither receives canonical-statement or proof credit in this phase. The mathlib module
itself also distinguishes stronger relative/equality-on-set variants, confirming that the omitted
choices change the literal target.

## Gate result and retry condition

First failed gate: section 5 exact-statement identity. Consequently there is no canonical Lean
expression to serialize, no honest expression fingerprint, and no meaningful removed-hypothesis,
changed-domain, binder-scope, or boundary mutation suite. Machine status remains `M4`, and no
`.stage1-worker-selftest.json` is emitted.

Retry after an authoritative source decision pins a numbered theorem and immutable edition (or an
explicit repository-level scope decision), including every domain and codomain assumption,
ordered quantifier, differentiability order, approximation topology/tolerance, relative/support
condition, and boundary convention. The statement phase can then encode that proposition, check
all credited transports and four required mutation classes, and serialize its elaborated kernel
expression.

