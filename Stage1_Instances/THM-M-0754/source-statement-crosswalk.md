# Source-statement crosswalk

## Repository source

`Docs/researches/math_theorems.md:5556-5561` is the only target-bearing source record. It gives the
title `算术层次`, names Stephen Kleene, gives the year 1943, and supplies the complete gloss
`算术集合的层次` ("the hierarchy of arithmetical sets"). Git history traces all six lines to
commit `bcf3f9fa79ab8c2b6610c9875668c2589b35b74f`. The record has no citation, edition, locator,
definition, proposition, premise, conclusion, proof, correction, erratum, or formal artifact.

`Docs/Stage0_Blueprint.md:20596-20621` repeats the gloss. It explicitly leaves the formal system,
foundations, definitions and premises, proof route, dependencies, equivalent forms, axioms,
machine status, and artifacts open. The rev-5.6 manifest preserves `已验证` only as
`source_status_untrusted` and resets the target to `L0 / rework_required`.

No primary mathematical source is identified in the repository. The attribution and year are
bibliographic search leads only. They do not identify one Kleene publication or a pinpoint
definition/theorem, and this intake does not infer a 1943 statement from memory. Consequently no
primary-source revision, page-level mapping, proof boundary, correction/errata disposition,
translation review, or independent source review receives credit.

## Component crosswalk

| Catalog phrase or missing component | Material choice required | Pinned Lean surface | Intake assessment |
|---|---|---|---|
| "arithmetical sets" | domain of sets/relations, coding, parameters, and standard-model semantics | `Set Nat`, `PrimrecPred`, `ComputablePred`, `REPred` | adjacent representations only; source selects none |
| "hierarchy" | indexed classes, base level, dual/intersection conventions, and inclusion relation | no source-selected declaration | topic label, not a truth-valued conclusion |
| formula complexity | arithmetic language, bounded quantifiers, alternating unbounded blocks, polarity, and free variables | `FirstOrder.Language.BoundedFormula`, `IsQF`, `IsPrenex`, `IsUniversal`, `IsExistential` | generic first-order syntax; not an arithmetical hierarchy implementation |
| semantic classification | intended arithmetic structure and equivalence between formula class and set membership | `BoundedFormula.Realize` | generic realization API; exact arithmetic encoding is open |
| possible strictness | for each level, a set in one class outside the opposing/lower class | no selected result | familiar candidate theorem, absent from the catalog wording |
| possible computability characterization | relation to c.e. predicates, oracle jumps, or relative computability | pinned computability APIs | possible later bridge, not source or statement credit |
| `已验证` | catalog metadata | no expression or proof object | no H or M credit |

## Lean and source boundary

At pinned mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`, the intake probe checks
generic first-order quantifier-complexity predicates and computability predicates. A bounded search
of pinned mathlib and repository Lean files finds no declaration named for the arithmetical
hierarchy. This is a reproducible local discovery observation, not an exhaustive anchor audit or a
global absence claim.

Mathlib's generic `IsUniversal` and `IsExistential` describe formulas with only one kind of
unbounded quantifier over a quantifier-free matrix. They do not by themselves define every
alternation level, select the language/standard model of arithmetic, classify sets of naturals, or
state strictness, completeness, closure, or a computability characterization. Likewise,
`PrimrecPred`, `ComputablePred`, and `REPred` are adjacent interfaces, not a crosswalk from the
catalog gloss to one theorem.

Before statement credit, reviewers must select and approve an exact source proposition, elaborate
and fingerprint its canonical Lean expression under minimal imports, compile every credited
transport, and distinguish removed-hypothesis, changed-domain, changed-binder-scope, and boundary-
case mutations. Before `H0`, an independent source reviewer must approve the immutable primary
passage, all incorporated definitions and assumptions, the proof mapping, corrections, and errata.
