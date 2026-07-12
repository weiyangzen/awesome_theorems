# Exact-statement gate: blocked

Item: `S56-M-1340-STATEMENT`

Theorem: `THM-M-1340`

Base revision: `3ed74ce8b03564707b34b6e2314d2bb6d0a6206e`

Verdict: `blocked`

## Decision

The exact Lean 4 target cannot be truthfully selected or elaborated from the
repository authority. The complete catalogue claim is only the title
`解对参数的可微性` and the gloss `解对参数的导数` ("derivative of solutions with
respect to parameters"). It supplies no cited theorem, equation, definitions,
hypotheses, or conclusion. Stage0 explicitly leaves the precise definitions and
premises open.

The words identify a classical ODE theorem family, not one proposition. They do
not fix:

- finite-dimensional Euclidean, normed, or Banach state and parameter spaces;
- an autonomous field or a time-dependent field `f(t, x, lambda)`;
- the open time-state-parameter domain and its boundary convention;
- joint `C^k` regularity or partial differentiability in the parameter;
- fixed or parameter-dependent initial time and initial value;
- a common local existence neighborhood or parameter-dependent maximal domains;
- Frechet, strict, coordinatewise, or within-set differentiation; or
- differentiability alone versus identification by a sensitivity equation.

These choices change the theorem. In particular, differentiability with respect
to initial values belongs near `THM-M-1339`, while a variational equation alone
belongs near `THM-M-1341`. A scalar, autonomous, linear, global, or
parameter-independent special case would not elaborate the unidentified root.

The intake records Gerald Teschl, *Ordinary Differential Equations and Dynamical
Systems* (AMS GSM 140, 2012), Theorem 2.11, page 47, as a credible modern
candidate. That theorem gives local joint `C^k` dependence of a finite-dimensional
solution map on time, initial time, initial state, and an external parameter. The
catalogue does not cite or select it, and the intake explicitly withholds canonical
or `H0` credit pending incorporated-definition, errata, boundary, and independent
source review. Encoding that candidate now would invent the missing source
identity and mathematical scope.

The first intrinsic failure is therefore the exact source-statement identity gate
in rev-5.6 sections 5 and 5.1. The dependency also remains provisional: the
execution DAG projects `S56-M-1340-INTAKE` as `[_]`, while its receipt has
`accepted: false` and no accepted receipt ID. No statement-node acceptance can be
dependency-legal before master acceptance of that intake.

## Lean boundary

The pinned Lean environment is usable. `IntakeProbe.lean` re-elaborates the
adjacent `IsIntegralCurveOn`, `IsIntegralCurveAt`, `IsPicardLindelof`, Frechet
derivative, and differentiability interfaces. Its three direct imports are
discovery-only inputs, not a minimal import certificate for a target that does not
exist.

A bounded search of the pinned mathlib ODE directory found only Picard-Lindelof
comments using the word "parameters" and no theorem-specific external-parameter
differentiability or sensitivity declaration. A repository-local Lean search found
no `THM-M-1340` declaration. These are feasibility observations, not the later
immutable anchor audit and not proof of global absence.

Consequently no `Statement.lean`, canonical declaration, minimal target imports,
elaborated expression hash, credited alternate transport, or mutation suite was
created. The required removed-hypothesis, changed-domain, changed-binder-scope,
and boundary mutations are undefined rather than passed. The root remains
`[H1, M4, R4]`.

## Validation record

Commands ran in this isolated worker clone on 2026-07-13 (`Asia/Shanghai`). The
automation-provided canonical `.lake` symlink was used read-only. No update,
build, dependency clone, fetch, or dependency mutation was run.

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | `check_stage1_standard: ok (15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, execution skill present)` |
| `python3 scripts/stage1_target.py check` | 0 | `stage1_target: ok (1546 unique targets, ranks 1..1546, all L0/rework_required)` |
| `python3 scripts/stage1_target.py show THM-M-1340` | 0 | rank 951; planned; `L0/rework_required`; no legacy slot; legacy artifacts unaccepted; theorem incomplete |
| `git status --short --untracked-files=all` before this report | 0 | only the pre-existing automation-provided `Formalizations/Lean/.lake` symlink |
| `git rev-parse HEAD && git rev-parse 'HEAD^{tree}'` | 0 | commit `3ed74ce8b03564707b34b6e2314d2bb6d0a6206e`; tree `5d5275ace8e7c0d1026c248e8f2760e18c3c8dda` |
| `cd Formalizations/Lean && lake env lean --version` | 0 | Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740`, target `x86_64-unknown-linux-gnu` |
| `cd Formalizations/Lean && lake --version` | 0 | Lake `5.0.0-src+98dc76e` with Lean 4.29.0 |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD && git -C Formalizations/Lean/.lake/packages/mathlib rev-parse 'HEAD^{tree}'` | 0 | revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`; tree `bdc39a3123201dae413a9d9be56ec242c19e5c2b` |
| `sha256sum Stage1_Instances/THM-M-1340/instance.json Stage1_Instances/THM-M-1340/scope-map.md Stage1_Instances/THM-M-1340/source-statement-crosswalk.md Stage1_Instances/THM-M-1340/IntakeProbe.lean Formalizations/Lean/lean-toolchain Formalizations/Lean/lake-manifest.json` | 0 | input hashes are recorded in `statement-blocker.json` |
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-1340/IntakeProbe.lean` | 0 | all eight adjacent ODE and calculus interface types elaborated; no target theorem was stated |
| `rg -n -i --glob '*.lean' 'parameter\|parametric\|sensitivity' Formalizations/Lean/.lake/packages/mathlib/Mathlib/Analysis/ODE` | 0 | two Picard-Lindelof comments about shrinking parameters; no matching theorem-specific parameter-differentiability result |
| `rg -n --glob '*.lean' 'THM-M-1340\|THM_M_1340\|解对参数的可微性' Formalizations/Lean/AwesomeTheorems` | 1 | expected no-match exit; no canonical repository-local Lean declaration exists |
| `python3 -B Stage1_Instances/THM-M-1340/check_intake.py` | 1 | historical intake replay stopped at its stale assertion that the intake DAG state is `[ ]`; current authority projects `[_]` |
| `python3 -m json.tool Stage1_Instances/THM-M-1340/statement-blocker.json` | 0 | finalized structured blocker is valid JSON |
| `rg -n --glob '*.lean' '\b(sorry\|admit\|sorryAx\|axiom\|constant\|opaque\|unsafe)\b' Stage1_Instances/THM-M-1340` | 1 | expected no-match exit; no prohibited Lean declaration or placeholder occurs |
| `git diff --no-index --check /dev/null Stage1_Instances/THM-M-1340/statement-blocker.md` and the same command for `.json` | 1 each | expected new-file difference exits with no whitespace diagnostic |
| `test ! -e .stage1-worker-selftest.json` | 0 | the ineligible statement self-test manifest is absent |

The historical intake checker also freezes the prior base revision and an exact
intake-only file inventory. It is not repaired here because doing so would rewrite
another phase's evidence. The current target-set and standard validators pass.

## Retry condition

The integration lane must first accept the intake dependency. An accountable
source reviewer must then preserve an immutable primary or authoritative theorem,
include every incorporated definition and existence hypothesis, audit corrections
and errata, resolve the boundaries with `THM-M-1339` and `THM-M-1341`, and obtain
independent approval of the source crosswalk. That review must freeze all domains,
universes, ordered binders, hypotheses, conclusions, derivative conventions,
solution-domain conventions, and degenerate cases.

A later statement worker can then encode that same claim, minimize its pinned
imports, serialize and hash the elaborated expression and environment, compile
every credited transport, and execute all four required mutation classes.

This blocker is the assigned phase's truthful result, not statement-node
completion. Lifecycle remains `planned`; `audit_complete: false` and
`theorem_complete: false`; no debt change, proof credit, receipt acceptance, or
master acceptance is claimed. Because the exact-statement deliverable did not
pass, no `.stage1-worker-selftest.json` is emitted.
