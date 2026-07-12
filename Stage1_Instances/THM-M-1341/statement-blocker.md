# Exact-statement gate: blocked

Item: `S56-M-1341-STATEMENT`

Theorem: `THM-M-1341`

Base revision: `53ef4456383f8ae0068669a633bb02c08056bce8` (tree
`d88aafa961abcd157b3f589fa1eaf2d675c2395d`).

Verdict: `blocked`

## Decision

The exact Lean 4 target cannot be truthfully selected or elaborated from the authoritative
repository material. The entire catalog claim is the title `变分方程` ("variational equation") and
the gloss `解的敏感性方程` ("solution sensitivity equation"). It contains no equation, citation,
state or parameter space, solution model, common domain, regularity assumptions, sensitivity
variable, initial condition, or conclusion strength. Its `已验证` label is untrusted metadata under
rev-5.6.

The intake's modern source lead confirms rather than resolves this ambiguity. Gerald Teschl's
*Ordinary Differential Equations and Dynamical Systems*, Sections 2.4-2.5, distinguishes at least
two inequivalent candidates:

- equations (2.49)-(2.50) describe the derivative of a local flow with respect to initial state by
  a homogeneous first variational equation with identity initial condition; and
- equation (2.58) describes sensitivity to a scalar external parameter by an inhomogeneous
  equation with a forcing term and zero initial condition when the initial data is
  parameter-independent.

Theorem 2.10 and Theorem 2.11 place these equations in different differentiability and parameter
dependence results. The catalog does not cite Teschl or select one of them. Choosing the parameter
equation would also require an approved boundary with neighboring `THM-M-1340`, differentiability
of solutions with respect to parameters. Choosing the initial-state equation is no more authorized
by the received wording. Either selection would invent the missing source-to-target mapping.

The first failed substantive gate is therefore exact source-statement identity under rev-5.6
sections 5 and 5.1. Independently, the prerequisite `S56-M-1341-INTAKE` is only provisional `[_]` in
the execution authority. Its worker receipt has `accepted: false`, no accepted receipt ID, and null
canonical mathematical and formal targets, so dependency-legal master acceptance is also blocked.

## Unresolved Proposition Choices

The missing choices change the proposition rather than merely its notation:

- sensitivity with respect to initial state, initial time, an external parameter, the vector field,
  or a specified combination;
- autonomous or time-dependent dynamics, finite-dimensional or Banach state and parameter spaces,
  and their scalar fields and universes;
- time, state, and parameter domains, including the exact common interval on which the relevant
  solutions and derivatives exist;
- classical, within-interval, integral-curve, local-flow, or maximal-solution encoding;
- continuity, local-Lipschitz, differentiability, and higher-regularity assumptions, including the
  variables and uniformity to which each applies;
- vector, matrix, or continuous-linear-map sensitivity and the orientation of each Frechet
  derivative and composition;
- a homogeneous equation with identity or arbitrary tangent initial data versus an inhomogeneous
  parameter equation with forcing and possibly parameter-dependent initial data;
- whether differentiability is concluded, assumed before deriving the equation, or combined with
  existence, uniqueness, and identification of the linearized solution; and
- zero-dimensional spaces, zero tangent directions, parameter-independent fields, equilibrium
  trajectories, domain-boundary behavior, empty or zero-width intervals, and loss of a common
  existence domain.

Selecting a scalar, autonomous, equilibrium-only, global, or one-dimensional special case would
substitute a narrower theorem. Assuming the desired derivative equation in a bundled structure and
projecting it would be circular. Picard-Lindelof existence, continuous dependence, a generic chain
rule, numerical sensitivity, and automatic differentiation are not the requested theorem.

## Pinned Lean Boundary

The existing `IntakeProbe.lean` was re-elaborated with the pinned environment. It directly imports
`Mathlib.Analysis.ODE.Basic` and `Mathlib.Analysis.Calculus.FDeriv.CompCLM` and checks nine adjacent
integral-curve, derivative, Frechet-calculus, and continuous-linear-map interfaces. The probe is
real feasibility evidence, but it defines no `THM-M-1341` proposition or proof body. Its imports
cannot be certified minimal for a target that has not been selected.

A bounded exact-name search found no ODE declaration named by "variational equation", "variation
equation", or "sensitivity equation" in repo-local Lean or the pinned mathlib source. This is
discovery-only evidence, not the downstream anchor audit or a claim of global absence.

