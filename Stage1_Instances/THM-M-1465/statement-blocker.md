# THM-M-1465 exact-statement gate: blocked

Item: `S56-M-1465-STATEMENT`

Base revision: `1305c30bb297a27f8ce539ca8c0c90dc241aa6c7` (tree
`b77b52bf93cbd1927fd17f0d7f5bcab2eba3ab07`). Attempt date: 2026-07-13
(`Asia/Shanghai`).

## Decision

The statement item remains `[ ]`. Its prerequisite `S56-M-1465-INTAKE` is only provisional worker
state `[_]`: `intake-receipt.json` is unaccepted and non-content-addressed, has no accepted receipt
IDs, and binds an older repository revision and older blueprint and execution-DAG hashes. There is
no master-accepted dependency receipt. Section 10.2 of the rev-5.6 blueprint permits preparation of
later provisional evidence, but master closure remains dependency ordered.

Independently and decisively, the exact-source-statement gate fails. The complete repository record
is the method-family title `有限差分法` and the gloss `偏微分方程的差分离散`: finite-difference
discretization of partial differential equations. It supplies no cited proposition, PDE or PDE
class, domain, coefficients, forcing, initial or boundary data, solution notion, grid, stencil,
scheme, step restriction, hypotheses, ordered binders, conclusion, norm, constants, rate, arithmetic
model, or boundary cases. Stage0 explicitly leaves the exact definitions, premises, proof route,
dependencies, alternate statements, axiom policy, machine status, and artifacts open.

Materially inequivalent theorem families fit the gloss: consistency or order of a stencil,
solvability of a discrete elliptic system, stability or convergence of an elliptic scheme,
semidiscrete or fully discrete parabolic analysis, hyperbolic scheme analysis, a CFL result, or a
normed error estimate. A consistent stencil need not be stable, and a stable scheme need not be the
scheme intended by this catalog entry. Selecting a five-point Poisson result, a heat-equation
scheme, or any other familiar theorem would invent, narrow, broaden, or substitute
proposition-changing mathematics. The same-name ODE finite-difference scope belongs to
`THM-M-1395`; finite elements, finite volumes, Lax equivalence, CFL, and von Neumann stability also
have separate target ownership.

Consequently there is no canonical expression to elaborate and no honest minimal-import claim.
The canonical expression and environment fingerprints, checked alternate transports, and the
required removed-hypothesis, changed-domain, changed-binder-scope, and boundary-case mutations are
undefined, not passed. No `Statement.lean`, theorem declaration, proof body, weakened special case,
or broadened interface was added. The root remains `[H5, M4, R4]`; `H5` classifies the received
method gloss as not yet a stable proposition and does not refute correctly stated finite-difference
PDE results.

## Pinned Lean Boundary

The existing `IntakeProbe.lean` was re-elaborated with the pinned environment. Its direct imports
expose algebraic forward differences and Newton identities, the continuous finite-dimensional
Laplacian, and a generic one-dimensional Taylor remainder estimate. All eight checks elaborated,
and the three representative axiom reports contained only `propext`, `Classical.choice`, and
`Quot.sound`. These APIs define no grid, stencil, discrete PDE, scheme solution, stability relation,
convergence limit, or scheme-specific error estimate. They cannot be certified minimal for an
absent target and receive no statement or proof credit.

A bounded exact-topic search over the selected repo-local, pinned-mathlib, and owned Lean roots
matched only the intake probe's explanatory disclaimer. It located no source-identical
finite-difference PDE target declaration. This is narrow statement-feasibility evidence, not the
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
| `python3 scripts/stage1_target.py show THM-M-1465` | 0 | rank 1142; planned; no legacy slot; legacy artifacts unaccepted; theorem incomplete |
| pre-edit `git status --short --untracked-files=all`; `git rev-parse HEAD 'HEAD^{tree}'` | 0 | only the automation-provided `.lake` symlink was untracked; base revision and tree appear above |
| `git blame -L 10693,10698 -- Docs/researches/math_theorems.md` | 0 | all six sparse catalog lines originate at commit `bcf3f9fa79ab8c2b6610c9875668c2589b35b74f` |
| `git blame -L 10160,10165 -- Docs/researches/math_theorems.md` | 0 | the distinct same-name ODE record has the same origin and remains owned by `THM-M-1395` |
| authority, source, intake, probe, toolchain, lockfile, and relevant mathlib `sha256sum` checks | 0 | exact current hashes are preserved in `statement-blocker.json` |
| `cd Formalizations/Lean && lake env lean --version && lake --version` | 0 | pinned Lean and Lake versions recorded above |
| mathlib `git rev-parse HEAD 'HEAD^{tree}'` and package status | 0 | pinned revision and tree recorded above; package worktree clean |
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-1465/IntakeProbe.lean` | 0 | eight adjacent APIs elaborated; stdout SHA-256 `0fb3f7680e8022568a8b33d61a33607b80a50a786f02bc146f9495c724cee1f9`; empty stderr; no target declaration |
| bounded finite-difference PDE target-pattern search | 0 | only the probe disclaimer matched; output SHA-256 `007cabdd559e5b0a55d9e19b82e8e7baf7123ff337e93e5bc75a245896640ce4` |
| `python3 -B Stage1_Instances/THM-M-1465/check_intake.py` | 1 | the historical intake checker expects authoritative intake state `[ ]`, while integration now records provisional `[_]`; this phase records rather than rewrites stale intake evidence |
| prohibited-construct scan over owned Lean files | 1, expected no match | no `sorry`, `admit`, `sorryAx`, `axiom`, `constant`, `opaque`, or `unsafe` declaration |

Final JSON, invariant, whitespace, scoped-change, dependency-status, and absent-self-test checks are
recorded in the structured blocker beside this report.

## Retry Condition

The integration lane must master-accept refreshed intake evidence. Accountable reviewers must
lawfully preserve one immutable primary or approved authoritative source and independently select
one exact numbered proposition or explicitly sourced conjunction. They must map every incorporated
definition, assumption, proof boundary, correction, and erratum, and freeze the PDE, domain and
data, solution regularity, grid, stencil and scheme, mesh restrictions, ordered binders,
hypotheses, conclusion, norm, constants, arithmetic model, neighboring-target boundaries, and
every degenerate case.

A fresh statement worker may then encode precisely that reviewed claim, minimize its pinned
imports, serialize and hash the elaborated expression and environment, compile every credited
transport, and execute all four required mutation classes.

This is a truthful blocked statement attempt, not completion of this node or any downstream node.
Lifecycle remains `planned`; `audit_complete: false` and `theorem_complete: false`; no debt-vector
change is proposed. Because the exact-statement deliverable did not pass, no
`.stage1-worker-selftest.json`, statement receipt, worker `[_]`, proof credit, or master acceptance
is claimed.
