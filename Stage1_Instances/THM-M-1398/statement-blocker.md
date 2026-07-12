# Exact-statement gate: blocked

Item: `S56-M-1398-STATEMENT`

Theorem: `THM-M-1398`

Base revision: `2cf42e232e732b5d915dc077d91524b386861821` (tree
`f37ffb23dda888fedd3da7b2d7a8bbceaee21d44`).

## Decision

The statement item remains `[ ]`. Its prerequisite `S56-M-1398-INTAKE` has provisional worker state
`[_]`, not master-accepted state `[x]`, so the dependency gate independently prevents acceptance.
More fundamentally, the exact Lean 4 target cannot be truthfully elaborated because the complete
repository record is only the topic `刚性方程` ("stiff equations") and the gloss `刚性问题的数值解法`
("numerical solution of stiff problems"). This is not a truth-valued proposition.

The record supplies no definition of stiffness, scalar or system equation, state space, interval,
initial or boundary data, numerical method, grid, arithmetic or solver model, analytic assumptions,
ordered binders, conclusion, constants, or exceptional cases. It does not decide whether the
desired conclusion is well-definedness, consistency, order, absolute stability, convergence, a
local or global error estimate, stiffness-independent behavior, or complexity. These choices yield
materially different claims.

Curtiss and Hirschfelder's 1952 paper *Integration of Stiff Equations* is an historical
source-family lead recorded by intake, not a catalog-cited or approved proposition. No immutable
edition, exact theorem/page, incorporated-definition crosswalk, proof boundary, errata disposition,
or independent approval has been admitted. Selecting backward Euler on a scalar test equation,
Runge-Kutta, a multistep or BDF result, or a convenient convergence theorem would therefore
substitute missing mathematics. `THM-M-1399` separately owns backward differentiation formulas;
`THM-M-1476`, `THM-M-1477`, and `THM-M-1478` separately own stiff, A-, and L-stability. They cannot
silently select this root.

Consequently there is no canonical human theorem proposition from which to derive a minimal import,
normalized kernel-expression fingerprint, checked alternate transport, or meaningful
removed-hypothesis, changed-domain, changed-binder-scope, and boundary-case mutations. All four
mutation classes are undefined rather than passed. No `Statement.lean`, theorem declaration,
axiom, placeholder, weakened special case, broadened interface, or circular assumed package was
added. The first substantive statement failure is exact source-statement and scope identity, and
the root remains `[H5, M4, R4]`.

## Pinned Lean boundary

The existing `IntakeProbe.lean` directly imports `Mathlib.Analysis.ODE.Basic`,
`Mathlib.Analysis.ODE.Gronwall`, and `Mathlib.Analysis.ODE.PicardLindelof`. It re-elaborates nine
generic integral-curve, Gronwall, trajectory-comparison, uniqueness, and exact-solution existence
interfaces. These declarations neither define stiffness nor select or verify a discrete numerical
method. The successful probe is discovery-only feasibility evidence. Its imports cannot be
certified minimal for a canonical target that does not exist.

A bounded source search of pinned mathlib analysis files and repository-local Lean files found no
exact-topic declaration under the searched stiff-equation, A-stability, multistep, Runge-Kutta, or
BDF terms. This is not the downstream immutable anchor audit and is not a global absence claim.

The environment is Lean `4.29.0` at commit
`98dc76e3c0a9b856c9b98726b713fb04fab16740`, Lake `5.0.0-src+98dc76e`, and pinned mathlib revision
`8a178386ffc0f5fef0b77738bb5449d50efeea95` with tree
`bdc39a3123201dae413a9d9be56ec242c19e5c2b`. The `lean-toolchain` SHA-256 is
`651c8accb402b0c071cd336e9d3dc0a55516b1bfb434ddc4801f14936785b1d2`, the
`lake-manifest.json` SHA-256 is
`321626c846f14bcae3019c2fa6fb25a8fe879c21094d22bf30badb3335cb2d81`, and the probe's complete
stdout SHA-256 is `c31836a6fb98c9f0b4fcee5047457856c21182a3315540cefd91b982962c620a`.

