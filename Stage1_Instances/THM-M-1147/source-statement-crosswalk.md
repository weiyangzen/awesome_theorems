# Source-statement crosswalk

## Available source record

`Docs/researches/math_theorems.md` gives the title "Kelvin transform", attribution "William Thomson
(Lord Kelvin)", date 1847, statement "inversion of harmonic functions", importance "high", and the
untrusted status `已验证`. `Docs/Stage0_Blueprint.md` repeats these fields while explicitly leaving
definitions, hypotheses, proof route, axioms, and machine artifacts open. No bibliography, edition,
theorem number, page, or errata record is supplied.

Consequently this intake asserts no primary source. The metadata establishes a recognizable family
but cannot distinguish its several domain-, dimension-, and normalization-dependent theorems.

## Crosswalk

| Source element | Information fixed | Information still required for Lean | Intake result |
|---|---|---|---|
| "Kelvin transform" | named transformation family | exact inversion and weight definitions | unresolved |
| "harmonic functions" | Laplace equation is involved | dimension, scalar codomain, regularity and harmonic predicate | unresolved |
| "inversion" | domain/function are transformed | center, radius, punctured domain, image domain | unresolved |
| Thomson / 1847 | historical metadata | primary edition, theorem/page, assumptions, errata | unverified |
| `已验证` | repository screening label | inspectable proof or kernel receipt | no credit |

## Formal boundary

No repository-local Lean artifact was found for this target by the intake search. A later anchor
audit must search pinned mathlib and credible external Lean projects without using a nearby theorem
as a substitute. Before `H0`, an independent reviewer must verify a primary edition, theorem/page,
assumptions, definitions and errata and approve a row-by-row mapping to the canonical Lean target.
