# Exact-statement gate: blocked

Item: `S56-M-0031-STATEMENT`

Theorem: `THM-M-0031`

Base revision: `a1c9974d7fb28cd680e6494b968544bf801a93a2` (tree
`1fa287bc821355aca2ca9e3ce107830a3eb58e64`).

## Decision

The statement item remains `[ ]`. Its prerequisite `S56-M-0031-INTAKE` has provisional worker
state `[_]`, not master-accepted state `[x]`. Rev-5.6 section 10.2 permits this dependency-ordered
inspection, but the intake receipt is unaccepted and non-content-addressed and has no accepted
receipt ID. Master acceptance remains required before any future statement transition.

Independently, the exact-statement gate cannot pass from the received record. The catalogue gives
only the name "Cohen structure theorem," the attribution Irving Cohen, the year 1946, and the gloss
"structure of complete Noetherian local rings." It supplies no proposition, bibliography, theorem
number, incorporated definitions, ordered binders, hypotheses, conclusion, proof boundary,
corrections, errata, or source reviewer. The Stage0 projection expressly leaves precise definitions
and premises open.

This omission is mathematically material. The inspected but unaccepted modern Stacks lead has two
distinct clauses: coefficient-ring existence for every complete local ring, and a finite-variable
power-series quotient presentation when the maximal ideal is finitely generated. Other familiar
statements package both clauses, specialize to complete Noetherian rings, state a regular-local
cover consequence, classify regular complete local rings, or give a domain normalization. They are
not interchangeable roots. Selecting one from memory, the mutable modern page, or formal
convenience would invent, narrow, broaden, or substitute mathematics.

The source also does not fix the inverse-limit versus adic-completeness convention, whether
Noetherianity or finite generation is assumed, the coefficient-field, unramified Cohen-ring, and
truncated p-nilpotent branches, the coefficient object, variables, quotient ideal, isomorphism
category, universes, or boundary cases. The existing intake obtained bibliographic metadata for
Cohen's 1946 paper but not an admitted theorem passage; the publisher text was unavailable, and no
independent source review was accepted.

Rev-5.6 sections 5 and 5.1 make statement ambiguity and a missing expression fingerprint hard
blockers. There is therefore no honest canonical expression whose imports can be certified minimal,
no source-approved alternate encoding for a checked transport, and no target against which the
required removed-hypothesis, changed-domain, changed-binder-scope, and boundary-case mutations can
run. Those mutation results are undefined, not passed. The root vector remains `[H1, M4, R4]`.

## Pinned Lean Boundary

The existing `IntakeProbe.lean` was re-elaborated with these four direct imports:

- `Mathlib.Algebra.CharP.MixedCharZero`
- `Mathlib.RingTheory.AdicCompletion.Completeness`
- `Mathlib.RingTheory.AdicCompletion.LocalRing`
- `Mathlib.RingTheory.MvPowerSeries.Basic`

The pinned environment checked sixteen adjacent local-ring, Noetherian, adic, residue-field,
power-series, and characteristic interfaces. `AdicCompletion.isAdicComplete` and
`isLocalRing_of_isAdicComplete_maximal` each reported axioms
`[propext, Classical.choice, Quot.sound]`. The 1939-byte output has SHA-256
`1923b0daedf84ceb4a0ada6a8279debed6528e103b6882ffcf1970adbc984fce`.

A bounded topic search located only the intake disclaimer and unrelated legacy planning structures;
it located no Cohen structure declaration in the searched repo-local Lean, pinned mathlib, or
Archive surfaces. This is adjacent API and bounded discovery evidence only, not the downstream
anchor audit or a whole-library absence claim. The probe defines no coefficient-ring object,
canonical target, checked source transport, or proof body, so its imports cannot be certified
minimal for the absent target.

The environment is Lean `4.29.0` at commit
`98dc76e3c0a9b856c9b98726b713fb04fab16740`, Lake `5.0.0-src+98dc76e`, and pinned mathlib revision
`8a178386ffc0f5fef0b77738bb5449d50efeea95` with tree
`bdc39a3123201dae413a9d9be56ec242c19e5c2b`. The automation-provided `.lake` symlink was used
read-only. No `lake update`, `lake build`, dependency clone or fetch, or other `.lake` mutation ran.

