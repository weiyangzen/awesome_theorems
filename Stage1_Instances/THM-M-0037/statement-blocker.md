# Exact-statement gate: blocked

Item: `S56-M-0037-STATEMENT`

Theorem: `THM-M-0037`

Base revision: `4ecdda4863162748b3ee70bc4ec842789418145d` (tree
`aace54662cd5e9ca38472011f41afdbffdedfa04`).

## Decision

The statement item remains `[ ]`. Its prerequisite `S56-M-0037-INTAKE` has provisional worker
state `[_]` in the authoritative execution DAG, not master-accepted state `[x]`. Rev-5.6 section
10.2 permits this dependency-ordered attempt while concurrency is enabled, so pending master
acceptance did not prevent the inspection. The intake receipt is non-content-addressed, declares
`accepted: false`, and has no accepted receipt ID. Master acceptance and fresh intake validation
remain required before any future statement transition.

Independently and decisively, the exact-statement gate cannot pass from the received claim. The
repository gives only the title "Brauer group theorem" and the gloss "classification of central
simple algebras over a field," with Richard Brauer, 1932, and an explicitly untrusted `verified`
label. It supplies no exact proposition, cited theorem passage, incorporated definitions, ordered
binders, hypotheses, conclusion, proof boundary, boundary cases, or errata disposition.

The intake records two historical leads: Brauer's 1929 "Ueber Systeme hyperkomplexer Zahlen" and
the 1932 Brauer-Noether-Hasse "Beweis eines Hauptsatzes in der Theorie der Algebren." Only
bibliographic metadata has been admitted. No immutable article text, exact theorem and page,
premise mapping, proof boundary, chronology resolution, translation, corrections, errata, or
independent source approval is accepted. The catalog's Brauer-only 1932 attribution does not by
itself select either paper or a precise claim.

Materially different roots remain possible:

- classification by stable positive-size matrix-algebra equivalence and equality in its quotient;
- construction of the tensor-product abelian group on Brauer classes, including unit and inverse;
- matrix-over-division-algebra normal form and existence or uniqueness of division representatives;
- characterization by Morita equivalence; or
- a cohomological, local, global, or other arithmetic classification under additional field data.

The catalog does not say which result, or which conjunction of results, it means. It also does not
fix field and universe policy, central-simple-algebra conventions, matrix sizes, representative
versus quotient-class formulation, algebra equivalences, ordered binders, split and base-field
classes, opposite algebras, universe lifts, or nontriviality assumptions. These choices produce
different propositions. Selecting one from memory or local API convenience would invent, narrow,
broaden, or substitute mathematics. Sections 5 and 5.1 of the rev-5.6 blueprint make statement
ambiguity and a missing elaborated-expression fingerprint hard blockers.

There is consequently no honest canonical Lean expression whose imports can be certified minimal,
no credited alternate encoding, and no meaningful removed-hypothesis, changed-domain,
changed-binder-scope, or boundary-case mutation suite. Those mutations are undefined, not passed.
The lifecycle remains `planned`, and the root vector remains `[H1, M3, R4]`.

## Pinned Lean Boundary

The existing `IntakeProbe.lean` was re-elaborated with the pinned toolchain. Its sole import,
`Mathlib.Algebra.BrauerGroup.Defs`, exposes:

- `CSA K`, bundling finite-dimensional central simple algebras;
- `IsBrauerEquivalent A B`, witnessed by positive-size matrix stabilizations;
- reflexivity, symmetry, transitivity, and `IsBrauerEquivalent.is_eqv`;
- `Brauer.CSA_Setoid K`; and
- `BrauerGroup K`, the quotient carrier.

