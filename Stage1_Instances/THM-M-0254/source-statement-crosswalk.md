# Source-statement crosswalk

## Repository record

`Docs/researches/math_theorems.md:1829-1834` supplies exactly the title `有界平均振动函数`, Fritz
John and Louis Nirenberg, 1961, the gloss `BMO函数的特征` ("a characterization of BMO
functions"), importance "high," and status `已验证`. Git blame attributes all six uncited lines
to repository commit `bcf3f9fa79ab8c2b6610c9875668c2589b35b74f`. The record contains no
bibliographic citation, theorem locator, definitions, domain, ordered binders, hypotheses,
conclusion, constants, proof boundary, corrections, reviewer, or formal artifact.

`Docs/Stage0_Blueprint.md:7031-7056` repeats the gloss while explicitly leaving the target formal
system, logical foundation, exact definitions and premises, proof route, dependencies, equivalent
forms, axioms, machine status, and artifact links open. Its generated planning language is not
source evidence. The rev-5.6 manifest preserves `已验证` only as `source_status_untrusted` and
resets the target to `L0 / rework_required`.

## Bibliographic discovery boundary

Crossref identifies Fritz John and Louis Nirenberg, *On functions of bounded mean oscillation*,
*Communications on Pure and Applied Mathematics* **14** (1961), no. 3, 415-426,
DOI `10.1002/cpa.3160140317`. Its authors, year, and title closely match the catalog metadata.
Semantic Scholar independently returns the same title, year, authors, and DOI while classifying
its PDF as closed access. Crossref also identifies a 1985 collected-papers reprint at pages
666-677, DOI `10.1007/978-1-4612-5412-6_36`.

These records establish a strong source lead, not an exact statement. No immutable primary text was
admitted to the dossier; no theorem/page locator, incorporated definition chain, premise map,
proof-node boundary, edition comparison, correction impact, or independent review was completed.
The repository gloss itself does not say which result inside the paper is intended. Accordingly,
the bibliographic identity supplies no H0 credit and selects no canonical root.

## Component crosswalk

| Repository element | Mathematical decision required | Prospective Lean component | Intake assessment |
|---|---|---|---|
| `有界平均振动函数` | decide whether this names a class of functions or a theorem about it | one exact canonical `Prop`, not merely a structure name | topic label only; root open |
| John/Nirenberg, 1961 | identify the exact primary edition, result, page, and any corrections | immutable source identity and version | strong bibliographic match; primary theorem unadmitted |
| `BMO函数` | fix domain, scalars, local integrability, a.e. equality, cubes/balls, average, oscillation, and quotient convention | carrier, measure, set basis, function model, mean-oscillation predicate or seminorm | every proposition-changing choice is absent |
| `特征` | select definition, implication, equivalence, distribution inequality, exponential criterion, or `L^p` comparison | exact conclusion and checked direction(s) | wording is not truth-valued |
| uniform boundedness reading | fix the supremum family, codomain, finiteness, and bound quantifiers | `MeasureTheory.average`, set integrals, norm, supremum | generic averages exist; BMO predicate absent |
| distribution-tail reading | fix threshold range and constants and quantify over cubes | restricted measure of a superlevel set and exponential estimate | not selected; overlaps `THM-M-0302` |
| exponential-integrability reading | fix exponential coefficient, normalization, and finite bound | integrability or set-average of an exponential | not selected; `THM-M-0302` explicitly owns this gloss |
| equivalent-oscillation reading | fix exponent range and both inequalities | paired implications or equivalence with checked witnesses | no exponent or relationship is given |
| `已验证` | untrusted inventory label | no proof object | explicitly rejected as evidence |

## Neighbor-source conflict

`Docs/researches/math_theorems.md:2167-2172` separately schedules `THM-M-0302`, "John-Nirenberg
inequality," with the same authors and year and the gloss "exponential integrability of BMO
functions." That is a substantially more precise theorem identity associated with the 1961 paper.
It makes it unsafe to interpret this target as the same inequality without an integration-lane
duplicate or relationship decision. Likewise, `THM-M-0301` and `THM-M-0363` separately own BMO-
`H^1` duality. Neighbor dossiers are discovery evidence only and confer no scope or proof credit.

## Required source correction

Before statement work, an accountable reviewer must approve one exact primary-source proposition
and immutable edition, pinpoint its theorem and incorporated definition locators, map every domain
restriction, binder, premise, constant, inequality direction, conclusion, and dependent source
node, inspect corrections and errata, reconcile `THM-M-0302`, and obtain an independent crosswalk
review. If the entry is a duplicate rather than an independent theorem, only the master may record
that identity and define a checked transport or workflow policy. Only after this correction may the
statement phase encode and mutation-test a canonical Lean expression. Until then the catalog
wording is provisionally `H5` because it is not a stable proposition and needs a master target
decision; this does not say that BMO mathematics is open or refuted. Machine and readability states
remain `M4` and `R4`.

## Lean intake boundary

At pinned mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`, the API-only probe
checks `MeasureTheory.average`, `MeasureTheory.setAverage_eq`,
`MeasureTheory.average_congr`, `MeasureTheory.setAverage_sub_setAverage`,
`Real.volume_Icc_pi`, and `Real.volume_pi_Ioo`. These declarations support future set-average and box
infrastructure, but they define neither BMO nor any characterization or John-Nirenberg theorem. A
bounded exact-topic search found no target-specific declaration. These checks neither elaborate a
canonical target nor supply proof evidence and are not the later immutable anchor audit.
