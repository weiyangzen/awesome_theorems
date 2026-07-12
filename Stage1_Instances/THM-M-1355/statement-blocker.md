# Exact-statement gate: blocked

Item: `S56-M-1355-STATEMENT`

Theorem: `THM-M-1355`

Base revision: `0d26adeae663d55eb536120f7d93ede975fe8f49` (tree
`6b5ab44050900e9a4a181b4fc56b1e965183f2c9`).

Verdict: `blocked`

## Decision

The exact Lean 4 target cannot be truthfully selected or elaborated from the authoritative
repository record. Its complete mathematical wording is the title `线性系统的稳定性` (stability of
linear systems) and the gloss `线性系统的稳定性判据` (a stability criterion for linear systems),
with a broad twentieth-century attribution. It gives no citation, equation, definition, ordered
binder, hypothesis, conclusion, proof boundary, correction history, or boundary convention. The
catalog's `已验证` label is untrusted under rev-5.6, and Stage0 explicitly leaves the exact
definitions and premises open.

The wording names a theorem family, not one truth-valued proposition. It does not choose:

- continuous or discrete time, autonomous or time-varying dynamics, or a semigroup;
- a homogeneous state equation, affine system, forced system, or input-output/control system;
- finite-dimensional real or complex coordinates or an infinite-dimensional state space;
- a solution carrier, time interval, equilibrium, existence policy, or completeness assumption;
- bounded, Lyapunov, asymptotic, exponential, uniform, marginal, BIBO, or input-to-state stability;
- a spectral, Jordan, matrix-exponential, Lyapunov-matrix, coefficient, resolvent, or frequency
  criterion; or
- a necessary, sufficient, or iff direction, its quantifier order, or its boundary cases.

The intake-recorded modern source lead makes the ambiguity concrete. Teschl's *Ordinary
Differential Equations and Dynamical Systems* separates bounded forward stability, whose spectral
criterion includes a semisimplicity condition on the imaginary-axis boundary, from asymptotic or
exponential stability, whose finite-dimensional autonomous criterion requires strictly negative
real parts. The catalog does not cite Teschl or select either result. It also does not exclude a
discrete-time, Lyapunov-equation, time-varying, controlled, or semigroup theorem. The source lead
has not received a complete assumption/proof/errata crosswalk or independent `H0` review.

Choosing a familiar Hurwitz or eigenvalue formulation would therefore add proposition-changing
mathematics. It could also consume the separately owned Floquet, characteristic-exponent,
Routh-Hurwitz, Nyquist, general Lyapunov-stability, or indirect-method targets. Rev-5.6 sections 5
and 5.1 make statement ambiguity and a missing expression fingerprint hard blockers.

Consequently there is no honest canonical declaration for which minimal imports can be claimed.
No `Statement.lean`, canonical expression, checked alternate transport, or mutation suite was
created. The required removed-hypothesis, changed-domain, changed-binder-scope, and boundary-case
mutations are undefined rather than passed. The lifecycle remains `planned`, and the root remains
`[H1, M4, R4]`.

The prerequisite `S56-M-1355-INTAKE` is also provisional `[_]`, not master-accepted `[x]`. Its
receipt is non-content-addressed, declares `accepted: false`, and contains no accepted receipt ID.
Rev-5.6 section 10.2 permits this dependency-ordered blocker investigation, but master acceptance
of a current intake remains required before any future statement transition can be accepted.

## Pinned Lean Boundary

The existing `IntakeProbe.lean` was re-elaborated under the pinned environment. Its direct imports
expose matrix-exponential algebra, finite-dimensional eigenvalue/spectrum interfaces, and generic
integral-curve predicates. All ten checks elaborate. The probe defines no linear-system solution
model, stability predicate, canonical criterion, source transport, or proof body. Its imports
therefore cannot be certified minimal for an absent target.

A bounded search of the repository-local Lean tree and the pinned mathlib ODE, matrix-exponential,
and linear-algebra sources found no declaration under the recorded linear-system stability,
Hurwitz-stability, asymptotic-stability, or exponential-stability terms. A target-ID/title search
also found no local declaration. These are discovery observations, not the downstream immutable
anchor audit and not a global absence claim.

