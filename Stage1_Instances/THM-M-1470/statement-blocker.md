# THM-M-1470 exact-statement gate: blocked

Item: `S56-M-1470-STATEMENT`

Base revision: `b4300806b9f337b5fa27a7787b8c0893eee48f30` (tree
`51afd3c8d2c9055c9e9e55e897cdb6b96037ce79`). Attempt date: 2026-07-13
(`Asia/Shanghai`).

## Decision

The statement item remains `[ ]`. Its prerequisite `S56-M-1470-INTAKE` is only provisional worker
state `[_]`: `intake-receipt.json` is unaccepted and non-content-addressed, has no accepted receipt
IDs, and binds an older repository revision and older blueprint and execution-DAG hashes. There is
no master-accepted dependency receipt. Section 10.2 of the rev-5.6 blueprint permits preparation of
later provisional evidence, but master closure remains dependency ordered.

Independently and decisively, the exact-source-statement gate fails. The complete repository record
is the title `后验误差估计`, the attribution Ivo Babuška (1971), and the gloss `数值解的误差估计`:
error estimation for a numerical solution. It supplies no continuous problem, exact solution,
discretization, numerical approximation, estimator, norm, inequality direction, constants,
oscillation terms, ordered binders, hypotheses, conclusion, or boundary cases. Stage0 explicitly
leaves exact definitions and premises, the proof route, dependencies, alternate statements, axiom
policy, formal system, machine status, and artifacts open.

Materially inequivalent theorem families fit the gloss: reliability, local or global efficiency,
a two-sided estimate with or without data oscillation, asymptotic exactness, estimator reduction,
adaptive contraction, or a stopping guarantee for one of many PDE, eigenvalue, time-stepping,
nonlinear, or iterative problems. Selecting any one would invent, narrow, broaden, or substitute
proposition-changing mathematics. Babuška's 1971 paper *Error-bounds for finite element method* is
a strong bibliographic lead, but the inspected metadata selects neither a theorem passage nor a
root proposition; no article definitions, assumptions, proof boundary, corrections, immutable
source admission, or independent statement review have been accepted.

Consequently there is no canonical expression to elaborate and no honest minimal-import claim.
The canonical expression and environment fingerprints, checked alternate transports, and the
required removed-hypothesis, changed-domain, changed-binder-scope, and boundary-case mutations are
undefined, not passed. No `Statement.lean`, theorem declaration, proof body, weakened special case,
or broadened interface was added. The root remains `[H5, M4, R4]`; `H5` classifies the received
theorem-family gloss as not yet a stable proposition and does not refute correctly stated a
posteriori error-estimation results.

## Pinned Lean Boundary

The existing `IntakeProbe.lean` was re-elaborated with the pinned environment. Its direct imports
expose coercive-form lower bounds and solvability, Hilbert projection minimality, and
`ContractingWith.aposteriori_dist_iterate_fixedPoint_le`. All six checks elaborated, and the three
representative axiom reports contained only `propext`, `Classical.choice`, and `Quot.sound`.

The first declarations are only adjacent variational substrate. The contraction declaration is a
genuine a posteriori estimate for fixed-point iterates, but it is source- and domain-mismatched with
the catalog's Babuška finite-element lead. None defines a source-selected PDE, mesh, numerical
solution, estimator, reliability or efficiency result. These imports cannot be certified minimal
for an absent target and receive no statement or proof credit.

A bounded exact-topic search over the selected repo-local, pinned-mathlib, and owned Lean roots
found only the fixed-point phrase match and explanatory prose. It located no source-selected
finite-element a posteriori estimator declaration. This is narrow statement-feasibility evidence,
not the downstream anchor audit or a global absence claim.

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
| `python3 scripts/stage1_target.py show THM-M-1470` | 0 | rank 1147; planned; no legacy slot; legacy artifacts unaccepted; theorem incomplete |
| pre-edit `git status --short --untracked-files=all`; `git rev-parse HEAD 'HEAD^{tree}'` | 0 | only the automation-provided `.lake` symlink was untracked; base revision and tree appear above |
| `git blame -L 10728,10733 -- Docs/researches/math_theorems.md` | 0 | all six sparse catalog lines originate at commit `bcf3f9fa79ab8c2b6610c9875668c2589b35b74f` |
| authority, source, intake, probe, toolchain, lockfile, and relevant mathlib `sha256sum` checks | 0 | exact current hashes are preserved in `statement-blocker.json` |
| `cd Formalizations/Lean && lake env lean --version && lake --version` | 0 | pinned Lean and Lake versions recorded above |
| mathlib `git rev-parse HEAD 'HEAD^{tree}'` and package status | 0 | pinned revision and tree recorded above; package worktree clean |
| `cd Formalizations/Lean && LC_ALL=C TZ=UTC lake env lean ../../Stage1_Instances/THM-M-1470/IntakeProbe.lean` | 0 | six adjacent APIs elaborated; stdout SHA-256 `df120f1610deea25c5cc7a9951c3f63bac55cf668102fe23072f435925161785`; no target declaration |
| bounded a posteriori and error-estimator target-pattern search | 0 | only the fixed-point phrase match and prose occurrences were found; output SHA-256 `b929bc0412e81d5a0890db65998c024ddfba5cc4181172d44290c3a3ec4a8a55`; no source-selected finite-element estimator declaration |
| `python3 -B Stage1_Instances/THM-M-1470/check_intake.py` | 1 | the historical intake validator expects authoritative intake state `[ ]`, while integration now records provisional `[_]`; this phase records rather than rewrites stale intake evidence |
| prohibited-construct scan over owned Lean files | 1, expected no match | no `sorry`, `admit`, `sorryAx`, `axiom`, `constant`, `opaque`, or `unsafe` declaration |

Final JSON, invariant, whitespace, scoped-change, dependency-status, and absent-self-test checks all
passed and are recorded in the structured blocker beside this report.

## Retry Condition

The integration lane must master-accept refreshed intake evidence. Accountable reviewers must
lawfully preserve one immutable primary or approved authoritative source and independently select
one exact numbered proposition or explicitly sourced conjunction. They must map every incorporated
definition, assumption, proof boundary, correction, and erratum, and freeze the problem, exact and
approximate solutions, discretization or iteration, estimator terms, norm, inequality direction,
constants, oscillation, ordered binders, hypotheses, conclusion, arithmetic boundary,
neighboring-target boundaries, alternate encodings, and every degenerate case.

A fresh statement worker may then encode precisely that reviewed claim, minimize its pinned
imports, serialize and hash the elaborated expression and environment, compile every credited
transport, and execute all four required mutation classes.

This is a truthful blocked statement attempt, not completion of this node or any downstream node.
Lifecycle remains `planned`; `audit_complete: false` and `theorem_complete: false`; no debt-vector
change is proposed. Because the exact-statement deliverable did not pass, no
`.stage1-worker-selftest.json`, statement receipt, worker `[_]`, proof credit, or master acceptance
is claimed.
