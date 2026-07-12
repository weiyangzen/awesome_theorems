# Source-statement crosswalk

The Stage0 label `雅可比场理论` names a family of results. Its accompanying phrase
`测地线变分的二阶导数` most directly selects the forward geodesic-variation theorem below. The
citations are discovery anchors, not immutable evidence receipts and not `H0` evidence.

| Claim component | Human source anchor | Planned Lean surface | Intake assessment |
|---|---|---|---|
| Variation fields of geodesic variations satisfy the Jacobi equation | M. do Carmo, *Riemannian Geometry*, Birkhauser, 1992, chapter 5 (Jacobi fields) | a two-parameter manifold map, its `s`-variation field, covariant derivatives along `t`, and curvature | Standard proof source located; exact proposition/page, edition hash, assumptions, and errata remain to be audited |
| Definition of a Jacobi field along a geodesic | J. M. Lee, *Introduction to Riemannian Manifolds*, 2nd ed., Springer, 2018, chapter 10 (Jacobi fields) | predicate asserting the selected signed Jacobi ODE along `gamma` | Secondary textbook anchor; the curvature convention must be mapped before statement freezing |
| Curvature commutator for a two-parameter variation | same textbook treatments, using the Levi-Civita connection | a checked identity commuting covariant derivatives in the `s` and `t` directions | Required proof bridge; no exact mathlib declaration or local proof is credited at intake |
| Geodesic hypothesis | every longitudinal curve `t |-> F(s,t)` has zero covariant acceleration | a geodesic/autoparallel predicate for each `s` | The universal-in-`s` hypothesis is essential; merely assuming the central curve is geodesic weakens the input and does not yield this root |
| Resulting equation | `D_t^2 J + R(J, gamma') gamma' = 0`, modulo the frozen curvature convention | equality in the tangent space over `gamma(t)` for every parameter `t` | Exact binder order, dependent vector-field representation, and sign transport remain open |
| Converse realization | a Jacobi field is locally induced by a variation through geodesics | separate future declaration | A classical companion theorem, explicitly excluded from the canonical root |
| Second variation and conjugate-point applications | index form, endpoint conditions, conjugate points, and Morse index results | separate downstream theorem families | Not equivalent to the forward Jacobi equation and excluded from root credit |

The forward implication needs enough joint smoothness to form and commute the relevant covariant
derivatives. The exact differentiability order is deliberately not invented at intake: the
statement phase must reconcile a pinpoint source theorem with the actual pinned Lean API. It must
also state the curvature convention explicitly, because common references place the terms or
curvature arguments differently while expressing the same geometric equation.

Required follow-up: inspect and hash a specific source edition; record exact theorem/page and any
errata; crosswalk every regularity and domain assumption; search the pinned mathlib sources for
geodesic, curvature, and covariant-derivative support; then elaborate and mutation-test one exact
Lean proposition. No source label `已验证`, citation, adjacent connection API, or prose equation is
credited as machine closure.
