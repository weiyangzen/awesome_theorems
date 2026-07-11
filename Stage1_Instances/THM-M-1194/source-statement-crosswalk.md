# Source-statement crosswalk

## Available source record

`Docs/researches/math_theorems.md` supplies only the Chinese title "Hamilton estimate", attribution
to Richard Hamilton, year 1993, the description "matrix Li-Yau inequality", importance `high`, and
the untrusted status `已验证`. `Docs/Stage0_Blueprint.md` repeats these fields and explicitly leaves
definitions, hypotheses, proof route, axioms, machine status, and artifact links open. No
bibliography, edition, theorem number, page, quotation, or errata record is attached.

Consequently no primary-source theorem is asserted at intake. The familiar mathematical name is
not enough to choose among related matrix Harnack and matrix gradient estimates without risking a
broadened or substituted theorem. The repository status label earns no `H0` or machine credit.

## Crosswalk

| Source element | Mathematical information fixed | Lean information required | Intake result |
|---|---|---|---|
| "Hamilton estimate" | an estimate attributed to Hamilton | exact proposition and namespace | unresolved |
| "matrix Li-Yau inequality" | matrix/tensor analogue related to Li-Yau | tensor order, Hessian/PDE expression, constants | unresolved |
| Richard Hamilton | author attribution | none | recorded, not independently verified |
| 1993 | reported year | immutable primary-source edition | recorded, not independently verified |
| PDE category | broad classification | manifold, flow, solution and analytic APIs | unresolved |
| `已验证` | untrusted metadata label | proof artifact and kernel receipt | no credit |

## Downstream source gate

Before exact statement work can receive credit, a primary-source audit must record edition,
theorem/page, definitions, every assumption, notation and errata, followed by an independent review.
Only then may the statement phase map each source binder and hypothesis to a canonical Lean target,
test boundary cases and alternate encodings, and decide whether mathlib has the required geometric
analysis interfaces. No repo-local Lean artifact for this target was found during intake.
