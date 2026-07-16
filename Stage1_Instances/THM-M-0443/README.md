# THM-M-0443 rev-5.6 intake

This directory is the `planned` intake for the target labelled "Mazur-Tate theorem". The repository
gloss, "the p-adic L-function of an elliptic curve", does not identify a unique theorem: it may
refer to interpolation, the Mazur-Tate-Teitelbaum exceptional-zero result, or a result about
Mazur-Tate elements. The ambiguity is retained as a statement-phase blocker.

The scope map and source crosswalk delimit these interpretations and the primary-source decision
needed next. No legacy status or artifact is accepted as rev-5.6 evidence. The provisional root
vector is `[H2, M4, R4]`; no Lean expression, proof, audit completion, or theorem completion is
claimed. Open downstream work is recorded in `task-dag.json`, and intake checks in `validation.md`.

The statement execution has now been normalized to the HEAD phase contract and remains blocked.
`statement.json` records the deliberately null canonical target, `Statement.lean` checks only pinned
adjacent interfaces, and `dependency-reuse-ledger.json` records the exact empty v2 parent/reuse
closure. `statement-receipt.json` and `check_statement.py` emit a typed negative result with
`phase_accepted=false`. The root worker packet proposes only `[_]`: the negative boundary was
self-tested, but the positive statement predicate and master acceptance remain open.
