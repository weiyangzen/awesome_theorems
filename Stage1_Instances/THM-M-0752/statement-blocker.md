# Exact-statement gate: blocked

Item: `S56-M-0752-STATEMENT`

Theorem: `THM-M-0752`

Base revision: `997541734bb32f987fb15f163335a82512992120` (tree
`2c866b9d840d48c48ac839740c62d3b9440be0e5`).

## Decision

The statement item remains `[ ]`. Its prerequisite, `S56-M-0752-INTAKE`, has provisional worker
state `[_]` in the execution DAG rather than master-accepted state `[x]`. The intake receipt says
`accepted: false`, contains no accepted receipt ID, and deliberately leaves the canonical human
statement and Lean target null. Master acceptance remains required before any future statement
transition can be accepted.

Independently, the exact Lean 4 target cannot be truthfully selected from the repository record.
The catalog gives only the jump-operator topic, Stephen Kleene and Emil Post attribution, the year
1954, and the gloss "the jump of Turing degrees." An operation name is not a truth-valued
proposition. The record supplies no formula, definition chain, theorem locator, ordered binders,
hypotheses, conclusion, proof boundary, correction history, formal artifact, or reviewer. Its
verified-status label is untrusted inventory metadata under rev-5.6.

Several inequivalent claims fit the gloss: representative invariance and descent to degrees, the
relative enumerable/noncomputable theorem, strict increase, monotonicity, relative completeness,
and finite iteration. They require different oracle models, encodings, binders, conclusions, and
proof obligations. Selecting one from mathematical familiarity, or conjoining several into a
package, would invent, narrow, broaden, or substitute proposition-changing mathematics.

The Kleene-Post 1954 paper identified in the intake is a matching bibliographic lead, but no
pinpoint jump theorem, incorporated definitions, proof boundary, corrections, or errata were
inspected and independently approved. The immutable Spring 2024 Stanford Encyclopedia of
Philosophy entry confirms the conventional relativized diagonal-halting construction and lists
several separate properties; it does not identify which one the catalog owns. It is family-level
discovery evidence, not a source-frozen root.

Sections 5 and 5.1 of the rev-5.6 blueprint make statement ambiguity and a missing elaborated
expression fingerprint hard blockers. There is consequently no honest canonical expression whose
imports can be certified minimal, no environment-expression fingerprint, and no credited
alternate encoding. Removed-hypothesis, changed-domain, changed-binder-scope, and boundary-case
mutations are undefined rather than passed. No theorem declaration, axiom, placeholder, weakened
special case, or broadened interface was added. The root vector stays `[H1, M4, R4]`.

## Pinned Lean boundary

The existing `IntakeProbe.lean` was re-elaborated with its single direct import,
`Mathlib.Computability.TuringDegree`. It checks eight pinned interfaces: `RecursiveIn`,
`TuringReducible`, `TuringEquivalent`, reducibility reflexivity and transitivity, the equivalence
proof, `TuringDegree`, and its partial order. The command exited 0. Its complete stdout SHA-256 is
`d904d2052b77c0ae001011b3651314a7a498dea43645b594b337f7f3ee962813`; stderr was empty with
SHA-256 `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`.

These interfaces provide adjacent oracle-computability and degree vocabulary. The probe does not
define the jump, state a canonical target, compile a transport, or contain a proof body. Its import
therefore cannot be certified minimal for the absent target and receives no statement or proof
credit. A bounded exact-topic search found no computability-theoretic Turing-jump declaration in
`Formalizations/Lean/AwesomeTheorems` or pinned mathlib. Other target dossiers were outside that
search. This is a discovery observation, not an exhaustive repo-local search, downstream immutable
anchor audit, or global absence claim.

The environment is Lean `4.29.0` at commit
`98dc76e3c0a9b856c9b98726b713fb04fab16740`, Lake `5.0.0-src+98dc76e`, and pinned mathlib revision
`8a178386ffc0f5fef0b77738bb5449d50efeea95` with tree
`bdc39a3123201dae413a9d9be56ec242c19e5c2b`. The automation-provided untracked
`Formalizations/Lean/.lake` symlink was used read-only, and the pinned mathlib package worktree
remained clean. No `lake update`, `lake build`, dependency clone or fetch, or other `.lake`
mutation was run.

