# Source-statement crosswalk

## Candidate primary sources

- William P. Thurston, "Three-dimensional manifolds, Kleinian groups and hyperbolic geometry",
  *Bulletin of the American Mathematical Society* 6 (1982), 357-381. This is the primary
  conjecture-era formulation candidate. The exact numbered statement, wording, page, conventions,
  and any corrections must be checked against an immutable scan before H0.
- Grigori Perelman, "The entropy formula for the Ricci flow and its geometric applications",
  arXiv:`math/0211159` (2002); "Ricci flow with surgery on three-manifolds",
  arXiv:`math/0303109` (2003); and "Finite extinction time for the solutions to the Ricci flow on
  certain three-manifolds", arXiv:`math/0307245` (2003). These are primary proof-series anchors,
  not one declaration-shaped statement identical to the root.

These citations establish discovery provenance only. Immutable versions, exact theorem/section
anchors, correction history, assumptions, and an independently reviewed source-to-node proof
crosswalk remain open.

## Crosswalk

| Root component | Human mathematical role | Required Lean surface | Intake status |
|---|---|---|---|
| closed connected orientable `3`-manifold | domain of the frozen claim | concrete topological/smooth manifold, compactness, no-boundary, connectedness, orientation | included; encoding open |
| prime decomposition | separates connected sums along essential spheres | embedded spheres, cutting/gluing, prime components, existence and uniqueness bridge | included; APIs and conventions open |
| JSJ/torus decomposition | canonical splitting of irreducible pieces | incompressible embedded tori, characteristic family, isotopy/canonicity | included; exact source relationship open |
| eight model geometries | exhaustive locally homogeneous models | explicit geometry index and model-space structures | included; formal definitions open |
| geometric pieces | terminal geometrization conclusion | complete locally homogeneous quotient/metric structure on each piece | included; volume and boundary conventions open |
| Perelman proof series | analytic route closing the conjecture | Ricci flow, noncollapsing, canonical neighborhoods, surgery, long-time analysis, topology bridge | architecture only; no machine credit |
| Poincare conjecture | spherical simply connected consequence | checked specialization and homeomorphism with `S^3` | excluded as substitute root |

## Repository Lean boundary

`Formalizations/Lean/AwesomeTheorems/Stage1/S1_M_128.lean` is a relevant legacy discovery file.
It imports mathlib's Poincare-conjecture statement surface, but its geometrization half is an
abstract `GeometrizationPackage`; `GeometrizationStatementShape` asks only for nonemptiness of that
assumption-bearing package. Consequently it is neither an exact encoding nor a proof candidate for
this target. Its dated anchor list must be repeated against the pinned environment during the
anchor-audit phase.

Before H0, a reviewer must pin the conjecture formulation and proof-series versions, identify
pinpoint locations and corrections, reconcile the decomposition and geometric-structure
conventions, and approve a row-by-row mapping from every root hypothesis and conclusion to the
eventual Lean expression and obligation registry.
