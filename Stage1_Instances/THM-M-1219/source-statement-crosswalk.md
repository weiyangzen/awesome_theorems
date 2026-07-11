# Source-statement crosswalk

## Available source record

`Docs/researches/math_theorems.md` gives the title "Dodson theorem", Benjamin Dodson, 2012, the
phrase "global well-posedness of the mass-critical NLS", and the untrusted label `已验证`.
`Docs/Stage0_Blueprint.md` repeats these fields while leaving exact definitions, hypotheses,
proof, axioms, and machine status open. It supplies no bibliography, theorem/page, edition, or
errata record. Repository search found no target-specific Lean artifact.

Therefore this intake asserts no primary-source candidate. The phrase describes a theorem family,
not one proposition. Choosing a familiar formulation now would invent missing mathematics, and the
metadata label supplies neither `H0` nor machine-proof credit.

## Crosswalk

| Source element | Mathematical information fixed | Lean information required | Intake result |
|---|---|---|---|
| "mass-critical" | critical regularity is the mass/L2 level | scaling action, mass, critical exponent | family indicated; definitions unresolved |
| "NLS" | nonlinear Schrodinger equation family | exact equation, sign, domain, solution predicate | unresolved |
| "global well-posedness" | a global existence/uniqueness claim | quantified data, lifespan, uniqueness and dependence predicates | clauses and bounds unresolved |
| Benjamin Dodson / 2012 | attribution and approximate discriminator | immutable primary-source identity | insufficient to select a theorem |
| `已验证` | untrusted repository label | inspectable human proof and kernel receipts | no credit |

The next gate is independently verified primary-source identification, followed by a row-by-row
mapping of every assumption and conclusion to a canonical Lean expression. Anchor discovery and
proof inspection belong to later assigned phases.
