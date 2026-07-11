# Source-statement crosswalk

## Available source record

`Docs/researches/math_theorems.md` records the title "wave equation", attribution to Jean le Rond
d'Alembert, date 1746, and the statement "solution of the one-dimensional wave equation". It also
contains the untrusted label `已验证`. `Docs/Stage0_Blueprint.md` repeats this information while
leaving exact definitions, assumptions, proof, axioms, and machine artifacts open. No edition,
theorem number, page, bibliography, or errata record is supplied.

The inventory immediately follows this entry with a distinct THM-M-1127, "d'Alembert formula",
whose wording is "general solution of the one-dimensional wave equation". That separation is
positive evidence that this intake must not collapse the two IDs. It still does not identify what
mathematical assertion THM-M-1126 denotes. No primary-source candidate is asserted at intake.

## Crosswalk

| Source element | Mathematical information fixed | Lean information required | Intake result |
|---|---|---|---|
| "one-dimensional" | one spatial coordinate | spatial domain and coordinate type | unresolved |
| "wave equation" | a hyperbolic PDE family | exact operator, speed, signs, time domain | unresolved |
| "solution" | a function satisfying some solution relation | function type, regularity, PDE predicate, data | unresolved |
| d'Alembert / 1746 | historical attribution metadata | none | insufficient to identify theorem/page |
| distinct formula item | THM-M-1127 must not be silently merged | separate canonical declarations | exclusion frozen |
| `已验证` | untrusted repository metadata | inspectable source proof and kernel receipt | no credit |

## First downstream gate

The statement phase must first identify a primary source and an exact theorem rather than infer one
from the topic label. Before `H0`, an independent reviewer must verify edition, theorem/page,
definitions, every hypothesis, conclusion, and relevant errata. Before machine credit, the exact
source claim must be mapped binder-by-binder to an elaborated Lean declaration. Until then M4 is
retained and no d'Alembert representation, existence, or uniqueness theorem is adopted.
