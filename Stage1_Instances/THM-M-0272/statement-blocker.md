# Exact-statement gate: blocked

Item: `S56-M-0272-STATEMENT`

Theorem: `THM-M-0272`

Base revision: `0e5ae82e6d507ee607c3f011900571ffd8096800` (tree
`400e6edf1f69b971b60a367e3ea29be359b07907`).

## Decision

The statement item remains `[ ]`. Its prerequisite `S56-M-0272-INTAKE` has provisional worker
state `[_]`, not master-accepted state `[x]`. The intake receipt declares `accepted: false`, is not
content-addressed, and has no accepted receipt ID. It deliberately leaves the canonical
mathematical claim, Lean declaration, elaborated-expression hash, and target environment
fingerprint null. Rev-5.6 section 10 treats both `[ ]` and `[_]` as unfinished, so the dependency
cannot support an accepted statement transition.

Independently, the exact-statement gate cannot pass from the received source record. The catalog
gives only the name Tonelli's theorem, Leonida Tonelli, the year 1909, and the gloss "multiple
integrals of nonnegative functions." It does not select the measure spaces or their finiteness
assumptions, product-measure and completion convention, function codomain and measurability mode,
one or both integration orders, equality orientation, set-integral scope, infinity convention, or
boundary cases. `Docs/Stage0_Blueprint.md` explicitly leaves the precise definitions and premises
open. No immutable primary or authoritative theorem passage with a complete, independently
reviewed premise and conclusion map has been admitted.

These are proposition-changing choices. Freezing the familiar sigma-finite textbook form or the
pinned `MeasureTheory.lintegral_prod` interface would supply mathematics that the source does not
state. The symmetric, curried, order-swap, and set-integral candidates have materially different
interfaces, so none can be substituted merely because mathlib calls it Tonelli's theorem.
Rev-5.6 sections 5 and 5.1 make statement ambiguity and a missing elaborated-expression
fingerprint hard blockers. There is consequently no honest canonical expression for which target
imports, checked transports, or the four required statement mutations can be certified. The
mutations are undefined, not passed, and the root vector remains `[H1, M3, R4]`.

## Pinned Lean Boundary

The existing `IntakeProbe.lean` re-elaborates with the pinned direct import
`Mathlib.MeasureTheory.Measure.Prod`. It checks `MeasureTheory.lintegral_prod`, its symmetric and
curried forms, the order-swap equality, product-set forms, and inner-integral measurability. All
nine API checks elaborate. The three representative declaration reports are exactly `propext`,
`Classical.choice`, and `Quot.sound`.

The closest direct candidate assumes measurable spaces `alpha` and `beta`, measures `mu` and
`nu`, `[SFinite nu]`, `f : alpha x beta -> ENNReal`, and
`AEMeasurable f (mu.prod nu)`. It equates the product `lintegral` with the `mu`-then-`nu` iterated
`lintegral`. The symmetric and order-swap forms additionally require `[SFinite mu]`; the curried
form reverses equality orientation; and the set form restricts integration to a measurable
rectangle. The module is the smallest direct module exposing that candidate, but it cannot be
certified as the minimal import of an absent canonical target.

This is real pinned interface evidence only. The probe defines no target proposition, checked
source-to-Lean transport, statement mutation, or proof body. A bounded repository and pinned-
mathlib search located exact-topic candidates and adjacent uses but no already accepted
source-identical root mapping. This observation is not the downstream anchor audit and makes no
global absence claim.

The environment is Lean `4.29.0` at commit
`98dc76e3c0a9b856c9b98726b713fb04fab16740`, Lake `5.0.0-src+98dc76e`, and pinned mathlib
revision `8a178386ffc0f5fef0b77738bb5449d50efeea95` with tree
`bdc39a3123201dae413a9d9be56ec242c19e5c2b`. The automation-provided
`Formalizations/Lean/.lake` symbolic link was used read-only. No update, build, dependency clone or
fetch, or other `.lake` mutation was run.

## Validation Record

