# THM-M-0741 rev-5.6 intake

This directory is the fail-closed `planned` intake dossier for the recursion-theory target
`停机问题` (the halting problem). The repository's complete target gloss is `停机问题不可判定`
("the halting problem is undecidable"), attributed to Alan Turing in 1936. A separate
proof-theory record, `THM-M-0707`, expresses the same English theorem family more fully. That
record is a duplicate discovery lead, not a dependency, substitute, or source of proof credit.

The theorem family is clear: no one effective total procedure decides for every encoded program
and input whether the computation eventually halts. The repository does not, however, fix the
machine model, encoding, execution semantics, validity convention, input domain, or precise
effective-decider interface. Turing's 1936 paper is the historical primary-source lead, but no
immutable copy and pinpoint passage, translation, correction/errata review, or independent source
review is accepted here. Choosing one of several inequivalent formal surfaces would belong to the
statement phase, not intake.

A narrow probe against the pinned environment confirms that mathlib exposes partial-recursive
program codes, their evaluator, recursively enumerable and computable predicates, and fixed-input
halting results. It also elaborates a prospective arbitrary-code/arbitrary-input predicate. These
are feasibility and discovery observations only. They do not freeze the source-identical target,
credit `ComputablePred.halting_problem`, import `THM-M-0707`, or prove this item.

The provisional root vector is `[H1, M4, R4]`. The lifecycle remains `planned`; all six downstream
tasks remain open; no proof state or receipt is accepted; and neither audit nor theorem completion
is claimed. Exact worker commands and results are recorded in `validation.md` and
`intake-receipt.json`.