Consequently there is no honest `Statement.lean`, canonical declaration, minimal target import
set, elaborated expression fingerprint, checked alternate transport, or removed-hypothesis,
changed-domain, changed-binder-scope, and boundary-case mutation suite. Those mutations are
undefined, not passed. The intake vector remains `[H1, M4, R4]`, and no statement, proof, audit, or
theorem completion is claimed.

## Validation Record

Commands ran from this isolated worker clone on 2026-07-13 (`Asia/Shanghai`). The
automation-provided canonical `.lake` symlink was used read-only. No `lake update`, build,
dependency clone or fetch, or other `.lake` mutation was run.

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | `check_stage1_standard: ok (15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, execution skill present)` |
| `python3 scripts/stage1_target.py check` | 0 | `stage1_target: ok (1546 unique targets, ranks 1..1546, all L0/rework_required)` |
| `python3 scripts/stage1_target.py show THM-M-1341` | 0 | rank 952; planned; `L0/rework_required`; no legacy slot; legacy artifacts unaccepted; theorem incomplete |
| `git rev-parse HEAD 'HEAD^{tree}'` | 0 | revision and tree recorded above |
| `git status --short --untracked-files=all` before this report | 0 | only the pre-existing automation-provided `Formalizations/Lean/.lake` symlink |
| authority, source, intake, probe, and toolchain `sha256sum` | 0 | fingerprints are recorded in `statement-blocker.json` |
| hash of the literal `Formalizations/Lean/.lake` symlink target | 0 | SHA-256 `e8714e9ebb75a5da1eeb16fdb6f50831a6cab29f115df43fa8e7535b38f59826` |
| `cd Formalizations/Lean && lake env lean --version` | 0 | Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740`, target `x86_64-unknown-linux-gnu` |
| `cd Formalizations/Lean && lake --version` | 0 | Lake `5.0.0-src+98dc76e` with Lean 4.29.0 |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD 'HEAD^{tree}'` | 0 | revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`; tree `bdc39a3123201dae413a9d9be56ec242c19e5c2b` |
| `git -C Formalizations/Lean/.lake/packages/mathlib status --short` | 0 | empty output; package worktree clean |
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-1341/IntakeProbe.lean` | 0 | all nine discovery-only interfaces elaborated and printed; no target declaration exists |
| bounded exact-name `rg` search in repo-local Lean and pinned mathlib | 1 | expected no-match exit; no named variational/sensitivity-equation declaration in the searched trees |
| `python3 -B Stage1_Instances/THM-M-1341/check_intake.py` | 1 | historical intake checker expects authoritative intake state `[ ]`, but the integrated DAG now projects `[_]`; this statement run does not rewrite earlier evidence |
| scoped prohibited-declaration scan over owned Lean files | 1 | expected no-match exit; no `sorry`, `admit`, `sorryAx`, `axiom`, `constant`, `opaque`, or `unsafe` declaration |
| JSON parse and scoped blocker-invariant check | 0 | blocker identity, null target/imports, unchanged vector, four undefined mutations, false completion flags, and absent self-test agree |
| `git diff --check -- Stage1_Instances/THM-M-1341` | 0 | no tracked whitespace diagnostics |
| per-new-file `git diff --no-index --check /dev/null` | 1 each | expected new-file difference exits with no whitespace diagnostic |
| `test ! -e .stage1-worker-selftest.json` | 0 | the ineligible worker self-test manifest is absent |

The historical intake validator freezes the earlier phase's authority state and exact nine-file
inventory. It currently fails first on authority-state drift, and the added statement artifacts
would also fail its historical inventory assertion. It is not repaired here because doing so would
rewrite the intake phase and its recorded hashes.

## Retry Condition And Status Boundary

First obtain master acceptance of the intake. Then preserve and hash one lawful immutable primary
or authoritative edition, select and independently approve one exact root proposition, transcribe
every incorporated definition, ordered binder, hypothesis, equation, initial condition,
conclusion, proof boundary, correction, and erratum, and reconcile the `THM-M-1339`/`THM-M-1340`
boundaries.

A fresh statement attempt can then encode that same claim with real Lean definitions, minimize its
pinned imports, serialize and hash the elaborated expression and environment, compile every
credited transport, and run all four required mutation classes.

This blocker is the assigned phase's truthful result, not completion of the statement node or any
downstream node. Lifecycle remains `planned`; `audit_complete: false` and
`theorem_complete: false`; no debt-vector change is proposed. Because the exact-statement
deliverable did not pass, no `.stage1-worker-selftest.json`, statement receipt, worker `[_]`, or
master acceptance is claimed.
