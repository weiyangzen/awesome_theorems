# THM-M-1475 exact-statement gate: blocked

Item: `S56-M-1475-STATEMENT`

Base revision: `fc0de001c634823043636f9380a991c027e42533` (tree
`b2e4d058036a1e9ec56bfc6aa5de3b015efe6330`). Attempt date: 2026-07-13
(`Asia/Shanghai`).

## Decision

The statement item remains `[ ]`. Its prerequisite `S56-M-1475-INTAKE` is only provisional worker
state `[_]`: the intake receipt is unaccepted and non-content-addressed, has no accepted receipt
IDs, and binds an older repository revision and older blueprint and execution-DAG hashes. There is
no master-accepted dependency receipt. Section 10.2 of the rev-5.6 blueprint permits preparation
of later provisional evidence, but master closure remains dependency ordered.

Independently and decisively, the exact-source-statement gate fails. The complete repository record
is the title `龙格-库塔法的稳定性`, the attribution "many mathematicians" in the twentieth century,
and the gloss `RK方法的稳定性区域` (stability regions of Runge-Kutta methods). It supplies no
truth-valued proposition, Runge-Kutta tableau, stage or update equation, problem class, stability
notion, complex parameter convention, function domain, predicate, conclusion, ordered binders, or
boundary cases. Stage0 explicitly leaves exact definitions and premises, proof route, formal
system, axioms, machine status, and artifacts open.

Materially inequivalent claims fit the gloss: an amplification recurrence for the scalar test
equation, a general-tableau stability-function formula, a definition of absolute stability or its
region, a region equality or inclusion for a named method, or an A-, L-, B-, algebraic,
contractive, internal, linear-system, or nonlinear stability result. Selecting the general rational
formula, explicit Euler, RK4, Gauss, Radau, or any other branch would invent, narrow, broaden, or
substitute proposition-changing mathematics. Hairer-Wanner, Driscoll-Braun, and Butcher are useful
source-family leads, but the catalog selects no proposition from them and no exact statement,
incorporated definitions, corrections, proof boundary, immutable source admission, or independent
review has been accepted. Neighboring targets separately own the general Runge-Kutta family, von
Neumann analysis, stiff stability, A-stability, and L-stability.

Consequently there is no canonical expression to elaborate and no honest minimal-import claim.
The canonical expression and target-environment fingerprints, checked alternate transports, and
the required removed-hypothesis, changed-domain, changed-binder-scope, and boundary-case mutations
are undefined, not passed. No `Statement.lean`, theorem declaration, proof body, weakened special
case, or broadened interface was added. The root remains `[H5, M4, R4]`; `H5` classifies the
received topic gloss as not yet a stable proposition and does not refute correctly stated
Runge-Kutta stability theorems.

## Pinned Lean Boundary

The existing `IntakeProbe.lean` was re-elaborated with the pinned environment. Its four direct
imports expose complex norms, finite matrices and matrix-vector multiplication, rational-function
evaluation, and analytic ODE predicates. All ten checks elaborated. None defines a Runge-Kutta
tableau, step equation, stability function, stability predicate, or source-selected conclusion.
These imports therefore cannot be certified minimal for an absent target and receive no statement
or proof credit.

A bounded exact-topic search over the selected repo-local and pinned-mathlib Lean roots found no
Runge-Kutta, Butcher-tableau, absolute-stability, stability-function, or stability-region
declaration under the recorded terms. This is narrow statement-feasibility evidence, not the
downstream anchor audit or a global absence claim.

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
| `python3 scripts/stage1_target.py show THM-M-1475` | 0 | rank 1152; planned; no legacy slot; legacy artifacts unaccepted; theorem incomplete |
| pre-edit `git status --short --untracked-files=all`; `git rev-parse HEAD 'HEAD^{tree}'` | 0 | only the automation-provided `.lake` symlink was untracked; base revision and tree appear above |
| `git blame -L 10763,10768 -- Docs/researches/math_theorems.md` | 0 | all six sparse catalog lines originate in commit `bcf3f9fa79ab8c2b6610c9875668c2589b35b74f` |
| authority, source, intake, probe, toolchain, lockfile, and relevant mathlib `sha256sum` checks | 0 | exact current hashes are preserved in `statement-blocker.json` |
| `cd Formalizations/Lean && lake env lean --version && lake --version` | 0 | pinned Lean and Lake versions recorded above |
| mathlib `git rev-parse HEAD 'HEAD^{tree}'` and package status | 0 | pinned revision and tree recorded above; package worktree clean |
| `cd Formalizations/Lean && LC_ALL=C TZ=UTC lake env lean ../../Stage1_Instances/THM-M-1475/IntakeProbe.lean` | 0 | ten adjacent APIs elaborated; stdout SHA-256 `92a7ac79a0315e35b078aace6e8a560bfac0d396f40e85e2b37697c68956a9ad`; no target declaration |
| bounded exact-topic Lean search | 1, expected no match | empty output; SHA-256 `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`; no matching declaration in the searched repo-local or pinned-mathlib roots |
| `python3 -B Stage1_Instances/THM-M-1475/check_intake.py` | 1 | historical intake validator expects authoritative intake state `[ ]`, while integration now records provisional `[_]`; this phase records rather than rewrites stale intake evidence |
| prohibited-construct scan over owned Lean files | 1, expected no match | no `sorry`, `admit`, `sorryAx`, `axiom`, `constant`, `opaque`, or `unsafe` declaration |

Final JSON, invariant, whitespace, scoped-change, dependency-status, and absent-self-test checks also
passed and are recorded in the structured blocker beside this report.

## Retry Condition

The integration lane must master-accept refreshed intake evidence. Accountable reviewers must then
preserve and hash one immutable primary or approved authoritative source and independently select
one exact numbered proposition or explicitly sourced conjunction. They must map every incorporated
definition, assumption, proof boundary, correction, and erratum, and freeze the Runge-Kutta
scheme, stage and update equations, equation class, stability notion, scalar and step conventions,
implicit-domain and pole treatment, predicate and boundary convention, ordered binders,
hypotheses, conclusion, neighboring-target ownership, arithmetic model, and all degenerate cases.

A fresh statement worker may then encode precisely that reviewed claim, minimize its pinned
imports, serialize and hash the elaborated expression and environment, compile every credited
transport, and execute all four required mutation classes.

This is a truthful blocked statement attempt, not completion of this node or any downstream node.
Lifecycle remains `planned`; `audit_complete: false` and `theorem_complete: false`; no debt-vector
change is proposed. Because the exact-statement deliverable did not pass, no
`.stage1-worker-selftest.json`, statement receipt, worker `[_]`, proof credit, or master acceptance
is claimed.
