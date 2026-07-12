# Exact-statement gate: blocked

Item: `S56-M-0950-STATEMENT`

Theorem: `THM-M-0950`

Base revision: `a07fc18923e20fd2876d04809a15d5b31e55512f` (tree
`1268491c8f2677e1c8e38754fa93dd190892e69e`).

## Decision

The statement item remains `[ ]`. Its prerequisite `S56-M-0950-INTAKE` is only provisional worker
state `[_]`, not master-accepted state `[x]`. Rev-5.6 section 10.2 permits this dependency-ordered
attempt from a provisional predecessor, but the intake receipt declares `accepted: false`, has no
accepted receipt ID, and deliberately leaves the canonical statement and Lean target null. Master
acceptance remains necessary before a future statement transition can be accepted.

Independently, the exact-statement gate cannot pass. The repository record supplies only the label
`Polymath project`, the attribution to many mathematicians, the year 2009, and the gloss "a
combinatorial proof of the density Hales-Jewett theorem." A collaboration and proof route are not
one truth-valued proposition. The record gives no citation, numbered result, definitions, ordered
binders, hypotheses, conclusion, quantitative convention, proof-provenance boundary, correction
history, or boundary cases. Its `verified` status is explicitly untrusted under rev-5.6.

The matching immutable primary-source snapshot confirms several inequivalent candidate roots:

- Theorem 1.4 is qualitative density Hales-Jewett: for every positive integer `k` and real
  `delta > 0`, sufficiently high-dimensional subsets of `[k]^n` of density at least `delta`
  contain a nondegenerate combinatorial line.
- Theorem 1.5 is a stronger quantitative result. It gives a `k = 3` tower-height bound of order
  `1 / delta^2` and describes the `k >= 4` bounds by an Ackermann-scale comparison whose printed
  wording is partly informal.
- The row's defining reference to a combinatorial proof may instead require Theorem 1.4 together
  with a source-faithful Polymath proof graph and checked composition, rather than only the
  proposition.

The catalog selects none of Theorem 1.4, Theorem 1.5, their conjunction, or a
provenance-sensitive theorem package. Moreover, `THM-M-0949` separately owns the density
Hales-Jewett theorem label and likely the qualitative proposition. Silently selecting Theorem 1.4
would duplicate that target and erase the proof-route distinction; selecting Theorem 1.5 or a
conjunction would strengthen the row without authority. These are substitutions, not elaboration
of an exact received claim.

The encoding choices also change the proposition: finite alphabet and coordinate types, line
encoding and nonempty wildcard convention, `Real` versus `NNReal` or `NNRat` density, strict versus
nonstrict inequalities, existential versus selected threshold, and all `k = 0`, `k = 1`,
`delta <= 0`, `delta > 1`, `n = 0`, empty-space, and empty-wildcard cases remain unresolved. If
Theorem 1.5 is selected, exact tower, Ackermann, asymptotic, and "broadly comparable" meanings must
also be sourced rather than invented.

Sections 5 and 5.1 make statement ambiguity and a missing expression fingerprint hard blockers.
There is therefore no canonical expression for which minimal imports, checked alternate
transports, or the required removed-hypothesis, changed-domain, changed-binder-scope, and
boundary-case mutations can be certified. The mutations are undefined, not passed. The existing
intake vector remains `[H5, M4, R4]`; `H5` classifies the catalog wording as not yet a stable
proposition and does not refute density Hales-Jewett or the published Polymath results.

## Pinned Lean Boundary

`IntakeProbe.lean` re-elaborates in the pinned environment. Its three imports expose
`Combinatorics.Line`, ordinary coloring Hales-Jewett, `Finset.dens`, finite word-space cardinality,
and two prospective predicates. All checks pass. Ordinary Hales-Jewett has no density premise, and
the probe declares no density-Hales-Jewett target, quantitative theorem, proof-provenance package,
checked source transport, or proof body. Its imports therefore cannot be certified minimal for the
absent canonical target.

A bounded exact-topic search of pinned mathlib found only the ordinary and multidimensional
Hales-Jewett module. The same search over repo-local Lean outside `.lake` found no match. These are
discovery observations only, not the downstream immutable anchor audit or a claim of global
absence.