The automation-provided `Formalizations/Lean/.lake` link points to canonical pinned artifacts and
was used read-only. No `lake update`, `lake build`, dependency clone/fetch, or other `.lake` mutation
was run.

## Validation evidence

Commands ran in this worker clone on 2026-07-13 (Asia/Shanghai).

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, and 1546 uniform-L0 targets passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all `L0/rework_required` |
| `python3 scripts/stage1_target.py show THM-M-1398` | 0 | rank 1008; planned; no legacy slot; legacy artifacts unaccepted; theorem incomplete |
| `git status --short --untracked-files=all` and `git rev-parse HEAD 'HEAD^{tree}'` (pre-edit) | 0 | only the automation-provided `.lake` symlink was untracked; base revision and tree appear above |
| scoped catalog, Stage0, manifest, blueprint, DAG, skill, guidelines, and intake inspection | 0 | found only the topic/gloss, explicit null target, and proposition-changing open decisions; no source-selected proposition |
| `sha256sum` over authority, intake, source, probe, toolchain, and pinned-environment inputs | 0 | hashes are recorded in `statement-blocker.json` |
| `python3 -B Stage1_Instances/THM-M-1398/check_intake.py` | 1 | known phase-evolution failure: the intake checker still asserts authoritative state `[ ]`, while integration advanced intake provisionally to `[_]`; historical evidence was not rewritten |
| `cd Formalizations/Lean && lake env lean --version && lake --version` | 0 | pinned Lean and Lake versions recorded above |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD 'HEAD^{tree}'` and package status | 0 | pinned mathlib revision and tree recorded above; package worktree clean |
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-1398/IntakeProbe.lean` | 0 | all nine generic adjacent APIs elaborated; no canonical target was declared |
| bounded exact-topic search for stiffness and named numerical-method terms | 1 | expected no-match result in the searched pinned and repository-local Lean sources; discovery-only evidence |
| prohibited-construct scan over owned Lean files | 1 | expected no-match result; no `sorry`, `admit`, `sorryAx`, `axiom`, `constant`, `opaque`, or `unsafe` declaration |
| `python3 -m json.tool Stage1_Instances/THM-M-1398/statement-blocker.json` and scoped invariant assertions | 0 each | valid JSON; identity, null target, unchanged vector, undefined mutations, false completion flags, exact change scope, and absent self-test agree |
| `git diff --check` plus per-new-file `git diff --no-index --check` | 0; 1 each | no whitespace diagnostics; both no-index exits are only the expected new-file differences |
| `test ! -e .stage1-worker-selftest.json` | 0 | self-test manifest intentionally absent because the exact-statement deliverable did not pass |

## Retry condition and status boundary

The integration lane must first accept the intake dependency. Accountable reviewers must then
preserve and hash an immutable primary or authoritative edition, select and independently approve
one exact root theorem or explicit conjunction, and transcribe every incorporated definition,
ordered binder, hypothesis, conclusion, constant, exceptional case, proof boundary, correction,
and erratum. The selection must freeze the stiffness criterion, equation and data model, exact
method and coefficients, grid, arithmetic and solver policy, analytic assumptions, conclusion, and
boundaries with the BDF and stability targets.

A fresh statement run can then encode precisely that source-selected claim, minimize pinned
imports, serialize and hash its elaborated expression and environment, compile every credited
transport, and run all four required mutation classes.

This blocker is the assigned phase's truthful result, not completion of the statement node or any
downstream node. Lifecycle remains `planned`; `audit_complete: false` and
`theorem_complete: false`; no debt-vector change is proposed. Because the exact-statement
deliverable did not pass, no `.stage1-worker-selftest.json`, statement receipt, worker `[_]`, or
master acceptance is claimed.
