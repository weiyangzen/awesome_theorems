# Exact-statement gate: blocked

Item: `S56-M-0038-STATEMENT`

Theorem: `THM-M-0038`

Base revision: `5fe11f4b5e32a06ffb4432460319fc8ae906fe7b` (tree
`64c5aacf7cf3eb79008f5a1970151e3e53cb9966`).

## Decision

The statement item remains `[ ]`. Its prerequisite `S56-M-0038-INTAKE` has provisional worker
state `[_]`, not master-accepted state `[x]`. Rev-5.6 section 10.2 permits this dependency-ordered
inspection, but the intake receipt is unaccepted and non-content-addressed and has no accepted
receipt ID. Master acceptance remains required before any future statement transition.

Independently, the exact-statement gate cannot pass from the received record. The catalogue gives
only the title `莫林定理`, an unsupported `Sigmund Morill` attribution, the date 1937, and the phrase
"about the index and degree of central simple algebras." That phrase names a topic, not a
proposition. It does not define either invariant or state a relation between them.

This omission is mathematically material. Plausible readings include index divides degree, common
prime support, invariance under a matrix or Brauer-equivalent representative, an index-exponent
relation, and a field-specific equality or bound. They are inequivalent. Selecting one from memory,
convention, or formal convenience would invent, narrow, broaden, or substitute mathematics. The
bounded intake search also did not verify the author identity or locate an immutable 1937 source;
that negative search is a retry boundary, not evidence of nonexistence.

The record fixes no base field or characteristic, central-simple-algebra convention, universes,
representative or class data, ordered binders, hypotheses, conclusion, split case, scalar-extension
behavior, or other boundary cases. The separately owned Artin-Wedderburn and Brauer-group targets
`THM-M-0036`, `THM-M-0037`, and `THM-M-0424` cannot supply the missing predicate or transfer proof
credit.

Rev-5.6 sections 5 and 5.1 make statement ambiguity and a missing expression fingerprint hard
blockers. There is therefore no honest canonical expression whose imports can be certified minimal,
no source-approved alternate form for a checked transport, and no target against which the required
removed-hypothesis, changed-domain, changed-binder-scope, and boundary-case mutations can run.
Those mutation results are undefined, not passed. The root vector remains `[H5, M3, R4]`.

## Pinned Lean Boundary

The existing `IntakeProbe.lean` was re-elaborated with its sole direct import,
`Mathlib.Algebra.BrauerGroup.Defs`. The pinned environment checked `CSA`,
`IsBrauerEquivalent`, `Brauer.CSA_Setoid`, and `BrauerGroup`; the equivalence proof reported axioms
`[propext, Classical.choice, Quot.sound]`. The 367-byte output has SHA-256
`fbd3c35af4d6d2ce46c479802ab8381bf2396bea85a0df935be9b1c4df72d055`.

A bounded declaration-name search found no `index`, `degree`, or `exponent` declaration in the
pinned `Mathlib/Algebra/BrauerGroup` and `Mathlib/Algebra/Central` source surfaces. This is adjacent
API and bounded discovery evidence only, not the downstream anchor audit or a whole-mathlib absence
claim. The probe defines no invariant, asserted relation, canonical target, checked transport, or
proof body, so its import cannot be certified minimal for the absent target.

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
| `python3 scripts/stage1_target.py show THM-M-0038` | 0 | rank 1516; planned; no legacy slot; legacy artifacts unaccepted; theorem incomplete |
| `git status --short --untracked-files=all`; `git rev-parse HEAD 'HEAD^{tree}'` (pre-edit) | 0 | only the automation-provided `.lake` symlink was untracked; base revision and tree appear above |
| `git blame -L 291,296 -- Docs/researches/math_theorems.md` | 0 | all six sparse catalogue fields originate at commit `bcf3f9fa79ab8c2b6610c9875668c2589b35b74f` |
| `cd Formalizations/Lean && lake env lean --version && lake --version` | 0 | pinned Lean and Lake versions recorded above |
| pinned mathlib status and `git rev-parse HEAD 'HEAD^{tree}'` | 0 | package worktree clean; pinned revision and tree recorded above |
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0038/IntakeProbe.lean` | 0 | four adjacent interfaces elaborated; stdout was 367 bytes with the SHA-256 above; no canonical target or proof body was declared |
| bounded declaration-name search in pinned `Mathlib/Algebra/BrauerGroup` and `Mathlib/Algebra/Central` | 1 (expected no match) | no declaration name containing `index`, `degree`, or `exponent` was found in those surfaces |
| `python3 -B Stage1_Instances/THM-M-0038/check_intake.py` | 1 | historical intake replay freezes intake state `[ ]`, while current authority records provisional `[_]`; it was not rewritten or used as statement evidence |
| prohibited-construct scan over owned Lean files | 1 (expected no match) | no `sorry`, `admit`, `sorryAx`, `axiom`, `constant`, `opaque`, or `unsafe` declaration |
| `python3 -m json.tool Stage1_Instances/THM-M-0038/statement-blocker.json` plus scoped invariant assertions | 0 | valid JSON; identity, dependency, null target/imports, unchanged vector, four undefined mutations, false completion flags, exact two-file scope, and no-self-test boundary agree |
| scoped and per-new-file whitespace checks | 0 diagnostics | no whitespace errors |
| `test ! -e .stage1-worker-selftest.json` | 0 | self-test manifest intentionally absent because the exact-statement deliverable did not pass |

The historical intake checker freezes the earlier scheduler state and the intake-only file
inventory. Integration subsequently recorded the intake as provisional `[_]`. Adding these
statement-phase blocker reports also intentionally changes that inventory. This run does not rewrite
the intake checker, intake receipt, instance manifest, local task DAG, generated blueprint, or
authoritative execution DAG to manufacture agreement.

## Retry Condition And Status Boundary

An accountable source reviewer must lawfully preserve and hash a complete primary or authoritative
source, resolve the `Sigmund Morill` identity and chronology, select and independently approve one
exact proposition, and transcribe every incorporated definition, ordered binder, hypothesis,
conclusion, proof boundary, correction, erratum, and boundary case. A later statement worker can
then encode that same claim, minimize pinned imports, serialize and hash the elaborated expression
and environment, compile every credited transport, and execute all four mutation classes. The
integration lane must master-accept the intake before accepting that future transition.

This blocker is the assigned phase's truthful result, not completion of the statement node or any
downstream node. Lifecycle remains `planned`; `audit_complete: false` and
`theorem_complete: false`; no debt-vector change is proposed. Because the exact-statement
deliverable did not pass, no `.stage1-worker-selftest.json`, statement receipt, worker `[_]`, proof
credit, or master acceptance is claimed.
