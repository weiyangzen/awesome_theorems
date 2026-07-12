# Source-statement crosswalk

## Source ledger

| Source | Locator | Role and intake status |
|---|---|---|
| Repository mathematics inventory | `Docs/researches/math_theorems.md`, lines 1182-1187: "geodesic equation" / "differential equation of shortest curves on a surface" | Authoritative repository discovery wording, but not a mathematical proof source and its `verified` label is untrusted |
| M. P. do Carmo, *Riemannian Geometry*, Birkhauser, 1992 | Chapter 3, section 2, "Geodesics; Convex Neighborhoods" | Credible source candidate for the covariant geodesic equation and local minimizing behavior; exact edition/page/theorem pin and errata audit remain open |
| J. M. Lee, *Riemannian Manifolds: An Introduction to Curvature*, 2nd ed., Springer GTM 176, 2006 | Chapter 4, "Geodesics" | Independent modern source candidate for intrinsic, coordinate, existence, and local-minimization formulations; exact theorem/page crosswalk remains open |
| Pinned mathlib source tree at revision `8a178386ffc0f5fef0b77738bb5449d50efeea95` | `Mathlib/Geometry/Manifold/VectorBundle/CovariantDerivative/Basic.lean` | Repo-local discovery shows a bundled `CovariantDerivative` substrate, not an exact geodesic-equation theorem and not machine closure |

No source above is accepted as `H0`. In particular, textbook chapter locators do not replace a
pinpoint theorem/page transcription, source-file digest, errata search, premise mapping, and
independent review.

## Claim crosswalk

| Claim component | Human-source candidate | Lean candidate boundary | Intake assessment |
|---|---|---|---|
| Riemannian metric determines the Levi-Civita connection used by the equation | do Carmo, Chapters 2-3; Lee, connection material preceding Chapter 4 | mathlib has Riemannian-bundle and covariant-derivative infrastructure | Required hypothesis and construction; existence/uniqueness is not credited here |
| Intrinsic equation `nabla_(gamma') gamma' = 0` | do Carmo Chapter 3 section 2; Lee Chapter 4 | No exact repo-local declaration identified during intake | Canonical invariant form; formal representation deferred |
| Coordinate equation with Christoffel symbols | Same source sections | Needs chart derivatives, Christoffel coefficients, finite coordinate sums, and a checked chart transport | Canonical coordinate form; no elaboration or equivalence witness yet |
| Locally minimizing regular curves satisfy the equation | Geodesic variational and local-minimization results in the cited chapters | Needs length/energy variation, fixed endpoints, regularity, and constant-speed reparametrization | Included only with these hypotheses; unrestricted "shortest iff geodesic" is rejected |
| Short geodesic segments locally minimize | Convex-normal-neighborhood results in the cited chapters | Requires exponential-map/normal-neighborhood infrastructure | Contextual converse boundary, not a global-minimum claim |

## Convention and exclusion ledger

- The affine equation is parametrization-sensitive. Constant-speed/affine parametrization is part
  of the intended claim; an arbitrary reparametrization can add a tangential acceleration term.
- The equation is chart-local but intrinsic. A whole curve need not lie in one chart, and changing
  charts must preserve the vanishing covariant-acceleration proposition.
- Constant curves solve the intrinsic equation but are not regular length-minimizing curves. The
  regular-minimizer implication and the general geodesic predicate must therefore remain distinct.
- Local and global minimization are not interchangeable. The dossier excludes an unrestricted
  claim that all geodesics are globally shortest.
- The target is Riemannian. The Lorentzian free-particle reading and proper-time notation belong to
  the separate physics inventory item `THM-P-0639`.
- Sign and index placement for `Gamma^k_ij` must be frozen with the future Lean definition; no
  convention-dependent coordinate formula receives credit before that check.

The statement phase must pin exact source pages, settle the formal domain and smoothness level,
elaborate the target with minimal imports, check the intrinsic-coordinate bridge, and mutation-test
the connection, parametrization, chart scope, regularity, and local/global-minimum boundaries.
