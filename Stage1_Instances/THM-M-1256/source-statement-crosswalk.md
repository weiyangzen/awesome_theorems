# Source-statement crosswalk

## Available source record

The only located source record is the repository inventory
`Docs/researches/math_theorems.md`: title "Hörmander theorem", proposer Lars Hörmander, date 1955,
statement "solvability of constant-coefficient PDE", and status `已验证`. `Docs/Stage0_Blueprint.md`
repeats these fields and leaves definitions, assumptions, equivalent formulations, axioms, and
machine artifacts open. Neither record supplies a publication, edition, theorem number, page,
quotation, or errata trail. They are secondary inventory metadata, not a primary source.

The nearby inventory entry for Malgrange-Ehrenpreis says "existence of fundamental solutions for
constant-coefficient PDE" and is a separate theorem ID. This makes a plausible mathematical
relationship visible but is not evidence that the two canonical claims are identical.

## Crosswalk

| Source element | Mathematical information fixed | Lean information required | Intake result |
|---|---|---|---|
| "Hörmander theorem" | an attributed theorem family | unique declaration name and proposition | ambiguous name |
| "constant-coefficient PDE" | constant-coefficient differential operator | scalar field, dimension, polynomial/symbol and operator encoding | unresolved |
| "solvability" | existence of a solution for admissible data | datum/solution types, equation, quantifier order | unresolved |
| Lars Hörmander / 1955 | attribution and date only | none | unverified metadata |
| `已验证` | repository screening label | inspectable proof and accepted receipt | no credit |

## Statement boundary

No canonical Lean expression is asserted at intake. A candidate based on a fundamental solution
must not be accepted until a primary source proves that it is the intended Hörmander statement and
the statement phase records checked implications between fundamental-solution existence and the
precise solvability formulation, including all domain and support assumptions.

The first downstream gate is primary-source identification. `H0` additionally requires edition,
theorem/page, definitions, assumptions, errata, a row-by-row mapping to the canonical Lean target,
and independent review. No repository-local or external Lean proof candidate was audited in this
phase.
