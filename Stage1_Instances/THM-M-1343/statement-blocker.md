# Exact-statement gate: blocked

Item: `S56-M-1343-STATEMENT`

Theorem: `THM-M-1343`

Base revision: `b72c38f3df59ba12e643e0a20be2dd36c063eafc` (tree
`4b2126951b48faf4dd3d85dc1e81962ea29a7004`)

Verdict: `blocked`

## Decision

The exact Lean 4 target cannot be truthfully selected or elaborated from the authoritative
repository record. Its complete mathematical wording is the title `李雅普诺夫直接法`
(`Lyapunov's direct method`) and the gloss `李雅普诺夫函数的稳定性判据` (`a stability criterion using a
Lyapunov function`). It supplies no cited proposition, equation, definition, ordered binder,
hypothesis, conclusion, or boundary convention. Stage0 explicitly leaves the exact definitions and
premises open, and the catalogue's `已验证` label is untrusted under rev-5.6.

The wording identifies a family of inequivalent direct-method theorems. It does not choose:

- an autonomous, nonautonomous, discrete-time, flow, or other dynamical model;
- the time domain, state and scalar spaces, system domain, or dimensions and universes;
- an equilibrium point, invariant set, trajectory, or another stability object;
- a classical, Caratheodory, integral-curve, or flow solution notion, or the needed existence and
  uniqueness assumptions;
- continuity or differentiability of the vector field and Lyapunov function, or a classical,
  Frechet-paired, Dini, or other orbital derivative;
- positive definiteness, comparison bounds, coercivity, properness, or radial unboundedness;
- nonpositive, negative-definite, strict-away-from-equilibrium, or invariance-based decay; or
- Lyapunov, uniform, asymptotic, exponential, local, semiglobal, or global stability and any basin,
  rate, or convergence conclusion.

Those choices change the theorem. Weak nonincrease may support local Lyapunov stability, while
asymptotic convergence requires a source-selected strictness or invariance premise. A global result
generally also needs global forward existence and a source-selected compactness, properness, or
coercivity condition. Selecting one familiar version would therefore invent or substitute
mathematics rather than elaborate the exact received theorem.

The first substantive failure is exact source-statement identity under rev-5.6 sections 5 and 5.1.
Independently, the prerequisite `S56-M-1343-INTAKE` is only provisional `[_]`: its receipt is
`accepted: false` and has no accepted receipt ID. No statement node can be dependency-legally
accepted before master acceptance of that intake.

## Pinned Lean Boundary

The existing `IntakeProbe.lean` was re-elaborated under the pinned environment. Its direct imports
are `Mathlib.Analysis.ODE.Basic` and `Mathlib.Analysis.Calculus.FDeriv.Basic`, and it prints the types
of six adjacent interfaces: `IsIntegralCurveOn`, `IsIntegralCurveAt`,
`IsIntegralCurveAt.hasDerivAt`, `HasFDerivAt`, `ContinuousAt`, and `Filter.Tendsto`.

This confirms that the pinned Lean environment and adjacent ODE/calculus substrate are available.
The probe declares no target, defines no stability predicate, and supplies no source identity or
proof credit. Its imports cannot be certified minimal for a canonical target that does not exist.
A bounded search of the repository-local Lean tree and pinned mathlib ODE/Dynamics sources found no
obvious named Lyapunov direct-method criterion under the recorded terms, and a target-ID search found
no local declaration. These are discovery observations, not an exhaustive anchor audit or proof of
global absence.

Consequently no `Statement.lean`, canonical declaration, minimal target imports, elaborated
expression hash, credited alternate transport, or mutation suite was created. The required
removed-hypothesis, changed-domain, changed-binder-scope, and boundary-case mutations are undefined,
not passed. The root remains `[H5, M4, R4]`.

The environment is Lean `4.29.0` at commit
`98dc76e3c0a9b856c9b98726b713fb04fab16740`, Lake `5.0.0-src+98dc76e`, and pinned mathlib
revision `8a178386ffc0f5fef0b77738bb5449d50efeea95` with tree
`bdc39a3123201dae413a9d9be56ec242c19e5c2b`. The automation-provided
`Formalizations/Lean/.lake` symlink was used read-only. No update, build, dependency clone, fetch, or
dependency mutation was run.

