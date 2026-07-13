# Source-statement crosswalk

## Repository source

`Docs/researches/math_theorems.md:5570-5575` is the only target-bearing source record. It gives the
title `超算术理论`, names Stephen Kleene, gives the year 1955, and supplies the complete gloss
`超算术集合的理论` ("the theory of hyperarithmetic sets"). Git history traces all six lines to
commit `bcf3f9fa79ab8c2b6610c9875668c2589b35b74f`. The record has no citation, edition, locator,
definition, proposition, premise, conclusion, proof, correction, erratum, or formal artifact.

`Docs/Stage0_Blueprint.md:20650-20675` repeats the gloss. It explicitly leaves the formal system,
foundations, definitions and premises, proof route, dependencies, equivalent forms, axioms,
machine status, and artifacts open. The rev-5.6 manifest preserves `已验证` only as
`source_status_untrusted` and resets the target to `L0 / rework_required`.

No primary mathematical source is identified in the repository. The attribution and year are
bibliographic search leads only. They do not identify one Kleene publication or a pinpoint
definition/theorem, and this intake does not infer a 1955 statement from memory. Consequently no
primary-source revision, page-level mapping, proof boundary, correction/errata disposition,
translation review, or independent source review receives credit.

## Component crosswalk

| Catalog phrase or missing component | Material choice required | Pinned Lean surface | Intake assessment |
|---|---|---|---|
| "hyperarithmetic sets" | object domain, extensional equality, coding, and parameter convention | `Set Nat`, `ComputablePred`, `REPred` | adjacent representations only; source selects none |
| "theory" | one definition package or truth-valued theorem and its direction/strength | no source-selected declaration | subject label, not a conclusion |
| relative computability | oracle class, partiality, reductions, and iteration mechanism | `RecursiveIn`, `TuringReducible` | finite oracle infrastructure only; no transfinite hierarchy |
| effective hierarchy | recursive-ordinal notation system, base, successor, limit, and well-foundedness conventions | `WellFounded`, ordinal APIs | generic recursion substrate; no effective notation system selected |
| possible characterization | exact lightface definability class, standard-model semantics, and both directions | no selected result | familiar candidate theorem absent from the catalog wording |
| possible closure/equivalence | operations and precise presentations being compared | pinned computability APIs | possible later bridge, not source or statement credit |
| `已验证` | catalog metadata | no expression or proof object | no H or M credit |

## Lean and source boundary

At pinned mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`, the intake probe checks
partial-recursive predicates, oracle recursion, Turing reducibility/equivalence, and generic well-
founded recursion. A bounded search of pinned mathlib and repository Lean files finds no declaration
named for hyperarithmetic theory. This is a reproducible local discovery observation, not an
exhaustive anchor audit or a global absence claim.

`RecursiveIn` closes partial functions under a fixed set of oracles and standard recursion
schemes. `TuringReducible` specializes it to one oracle. These declarations do not by themselves
define an effective transfinite hierarchy, distinguish recursive ordinal notations from arbitrary
codes, select a hyperarithmetic class, or state a source-identical characterization. General
`WellFounded` and ordinal APIs likewise do not supply the required effective coding.

Before statement credit, reviewers must select and approve an exact source proposition, elaborate
and fingerprint its canonical Lean expression under minimal imports, compile every credited
transport, and distinguish removed-hypothesis, changed-domain, changed-binder-scope, and boundary-
case mutations. Before `H0`, an independent source reviewer must approve the immutable primary
passage, all incorporated definitions and assumptions, proof mapping, corrections, and errata.