Commands ran from this isolated worker clone on 2026-07-13 (`Asia/Shanghai`).

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | `check_stage1_standard: ok (15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, execution skill present)` |
| `python3 scripts/stage1_target.py check` | 0 | `stage1_target: ok (1546 unique targets, ranks 1..1546, all L0/rework_required)` |
| `python3 scripts/stage1_target.py show THM-M-0272` | 0 | rank 1279; planned; `L0/rework_required`; no legacy slot; legacy artifacts unaccepted; theorem incomplete |
| `git status --short --untracked-files=all`; `git rev-parse HEAD 'HEAD^{tree}'` (pre-edit) | 0 | only the automation-provided `.lake` link was untracked; base revision and tree appear above |
| repository source, Stage0, and intake-dossier inspection | 0 | confirmed that the received gloss does not select one proposition and no admitted exact source crosswalk exists |
| `sha256sum` over authority, intake, toolchain, probe, and pinned candidate sources | 0 | exact fingerprints are recorded in `statement-blocker.json` |
| `cd Formalizations/Lean && lake env lean --version && lake --version` | 0 | pinned Lean and Lake versions recorded above |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD 'HEAD^{tree}'` and package status | 0 | pinned mathlib revision and tree recorded above; package worktree clean |
| `cd Formalizations/Lean && LC_ALL=C TZ=UTC lake env lean ../../Stage1_Instances/THM-M-0272/IntakeProbe.lean` | 0 | nine product-measure and Tonelli APIs elaborated; three candidate declarations reported the three axioms above; stdout SHA-256 `479bf36e3107147821c7641573e1463153cac582d3da01a8ec3a8fd0d5f8d251` |
| bounded `rg` exact-topic search in repo-local Lean and pinned mathlib | 0 | found exact-topic candidate families and adjacent uses; no source-identical mapping was credited |
| `python3 -B Stage1_Instances/THM-M-0272/check_intake.py` | 1 | historical intake replay stops at its frozen repository-base assertion: intake records base `bd81d4853a030765585ef6fed4310484ceb1e458`, while this later worker clone is at the base above; intake evidence was not rewritten |
| prohibited-declaration scan over owned Lean files | 1 | expected no-match result: no `sorry`, `admit`, `sorryAx`, `axiom`, `constant`, `opaque`, or `unsafe` declaration token; diagnostic `#print axioms` commands are permitted |
| `python3 -m json.tool Stage1_Instances/THM-M-0272/statement-blocker.json` plus scoped blocker invariants | 0 | structured blocker parses; identity, dependency, null target/imports, undefined mutations, unchanged vector, false completion flags, and no-self-test boundary agree |
| `git diff --check -- Stage1_Instances/THM-M-0272` plus direct byte checks on both blocker files | 0 | no whitespace, missing-newline, carriage-return, or NUL diagnostics |
| `test ! -e .stage1-worker-selftest.json` | 0 | the worker self-test manifest is intentionally absent because the exact-statement deliverable did not pass |

The intake checker freezes the intake run's original commit and nine-file artifact inventory. It is
historical evidence, not a later-phase validator. This statement run records its stale-base failure
instead of rewriting the intake instance, receipt, checker, task DAG, generated blueprint, or
authoritative execution DAG to manufacture agreement.

## Retry Condition And Status Boundary

The integration lane must master-accept the intake dependency before accepting a later statement
transition. Accountable reviewers must preserve and hash a lawful immutable source edition,
transcribe and independently approve one exact root proposition with every incorporated
definition, ordered binder, hypothesis, conclusion, proof boundary, correction, erratum,
translation, infinity convention, integration order, and boundary case.

A fresh statement worker can then encode precisely that approved claim, minimize its pinned
imports, serialize and hash the elaborated expression and environment, compile each credited
transport, and execute the removed-hypothesis, changed-domain, changed-binder-scope, and boundary-
case mutations.

This blocker is the assigned phase's truthful result, not completion of the statement node or any
downstream node. Lifecycle remains `planned`; `audit_complete: false` and
`theorem_complete: false`; no debt-vector change is proposed. Because the exact-statement
deliverable did not pass, no `.stage1-worker-selftest.json`, statement receipt, worker `[_]`, or
master acceptance is claimed.
