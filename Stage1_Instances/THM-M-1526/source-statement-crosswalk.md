# Source-statement crosswalk

## Candidate primary sources

- P. A. M. Dirac, "The Quantum Theory of the Electron", *Proceedings of the Royal Society A* 117
  (1928), 610-624, DOI `10.1098/rspa.1928.0023`. This is the historical primary paper candidate;
  exact equation/page wording, conventions, and corrections have not yet been inspected.
- P. A. M. Dirac, *The Principles of Quantum Mechanics*, fourth edition, Oxford University Press
  (1958), relativistic-electron chapter. This is a primary-author exposition candidate; exact
  section/page and edition-specific conventions remain open.

These bibliographic anchors do not establish `H0`. The statement phase must inspect a stable copy,
choose the actual theorem-sized claim, and record equations, assumptions, and errata.

## Crosswalk

| Repository/source phrase | Intended component | Required Lean component | Intake status |
|---|---|---|---|
| "Dirac equation" | first-order relativistic wave equation | explicitly typed Dirac operator and solution predicate | included; conventions open |
| gamma matrices | Clifford relation for the metric | concrete matrices or Clifford representation | included; representation open |
| free massive particle | mass term without gauge field | scalar mass and uncoupled derivative operator | included; units/domain open |
| squaring/factorization | cancellation of antisymmetric cross terms | checked operator identity using commuting derivatives | selected claim; analytic interface open |
| Klein-Gordon consequence | second-order equation for each spinor component | equality on a fixed function space/domain | included; regularity open |

## Existing Lean boundary

`Formalizations/Lean/AwesomeTheorems/Stage1/S1_M_194.lean` records substantial historical
exploration, gamma-matrix identities, derivative-semantics candidates, and an external-project
survey. Under rev-5.6 it supplies discovery evidence only: its claims explicitly leave the concrete
representation and analytic integration path open, and its older checks cannot supply accepted
statement or proof credit. The pinned mathlib and external search must be repeated after the exact
statement is frozen.

Before `H0`, an independent reviewer must verify the chosen source edition, exact equations/pages,
signature and unit conventions, assumptions, derivation boundaries, and known errata, then approve
the source-to-Lean mapping row by row.
