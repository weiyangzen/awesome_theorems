# Source-statement crosswalk

## Repository source record

`Docs/Stage0_Blueprint.md` identifies `THM-M-0569` as the Chern-Gauss-Bonnet theorem and summarizes
its content as a curvature representation of the Euler characteristic. It names Shiing-Shen Chern
and the year 1944, but leaves precise definitions, assumptions, proof path, axioms, and formal
artifacts open. The manifest repeats the name and an untrusted source label of `已验证`; neither is
source-fidelity or machine-proof evidence.

## Candidate primary sources

- Shiing-Shen Chern, "A Simple Intrinsic Proof of the Gauss-Bonnet Formula for Closed Riemannian
  Manifolds," *Annals of Mathematics*, Second Series 45(4), 1944, pages 747-752. This is the
  historical primary paper matching the repository's attribution and year. Its exact displayed
  formula, orientation/dimension conventions, normalization, and any corrigenda have not yet been
  inspected in this run.
- Shiing-Shen Chern, "On the Curvatura Integra in a Riemannian Manifold," *Annals of Mathematics*,
  Second Series 46(4), 1945, pages 674-684. This is a related primary development and must not be
  conflated with the exact 1944 statement without source inspection.

These bibliographic records are discovery anchors only. They support `H1`, not `H0`. An independent
review must inspect a stable scan/edition, pinpoint the theorem/formula and pages, check errata, and
approve the assumption and notation crosswalk.

## Crosswalk

| Repository/source phrase | Frozen mathematical component | Required Lean component | Intake status |
|---|---|---|---|
| "closed Riemannian manifolds" | compact and boundaryless smooth Riemannian `M` | concrete compact manifold-without-boundary hypotheses | included; exact API open |
| orientation and even dimension | oriented `M`, `dim M = 2n` | dimension witness and orientation structure | included; binder encoding open |
| curvature | curvature of the Levi-Civita connection | connection and curvature two-form | included; API open |
| Gauss-Bonnet integrand | normalized Pfaffian/Euler form | alternating-matrix Pfaffian and top differential form | included; sign and normalization open |
| integral over `M` | oriented integral of the Euler form | manifold integration with integrability/top-degree conditions | included; API open |
| Euler characteristic | topological `chi(M)` | a concrete homology/cohomology or finite-CW definition | included; representation open |
| equality | integral equals `chi(M)` | exact equality after scalar coercions | included; codomain open |

## Lean discovery boundary

A scoped repository and pinned-mathlib text search found no target-specific legacy Stage1 module and
no declaration text matching Chern-Gauss-Bonnet, Gauss-Bonnet, Euler-form curvature, or Pfaffian.
This is useful negative intake evidence only. The later anchor-audit phase must repeat a declared
symbol/module/API search at immutable revisions and record candidates, types, bodies, axioms, and
dependency feasibility. Absence of a text match does not establish absence of a formalization.

Before the statement gate can close, the selected primary formula must be mapped row by row to a
canonical Lean proposition, including normalization, scalar codomain, disconnected and
zero-dimensional cases, and every implicit smoothness/compactness/orientation assumption.
