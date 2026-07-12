# Exact-statement gate: blocked

Item: `S56-M-0897-STATEMENT`

Theorem: `THM-M-0897`

Base revision: `5c38e670073bc890a78e61556f36d2c6b35d257d`

Base tree: `95a189ecdfe548d9cff4faaebc111079babceb92`

## Decision

No exact Lean 4 target can be truthfully elaborated from the authoritative repository record. Its
complete mathematical wording is the family label `设计理论` (design theory) and the gloss
`组合设计的存在性` (existence of combinatorial designs), attributed only to many mathematicians
in the twentieth century. This describes a subject and an existence-problem family, not one
truth-valued proposition with fixed domains, ordered binders, hypotheses, and conclusion.

The wording does not choose a `t-(v,k,lambda)` design, balanced incomplete block design, pairwise
balanced design, Steiner system, resolvable or group-divisible design, covering, packing,
Latin-square design, or another design class. It also leaves open the point and block encoding,
parameter domains, incidence and admissibility conditions, repeated-block multiplicity, simplicity,
exact versus asymptotic regime, and every empty, zero, singleton, trivial-block, and vacuous case.
These choices produce inequivalent theorems rather than alternate notations for one theorem.

The catalog immediately schedules several plausible readings as separate targets:

- `THM-M-0898` owns the Kirkman schoolgirl and Steiner triple-system existence target.
- `THM-M-0899` owns the named Wilson `t`-design existence target.
- `THM-M-0900` owns the named asymptotic design-existence target.
- `THM-M-0901` owns Latin-square existence and counting.

Selecting any familiar result would therefore invent or substitute proposition-changing
mathematics and could absorb a neighboring target. The catalog status `已验证` is explicitly
untrusted under rev-5.6 and supplies neither source nor kernel evidence.

The existing intake correctly leaves `canonical_statement`, `canonical_claim`, the Lean module and
expression, the elaborated-expression hash, and the target environment fingerprint null. Its
worker receipt is provisional `[_]`, has `accepted: false`, and has no accepted receipt ID. Section
5 of the rev-5.6 blueprint makes statement ambiguity and a missing expression fingerprint hard
blockers. With no canonical proposition, minimal target imports, checked alternate transports, and
the required removed-hypothesis, changed-domain, changed-binder-scope, and boundary-case mutations
are undefined rather than failed Lean tests. The root remains `[H5, M4, R4]`; no statement or
theorem completion is claimed.

## Pinned Lean Boundary

The discovery-only `IntakeProbe.lean` imports `Mathlib.Combinatorics.SetFamily.LYM` and checks
`Finset.powersetCard`, `Finset.card_powersetCard`, `Finset.falling`, `Finset.mem_falling`,
`Set.Sized`, `Nat.choose`, and `Fintype.card`. It re-elaborates under the pinned environment. These
are generic finite set-family and counting interfaces only: they define no combinatorial design,
choose no parameters, state no existence theorem, and contain no proof of one. The probe import is
therefore not claimed to be minimal for the absent canonical target.

A bounded exact-name search found no `BlockDesign`, `BalancedIncompleteBlockDesign`,
`CombinatorialDesign`, `SteinerSystem`, `SteinerTripleSystem`, or `TDesign` declaration in pinned
mathlib or repository-local Lean. This is narrow feasibility evidence, not the downstream exhaustive
anchor audit or a claim of global absence.

The environment is Lean `4.29.0` at commit
`98dc76e3c0a9b856c9b98726b713fb04fab16740`, Lake `5.0.0-src+98dc76e`, and pinned mathlib revision
`8a178386ffc0f5fef0b77738bb5449d50efeea95` with tree
`bdc39a3123201dae413a9d9be56ec242c19e5c2b`. The pre-existing `Formalizations/Lean/.lake` link to
the canonical pinned artifacts was used read-only. No update, build, clone, fetch, or dependency
mutation was run.

## Validation Evidence

