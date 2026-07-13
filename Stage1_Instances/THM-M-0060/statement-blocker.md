# Exact-statement gate: blocked

Item: `S56-M-0060-STATEMENT`

Theorem: `THM-M-0060`

Base revision: `c5f6fb269f6eb84efa935ee66c4e9bab92495e61` (tree
`7a41063c920c1b9cb849aa35c2f02ec4a4733655`).

## Decision

The statement item remains `[ ]`. Its prerequisite `S56-M-0060-INTAKE` has provisional worker
state `[_]`, not master-accepted state `[x]`. Its unaccepted intake receipt deliberately leaves the
canonical human statement, Lean module, expression, elaborated-expression hash, and canonical-target
environment fingerprint null.

The complete repository wording is only `整数矩阵的等价标准形` (an equivalent normal form of
integer matrices). It does not fix the row and column dimensions or their orientation, define
matrix equivalence, specify the rectangular diagonal and zero convention, state a divisibility
condition, choose signs or associates, decide existence versus uniqueness, or settle zero-sized
and rank-deficient cases. Each choice changes the proposition or requires a checked transport.

The identified source lead, Smith's 1861 paper *On systems of linear indeterminate equations and
congruences*, has not been admitted at the required granularity. Intake inspected bibliographic
metadata and an abstract, but the publisher PDF returned HTTP 403. No immutable theorem passage,
incorporated definition chain, complete proof boundary, correction or errata disposition, or
independent source review is accepted. The lead supports `H1`; it does not select an exact claim.

Selecting the familiar theorem for arbitrary rectangular integer matrices would therefore invent
missing binders and conventions. Selecting `Submodule.exists_smith_normal_form_of_le` would instead
substitute a general-PID submodule-inclusion theorem. Its diagonal basis relation has no
divisibility-chain, integer sign-normalization, or uniqueness field, and there is no checked
matrix-to-submodule transport to an approved source root.

Rev-5.6 treats statement ambiguity and a missing elaborated-expression fingerprint as hard
blockers. There is no truthful canonical expression whose imports can be certified minimal, no
credited alternate form for a checked wrapper, and no canonical target against which the required
removed-hypothesis, changed-domain, changed-binder-scope, and boundary-case mutations can run.
Those mutation results are undefined, not passed. The root vector remains `[H1, M3, R4]`.

## Pinned Lean Boundary

The existing `IntakeProbe.lean` was re-elaborated with its sole direct import,
`Mathlib.LinearAlgebra.FreeModule.PID`. It checks the adjacent Smith-normal-form structure, its five
fields, three submodule APIs, and the matrix/linear-map conversion interfaces. The existence theorem
reports `[propext, Classical.choice, Quot.sound]`. This confirms that the pinned discovery surface
is available, but the probe declares no canonical target, transport, or proof body. Its import is
minimal only for that existing discovery probe, not for the absent target.

The environment is Lean `4.29.0` at commit
`98dc76e3c0a9b856c9b98726b713fb04fab16740`, Lake `5.0.0-src+98dc76e`, and pinned mathlib revision
`8a178386ffc0f5fef0b77738bb5449d50efeea95` with tree
`bdc39a3123201dae413a9d9be56ec242c19e5c2b`. The automation-provided `.lake` symlink was used
read-only. No update, build, clone, fetch, or dependency mutation was run.

## Validation Record

Commands ran from this worker clone on 2026-07-13 (`Asia/Shanghai`).

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, and 1546 uniform-L0 Lean 4 targets passed; execution skill present |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all `L0/rework_required` |
| `python3 scripts/stage1_target.py show THM-M-0060` | 0 | rank 1092; planned; no legacy slot; legacy artifacts unaccepted; theorem incomplete |
| initial `git status --short --untracked-files=all`; `git rev-parse HEAD`; `git rev-parse 'HEAD^{tree}'` | 0 | only the automation-provided `Formalizations/Lean/.lake` symlink was untracked; base revision and tree appear above |
| `git blame -L 447,452 -- Docs/researches/math_theorems.md` | 0 | all six sparse catalog fields originate at commit `bcf3f9fa79ab8c2b6610c9875668c2589b35b74f` |
| `cd Formalizations/Lean && lake env lean --version && lake --version && sha256sum lean-toolchain lake-manifest.json` | 0 | pinned versions above; input hashes `651c8a...1d2` and `321626...d81` |
| `git -C Formalizations/Lean/.lake/packages/mathlib status --short`; revision and tree queries | 0 | package worktree clean; pinned revision and tree recorded above |
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0060/IntakeProbe.lean` | 0 | all adjacent Smith and matrix interfaces elaborated; reported axioms are `[propext, Classical.choice, Quot.sound]`; no target declared |
| bounded repo-local and pinned-mathlib search for Smith normal form, unimodular, and invariant-factor declarations | 0 | found the general-PID basis/submodule implementation and unrelated totally-unimodular APIs; no exact full integer-matrix source root |
| `python3 -B Stage1_Instances/THM-M-0060/check_intake.py` | 1 | historical intake checker rejected the integration-updated intake state `[_]`; it is stale statement input, was not edited, and is not represented as statement evidence |
| `python3 -m json.tool Stage1_Instances/THM-M-0060/statement-blocker.json` and scoped `jq -e` invariant check | 0 | valid JSON; null target/imports, four undefined mutations, false completion flags, unchanged vector, and no-self-test boundary agree |
| prohibited-declaration scan over owned Lean files | 0 | no `sorry`, `admit`, `sorryAx`, axiom, constant, opaque, or unsafe declaration found |
| scoped whitespace checks for the two new blocker artifacts | expected new-file difference | no whitespace diagnostics |
| `test ! -e .stage1-worker-selftest.json` | 0 | self-test manifest intentionally absent because the statement deliverable did not pass |

## Retry Condition And Status Boundary

Accountable reviewers must lawfully preserve and hash an immutable primary or authoritative source,
select and independently approve one exact proposition, and transcribe every incorporated
definition, binder, hypothesis, conclusion, proof boundary, correction, and boundary case. They
must resolve matrix versus module scope; integer versus PID domain; dimensions and orientation;
left/right equivalence; diagonal, zero, divisibility, sign, and associate conventions; existence
versus uniqueness; and all degenerate cases. A later statement run can then encode precisely that
claim, minimize its pinned imports, serialize the elaborated expression and environment, compile
every credited transport, and execute all four mutation classes. Master acceptance of the intake
also remains required before an accepted statement transition.

This blocker is the assigned phase's truthful result, not completion of the statement node or any
downstream node. Lifecycle remains `planned`; `audit_complete: false` and
`theorem_complete: false`; no debt-vector change is proposed. No `.stage1-worker-selftest.json`,
statement receipt, worker `[_]`, master acceptance, statement fingerprint, or proof credit is
claimed.