## Validation Record

Commands ran from this isolated worker clone on 2026-07-13 (`Asia/Shanghai`).

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, and 1546 uniform-L0 Lean 4 targets passed; execution skill present |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all `L0/rework_required` |
| `python3 scripts/stage1_target.py show THM-M-0031` | 0 | rank 1515; planned; no legacy slot; legacy artifacts unaccepted; theorem incomplete |
| `git status --short --untracked-files=all`; `git rev-parse HEAD 'HEAD^{tree}'` (pre-edit) | 0 | only the automation-provided `.lake` symlink was untracked; base revision and tree appear above |
| `git blame -L 242,247 -- Docs/researches/math_theorems.md` | 0 | all six sparse catalogue fields originate at commit `bcf3f9fa79ab8c2b6610c9875668c2589b35b74f` |
| `cd Formalizations/Lean && lake env lean --version && lake --version` | 0 | pinned Lean and Lake versions recorded above |
| pinned mathlib status and `git rev-parse HEAD 'HEAD^{tree}'` | 0 | package worktree clean; pinned revision and tree recorded above |
| `cd Formalizations/Lean && LC_ALL=C TZ=UTC lake env lean ../../Stage1_Instances/THM-M-0031/IntakeProbe.lean` | 0 | sixteen adjacent interfaces elaborated; stdout was 1939 bytes with the SHA-256 above; no canonical target or proof body was declared |
| bounded topic search over repo-local Lean, pinned mathlib, and Archive | 0 | only the intake disclaimer and unrelated legacy planning structures matched; no Cohen structure declaration was located in the searched surfaces |
| `python3 -B Stage1_Instances/THM-M-0031/check_intake.py` | 1 | historical intake replay freezes intake state `[ ]` and attempts 0, while current authority records provisional `[_]` and attempts 1; it was not rewritten or used as statement evidence |
| prohibited-construct scan over owned Lean files | 1 (expected no match) | no `sorry`, `admit`, `sorryAx`, `axiom`, `constant`, `opaque`, or `unsafe` declaration |
| `python3 -m json.tool Stage1_Instances/THM-M-0031/statement-blocker.json` plus scoped invariant assertions | 0 | valid JSON; identity, dependency, null target/imports, unchanged vector, four undefined mutations, false completion flags, exact two-file scope, and no-self-test boundary agree |
| scoped and per-new-file whitespace checks | 0 diagnostics | no whitespace errors |
| `test ! -e .stage1-worker-selftest.json` | 0 | self-test manifest intentionally absent because the exact-statement deliverable did not pass |

The historical intake checker freezes the earlier scheduler state and intake-only file inventory.
Integration subsequently recorded the intake as provisional `[_]`. Adding these statement-phase
blocker reports also intentionally changes that inventory. This run does not rewrite the intake
checker, intake receipt, instance manifest, local task DAG, generated blueprint, or authoritative
execution DAG to manufacture agreement.

## Retry Condition And Status Boundary

An accountable source reviewer must lawfully preserve and hash a complete primary or approved
authoritative source, select and independently approve one exact proposition, and transcribe every
incorporated definition, ordered binder, hypothesis, conclusion, proof boundary, correction,
erratum, and boundary case. The selection must resolve coefficient-ring existence versus
power-series quotient versus a combined or regular-local formulation, completeness and
Noetherian/finite-generation conventions, all characteristic branches, coefficient objects,
variables, quotient and isomorphism data, and degenerate cases. A later statement worker can then
encode that same claim, minimize pinned imports, serialize and hash the elaborated expression and
environment, compile every credited transport, and execute all four mutation classes. The
integration lane must master-accept the intake before accepting that future transition.

This blocker is the assigned phase's truthful result, not completion of the statement node or any
downstream node. Lifecycle remains `planned`; `audit_complete: false` and
`theorem_complete: false`; no debt-vector change is proposed. Because the exact-statement
deliverable did not pass, no `.stage1-worker-selftest.json`, statement receipt, worker `[_]`, proof
credit, or master acceptance is claimed.
