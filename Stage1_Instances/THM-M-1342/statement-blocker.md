# Exact-statement gate: blocked

Item: `S56-M-1342-STATEMENT`

Theorem: `THM-M-1342`

Base revision: `531673f2e97293dd22e5727b12fc7e13eca7d6e5` (tree
`4acbd91f6e676b2b89949bb52992c0be522de40f`).

Verdict: `blocked`

## Decision

The exact Lean 4 target cannot be truthfully selected or elaborated from the authoritative
repository record. Its complete mathematical wording is the title `李雅普诺夫稳定性理论`
(`Lyapunov stability theory`) and the gloss `平衡点的稳定性` (`stability of an equilibrium`). It
supplies no cited proposition, equation, definition, ordered binder, hypothesis, conclusion, proof
boundary, or boundary convention. Stage0 explicitly leaves the exact definitions and premises open,
and the catalog's `已验证` label is untrusted under rev-5.6.

The wording names a theory family, not one proposition. It does not choose:

- a definition, criterion, characterization, implication, equivalence, or instability result;
- an autonomous or nonautonomous ODE, flow, semiflow, discrete system, differential inclusion, or
  another dynamical model;
- the time domain, state and scalar spaces, system domain, topology or metric, dimensions, and
  universes;
- a fixed point, equilibrium trajectory, invariant set, orbit, or another stability object;
- a classical, Caratheodory, integral-curve, flow, maximal-solution, or another solution notion,
  together with local or global existence, uniqueness, and forward-completeness policy;
- Lyapunov, uniform, asymptotic, exponential, orbital, practical, input-to-state, or another
  stability notion; or
- neighborhood versus epsilon-delta quantifiers, locality, attraction, basin, rate, time origin,
  endpoints, and degenerate cases.

The intake's inspected modern source lead makes the ambiguity concrete: Teschl, Section 6.5,
separately defines Lyapunov, asymptotic, and exponential stability and notes that attraction need
not imply stability. The catalog does not cite that source or select one of its definitions or a
theorem. Choosing one familiar formulation would therefore invent or substitute mathematics. It
could also absorb the distinct direct-method, indirect-method, or linear-system targets
`THM-M-1343`, `THM-M-1344`, or `THM-M-1355`.

The first substantive failure is exact source-statement and scope identity under rev-5.6 sections 5
and 5.1. Independently, the prerequisite `S56-M-1342-INTAKE` is only provisional `[_]`: its receipt
is `accepted: false` and has no accepted receipt ID. The statement node cannot be dependency-legally
accepted before master acceptance of a current intake.

Consequently there is no honest canonical declaration for which minimal imports can be claimed. No
`Statement.lean`, canonical expression, checked alternate transport, or mutation suite was created.
The required removed-hypothesis, changed-domain, changed-binder-scope, and boundary-case mutations
are undefined rather than passed. The root remains `[H5, M4, R4]`.

## Pinned Lean Boundary

The existing `IntakeProbe.lean` was re-elaborated under the pinned environment. Its direct imports
are `Mathlib.Analysis.ODE.Basic`, `Mathlib.Dynamics.FixedPoints.Basic`, and
`Mathlib.Topology.MetricSpace.Pseudo.Defs`. It prints the types of seven adjacent integral-curve,
fixed-point, metric-ball, neighborhood, and convergence interfaces.

This confirms that the pinned Lean environment and adjacent substrate are available. The probe
declares no target, defines no stability predicate, and supplies no source identity or proof credit.
Its imports cannot be certified minimal for a canonical target that does not exist. A bounded search
of the repository-local Lean tree and pinned mathlib ODE and Dynamics sources found no obvious named
target under the recorded terms, and a target-ID search found no local declaration. These are
discovery observations, not the downstream anchor audit or a global absence claim.

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
| `python3 scripts/stage1_target.py show THM-M-1342` | 0 | rank 953; planned; no legacy slot; legacy artifacts unaccepted; theorem incomplete |
| `git status --short --untracked-files=all`; `git rev-parse HEAD 'HEAD^{tree}'` (pre-edit) | 0 each | only the automation-provided `.lake` symlink was untracked; base revision and tree appear above |
| repository record, Stage0, manifest, DAG, intake, source-boundary, and neighbor inspection | 0 | found only the theory-family title and noun phrase, an explicit null canonical target, and proposition-changing unresolved choices |
| `sha256sum` over authority, source, intake, probe, toolchain, and dependency-lock inputs | 0 | current hashes are recorded in `statement-blocker.json` |
| `cd Formalizations/Lean && lake env lean --version`; `lake --version` | 0 each | pinned Lean and Lake versions recorded above |
| pinned mathlib revision/tree and package-status checks | 0 each | pinned revision and tree recorded above; package worktree clean |
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-1342/IntakeProbe.lean` | 0 | seven adjacent interfaces elaborated; no canonical target was declared |
| bounded Lyapunov/equilibrium-stability search over repository-local and pinned ODE/Dynamics Lean files | 1 | expected no-match result; discovery only, not an anchor audit |
| repository-local target-ID and Chinese-title search | 1 | expected no-match result; no local Lean declaration under those identifiers |
| `python3 -B Stage1_Instances/THM-M-1342/check_intake.py` | 1 | historical intake replay stopped at its stale assertion that intake state is `[ ]`; current authority records `[_]`; the statement phase did not rewrite historical intake evidence |
| `python3 -m json.tool Stage1_Instances/THM-M-1342/statement-blocker.json` plus scoped blocker invariants | 0 each | identity, null target/imports, false completion flags, four undefined mutations, unchanged vector, empty receipts, and absent self-test agree |
| prohibited-construct `rg` scan over owned Lean files | 1 | expected no-match result; no `sorry`, `admit`, `sorryAx`, `axiom`, `constant`, `opaque`, or `unsafe` declaration |
| `git diff --check -- Stage1_Instances/THM-M-1342` plus per-new-file no-index checks | 0; 1 each | no whitespace diagnostics; both no-index exits are only the expected nonempty new-file differences |
| `test ! -e .stage1-worker-selftest.json` | 0 | self-test manifest intentionally absent because the exact-statement deliverable did not pass |

The historical intake checker also freezes an earlier base revision, authority hashes, and an exact
intake-only artifact inventory. Adding this statement report makes that inventory stale as well.
This phase records the limitation instead of rewriting another phase's evidence, instance, task
DAG, generated blueprint, or authoritative execution DAG to manufacture agreement.

## Retry Condition And Status Boundary

The integration lane must first master-accept a current intake dependency. Accountable reviewers
must then preserve and hash a lawful immutable primary or authoritative source, redirect the
theory-family label to one exact definition or theorem, transcribe every incorporated definition,
ordered binder, premise, conclusion, proof boundary, correction, erratum, and boundary case,
reconcile `THM-M-1343`, `THM-M-1344`, `THM-M-1355`, and `THM-P-0796`, and independently approve the
source-to-target crosswalk.

A later statement worker can encode precisely that claim, minimize its pinned imports, serialize
and hash the elaborated expression and environment, compile every credited transport, and execute
all four required mutation classes.

This blocker is the assigned phase's truthful result, not completion of the statement node or a
downstream node. Lifecycle remains `planned`; `audit_complete: false` and
`theorem_complete: false`; no debt-vector change is proposed. Because the exact-statement
deliverable did not pass, no `.stage1-worker-selftest.json`, statement receipt, worker `[_]`, or
master acceptance is claimed.
