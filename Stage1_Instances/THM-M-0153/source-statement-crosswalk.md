# Source-statement crosswalk

## Repository record

`Docs/researches/math_theorems.md` names Shiing-Shen Chern, gives the year 1944, and summarizes the
claim as a relation between the total curvature of a higher-dimensional manifold and a
characteristic number. The target manifest classifies it under differential geometry and carries
the untrusted label `已验证`. That short wording identifies the theorem family but does not specify
the domain, formula, normalization, or formal artifact.

## Candidate primary sources

- Shiing-Shen Chern, "A Simple Intrinsic Proof of the Gauss-Bonnet Formula for Closed Riemannian
  Manifolds," *Annals of Mathematics*, Second Series 45(4), 1944, pages 747-752.
- Shiing-Shen Chern, "On the Curvatura Integra in a Riemannian Manifold," *Annals of Mathematics*,
  Second Series 46(4), 1945, pages 674-684.

These are bibliographic discovery anchors, not immutable source receipts. This intake did not
inspect a stable scan or complete an errata search, so it assigns `H1`, not `H0`. The source-audit
phase must pin the source bytes, displayed formula and page, map every convention and assumption,
and obtain independent review.

## Component crosswalk

| Repository/source phrase | Frozen intended component | Required Lean component | Intake assessment |
|---|---|---|---|
| higher-dimensional manifold | smooth compact oriented boundaryless Riemannian `M`, `dim M = 2n` | concrete manifold, metric, compactness, orientation, boundary, and dimension binders | intended scope fixed; exact API open |
| total curvature | integral of the normalized Pfaffian Euler form | Levi-Civita connection, curvature two-form, invariant Pfaffian, top-form integration | interpretation matches the classical theorem; conventions open |
| characteristic number | Euler characteristic `chi(M)` | concrete topological Euler-characteristic definition | intended invariant fixed; representation open |
| relation | equality of the integral and `chi(M)` | typed equality after explicit scalar coercions | exact codomain and coercions open |
| Chern, 1944 | 1944 intrinsic closed-manifold formula | source provenance record | candidate primary paper identified; pinpoint review open |

The two-dimensional theorem and the cohomological Euler-class evaluation are useful alternate
surfaces only. Neither may replace the higher-dimensional curvature formula without checked
specialization or Chern-Weil transports.

## Lean and duplicate-target boundary

A narrow repository and pinned-mathlib text search found no declaration named for Gauss-Bonnet or
Chern-Gauss-Bonnet and no end-to-end target-specific module for `THM-M-0153`. This negative result
is intake discovery, not an exhaustive anchor audit. The catalog also contains `THM-M-0569`, a
separate ID with nearly identical mathematical naming. Its dossier can inform later discovery, but
rev-5.6 forbids transferring its scope decisions, state, or proof credit to this target.

The statement phase must independently elaborate this target with pinned concrete interfaces and
mutation-test its hypotheses, domain, binder scope, and boundary cases.
