# Exact-statement gate: blocked

Item: `S56-M-0820-STATEMENT`

Theorem: `THM-M-0820`

Base revision: `39704171d88ffcdc33a47365ae9791f855fa3a44` (tree
`050ab5c6392560337051d2eadd1b82277dbe1c4f`).

## Decision

The statement item remains `[ ]`. Its prerequisite intake has provisional worker state `[_]`, not
master-accepted state `[x]`. More importantly, the intake deliberately leaves the canonical human
statement and Lean expression null because the exact source statement and proposition-changing
conventions are not approved.

The catalog says only that Mirsky's theorem gives the minimum number of antichains in a
decomposition of a partially ordered set. It does not state that the carrier is finite or
inhabited, define decomposition as a possibly overlapping cover or a partition, choose whether
chains and antichain parts must be nonempty, fix a chain-height convention, encode the minimum, or
settle the empty and singleton cases. Each choice changes the proposition or requires a checked
transport.

Mirsky's 1971 article is identified bibliographically, but its theorem passage, incorporated
definitions, proof, corrections, errata, immutable full text, and independent review were not
obtained. The strongest inspected secondary source, Singh's Coq exposition, states the result for a
finite inhabited poset: the cardinality of a largest inhabited chain equals the cardinality of a
smallest possibly overlapping cover by inhabited antichains. That source discriminates the theorem
family but does not authorize an empty-inclusive partition form. A discovered external Lean
candidate makes exactly those alternative partition and empty-carrier choices and is not in the
pinned validation closure.

Selecting a convenient `Finpartition`, indexed cover, `Set.chainHeight`, `Nat` height, or finite
subset formulation from general mathematical knowledge would therefore invent missing binders and
conventions. Dilworth's theorem, Sperner's theorem, a one-sided bound, or existence of some cover
cannot substitute for the target.

Rev-5.6 treats statement ambiguity and a missing expression fingerprint as hard blockers. There is
no honest canonical expression whose imports can be certified minimal, no approved alternate form
for a checked transport, and no canonical target against which the required removed-hypothesis,
changed-domain, changed-binder-scope, and boundary-case mutations can run. Those mutations are
undefined, not passed. The vector remains `[H1, M3, R4]`.

## Pinned Lean boundary

The existing `IntakeProbe.lean` was re-elaborated with these direct imports:

- `Mathlib.Order.Height`
- `Mathlib.Order.Partition.Finpartition`

It checks eight adjacent chain-height, antichain, chain, and finite-partition interfaces, plus the
`Fin 0` and `Fin 1` chain-height boundaries. All checks pass under pinned Lean `4.29.0` at commit
`98dc76e3c0a9b856c9b98726b713fb04fab16740` and mathlib revision
`8a178386ffc0f5fef0b77738bb5449d50efeea95`. A bounded search found no source-selected Mirsky or
antichain-cover-minimum declaration in pinned mathlib or repository-local Lean.

The probe declares no target, transport, or proof body, so its imports cannot be certified minimal
for an absent canonical statement. The automation-provided `.lake` symlink was used read-only. No
update, build, clone, fetch, or dependency mutation was run.

## Validation record

Commands ran from this worker clone on 2026-07-13 (`Asia/Shanghai`).

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, and 1546 uniform-L0 Lean 4 targets passed; execution skill present |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all `L0/rework_required` |
| `python3 scripts/stage1_target.py show THM-M-0820` | 0 | rank 1378; planned; no legacy slot; legacy artifacts unaccepted; theorem incomplete |
| `git status --short --untracked-files=all`; `git rev-parse HEAD 'HEAD^{tree}'` (pre-edit) | 0 | only the automation-provided `.lake` symlink was untracked; the base revision and tree appear above |
| `git blame -L 6026,6031 -- Docs/researches/math_theorems.md` | 0 | all six sparse catalog fields originate at commit `bcf3f9fa79ab8c2b6610c9875668c2589b35b74f` |
| primary metadata, closed-full-text, secondary-source, and external-candidate inspection | 0 | bibliography and theorem family identified; no accepted exact source statement or source-to-Lean variant decision obtained |
| `cd Formalizations/Lean && lake env lean --version && lake --version` | 0 | pinned Lean and Lake versions recorded above |
| pinned mathlib revision/tree/status checks | 0 | revision `8a178386...`, tree `bdc39a31...`; package worktree clean |
| `cd Formalizations/Lean && LC_ALL=C TZ=UTC lake env lean ../../Stage1_Instances/THM-M-0820/IntakeProbe.lean` | 0 | eight adjacent interfaces and the empty/singleton examples elaborated; no canonical target or proof declared |
| bounded exact-topic `rg` search over pinned mathlib, repository Lean, and the owned probe | 0 | only intake disclaimers and unrelated generic antichain occurrences matched; no source-selected target declaration found |
| `python3 -B Stage1_Instances/THM-M-0820/check_intake.py` | 1 | historical checker expects intake `[ ]`, while integration now records `[_]`; this stale historical evidence was not rewritten |
| prohibited Lean construct scan over the owned target | 1 (expected no match) | no `sorry`, `admit`, `sorryAx`, `axiom`, `constant`, `opaque`, or `unsafe` declaration found |

## Retry condition and status boundary

Accountable reviewers must preserve and hash an immutable primary or approved authoritative source,
select and independently approve one exact proposition, and transcribe every incorporated
definition, ordered binder, hypothesis, conclusion, proof boundary, correction, erratum, and
boundary case. They must decide carrier and nonemptiness scope; cover versus partition and its
transport; nonempty-member policy; chain-height representation; minimum encoding; and the empty,
singleton, total-order, and discrete-order cases.

A fresh statement run can then encode precisely that claim, minimize its pinned imports, serialize
the elaborated expression and environment, compile every credited transport, and execute all four
mutation classes. Master acceptance of the intake remains required before an accepted statement
transition.

This blocker is the assigned phase's truthful result, not completion of the statement node or any
downstream node. Lifecycle remains `planned`; `audit_complete: false` and
`theorem_complete: false`; no debt-vector change is proposed. No `.stage1-worker-selftest.json`,
statement receipt, worker `[_]`, master acceptance, statement fingerprint, or proof credit is
claimed.