## Validation record

Commands ran from this isolated worker clone on 2026-07-13 (`Asia/Shanghai`).

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, and the execution skill passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all `L0/rework_required` |
| `python3 scripts/stage1_target.py show THM-M-0752` | 0 | rank 1338; planned; no legacy slot; legacy artifacts unaccepted; theorem incomplete |
| `git status --short --untracked-files=all`; `git rev-parse HEAD 'HEAD^{tree}'` (pre-edit) | 0 | only the automation-provided `.lake` symlink was untracked; base revision and tree appear above |
| `git blame -L 5542,5547 -- Docs/researches/math_theorems.md`; inspect the manifest, execution nodes, Stage0 record, and intake dossier | 0 | all six catalog lines originate at `bcf3f9fa79ab8c2b6610c9875668c2589b35b74f`; the scheduled root remains an operation/family label without one proposition |
| hash-scope check summarized in `statement-blocker.json` | 0 | current authority, source, intake, toolchain, lockfile, and pinned-source hashes are recorded |
| `cd Formalizations/Lean && lake env lean --version && lake --version` | 0 | pinned Lean and Lake versions recorded above |
| `git -C Formalizations/Lean/.lake/packages/mathlib status --short --untracked-files=all`; `git -C ... rev-parse HEAD 'HEAD^{tree}'` | 0 | dependency worktree clean; pinned mathlib revision and tree recorded above |
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0752/IntakeProbe.lean` | 0 | eight adjacent pinned interfaces elaborated; output hashes appear above; no jump, target, transport, or proof body declared |
| bounded exact-topic `rg` command recorded in `statement-blocker.json` | 1 (expected) | no exact-topic declaration found in `Formalizations/Lean/AwesomeTheorems` or pinned mathlib; discovery only, not an exhaustive repo-local search, anchor audit, or absence proof |
| `PYTHONPYCACHEPREFIX=/tmp/stage1-thm-m-0752-statement-pycache python3 -m py_compile Stage1_Instances/THM-M-0752/check_intake.py` | 0 | historical intake checker compiled without creating an owned generated file |
| `python3 -B Stage1_Instances/THM-M-0752/check_intake.py` | 1 (expected fail-closed) | historical receipt is bound to an earlier blueprint hash; it is not current statement evidence and was not edited |
| prohibited-declaration scan over owned Lean files | 1 (expected no match) | no `sorry`, `admit`, `sorryAx`, `axiom`, `constant`, `opaque`, or `unsafe` declaration |
| `python3 -m json.tool Stage1_Instances/THM-M-0752/statement-blocker.json`; scoped blocker invariants | 0 | valid JSON; null target/imports, unchanged vector, undefined mutations, false completion flags, exact two-file scope, and no-self-test boundary agree |
| scoped tracked and per-new-file whitespace checks | 0 | no whitespace diagnostics; each no-index command returned only its expected added-file difference status |
| `test ! -e .stage1-worker-selftest.json` | 0 | self-test manifest intentionally absent because the exact-statement deliverable did not pass |

The historical intake checker freezes its intake-time authority hashes and closed artifact
inventory. Integration subsequently changed generated authority, and this phase adds two owned
blocker artifacts. The checker therefore fails closed as designed. This report records that result
rather than rewriting historical intake evidence or generated authority.

## Retry condition and status boundary

The integration lane must master-accept the intake. Accountable reviewers must also lawfully
preserve and hash an immutable primary or approved authoritative source, select and independently
approve exactly one Turing-jump proposition, and transcribe every incorporated definition, ordered
binder, hypothesis, conclusion, proof boundary, correction, erratum, and boundary convention. The
selection must fix the oracle numbering and halting convention, object encoding, reducibility and
relative-enumerability definitions, representative and quotient policy, degenerate cases, and
neighboring-target ownership.

A later statement worker can then encode only that approved claim, minimize its pinned imports,
serialize and hash the elaborated expression and environment, compile every credited transport,
and execute all four required mutation classes. This blocker is the assigned phase's truthful
result, not completion of the node or a downstream task. Lifecycle remains `planned`; audit and
theorem completion remain false. Because the exact-statement deliverable did not pass, no statement
receipt, worker `[_]`, accepted receipt, or `.stage1-worker-selftest.json` is emitted.
