# Exact-statement gate: blocked

Item: `S56-M-0301-STATEMENT`

Theorem: `THM-M-0301`

Base revision: `4b93dbd88c5b39d7b83f2f9278c3371f53703d76` (tree
`a526f0ad0273426336b064730ac8b85143e3e5db`).

## Decision

The exact Lean 4 target cannot be truthfully elaborated from the accepted inputs. The inspected
source identifies the classical theorem family, but it does not fix all proposition-changing
choices. The pinned Lean environment also lacks the concrete analytic objects needed to state that
family without inventing an abstract proxy.

The intake predecessor has provisional worker state `[_]`, not master-accepted state `[x]`. Its
receipt declares `accepted: false`, is not content-addressed, and contains no accepted receipt ID.
This statement inspection therefore does not satisfy the dependency acceptance gate. Independently,
the intake manifest leaves the canonical mathematical statement, Lean module and expression,
expression hash, and environment fingerprint null. Rev-5.6 makes statement ambiguity and a missing
expression fingerprint hard blockers.

The primary statement source inspected at intake is Charles Fefferman, "Characterizations of
bounded mean oscillation", *Bulletin of the American Mathematical Society* 77(4) (1971), 587-588,
DOI `10.1090/S0002-9904-1971-12763-5`. The official two-page PDF has SHA-256
`7352edb3d25ffcfd7473ad738751b5e0d8e7dccd13540b45a57647289405524d`.
On page 587, BMO is defined on `R^n` by uniformly bounded average absolute oscillation over cubes,
with functions identified modulo constants. Theorem 1 states that BMO is the dual of `H^1(R^n)`
through the integral pairing, initially for a dense subspace of smooth rapidly decreasing `H^1`
functions. The adjacent paragraph regards `H^1` as the `L^1` functions whose Riesz transforms are
all in `L^1`.

That announcement does not itself freeze the positive-dimension convention, real versus complex
scalars and conjugation order, almost-everywhere representatives, cube conventions, BMO seminorm
kernel and quotient norm, Riesz-transform normalizations, the precise `H^1` norm and completion,
the pairing's integrability and continuous extension, or the quantitative two-sided norm
comparison. It points to work then in preparation for detailed proofs. The later Fefferman-Stein
source candidate has not been accepted with proposition-level definition, assumption, proof, and
errata mapping. The probable duplicate `THM-M-0363` also has no accepted identity, ownership, or
exact-statement transport decision.

These choices yield different Lean propositions. Introducing abstract types called `H1` and `BMO`,
assuming their duality, defining one as the other's dual, stating only one representation direction,
or substituting a toy, bounded-domain, holomorphic, martingale, or finite-dimensional result would
broaden or replace the source theorem. None is permitted.

Consequently there is no honest canonical expression whose direct imports can be certified
minimal. Ordered binders, checked alternate-form transports, a serialized expression fingerprint,
and the removed-hypothesis, changed-domain, changed-binder-scope, and boundary-case mutation suite
are undefined, not passed. The root vector remains `[H1, M4, R4]`.

## Pinned Lean Boundary

The existing `IntakeProbe.lean` was re-elaborated with its three direct imports:

- `Mathlib.Analysis.Distribution.SchwartzSpace.Basic`
- `Mathlib.MeasureTheory.Function.LocallyIntegrable`
- `Mathlib.MeasureTheory.Function.LpSpace.Basic`

It checks seven adjacent interfaces: `MeasureTheory.LocallyIntegrable`, `MeasureTheory.MemLp`,
`MeasureTheory.Lp`, `MeasureTheory.integral`, `SchwartzMap`, `SchwartzMap.integralCLM`, and
`ContinuousLinearMap`. All elaborated. They provide generic measure, Schwartz-space, integration,
and functional-analysis infrastructure only. They define neither Euclidean BMO, real Hardy
`H^1`, analytic Riesz transforms, the extended pairing, nor the dual representation theorem.

A bounded exact-topic search of pinned mathlib and repo-local Lean found only four unrelated local
identifiers named `Bmo` and the read-only `THM-M-0363` probe comments. This is feasibility evidence,
not the downstream exhaustive anchor audit. The probe deliberately declares no target and its
imports cannot be certified minimal for an absent canonical proposition.

