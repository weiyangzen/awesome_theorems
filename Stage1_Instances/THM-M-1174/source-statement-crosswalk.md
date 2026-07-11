# Source-statement crosswalk

## Available source record

`Docs/researches/math_theorems.md` records only the title "Moser iteration", attribution "Jürgen
Moser", year 1960, and statement "local boundedness of weak solutions". The corresponding
`Docs/Stage0_Blueprint.md` entry repeats those fields while explicitly leaving precise definitions,
hypotheses, proof route, axioms, and machine artifact open. Neither record gives a bibliography,
edition, theorem number, page, equation class, or errata information. The `已验证` field is explicitly
untrusted rev-5.6 screening metadata.

No primary-source candidate is asserted at intake. A historical-paper search and edition-level
verification belong to the later statement/source work; guessing a familiar Moser theorem now
would silently substitute missing mathematics.

## Crosswalk

| Source element | Information fixed | Information still required for Lean | Intake result |
|---|---|---|---|
| "Moser iteration" | a named iterative proof method/family | one proposition rather than a method label | unresolved |
| "weak solutions" | a weak formulation is intended | operator, test functions, spaces, data, solution predicate | unresolved |
| "local" | an interior or local region is involved | ambient domain and nested balls/cylinders | unresolved |
| "boundedness" | an essential-supremum conclusion is plausible | exact norm inequality, exponents, constants | unresolved |
| Jürgen Moser / 1960 | historical discovery hint | primary source edition, theorem/page, assumptions, errata | unresolved |
| `已验证` | untrusted inventory label | inspectable proof and kernel receipts | no credit |

## Lean boundary

Repository search found no target-specific Lean module or declaration for `THM-M-1174`. Even an
abstract iteration lemma would not establish the unidentified PDE statement without checked
analytic bridges. The first downstream gate is primary-source identification followed by an exact
human claim and canonical Lean target. Until those are independently crosswalked, the status remains
`H4/M4/R4`.
