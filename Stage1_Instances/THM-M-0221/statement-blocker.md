# Exact-statement gate: blocked

Item: `S56-M-0221-STATEMENT`

Theorem: `THM-M-0221`

Base revision: `5bc32428da3d17f138ceca67f30fbc2d149da1ba` (tree
`7d2433c3e014a9cc8c4d061bcc1b7d5c637ce33f`).

## Decision

The statement item remains `[ ]`. Its prerequisite, `S56-M-0221-INTAKE`, is projected as
provisional worker state `[_]`, not master-accepted `[x]`; its receipt is unsigned,
non-content-addressed, and explicitly `accepted: false`. The historical intake checker also
expects the pre-integration execution-DAG state and no longer replays at this revision. Those
dependency facts prevent an accepted transition, but the decisive blocker is mathematical.

The repository record supplies only the name "Cauchy integral theorem," the attribution to
Augustin Cauchy in 1825, and the gloss that the integral of a holomorphic function along a closed
curve is zero. It gives no bibliography, definition chain, ordered binders, hypotheses, exact
conclusion, proof boundary, correction history, errata, or independent review. Its `verified`
source label is untrusted under rev-5.6.

The gloss is false as an unrestricted universal claim. On `Complex \ {0}`, the function
`f z = 1 / z` is holomorphic, but pinned mathlib's
`circleIntegral.integral_sub_center_inv` computes its integral around a nonzero-radius positively
oriented circle as `2 * pi * I`. A valid theorem therefore needs a proposition-changing premise:
for example, filled-interior containment, simple connectedness, null-homotopy, zero winding, or an
available primitive. The catalog selects none of these. It also leaves open the scalar or
Banach-valued codomain, curve object and regularity, integral encoding, Cauchy-versus-Goursat
assumptions, binder order, and degenerate cases.

Rectangle, disk/circle, primitive, and smooth-homotopy formulations all fit parts of the gloss but
are not interchangeable. Selecting whichever one already has a convenient mathlib theorem would
silently repair, narrow, or substitute the received target. The inspected Stein-Shakarchi source
lead confirms the family of different formulations but is neither the catalog-cited historical
source nor an immutable, completely crosswalked, independently accepted source root.

Rev-5.6 sections 5 and 5.1 make statement ambiguity and a missing elaborated-expression
fingerprint hard blockers. There is consequently no honest canonical Lean expression whose import
can be certified minimal, no credited alternate encoding, and no meaningful removed-hypothesis,
changed-domain, changed-binder-scope, or boundary-case mutation suite. No mathematical or Lean
statement was added. The lifecycle stays `planned`, and the root vector stays `[H1, M3, R4]`.

## Pinned Lean Boundary

The existing discovery-only `IntakeProbe.lean` re-elaborates with two direct imports:

- `Mathlib.Analysis.Complex.HasPrimitives`
- `Mathlib.MeasureTheory.Integral.CurveIntegral.Poincare`

It authenticates nine adjacent APIs: rectangle and circle zero-integral theorems, exactness and
primitive interfaces, curve-integral and homotopy infrastructure, and the counterexample integral.
The rectangle and circle candidates have materially different types. For example, the former
assumes complex differentiability on a closed rectangle, while the latter may assume continuity on
a closed disk and differentiability on its interior away from a countable set. The primitive and
homotopy APIs introduce still different hypotheses and proof obligations.

All nine checks elaborate. Representative axiom reports list `propext`, `Classical.choice`, and
`Quot.sound`. These are feasibility and scope-boundary facts only: the probe declares no canonical
target, compiles no source transport or mutation, and receives no proof credit. Its imports cannot
be called minimal for an absent canonical target.

The environment is Lean `4.29.0` at commit
`98dc76e3c0a9b856c9b98726b713fb04fab16740`, Lake `5.0.0-src+98dc76e`, and pinned mathlib
revision `8a178386ffc0f5fef0b77738bb5449d50efeea95` with tree
`bdc39a3123201dae413a9d9be56ec242c19e5c2b`. The automation-provided
`Formalizations/Lean/.lake` symlink was used read-only. No update, build, dependency clone, fetch,
or other dependency mutation was run.

## Validation Record

Commands ran from this isolated worker clone on 2026-07-13 (`Asia/Shanghai`).

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, and 1546 uniform-L0 Lean 4 targets passed; execution skill present |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all `L0/rework_required` |
| `python3 scripts/stage1_target.py show THM-M-0221` | 0 | rank 1234; planned; no legacy slot; legacy artifacts unaccepted; theorem incomplete |
| `git status --short --untracked-files=all`; `git rev-parse HEAD 'HEAD^{tree}'` (pre-edit) | 0 | only the automation-provided `.lake` symlink was untracked; base identifiers appear above |
| catalog blame, blob, and excerpt-hash checks | 0 | all six uncited catalog lines originate at `bcf3f9fa...`; catalog excerpt SHA-256 `cc4f47e6...340`; Stage0 excerpt SHA-256 `ce7af248...2a0` |
| `cd Formalizations/Lean && lake env lean --version && lake --version` | 0 | pinned Lean and Lake versions recorded above |
| pinned mathlib revision/tree/status checks | 0 | pinned revision and tree recorded above; package worktree clean |
| `cd Formalizations/Lean && LC_ALL=C TZ=UTC lake env lean ../../Stage1_Instances/THM-M-0221/IntakeProbe.lean` | 0 | nine adjacent APIs and four axiom reports elaborated; stdout SHA-256 `130573b8...4148`; empty stderr; no target declaration |
| `python3 -B Stage1_Instances/THM-M-0221/check_intake.py` | 1 | historical checker expects intake `[ ]`, attempts 0, while integrated authority projects `[_]`, attempts 1; historical intake evidence was not rewritten |
| JSON parse and scoped blocker-invariant checks | 0 | structured blocker identity, null target/import/fingerprints, unchanged vector, four undefined mutations, false completion flags, and blocked state agree |
| declaration-position prohibited-construct scan over owned Lean files | 1 | expected no-match result; no `sorry`, `admit`, `sorryAx`, axiom, constant, opaque, or unsafe declaration |
| per-new-file no-index whitespace checks; scoped tracked diff check | 1 for each new file; 0 scoped | expected added-file difference status with no whitespace diagnostics; no tracked whitespace diagnostics |
| `test ! -e .stage1-worker-selftest.json` | 0 | worker self-test manifest intentionally absent because the exact-statement deliverable did not pass |

## Retry Condition

The integration lane must master-accept refreshed intake evidence before accepting a future
statement transition. Accountable reviewers must preserve and hash a lawful immutable primary or
approved authoritative source, select and independently approve one exact valid formulation, and
transcribe every incorporated definition, ordered binder, hypothesis, domain, codomain, curve or
cycle, regularity condition, topology or winding premise, integral convention, exact conclusion,
proof boundary, correction, erratum, transport, and boundary case. A later statement run can then
encode only that reviewed claim, minimize pinned imports, serialize the elaborated expression and
environment, compile every credited transport, and run all four mutation classes.

This is a truthful blocked statement attempt, not completion of this node or any downstream node.
`audit_complete: false` and `theorem_complete: false`; no debt change is proposed. Because the
exact-statement deliverable did not pass, no `.stage1-worker-selftest.json`, statement receipt,
worker `[_]`, or master acceptance is claimed.