The environment is Lean `4.29.0` at commit
`98dc76e3c0a9b856c9b98726b713fb04fab16740`, Lake `5.0.0-src+98dc76e`, and pinned mathlib
revision `8a178386ffc0f5fef0b77738bb5449d50efeea95` with tree
`bdc39a3123201dae413a9d9be56ec242c19e5c2b`. The automation-provided
`Formalizations/Lean/.lake` symlink was used read-only. No update, build, dependency clone, fetch,
or other `.lake` mutation was run.

## Validation Record

Commands ran in this isolated worker clone on 2026-07-13 (`Asia/Shanghai`).

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, and 1546 uniform-L0 Lean 4 targets passed; execution skill present |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all `L0/rework_required` |
| `python3 scripts/stage1_target.py show THM-M-1355` | 0 | rank 965; planned; no legacy slot; legacy artifacts unaccepted; theorem incomplete |
| `git status --short --untracked-files=all`; `git rev-parse HEAD 'HEAD^{tree}'` (pre-edit) | 0 each | only the automation-provided `.lake` symlink was untracked; base revision and tree appear above |
| repository record, Stage0, manifest, DAG, intake, source-boundary, and neighbor inspection | 0 | found only the theorem-family title/gloss, explicit null target fields, and proposition-changing unresolved choices |
| `sha256sum` over authority, source, intake, probe, toolchain, lock, and pinned mathlib inputs | 0 | current hashes are recorded in `statement-blocker.json` |
| `cd Formalizations/Lean && lake env lean --version && lake --version` | 0 | pinned Lean and Lake versions recorded above |
| pinned mathlib revision/tree and package-status checks | 0 | pinned revision and tree recorded above; package worktree clean |
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-1355/IntakeProbe.lean` | 0 | ten adjacent pinned APIs elaborated; no canonical target or proof body was declared |
| bounded exact-topic search in pinned mathlib and repository-local Lean | 1 | expected no-match result; discovery only, not an anchor audit |
| repository-local target-ID and Chinese-title search | 1 | expected no-match result; no local Lean declaration under those identifiers |
| `python3 -B Stage1_Instances/THM-M-1355/check_intake.py` | 1 | the historical intake checker stops at its stale assertion that intake state is `[ ]`; current authority records `[_]` |
| `python3 -m json.tool Stage1_Instances/THM-M-1355/statement-blocker.json` plus scoped blocker invariants | 0 | identity, null target/imports, unchanged vector, four undefined mutations, false completion flags, empty receipts, and absent self-test agree |
| prohibited-construct scan over owned Lean files | 1 | expected no-match result; no `sorry`, `admit`, `sorryAx`, `axiom`, `constant`, `opaque`, or `unsafe` declaration |
| `git diff --check -- Stage1_Instances/THM-M-1355` plus per-new-file no-index checks | 0; 1 each | no whitespace diagnostics; no-index exits only report the expected new-file differences |
| `test ! -e .stage1-worker-selftest.json` | 0 | self-test manifest intentionally absent because the exact-statement deliverable did not pass |

The historical intake checker freezes the intake's earlier authority hashes, execution-DAG state,
and exact nine-file intake inventory. Adding this statement report also makes that inventory
historical. This phase records the limitation instead of rewriting the intake checker, intake
receipt, instance, task DAG, generated blueprint, or authoritative execution DAG to manufacture
agreement.

## Retry Condition And Status Boundary

The integration lane must master-accept a current intake dependency. Accountable reviewers must
also preserve and hash a lawful immutable primary or authoritative source, select one exact
proposition, transcribe every incorporated definition, ordered binder, hypothesis, conclusion,
proof boundary, correction, erratum, and boundary case, reconcile neighboring target ownership,
and independently approve the source-to-target crosswalk.

A later statement worker can then encode precisely that source-selected claim, minimize its pinned
imports, serialize and hash the elaborated expression and environment, compile every credited
transport, and execute all four required mutation classes.

This blocker is the assigned phase's truthful result, not completion of the statement node or any
downstream node. `audit_complete: false` and `theorem_complete: false`; no debt-vector change is
proposed. Because the exact-statement deliverable did not pass, no
`.stage1-worker-selftest.json`, statement receipt, worker `[_]`, or master acceptance is claimed.
