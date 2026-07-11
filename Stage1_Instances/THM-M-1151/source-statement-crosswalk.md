# Source-statement crosswalk

## Available source record

The repository inventory `Docs/researches/math_theorems.md` gives the title "Robin problem",
Victor Robin, 1886, and the statement "mixed boundary-value problem". The generated Stage0 record
repeats those fields while leaving definitions, hypotheses, proof path, equivalences, axioms, and
machine artifact open. Neither record supplies a bibliography, edition, theorem number, page, or
errata. The `verified` label is explicitly untrusted under rev-5.6.

No primary-source theorem is consequently asserted at intake. "Robin boundary condition" is a
widely used name for a relation combining boundary value and normal derivative, but adopting a
particular PDE and solvability theorem from that convention would invent mathematics absent from
the source record.

## Crosswalk

| Source element | Mathematical information fixed | Lean information required | Intake result |
|---|---|---|---|
| "Robin problem" | named boundary-problem family | canonical proposition, definitions, ordered binders | unresolved |
| "mixed boundary-value problem" | more than one kind of boundary behavior may be involved | boundary API, partition or linear boundary operator | ambiguous |
| Victor Robin / 1886 | historical metadata | primary edition, theorem/page, definitions and errata | unverified |
| `verified` | repository screening label only | inspectable proof and kernel receipt | no credit |

## Statement boundary

There is no repo-local Lean artifact identified for this target and no canonical expression to
elaborate at intake. The first downstream gate is primary-source identification and disambiguation
of whether "mixed" means a Robin linear combination on one boundary or distinct boundary-condition
types on separate pieces. Before `H0`, independent review must check the edition, exact claim,
assumptions, definitions, page and errata, followed by a row-by-row mapping to the canonical Lean
statement. Until then `H4/M4/R4` is the truthful boundary.