Commands ran in this worker clone on `2026-07-13` (`Asia/Shanghai`). Lean commands ran from
`Formalizations/Lean`; all others ran from the repository root unless noted.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, and the execution skill passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all `L0/rework_required` |
| `python3 scripts/stage1_target.py show THM-M-0897` | 0 | rank 1039; planned; no legacy slot; legacy artifacts unaccepted; theorem incomplete |
| `git status --short --untracked-files=all`; `git rev-parse HEAD 'HEAD^{tree}'` before edits | 0 | only the automation-provided `.lake` symlink was untracked; base revision and tree appear above |
| scoped reads of the blueprint, skill, manifest, catalog, Stage0 record, and complete intake dossier | 0 | the family label is not a source-complete proposition; the intake intentionally leaves its canonical statement and formal target null |
| `sha256sum` over authority, intake, toolchain, lockfile, and probe inputs | 0 | exact current digests are recorded in `statement-blocker.json` |
| `lake env lean --version`; `lake --version` | 0 | pinned Lean and Lake versions recorded above |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD 'HEAD^{tree}'` and package status | 0 | pinned mathlib revision and tree recorded above; package worktree clean |
| `lake env lean ../../Stage1_Instances/THM-M-0897/IntakeProbe.lean` | 0 | seven adjacent pinned APIs elaborated; output SHA-256 `f11f4ea2a142713a4343feba8ce7001713683cddf301fcd30ae0937ae18fcf5a`; no target or proof body was declared |
| bounded exact-design declaration search in pinned mathlib and repo-local Lean | 1 | expected no-match exit; discovery-only feasibility evidence |
| `python3 -B Stage1_Instances/THM-M-0897/check_intake.py` | 1 | historical intake replay stops on a stale blueprint input hash after integration changed authority bytes; its original nine-file inventory is also historical after this phase |
| `python3 -m json.tool Stage1_Instances/THM-M-0897/statement-blocker.json` plus scoped blocker assertions | 0 | identity, null target/imports, unchanged vector, four undefined mutations, false completion flags, exact changed paths, and no-self-test boundary agree |
| prohibited-construct scan over owned Lean files | 1 | expected no-match result; no `sorry`, `admit`, `sorryAx`, `axiom`, `constant`, `opaque`, or `unsafe` declaration |
| scoped whitespace checks for both new files and `git diff --check -- Stage1_Instances/THM-M-0897` | 0 | no whitespace diagnostics |
| `test ! -e .stage1-worker-selftest.json` | 0 | self-test manifest intentionally absent because the exact-statement deliverable did not pass |

The intake checker is frozen to the inputs and nine-file inventory of the earlier provisional intake
attempt. The integration lane later changed the generated blueprint and DAG, so replay already
fails its stored blueprint digest. Adding these two statement artifacts also makes its intake-only
inventory historical. This statement run records that limitation instead of rewriting the intake
checker, intake receipt, instance, task DAG, generated blueprint, or authoritative execution DAG to
manufacture agreement.

## Retry Condition And Status Boundary

Accountable reviewers must preserve and hash an immutable primary or authoritative source, select
and independently approve one exact truth-valued design-existence proposition, and transcribe every
incorporated definition, ordered binder, hypothesis, conclusion, proof boundary, correction, and
boundary case. They must also issue accountable boundary decisions for `THM-M-0898` through
`THM-M-0901`. The integration lane must master-accept the intake dependency before it can accept a
future statement transition.

A fresh statement worker can then encode exactly that source-selected claim, minimize pinned
imports, serialize and hash the elaborated expression and environment, compile every credited
transport, and execute all four required mutation classes.

This blocker is the assigned phase's truthful result, not completion of the statement node or any
downstream node. Lifecycle remains `planned`; `audit_complete: false` and
`theorem_complete: false`; no debt-vector change is proposed. Because the exact-statement
deliverable did not pass, no `.stage1-worker-selftest.json`, statement receipt, worker `[_]`, or
master acceptance is claimed.
