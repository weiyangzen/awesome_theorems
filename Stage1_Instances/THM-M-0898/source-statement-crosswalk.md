# Source-statement crosswalk

## Repository provenance

The authoritative repository record is currently only metadata:

- `Docs/researches/math_theorems.md:6572-6577` gives the title, Thomas Kirkman attribution, year
  1850, gloss `Steiner三元系的存在性`, importance, and `已验证` label. The record was introduced by
  commit `bcf3f9fa79ab8c2b6610c9875668c2589b35b74f` and contains no citation.
- `Docs/Stage0_Blueprint.md:24494-24519` repeats those fields but explicitly leaves exact
  definitions and premises, proof history, equivalent forms, axioms, formal system, and machine
  artifact open.
- `Docs/Stage1_Targets_rev-5.6.json` admits the metadata-screened record at rank 1040 as uniform
  `L0 / rework_required`; it expressly treats the historical source status as untrusted and legacy
  artifacts as unaccepted.

These records explain why the target exists. They are secondary repository metadata, not a primary
mathematical statement or H0 evidence.

## Name-versus-gloss crosswalk

| Repository component | Mathematical reading | Required Lean component | Intake status |
|---|---|---|---|
| Kirkman schoolgirl problem | schedule 15 points in triples over seven parallel classes | typed 15-point carrier, seven indexed partitions, five 3-blocks per class | named reading; not selected by a source |
| pair meets once | every unordered 2-subset lies in exactly one triple over all days | exact pair-coverage existence and uniqueness predicate | absent from the gloss |
| Steiner triple system | 3-uniform blocks with unique coverage of each unordered pair | block family and exact `2-(v,3,1)` incidence laws | gloss names only the family |
| resolvability | blocks partition into parallel classes, each covering all points once | resolution/parallel-class structure and composition laws | required by named problem, omitted by gloss |
| existence | concrete `KTS(15)` witness, fixed-order `Exists`, or all-order iff | one source-selected quantifier and conclusion shape | unresolved |
| `已验证` | untrusted inventory label | no declaration, body, receipt, or axiom report | no proof credit |

The implication from a schoolgirl schedule to an ordinary `STS(15)` forgets the resolution and is
not reversible merely by definition. A concrete `KTS(15)` existence theorem, ordinary `STS(v)`
existence, and general admissible-order characterizations therefore cannot be interchanged without
checked transports and source authority.

## Historical discovery boundary

The catalog attribution and year suggest Kirkman's 1850 schoolgirl question, but the repository
does not provide the original publication, edition, item/page locator, transcription, or proof
source. Secondary descriptions commonly give the fifteen-girl/seven-day wording and its equivalence
to a Kirkman triple system; those descriptions are useful for detecting the catalog conflict only.
They are not admitted as immutable E4/H0 evidence here.

Before source credit, an independent reviewer must verify a stable copy of the selected primary or
authoritative source, edition/version, exact item/theorem and page, every definition and premise,
the direction of each schedule/design equivalence, proof boundary, translations, corrections and
errata, and the relationship to the repository gloss. If the intended target is instead a modern
general existence theorem, its primary proof source and exact congruence domain must be selected
separately rather than attributed wholesale to the 1850 problem.

## Lean discovery boundary

A bounded intake search found no occurrence of `Kirkman`, `schoolgirl`, `Steiner triple`, or a
resolvable triple-system declaration in the pinned mathlib source or repo-local Lean modules.
`IntakeProbe.lean` checks only generic `Finset.powersetCard`, fixed-cardinality membership/cardinality,
pairwise disjointness, and natural congruence APIs. This is feasibility evidence for vocabulary,
not an exhaustive anchor audit, absence proof, canonical expression, formal candidate, or proof
body. The dependency-ordered `ANCHOR_AUDIT` remains open.
