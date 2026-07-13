# Exact-statement gate: blocked

Item: `S56-M-0252-STATEMENT`

Theorem: `THM-M-0252`

Base revision: `bd81d4853a030765585ef6fed4310484ceb1e458` (tree
`fb92fc7476bff9a2ce8c20f1d7be34c6655ca6b4`).

## Decision

The statement item remains `[ ]`. Its prerequisite `S56-M-0252-INTAKE` has provisional worker
state `[_]` in the execution DAG, but its receipt is not master-accepted, is not content-addressed,
and lists no accepted receipt ID. Master acceptance remains a separate prerequisite for any future
statement transition.

Independently, the exact Lean 4 target cannot be truthfully elaborated from the authoritative
repository record. The record supplies only the title `科罗纳问题` ("corona problem"), Lennart
Carleson, the year 1962, and the gloss `H^∞的极大理想空间` ("the maximal ideal space of
H-infinity"). It names a mathematical subject and object, but asserts no density, equality,
existence, classification, Bezout identity, or other truth-valued conclusion. It also gives no
bibliography, definition of `H^∞`, domain, maximal-ideal or character encoding, topology,
evaluation map, ordered binders, hypotheses, proof boundary, correction history, or boundary
cases. The catalog status `已验证` is untrusted metadata under rev-5.6.

The intake records one matching bibliographic lead, Carleson's 1962 paper *Interpolations by
Bounded Analytic Functions and the Corona Problem*, but no immutable primary text, exact theorem
or page passage, incorporated definition chain, assumption map, correction or errata audit, or
independent source approval was admitted. It therefore selects no exact proposition.

The duplicate boundary is also proposition-changing. `THM-M-0373` separately catalogs
`Corona定理`, with the gloss `H^∞的Corona问题`; its dossier selected the classical finite-generator
Bezout formulation and left maximal-ideal-space density as an unchecked alternate. This worker
cannot merge the IDs, inherit that formulation, or transfer its statement or evidence. Candidate
density and Bezout formulations are mathematically related, but no source-approved root or
kernel-checked transport has been selected for this target.

Sections 5 and 5.1 of the rev-5.6 blueprint make statement ambiguity and a missing elaborated
expression fingerprint hard blockers. There is consequently no honest canonical expression for
which minimal imports, alternate transports, or removed-hypothesis, changed-domain,
changed-binder-scope, and boundary-case mutations can be certified. Those mutations are undefined,
not passed. No `Statement.lean`, theorem declaration, axiom, placeholder, broadened interface, or
convenient substitute was added. The root remains `[H5, M4, R4]`.

## Pinned Lean Boundary

The existing `IntakeProbe.lean` re-elaborates using the pinned environment. Its four direct imports
expose the complex unit disc, `AnalyticOnNhd`, generic character spaces, maximal ideals,
`Ideal.toCharacterSpace`, and `DenseRange`. These are adjacent encoding ingredients only. The
probe does not construct the bounded-analytic Banach algebra `H^∞`, define evaluation characters,
choose a topology or root formulation, or state or prove a corona theorem. Its imports therefore
cannot be certified minimal for an absent canonical target and receive no statement, anchor, or
proof credit.

A bounded exact-topic search of `Formalizations/Lean/AwesomeTheorems` and pinned mathlib found no
corona, H-infinity, bounded-analytic, or maximal-ideal-space target declaration. It deliberately
did not search other target dossiers, because `THM-M-0373` is already recorded above as a separate
repo-local candidate that this worker may not inherit. This is discovery-only feasibility
evidence, not a downstream anchor audit or a global absence claim.

The environment is Lean `4.29.0` at commit
`98dc76e3c0a9b856c9b98726b713fb04fab16740`, Lake `5.0.0-src+98dc76e`, and pinned mathlib
revision `8a178386ffc0f5fef0b77738bb5449d50efeea95` with tree
`bdc39a3123201dae413a9d9be56ec242c19e5c2b`. The automation-provided untracked
`Formalizations/Lean/.lake` symlink was used read-only. No `lake update`, `lake build`, dependency
clone or fetch, or other `.lake` mutation was run.

## Validation Record

Commands ran from this isolated worker clone on 2026-07-13 (`Asia/Shanghai`).

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, and the execution skill passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all `L0/rework_required` |
| `python3 scripts/stage1_target.py show THM-M-0252` | 0 | rank 1262; planned; no legacy slot; legacy artifacts unaccepted; theorem incomplete |
| `git status --short --untracked-files=all`; `git rev-parse HEAD 'HEAD^{tree}'` (pre-edit) | 0 | only the automation-provided `.lake` symlink was untracked; base revision and tree appear above |
| `git blame -L 1815,1820 -- Docs/researches/math_theorems.md` and source-block hashing | 0 | all six uncited catalog lines originate at `bcf3f9fa79ab8c2b6610c9875668c2589b35b74f`; target block SHA-256 `4e15802a...f7f`, duplicate block `41990347...9e1` |
| `sha256sum Docs/Stage1_Blueprint_rev-5.6.md Docs/Stage1_Targets_rev-5.6.json Docs/Stage1_Execution_DAG_rev-5.6.json skills/execute-stage1-rev56/SKILL.md Docs/Blueprint_Guidelines.md Docs/researches/math_theorems.md Docs/Stage0_Blueprint.md Formalizations/Lean/lean-toolchain Formalizations/Lean/lake-manifest.json Stage1_Instances/THM-M-0252/{instance.json,source-statement-crosswalk.md,scope-map.md,task-dag.json,intake-receipt.json,IntakeProbe.lean}` | 0 | authority, source, intake, probe, and toolchain hashes matched `statement-blocker.json` |
| `(cd Formalizations/Lean && lake env lean --version && lake --version)` | 0 | pinned Lean and Lake versions recorded above |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD 'HEAD^{tree}'` and package status | 0 | pinned mathlib revision and tree recorded above; package worktree clean |
| `(cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0252/IntakeProbe.lean)` | 0 | seven adjacent disc, analytic, character-space, maximal-ideal, and density APIs elaborated; no target theorem was stated |
| bounded exact-topic `rg` over `Formalizations/Lean/AwesomeTheorems` and pinned mathlib | 1 | expected no-match result; other target dossiers excluded; discovery only, not an anchor audit or global absence claim |
| `python3 -B Stage1_Instances/THM-M-0252/check_intake.py` | 1 | known phase-evolution failure: the historical intake checker expects execution-DAG intake state `[ ]`, while integration records `[_]`; its frozen intake inventory is not rewritten |
| prohibited-construct scan wrapper over target Lean files | 0 | inner `rg` returned expected no-match exit 1; no `sorry`, `admit`, `sorryAx`, `axiom`, `constant`, `opaque`, or `unsafe` declaration |
| `python3 -m json.tool Stage1_Instances/THM-M-0252/statement-blocker.json` plus scoped blocker invariants | 0 | structured blocker parses; identity, null target/imports, undefined mutations, unchanged `H5/M4/R4`, false completion flags, and no-self-test gate agree |
| scoped tracked and added-file whitespace checks | 0 | no whitespace diagnostics in either blocker artifact |
| `test ! -e .stage1-worker-selftest.json` | 0 | self-test manifest intentionally absent because the exact-statement deliverable did not pass |

The intake checker is bound to its original pre-integration authority state and closed nine-file
intake inventory. This statement attempt records that expected historical replay failure rather
than modifying intake evidence, generated authority, or another phase's artifacts.

## Retry Condition And Status Boundary

The integration lane must master-accept the intake dependency before it can accept a later
statement transition. Accountable reviewers must preserve and hash an immutable primary or
authoritative source, pinpoint and transcribe one exact proposition and every incorporated
definition, map all assumptions and the proof boundary, audit corrections and errata, reconcile
the relationship to `THM-M-0373`, and independently approve the source-statement crosswalk.

That decision must freeze the disc or other domain; the carrier, norm, algebra, completeness, and
equality of `H^∞`; maximal ideals versus continuous characters and their correspondence; the
topology and evaluation map; density versus Bezout or another exact conclusion; any equivalence
directions; all ordered binders and hypotheses; and every empty-family, singleton, zero-bound,
constant, invertible, boundary-domain, boundedness, topology, and density convention. A later
statement worker can then encode that same claim, minimize pinned imports, serialize and hash the
elaborated expression and environment, compile every credited transport, and run all four required
mutation classes.

This blocker is the assigned phase's truthful result, not completion of the statement node or any
downstream node. Lifecycle remains `planned`; `audit_complete: false` and
`theorem_complete: false`; no debt-vector change is proposed. Because the exact-statement
deliverable did not pass, no `.stage1-worker-selftest.json`, statement receipt, worker `[_]`, or
master acceptance is claimed.
