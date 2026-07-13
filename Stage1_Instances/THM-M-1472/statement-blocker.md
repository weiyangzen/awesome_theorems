# THM-M-1472 exact-statement gate: blocked

Item: `S56-M-1472-STATEMENT`

Base revision: `fc0de001c634823043636f9380a991c027e42533` (tree
`b2e4d058036a1e9ec56bfc6aa5de3b015efe6330`). Attempt date: 2026-07-13
(`Asia/Shanghai`).

## Decision

The statement item remains `[ ]`. Its prerequisite `S56-M-1472-INTAKE` is only provisional worker
state `[_]`: `intake-receipt.json` is unaccepted and non-content-addressed, has no accepted receipt
IDs, and binds an older repository revision and older blueprint and execution-DAG hashes. There is
no master-accepted dependency receipt. Section 10.2 of the rev-5.6 blueprint permits preparation of
later provisional evidence, but master closure remains dependency ordered.

Independently and decisively, the exact-source-statement gate fails. The complete repository record
is the title `Lax等价定理`, the Peter Lax attribution and 1956 date, and the slogan
`稳定性+相容性=收敛性`: stability plus consistency equals convergence. It gives no citation,
continuous or discrete problem, spaces, operators, restriction maps, step family, definitions,
ordered binders, hypotheses, direction, exact conclusion, norms, filters, time/data scope, boundary
cases, proof boundary, corrections, or formal artifact. Stage0 explicitly leaves the precise
definitions and premises, formal system, foundations, proof route, dependencies, alternate forms,
axiom policy, machine status, and artifact links open. The catalog's `已验证` label is untrusted
metadata under rev-5.6.

The likely historical source family is Lax and Richtmyer's 1956 paper *Survey of the stability of
linear finite difference equations*, but intake obtained bibliographic metadata only; publisher
full text returned HTTP 403. It did not inspect or admit a theorem/page text, incorporated
definitions and assumptions, direction, proof boundary, corrections, errata, or independent source
review. The catalog's Lax-only attribution also omits Richtmyer.

The inspected 2021 Tekriwal-Duraisamy-Jeannin result follows the generalized
Sanz-Serna-Palencia setting and proves one direction: consistency and stability imply convergence.
That does not select it as the repository's source-identical root. A classical formulation may
instead state that, for a consistent approximation to a properly posed linear problem, stability
is necessary and sufficient for convergence. Encoding the typography as
`(Stable and Consistent) iff Convergent`, using arbitrary `Prop` parameters, or silently adopting
the 2021 theorem would invent or substitute proposition-changing mathematics.

Consequently there is no canonical expression to elaborate and no honest minimal-import claim.
The canonical expression and environment fingerprints, checked alternate transports, and the
required removed-hypothesis, changed-domain, changed-binder-scope, and boundary-case mutations are
undefined, not passed. No `Statement.lean`, theorem declaration, proof body, weakened special case,
or broadened interface was added. The root remains `[H1, M4, R4]`.

## Pinned Lean Boundary

The existing `IntakeProbe.lean` was re-elaborated with the pinned environment. Its direct imports
expose operator-norm inequalities, Banach-Steinhaus, continuous-linear-map limit interfaces, and a
squeeze lemma. All six checks elaborated, and the two axiom reports contained only `propext`,
`Classical.choice`, and `Quot.sound`. Those APIs define no finite-difference approximation family
or source-selected consistency, stability, convergence, or equivalence predicate. They cannot be
certified minimal for an absent target and receive no statement or proof credit.

A bounded exact-topic search over the selected repo-local, pinned-mathlib, and owned Lean roots
matched only the intake probe's disclaimer and a legacy `THM-M-1551` PDE/spectral-bridge obligation
blocker in `Formalizations/Lean/AwesomeTheorems/Stage1/S1_M_210.lean`.
It located no source-identical Lax-Richtmyer target declaration. This is narrow
statement-feasibility evidence, not the downstream anchor audit and not a global absence claim.

The environment is Lean `4.29.0` at commit
`98dc76e3c0a9b856c9b98726b713fb04fab16740`, Lake `5.0.0-src+98dc76e`, and pinned mathlib revision
`8a178386ffc0f5fef0b77738bb5449d50efeea95` with tree
`bdc39a3123201dae413a9d9be56ec242c19e5c2b`. The automation-provided canonical `.lake` symlink was
used read-only. No dependency update, build, clone, fetch, or other `.lake` mutation was run.

## Validation Record