The relation's transitivity and equivalence witnesses report axioms `[propext, Classical.choice,
Quot.sound]`. The module header explicitly leaves the tensor-product abelian group, field
functoriality, and Morita-equivalence characterization as TODO work. Thus this is real API
feasibility evidence, but definition and quotient infrastructure is not a source-selected
classification theorem.

A bounded search also found the separately owned `THM-M-0424` statement artifacts and legacy file
`Formalizations/Lean/AwesomeTheorems/Stage1/S1_M_078.lean`. They include quotient wrappers,
Artin-Wedderburn support, and interfaces for missing Brauer-group operations. The current intake
explicitly prohibits transferring that target's selected statement, lifecycle state, or proof
credit. The `THM-M-0036` central-simple Artin-Wedderburn target is likewise not a substitute.

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
| `python3 scripts/stage1_target.py show THM-M-0037` | 0 | rank 1080; planned; no legacy slot; legacy artifacts unaccepted; theorem incomplete |
| `git status --short --untracked-files=all`; `git rev-parse HEAD 'HEAD^{tree}'` (pre-edit) | 0 | only the automation-provided `.lake` symlink was untracked; base revision and tree appear above |
| `cd Formalizations/Lean && lake env lean --version && lake --version` | 0 | pinned Lean and Lake versions recorded above |
| pinned mathlib revision/tree and package-status checks | 0 | revision and tree recorded above; package worktree clean |
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0037/IntakeProbe.lean` | 0 | eight adjacent APIs elaborated; `trans` and `is_eqv` reported the three axioms above; stdout was 970 bytes and 12 lines with SHA-256 `57765ffdef12498d89b2a499069afcbb2d172f8947effad3632c9a72f4f14f93`; no canonical target was declared |
| bounded exact-topic search in pinned mathlib and repository-local Lean | 0 | found quotient infrastructure and separately owned THM-M-0424 artifacts; no source-selected THM-M-0037 root; discovery-only evidence |
| `python3 -B Stage1_Instances/THM-M-0037/check_intake.py` | 1 | historical intake replay stops because it freezes intake authority state `[ ]` while current authority records provisional `[_]`; its exact file inventory is also intake-only |
| prohibited-construct scan over owned Lean files | 1 | expected no-match result; no `sorry`, `admit`, `sorryAx`, `axiom`, `constant`, `opaque`, or `unsafe` declaration |
| `python3 -m json.tool Stage1_Instances/THM-M-0037/statement-blocker.json` plus scoped blocker invariants | 0 | valid JSON; identity, dependency state, null target/imports, unchanged vector, four undefined mutations, false completion flags, and no-self-test boundary agree |
| per-file and scoped whitespace checks | 0 diagnostics | no whitespace diagnostics |
| `test ! -e .stage1-worker-selftest.json` | 0 | self-test manifest intentionally absent because the exact-statement deliverable did not pass |

The historical intake checker freezes the original authority state `[ ]`, its intake-only file
inventory, and the intake worker-packet contract. The integration lane subsequently recorded the
provisional intake state `[_]`, so replay already stops at that earlier state assertion. Adding
statement-phase blocker artifacts also intentionally makes its inventory historical. This run does
not rewrite `check_intake.py`, the intake receipt, instance manifest, target-local DAG, generated
blueprint, or authoritative execution DAG to manufacture agreement.

## Retry Condition And Status Boundary

An accountable source reviewer must preserve and hash a lawful immutable primary or authoritative
source, select and independently approve one exact theorem passage, and transcribe every
incorporated definition, ordered binder, hypothesis, conclusion, proof boundary, convention,
chronology decision, translation, erratum, and boundary case. The review must also settle target
identity and ownership against `THM-M-0036` and `THM-M-0424`. A fresh statement worker can then
encode exactly that claim, minimize pinned imports, serialize and hash the elaborated expression
and environment, compile each credited transport, and execute all four mutation classes. The
integration lane must master-accept the intake dependency before accepting that future statement
transition.

This blocker is the assigned phase's truthful result, not completion of the statement node or any
downstream node. Lifecycle remains `planned`; `audit_complete: false` and
`theorem_complete: false`; no debt-vector change is proposed. Because the exact-statement
deliverable did not pass, no `.stage1-worker-selftest.json`, statement receipt, worker `[_]`, or
master acceptance is claimed.
