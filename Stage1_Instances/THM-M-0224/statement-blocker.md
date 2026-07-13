# Exact-statement gate: blocked

Item: `S56-M-0224-STATEMENT`

Theorem: `THM-M-0224`

Base revision: `db6914155f1f63e835364b89ba0a3b25f1d7f936` (tree
`a5488edccb2687c4ff0bbdccf4650e06b2e45337`).

## Decision

The statement item remains `[ ]`. Its prerequisite `S56-M-0224-INTAKE` has provisional state
`[_]`, not a master-accepted receipt. Provisional preparation of a later node does not permit
dependency-ordered acceptance. Independently, no exact Lean 4 target can be truthfully elaborated
from the authoritative repository record.

That record supplies only the title Liouville's theorem, Joseph Liouville, 1844, and the gloss
"every bounded entire function is constant." It provides no bibliography, exact proposition,
incorporated definitions, ordered binders, proof boundary, correction history, or independent
review. Stage0 explicitly leaves the precise definitions and premises open, and rev-5.6 treats the
catalog's `verified` label as untrusted metadata.

The following decisions change the proposition or require a checked source transport:

- scalar `f : Complex -> Complex` versus a generalized map between complex normed spaces;
- entire as everywhere complex differentiability versus an analytic or holomorphic encoding;
- bounded image versus a quantified global norm bound, with its exact quantifier order;
- pairwise equality, an existential pointwise constant, or equality with `Function.const`; and
- universes, implicit parameters, binder order, fixed options, and all degenerate cases.

The intake deliberately leaves each decision open. Selecting the familiar scalar proposition from
mathematical memory would invent the missing definition chain. Selecting the stronger pinned
mathlib `E -> F` formulation would broaden the received scalar family. Neither is an exact source
freeze. Harmonic, Hamiltonian-volume, number-theoretic, and other namesake results are distinct
targets and cannot supply statement or proof credit.

Section 5 of the rev-5.6 blueprint makes statement ambiguity and a missing expression fingerprint
hard blockers. There is therefore no canonical expression for which minimal imports, checked
alternate transports, or the required removed-hypothesis, changed-domain, changed-binder-scope, and
boundary-case mutations can be certified. Those mutations are undefined, not passed. The root
remains `[H1, M3, R4]`.

## Pinned Lean Boundary

The existing `IntakeProbe.lean` was re-elaborated with the one direct import
`Mathlib.Analysis.Complex.Liouville`. It checks the bounded-range and constant-function vocabulary
and these three exact-topic interfaces:

- `Differentiable.apply_eq_apply_of_bounded`;
- `Differentiable.exists_const_forall_eq_of_bounded`; and
- `Differentiable.exists_eq_const_of_bounded`.

All checks pass in the pinned environment. Each candidate's direct axiom report is
`[propext, Classical.choice, Quot.sound]`. The first candidate concludes pairwise equality; the
second, existence of a pointwise constant value; and the third, function equality. All are
generalized over complex normed domain and codomain spaces. The probe declares no canonical target,
checked transport, or proof body, and its import cannot be certified minimal for a source-selected
target that does not yet exist. This is only the intake's `M3` interface evidence, not an anchor
audit or proof credit.

The environment is Lean `4.29.0` at commit
`98dc76e3c0a9b856c9b98726b713fb04fab16740`, Lake `5.0.0-src+98dc76e`, and pinned mathlib revision
`8a178386ffc0f5fef0b77738bb5449d50efeea95` with tree
`bdc39a3123201dae413a9d9be56ec242c19e5c2b`. The automation-provided `.lake` symlink was used
read-only, and the mathlib package worktree remained clean. No update, build, clone, fetch, or other
dependency mutation was run.

## Validation Record

Commands ran in the isolated worker checkout on 2026-07-13 (Asia/Shanghai).

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, and 1546 uniform-L0 Lean 4 targets passed; execution skill present |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all `L0/rework_required` |
| `python3 scripts/stage1_target.py show THM-M-0224` | 0 | rank 1237; planned; no legacy slot; legacy artifacts unaccepted; theorem incomplete |
| `git status --short --untracked-files=all` (pre-edit); `git rev-parse HEAD 'HEAD^{tree}'` | 0 each | only the automation-provided `.lake` symlink was untracked; base revision and tree are recorded above |
| `git blame -L 1619,1624 -- Docs/researches/math_theorems.md` | 0 | all six sparse catalog fields originate at commit `bcf3f9fa79ab8c2b6610c9875668c2589b35b74f` |
| `cd Formalizations/Lean && lake env lean --version && lake --version` | 0 | Lean 4.29.0 and Lake 5.0.0 at the revisions above |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD 'HEAD^{tree}'`; package `status --short` | 0 each | pinned mathlib revision and tree above; package status output empty |
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0224/IntakeProbe.lean` | 0 | six substrate or named candidate interfaces elaborated; all three candidate axiom reports were `[propext, Classical.choice, Quot.sound]`; stdout SHA-256 `1bd42de80e934a818e37abdb3e3bde382b7b3f3696410f8790412dff8025a418` |
| bounded exact-topic `rg` search recorded in `statement-blocker.json` | 0 | candidates were confined to pinned complex Liouville and the intake probe; the Hamiltonian match explicitly excludes this namesake; discovery only |
| `python3 -B Stage1_Instances/THM-M-0224/check_intake.py` | 1 | known historical-intake freshness failure: the checker is bound to intake base `62fad55ced807fdc06921c45d6fcd1f9ad86a1c2`, not the current integrated HEAD; historical evidence was not rewritten |
| `python3 -m json.tool Stage1_Instances/THM-M-0224/statement-blocker.json`; scoped JSON invariant check | 0 each | identity, null target and imports, four undefined mutations, unchanged vector, false completion flags, and no-self-test boundary passed |
| prohibited-declaration scan over owned Lean files | 1 | expected no match: no `sorry`, `admit`, `sorryAx`, `axiom`, `constant`, `opaque`, or `unsafe` declaration |
| `git diff --check -- Stage1_Instances/THM-M-0224`; separate new-file checks recorded in the JSON | 0 / 1 each | no whitespace diagnostics; each no-index exit 1 is only the expected added-file difference |
| `test ! -e .stage1-worker-selftest.json` | 0 | self-test manifest intentionally absent because the exact-statement deliverable did not pass |

The historical intake checker is not represented as current statement evidence. Its receipt and
invariants are bound to the intake worker's earlier source snapshot. Rewriting that provisional
history is outside this phase and would not cure the missing proposition.

## Retry Condition And Status Boundary

The integration lane must master-accept the intake before an eventual accepted statement
transition. Accountable reviewers must preserve and hash a lawful immutable primary or
authoritative source, transcribe and independently approve its exact scalar or explicitly
generalized theorem with every incorporated definition, ordered binder, hypothesis, conclusion,
proof boundary, correction, erratum, transport, and boundary case. A later statement worker can
then encode only that claim, minimize its pinned imports, serialize and hash the elaborated
expression and environment, compile every credited transport, and run all four mutation classes.

This records the first failed gate. It does not complete the statement node or any downstream node.
The root remains `[H1, M3, R4]`; `audit_complete` and `theorem_complete` remain false, and no debt
change is proposed. The assigned phase is not genuinely self-tested to its completion gate, so no
`.stage1-worker-selftest.json`, node-specific completion receipt, worker `[_]`, proof credit, or
master-acceptance claim is emitted.
