# Source-statement crosswalk

## Repository record

`Docs/researches/math_theorems.md:2167-2172` supplies exactly the title
`约翰-尼伦伯格不等式`, Fritz John and Louis Nirenberg, 1961, the gloss `BMO函数的指数可积性`
("exponential integrability of BMO functions"), importance `高` ("high"), and status `已验证`
(`verified`). Git blame attributes all six uncited lines to commit
`bcf3f9fa79ab8c2b6610c9875668c2589b35b74f`. The record contains no bibliography, theorem
locator, definitions, domain, ordered binders, hypotheses, constants, conclusion formula, proof
boundary, corrections, reviewer, or formal artifact.

`Docs/Stage0_Blueprint.md:8332-8357` repeats the gloss while leaving the target formal system,
logical foundation, exact definitions and premises, proof route, dependencies, equivalent forms,
axioms, machine status, and artifact links open. The rev-5.6 manifest preserves `已验证` only as
`source_status_untrusted` and resets the target to `L0 / rework_required`.

## Bibliographic discovery boundary

Crossref identifies Fritz John and Louis Nirenberg, *On functions of bounded mean oscillation*,
*Communications on Pure and Applied Mathematics* **14** (1961), no. 3, 415-426,
DOI `10.1002/cpa.3160140317`. Semantic Scholar independently returns the same title, year,
authors, DOI, journal, volume, and pages and reports no open-access PDF. The DOI publisher endpoint
was access-challenged in this worker environment, so no primary text was admitted.

These records establish a strong source identity and a published theorem family, not exact source
fidelity. No immutable primary text, theorem/page locator, definition chain, assumption map,
constant normalization, proof-node boundary, edition comparison, correction audit, or independent
review was completed. This supports provisional H1 rather than H0.

## Component crosswalk

| Repository element | Mathematical decision required | Prospective Lean component | Intake assessment |
|---|---|---|---|
| John-Nirenberg inequality | locate the exact primary result and decide its canonical formulation | one exact canonical `Prop` with source-bound constants | family identified; locator open |
| BMO function | fix Euclidean domain, scalars, local integrability, a.e. equality, cubes, average, oscillation, and quotient | carrier, measure, set basis, function model, BMO predicate or seminorm | target definition absent |
| exponential integrability | fix centering, coefficient, normalization, cube restriction, integral or average, and bound | `MeasureTheory.average`, restricted integral, `Real.exp`, `Integrable` | exact conclusion open |
| inequality | fix positivity and dependency of constants and all quantifier scopes | explicit witnesses and ordered binders | constants and binders absent |
| distribution-tail form | decide whether it is the root, a consequence, or an alternate encoding | measure of a superlevel set plus exponential decay | relationship not source-mapped |
| `已验证` | treat as untrusted inventory metadata | no proof object | rejected as evidence |

## Source work required

Before H0, accountable reviewers must admit an immutable primary edition, pinpoint the theorem and
all incorporated definitions, map every binder, premise, constant, inequality direction,
conclusion, and proof node, compare relevant editions, inspect corrections and errata, and obtain an
independent crosswalk review. Before the statement gate, they must choose the exact exponential or
distribution form and elaborate it without broadening or narrowing the source claim.

## Neighbor-source boundary

`THM-M-0254` has the same authors and year but only the gloss "a characterization of BMO
functions." Its planned dossier treats John-Nirenberg and exponential integrability as one possible
reading and explicitly reserves that reading for this target. It cannot provide inherited source
or proof credit. BMO-`H^1` duality targets `THM-M-0301` and `THM-M-0363` are distinct conclusions.

## Lean intake boundary

At pinned mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`, the API-only probe
checks set averages, Euclidean box volumes, Markov inequalities, and positivity of integrals of
integrable exponentials. These are plausible future ingredients but define neither Euclidean BMO
nor the John-Nirenberg theorem. A bounded exact-topic search found no target-specific declaration.
The probe does not elaborate a canonical target or supply proof evidence.
