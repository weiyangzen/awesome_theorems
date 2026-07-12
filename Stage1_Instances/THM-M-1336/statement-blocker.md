# Exact-statement gate: blocked

Item: `S56-M-1336-STATEMENT`

Theorem: `THM-M-1336`

Base revision: `8bbb7ffdbb5e6e8e3e1ffaba9955137f6b68c76c` (tree
`ade61913e5912b1160e25afe096df7f5b3b0cfed`)

Verdict: `blocked`

## Decision

The exact Lean 4 target cannot be truthfully selected or elaborated from the authoritative
repository record. Its complete mathematical wording is the generic title `比较定理`
(`comparison theorem`) and the gloss `微分不等式与解的比较` (`comparison of differential
inequalities and solutions`). It provides no source, definition, formula, ordered binder,
hypothesis, conclusion, or boundary convention. Stage0 explicitly leaves the exact definitions
and premises open, and the catalog's `已验证` label is untrusted under rev-5.6.

At least the following materially different roots remain compatible with that wording:

- a scalar fencing theorem comparing differentiable functions directly;
- a scalar subsolution/supersolution theorem for `y' = F(t,y)`;
- an order-preservation result for a cooperative or quasimonotone system;
- a quantitative distance estimate for exact or approximate ODE trajectories; or
- a Gronwall-like differential or integral inequality.

Those formulations differ in state space, interval, derivative and solution notions, vector-field
regularity, Lipschitz or monotonicity assumptions, initial order, strictness, and conclusion. The
last family also overlaps the separately cataloged Gronwall and Bihari-LaSalle targets
`THM-M-1337` and `THM-M-1338`. Selecting a familiar formulation would therefore invent or
substitute mathematics rather than elaborate the exact received theorem.

The first failed substantive gate is exact source-statement identity under rev-5.6 sections 5 and
5.1. Independently, the prerequisite `S56-M-1336-INTAKE` is only provisional `[_]`: its receipt is
unsigned, non-content-addressed, and `accepted: false`, so the statement node cannot be
dependency-legally accepted until the intake is master-accepted. No canonical human claim,
minimal target import, expression fingerprint, checked transport, or statement mutation can be
produced. Removed-hypothesis, changed-domain, changed-binder-scope, and boundary-case mutations
are undefined, not passed. The root remains `[H5, M4, R4]`.

## Pinned Lean Boundary

The existing `IntakeProbe.lean` was re-elaborated under the pinned environment. It imports
`Mathlib.Analysis.Calculus.MeanValue` and `Mathlib.Analysis.ODE.Gronwall` and prints seven
materially different declarations:

- scalar strict first-contact and weak derivative fencing theorems;
- scalar and norm-valued Gronwall bounds;
- approximate- and exact-trajectory distance estimates; and
- ODE solution uniqueness.

This confirms that the Lean environment is available while illustrating the unresolved theorem
choice. The probe declares no target, supplies no source identity or proof credit, and its imports
cannot be certified minimal for an absent canonical proposition. A bounded search of pinned
mathlib's ODE and calculus sources found the fencing and Gronwall families but no source-selected
subsolution, supersolution, quasimonotone-system, or generic comparison-principle declaration.
That search is discovery-only evidence, not the downstream anchor audit or proof of global
absence.

The environment is Lean `4.29.0` at commit
`98dc76e3c0a9b856c9b98726b713fb04fab16740`, Lake `5.0.0-src+98dc76e`, and pinned mathlib
revision `8a178386ffc0f5fef0b77738bb5449d50efeea95` with tree
`bdc39a3123201dae413a9d9be56ec242c19e5c2b`. The automation-provided
`Formalizations/Lean/.lake` symlink was used read-only. No update, build, clone, fetch, or
dependency mutation was run.

## Validation Record

Commands ran from this worker clone on 2026-07-13 (`Asia/Shanghai`).

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, and 1546 uniform-L0 Lean 4 targets passed; execution skill present |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all `L0/rework_required` |
| `python3 scripts/stage1_target.py show THM-M-1336` | 0 | rank 947; planned; no legacy slot; legacy artifacts unaccepted; theorem incomplete |
| `git status --short --untracked-files=all`; `git rev-parse HEAD`; `git rev-parse 'HEAD^{tree}'` (pre-edit) | 0 | only the automation-provided `.lake` symlink was untracked; base revision and tree appear above |
| `git blame -L 9747,9752 -- Docs/researches/math_theorems.md` and repository source search | 0 | the uncited six-line catalog record originates at `bcf3f9fa...`; no proposition-level source was found |
| `cd Formalizations/Lean && lake env lean --version && lake --version` | 0 | pinned Lean and Lake versions recorded above |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD 'HEAD^{tree}'` | 0 | pinned mathlib revision and tree recorded above; package status was clean |
| `sha256sum` over authority, source, intake, probe, toolchain, and candidate mathlib inputs | 0 | hashes recorded in `statement-blocker.json` |
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-1336/IntakeProbe.lean` | 0 | all seven adjacent scalar fencing, Gronwall, trajectory-comparison, and uniqueness declarations elaborated; no target theorem was declared |
| bounded pinned-mathlib search over comparison, sub/supersolution, quasimonotone, fencing, and trajectory terms | 0 | found the known inequivalent fencing and trajectory families; no source-selected canonical result |
| `python3 -B Stage1_Instances/THM-M-1336/check_intake.py` | 1 | historical intake replay rejected a stale recorded blueprint hash after integration changed intake states; this statement run does not rewrite accepted historical evidence |
| prohibited-construct `rg` scan over owned Lean files | 1 | expected no-match result; no `sorry`, `admit`, `sorryAx`, `axiom`, `constant`, `opaque`, or `unsafe` declaration |
| `python3 -m json.tool Stage1_Instances/THM-M-1336/statement-blocker.json` plus scoped blocker invariants | 0 | identity, dependency state, null target/imports, four undefined mutations, unchanged vector, false completion flags, and no-self-test boundary agree |
| scoped whitespace checks for both new files and `git diff --check -- Stage1_Instances/THM-M-1336` | 0 | no whitespace diagnostics |
| `test ! -e .stage1-worker-selftest.json` | 0 | self-test manifest intentionally absent because the exact-statement deliverable did not pass |

The integrated historical intake checker is bound to the earlier authority-file bytes and its
original nine-file artifact inventory. The integration lane subsequently changed the generated
intake states, so replay now fails before the inventory assertion. Adding these two statement
artifacts would also make that frozen intake-only inventory stale. This statement run records the
limitation instead of rewriting the intake checker, intake receipt, instance, task DAG, generated
blueprint, or authoritative execution DAG to manufacture agreement.

## Retry Condition And Status Boundary

The integration lane must first master-accept the intake dependency. Accountable reviewers must
then preserve and hash a lawful immutable primary or authoritative source, select one exact
comparison theorem, transcribe every incorporated definition, ordered binder, premise, conclusion,
proof boundary, correction, erratum, and degenerate case, and independently approve both the
source-to-target mapping and separation from `THM-M-1337` and `THM-M-1338`.

A later statement worker can encode that same claim with concrete Lean definitions, minimize its
pinned imports, serialize and hash the elaborated expression and environment, compile each
credited transport, and execute all four required mutation classes.

This blocker is the assigned phase's truthful result, not completion of the statement node or a
downstream node. Lifecycle remains `planned`; `audit_complete: false` and
`theorem_complete: false`; no debt-vector change is proposed. Because the exact-statement
deliverable did not pass, no `.stage1-worker-selftest.json`, statement receipt, worker `[_]`, or
master acceptance is claimed.
