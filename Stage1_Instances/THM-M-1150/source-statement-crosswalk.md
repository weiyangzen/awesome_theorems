# Source-statement crosswalk

## Available source record

`Docs/researches/math_theorems.md` supplies only the title "Neumann problem", attribution to Carl
Neumann, date 1877, the phrase "the boundary-value problem for Laplace's equation", importance
"high", and the untrusted label `已验证`. `Docs/Stage0_Blueprint.md` repeats this metadata and leaves
definitions, hypotheses, proof route, axioms, and machine artifacts open. No bibliography, edition,
theorem number, page, or errata record is attached.

This record describes a problem family rather than one proposition. No primary-source candidate is
asserted at intake, because choosing a modern existence or uniqueness theorem would invent scope.

## Crosswalk

| Source element | Mathematical information fixed | Lean information required | Intake result |
|---|---|---|---|
| "Laplace equation" | harmonic/Possion operator family | domain, Laplacian definition, solution notion | unresolved |
| "Neumann" | normal derivative boundary data | boundary, normal/trace API, data function | unresolved |
| "boundary-value problem" | seek a solution satisfying PDE and boundary data | exact hypotheses and conclusion | unresolved |
| Carl Neumann / 1877 | historical attribution metadata | none | insufficient to identify a theorem |
| `已验证` | untrusted repository label | inspectable human proof or kernel receipt | no credit |

## Statement boundary

A standard modern formulation often couples solvability to an integral compatibility condition and
uniqueness only modulo constants. That observation is a scoping warning, not the canonical claim.
The statement phase must locate a primary, pinpointed theorem and map its sign conventions,
regularity, connectedness, compatibility condition, and normalization row by row before Lean
elaboration. Independent review is required before `H0`.

