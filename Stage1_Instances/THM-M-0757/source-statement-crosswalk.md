# Source-statement crosswalk

## Repository record

`Docs/researches/math_theorems.md:5577-5582` supplies exactly the title `可容许序数`, attribution
to Gerald Sacks, year 1966, the gloss `alpha-recursion theory`, importance "high," and status
`已验证`. Git blame attributes all six uncited lines to repository commit
`bcf3f9fa79ab8c2b6610c9875668c2589b35b74f`. The record contains no truth-valued statement,
bibliographic citation, definition of admissibility, domain, binders, hypotheses, conclusion,
proof boundary, or formal artifact.

`Docs/Stage0_Blueprint.md:20677-20702` repeats the gloss while explicitly leaving the target formal
system, logical foundation, exact definitions and premises, proof route, dependencies, equivalent
forms, axioms, machine state, and artifact links open. Its generated planning language is not
source evidence. The rev-5.6 manifest preserves `已验证` only as `source_status_untrusted` and resets
the target to `L0 / rework_required`.

## Bibliographic discovery boundary

Crossref metadata identifies Gerald E. Sacks, *Metarecursively enumerable sets and admissible
ordinals*, *Bulletin of the American Mathematical Society* 72(1) (1966), 59-64, DOI
`10.1090/S0002-9904-1966-11416-7`. A second 1966 source lead is Gerald E. Sacks,
*Post's problem, admissible ordinals, and regularity*, *Transactions of the American Mathematical
Society* 124(1), 1-23, DOI `10.1090/S0002-9947-1966-0201299-1`.

These leads align with the catalog author, year, and subject, but they do not identify a unique
root. The titles name several concepts and results. Full primary text was not admitted into this
worker evidence: direct version-of-record access was blocked, and no theorem/page, incorporated
definition chain, exact premises, conclusion, proof boundary, corrections, errata, or independent
review was inspected. Crossref responses are mutable discovery metadata, not H0 evidence.

## Component crosswalk

| Repository element | Mathematical decision required | Prospective Lean component | Intake assessment |
|---|---|---|---|
| `可容许序数` | select a definition or theorem rather than an object family | one exact canonical `Prop` | title only; root open |
| Gerald Sacks / 1966 | identify the intended publication and exact result | immutable source identity and version | two aligned source leads; neither selected |
| `alpha-recursion theory` | select one theorem in a broad research program | exact conclusion and dependency tree | subject label, not a proposition |
| admissible ordinal | freeze closure, constructible-level, or other source definition | predicate on `Ordinal` or a checked set-theoretic representation | generic ordinal APIs only |
| alpha-recursive object | fix functions/sets, domain, coding, parameters, enumerability, and totality | source-mapped recursion predicate and encodings | ordinary `RecursiveIn` is not a bridge |
| special ordinal | settle arbitrary/countable/recursive alpha and Church-Kleene conventions | explicit ordinal binder and hypotheses | all choices absent |
| theorem conclusion | select characterization, closure, existence, degree, regularity, or another result | exact result type and binder scope | wholly absent |
| `已验证` | untrusted inventory label | no proof object | explicitly rejected as evidence |

## Candidate readings and conflicts

Admissibility characterizations, alpha-recursion definitions, the metarecursive specialization,
bounded enumerable-set existence, Post-problem results, regularity theorems, and degree statements
are not interchangeable. The neighboring targets on hierarchies, hyperarithmetic theory, jumps,
and c.e. degrees make silent scope absorption especially unsafe.

## Required source correction

Before statement work, an accountable reviewer must approve one exact truth-valued proposition and
immutable primary edition, pinpoint all theorem and definition locators, map every domain restriction,
binder, premise, conclusion, and dependent source node, inspect corrections and errata, reconcile the
catalog identity with the chosen result, and independently review the crosswalk. Only then may the
statement phase encode and mutation-test a canonical Lean expression. Until that correction, the
catalog target is provisionally `H5`, while machine and readability states remain `M4` and `R4`.

## Lean intake boundary

At pinned mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`, the API-only probe
checks generic type-theoretic ordinals, set-theoretic ordinals, and natural-number oracle
computability. The bounded exact-topic search found no admissible-ordinal or alpha-recursion target.
These checks neither elaborate a canonical target nor supply proof evidence.