The environment is Lean `4.29.0` at commit
`98dc76e3c0a9b856c9b98726b713fb04fab16740`, Lake `5.0.0-src+98dc76e`, and
pinned mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95` with tree
`bdc39a3123201dae413a9d9be56ec242c19e5c2b`. The automation-provided
`Formalizations/Lean/.lake` symlink was used read-only. No update, build, clone, fetch, or other
dependency mutation was run.

## Validation Record

Commands ran from this isolated worker clone on 2026-07-13 (`Asia/Shanghai`).

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, and the execution skill passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all `L0/rework_required` |
| `python3 scripts/stage1_target.py show THM-M-0301` | 0 | rank 1047; planned; no legacy slot; legacy artifacts unaccepted; theorem incomplete |
| `git status --short --untracked-files=all`; `git rev-parse HEAD 'HEAD^{tree}'` | 0 | before statement edits, only the automation-provided untracked `.lake` symlink existed; base revision and tree are recorded above |
| source, intake, scope, duplicate-boundary, manifest, blueprint, and DAG inspection | 0 | source theorem family identified; exact proposition and formal target remain null; intake is provisional `[_]` only |
| `cd Formalizations/Lean && lake env lean --version && lake --version` | 0 | pinned Lean and Lake versions recorded above |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD 'HEAD^{tree}'` and package status | 0 | pinned mathlib revision/tree recorded above; package source status empty |
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0301/IntakeProbe.lean` | 0 | seven adjacent pinned APIs elaborated; no target theorem or proof body declared |
| bounded exact-topic `rg` search in pinned mathlib, repo-local Lean, and read-only `THM-M-0363` | 0 | only four unrelated `Bmo` locals and two probe-comment lines matched; no concrete target API found |
| `python3 -B Stage1_Instances/THM-M-0301/check_intake.py` | 1 | historical intake replay stops at line 72 because it freezes authority state `[ ]` while current authority records provisional `[_]`; it also freezes its original nine-file inventory, so this phase records rather than rewrites historical evidence |
| `python3 -m json.tool Stage1_Instances/THM-M-0301/statement-blocker.json` plus scoped blocker invariants | 0 | structured blocker and phase-specific invariants passed |
| prohibited Lean construct scan over the owned path | 1 | expected no-match result; no `sorry`, `admit`, `sorryAx`, `axiom`, bodyless `constant`, `opaque`, or `unsafe` declaration |
| scoped newline/trailing-whitespace checks plus tracked `git diff --check -- Stage1_Instances/THM-M-0301` | 0 | no whitespace diagnostics in either new file |
| `test ! -e .stage1-worker-selftest.json` | 0 | self-test manifest intentionally absent because the exact-statement deliverable did not pass |

The historical intake checker and receipt are not rewritten to manufacture agreement with later
authority or the statement-phase artifact inventory. No generated blueprint, execution DAG,
target manifest, target-local task DAG, dependency, or foreign target was modified.

## Retry Condition And Status Boundary

The integration lane must master-accept the intake dependency and decide the identity and ownership
relationship with `THM-M-0363`. Accountable reviewers must preserve and hash a complete
authoritative source, map every incorporated definition, convention, ordered binder, hypothesis,
conclusion, proof boundary, norm comparison, correction, erratum, and boundary case, and
independently approve one exact proposition. Concrete Lean foundations for Euclidean BMO modulo
almost-everywhere constants, normalized real Hardy `H^1`, Riesz transforms, the dense test
subspace, and the extended pairing must then be implemented or pinned.

A later statement run can encode that same source claim, minimize pinned imports, serialize and
hash the elaborated expression and environment, compile every credited transport, and execute all
four required mutation classes.

This is a truthful statement-node blocker, not completion of the assigned deliverable. Lifecycle
remains `planned`; `audit_complete: false` and `theorem_complete: false`; no debt-vector change,
statement receipt, worker `[_]`, proof credit, or master acceptance is claimed. Because the assigned
phase is not genuinely self-tested to its completion gate, no `.stage1-worker-selftest.json` is
emitted.