Commands ran from this isolated worker clone on 2026-07-13 (`Asia/Shanghai`).

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, and the execution skill passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all `L0/rework_required` |
| `python3 scripts/stage1_target.py show THM-M-1472` | 0 | rank 1149; planned; no legacy slot; legacy artifacts unaccepted; theorem incomplete |
| pre-edit `git status --short --untracked-files=all`; `git rev-parse HEAD 'HEAD^{tree}'` | 0 | only the automation-provided `.lake` symlink was untracked; base revision and tree appear above |
| `git blame -L 10742,10747 -- Docs/researches/math_theorems.md` | 0 | all six sparse catalog lines originate at commit `bcf3f9fa79ab8c2b6610c9875668c2589b35b74f` |
| `sha256sum Docs/Stage1_Blueprint_rev-5.6.md Docs/Stage1_Targets_rev-5.6.json Docs/Stage1_Execution_DAG_rev-5.6.json skills/execute-stage1-rev56/SKILL.md Docs/Blueprint_Guidelines.md Docs/researches/math_theorems.md Docs/Stage0_Blueprint.md Stage1_Instances/THM-M-1472/instance.json Stage1_Instances/THM-M-1472/source-statement-crosswalk.md Stage1_Instances/THM-M-1472/scope-map.md Stage1_Instances/THM-M-1472/task-dag.json Stage1_Instances/THM-M-1472/intake-receipt.json Stage1_Instances/THM-M-1472/IntakeProbe.lean Formalizations/Lean/lean-toolchain Formalizations/Lean/lake-manifest.json Formalizations/Lean/.lake/packages/mathlib/Mathlib/Analysis/Normed/Operator/Basic.lean Formalizations/Lean/.lake/packages/mathlib/Mathlib/Analysis/Normed/Operator/BanachSteinhaus.lean Formalizations/Lean/.lake/packages/mathlib/Mathlib/Analysis/Normed/Operator/Completeness.lean` | 0 | exact current hashes are preserved in `statement-blocker.json` |
| `cd Formalizations/Lean && lake env lean --version && lake --version` | 0 | pinned Lean and Lake versions recorded above |
| mathlib `git rev-parse HEAD 'HEAD^{tree}'` and package status | 0 | pinned revision and tree recorded above; package worktree clean |
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-1472/IntakeProbe.lean` | 0 | six adjacent APIs elaborated; stdout SHA-256 `b8e000af7bd6b5c69c599349fadef4c69b0ac10132d43c8aa62d158989add909`; empty stderr; no target declaration |
| bounded Lax-Richtmyer and Lax-equivalence target-pattern search | 0 | only the intake disclaimer and a legacy `THM-M-1551` PDE/spectral-bridge obligation blocker in `S1_M_210.lean` matched; output SHA-256 `17542602740db8be1ac07811ed4ef7873d88d68a2527875be465ec152a0e74e7` |
| `python3 -B Stage1_Instances/THM-M-1472/check_intake.py` | 1 | the historical intake checker expects authoritative intake `[ ]`/attempt 0, while integration now records provisional `[_]`/attempt 1; this phase records rather than rewrites stale intake evidence |
| prohibited-construct scan over owned Lean files | 1, expected no match | no `sorry`, `admit`, `sorryAx`, `axiom`, `constant`, `opaque`, or `unsafe` declaration |

Final JSON, invariant, whitespace, scoped-change, dependency-status, and absent-self-test checks are
recorded in the structured blocker beside this report.

## Retry Condition

The integration lane must master-accept refreshed intake evidence. Accountable reviewers must
lawfully preserve one immutable primary or approved authoritative source, settle corrected
Lax-Richtmyer attribution, and independently select one exact historical or generalized
proposition. They must map every incorporated definition, assumption, proof boundary, correction,
and erratum, and freeze the continuous and discrete problems, spaces, operators and comparison
maps, step family and filter, exact consistency/stability/convergence predicates, norms, direction,
time/data scope, ordered binders, foundation/TCB/computation profiles, neighboring-target
boundaries, alternate encodings, and every degenerate case.

A fresh statement worker may then encode precisely that reviewed claim, minimize its pinned
imports, serialize and hash the elaborated expression and environment, compile every credited
transport, and execute all four required mutation classes.

This is a truthful blocked statement attempt, not completion of this node or any downstream node.
Lifecycle remains `planned`; `audit_complete: false` and `theorem_complete: false`; no debt-vector
change is proposed. Because the exact-statement deliverable did not pass, no
`.stage1-worker-selftest.json`, statement receipt, worker `[_]`, proof credit, or master acceptance
is claimed.