## Validation Record

Commands ran in this isolated worker clone on 2026-07-13 (`Asia/Shanghai`).

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, and 1546 uniform-L0 Lean 4 targets passed; execution skill present |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all `L0/rework_required` |
| `python3 scripts/stage1_target.py show THM-M-1343` | 0 | rank 954; planned; no legacy slot; legacy artifacts unaccepted; theorem incomplete |
| `git status --short --untracked-files=all`; `git rev-parse HEAD 'HEAD^{tree}'` (pre-edit) | 0 | only the automation-provided `.lake` symlink was untracked; base revision and tree appear above |
| `cd Formalizations/Lean && lake env lean --version && lake --version` | 0 | pinned Lean and Lake versions recorded above |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD 'HEAD^{tree}'`; separate `git ... status --short` | 0 each | pinned mathlib revision and tree recorded above; status output empty, so the package worktree was clean |
| `sha256sum` over authority, source, intake, probe, toolchain, and dependency-lock inputs | 0 | hashes recorded in `statement-blocker.json` |
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-1343/IntakeProbe.lean` | 0 | all six adjacent interface types elaborated; no target theorem was declared |
| bounded Lyapunov/direct-method search over repository-local and pinned ODE/Dynamics Lean files | 1 | expected no-match result; no obvious named criterion under the terms; discovery only |
| repository-local search for `THM-M-1343`, `THM_M_1343`, and the Chinese title | 1 | expected no-match result; no local Lean declaration was found under those searched identifiers |
| `python3 -B Stage1_Instances/THM-M-1343/check_intake.py` | 1 | historical intake replay rejected its stale assertion that the intake DAG state is `[ ]`; current authority projects `[_]` |
| `python3 -m json.tool Stage1_Instances/THM-M-1343/statement-blocker.json` plus scoped blocker invariants | 0 | identity, null target/imports, false completion flags, four undefined mutations, unchanged vector, empty receipts, and no-self-test boundary agree |
| prohibited-construct `rg` scan over owned Lean files | 1 | expected no-match result; no `sorry`, `admit`, `sorryAx`, `axiom`, `constant`, `opaque`, or `unsafe` declaration |
| `git diff --no-index --check /dev/null Stage1_Instances/THM-M-1343/statement-blocker.md` | 1 | expected new-file difference exit; diagnostic output was empty |
| the same no-index command for `statement-blocker.json` | 1 | expected new-file difference exit; diagnostic output was empty |
| `git diff --check -- Stage1_Instances/THM-M-1343` | 0 | no whitespace diagnostics on tracked diffs; the explicit no-index checks cover the two untracked files |
| `test ! -e .stage1-worker-selftest.json` | 0 | self-test manifest intentionally absent because the exact-statement deliverable did not pass |

The integrated historical intake checker also freezes the earlier base revision, authority-file
hashes, and an exact intake-only artifact inventory. Adding this statement report makes that
intake-only inventory stale as well. This statement phase records the limitation instead of
rewriting another phase's evidence, instance, task DAG, generated blueprint, or authoritative
execution DAG to manufacture agreement.

## Retry Condition And Status Boundary

The integration lane must first master-accept the intake dependency. Accountable reviewers must
then preserve and hash a lawful immutable primary or authoritative direct-method theorem, transcribe
every incorporated definition, ordered binder, premise, conclusion, proof boundary, correction,
erratum, and boundary case, reconcile the boundaries with `THM-M-1342`, `THM-M-1344`, and
`THM-P-0796`, and independently approve the source-to-target crosswalk.

A later statement worker can encode precisely that claim, minimize its pinned imports, serialize
and hash the elaborated expression and environment, compile each credited transport, and execute all
four required mutation classes.

This blocker is the assigned phase's truthful result, not completion of the statement node or a
downstream node. Lifecycle remains `planned`; `audit_complete: false` and
`theorem_complete: false`; no debt-vector change is proposed. Because the exact-statement
deliverable did not pass, no `.stage1-worker-selftest.json`, statement receipt, worker `[_]`, or
master acceptance is claimed.