The environment is Lean `4.29.0` at commit
`98dc76e3c0a9b856c9b98726b713fb04fab16740`, Lake `5.0.0-src+98dc76e`, and pinned mathlib
revision `8a178386ffc0f5fef0b77738bb5449d50efeea95` with tree
`bdc39a3123201dae413a9d9be56ec242c19e5c2b`. The automation-provided
`Formalizations/Lean/.lake` symlink was used read-only. No update, build, clone, fetch, or other
dependency mutation was run.

## Validation Record

Commands ran from this isolated worker clone on 2026-07-13 (`Asia/Shanghai`).

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, and 1546 uniform-L0 Lean 4 targets passed; execution skill present |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all `L0/rework_required` |
| `python3 scripts/stage1_target.py show THM-M-0950` | 0 | rank 1022; planned; no legacy slot; legacy artifacts unaccepted; theorem incomplete |
| `git status --short --untracked-files=all`; `git rev-parse HEAD 'HEAD^{tree}'` (pre-edit) | 0 | only the automation-provided `.lake` symlink was untracked; base revision and tree appear above |
| repository record, Stage0 projection, intake, and publisher-paper inspection | 0 | confirmed the project/proof-route wording, distinct Theorems 1.4 and 1.5, quantitative wording, unresolved source selection, and `THM-M-0949` boundary |
| `sha256sum` over authority, source, intake, probe, toolchain, and pinned-mathlib inputs | 0 | exact hashes are recorded in `statement-blocker.json` |
| `cd Formalizations/Lean && lake env lean --version && lake --version` | 0 | pinned Lean and Lake versions recorded above |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD 'HEAD^{tree}'`; package `status --short` | 0 | pinned mathlib revision and tree recorded above; package status was empty |
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0950/IntakeProbe.lean` | 0 | seven adjacent pinned API and prospective-predicate signatures elaborated; no canonical target or proof body was declared |
| bounded exact-topic search in pinned mathlib and repo-local Lean | 0 / 1 | mathlib hits were ordinary Hales-Jewett only; repo-local search had no match; discovery-only evidence |
| `python3 -B Stage1_Instances/THM-M-0950/check_intake.py` | 1 | historical intake replay stops because it freezes intake state `[ ]` while current authority records provisional `[_]`; its original nine-file inventory is also historical after this phase |
| prohibited-construct scan over owned Lean files | 1 | expected no-match result; no `sorry`, `admit`, `sorryAx`, `axiom`, `constant`, `opaque`, or `unsafe` declaration |
| JSON parsing plus scoped blocker invariants | 0 | identity, dependency state, null target/imports, unchanged vector, four undefined mutations, false completion flags, and no-self-test boundary agree |
| scoped whitespace checks and `git diff --check -- Stage1_Instances/THM-M-0950` | 0 | no whitespace diagnostics |
| `test ! -e .stage1-worker-selftest.json` | 0 | self-test manifest intentionally absent because the exact-statement deliverable did not pass |

The historical intake checker is bound to the intake authority state and original nine-file
inventory. Integration changed the generated intake state to `[_]`, so replay fails before its
inventory check; adding these statement blocker artifacts also makes that inventory historical.
This run records the limitation instead of rewriting the intake checker, intake receipt, instance,
task DAG, generated blueprint, or authoritative execution DAG to manufacture agreement.

## Retry Condition And Status Boundary

The integration lane must master-accept the intake dependency before accepting any future
statement transition. Accountable source and duplicate-scope reviewers must preserve and hash an
immutable authoritative source, select and independently approve exactly one numbered result or
provenance-sensitive package, resolve ownership relative to `THM-M-0949`, bind every incorporated
definition, ordered binder, premise, conclusion, proof boundary, correction, quantitative
convention, and boundary case to immutable locators, and settle the exponent and informal-bound
wording if quantitative scope is selected.

A fresh statement worker can then encode that exact claim, minimize pinned imports, serialize and
hash the elaborated expression and environment, compile every credited transport, and run all four
required mutation classes.

This blocker is the assigned phase's truthful result, not completion of the statement node or any
downstream node. Lifecycle remains `planned`; `audit_complete: false` and
`theorem_complete: false`; no debt-vector change is proposed. Because the exact-statement
deliverable did not pass, no `.stage1-worker-selftest.json`, statement receipt, worker `[_]`, or
master acceptance is claimed.
