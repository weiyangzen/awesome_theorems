# Exact-statement gate: blocked

Item: `S56-M-0302-STATEMENT`

Theorem: `THM-M-0302`

Base revision: `be8701e88e791545c16a262edd1909486d5cef4b` (tree
`78b0a751473bf6d71f453a6aad18b130268a3428`).

## Decision

The exact Lean 4 target cannot be truthfully elaborated from the accepted inputs. The repository
fixes the name "John-Nirenberg inequality," the authors Fritz John and Louis Nirenberg, the year
1961, and the gloss "exponential integrability of BMO functions." These identify the classical
Euclidean BMO theorem family, but not one binder-complete proposition.

The intake predecessor has provisional worker state `[_]`, not master-accepted state `[x]`. Its
receipt declares `accepted: false`, is not content-addressed, and contains no accepted receipt ID.
This statement inspection therefore cannot satisfy the dependency acceptance gate. Independently,
the intake manifest leaves the canonical statement, Lean module and expression, elaborated
expression hash, and canonical-target environment fingerprint null. Rev-5.6 makes statement
ambiguity and a missing expression fingerprint hard blockers.

The bibliographic match is F. John and L. Nirenberg, *On functions of bounded mean oscillation*,
*Communications on Pure and Applied Mathematics* 14(3) (1961), 415-426, DOI
`10.1002/cpa.3160140317`. Crossref confirms only metadata and exposes Wiley PDF and text-mining
links; the PDF returned HTTP 403 and the text-mining endpoint returned HTTP 400. Semantic Scholar
identifies the paper but marks its PDF closed. No primary theorem text or page-level result was
admitted, so no incorporated definition, assumption, constant, proof boundary, correction, or
erratum has an accepted source crosswalk.

In particular, the received material does not fix:

- a positive dimension convention and representation of Euclidean space;
- real or complex values, raw functions or almost-everywhere classes, and local integrability;
- admissible cubes, their endpoint and degeneracy conventions, and set-average normalization;
- the BMO seminorm, its kernel or quotient convention, and zero or infinite seminorm cases;
- whether the root is averaged exponential integrability or the distribution-tail estimate;
- the exponential coefficient, leading constant, threshold range, strictness, or dependencies;
- ordered binders, hypotheses, conclusion, alternate encodings, or all boundary cases.

These choices change the proposition. Selecting a familiar formulation, an interval or one-cube
specialization, or an abstract BMO predicate that assumes the desired estimate would invent,
narrow, or substitute mathematics. Consequently there is no honest canonical expression whose
direct imports can be certified minimal. Checked transports and the removed-hypothesis,
changed-domain, changed-binder-scope, and boundary-case mutation suite are undefined, not passed.
The root vector remains `[H1, M4, R4]`.

## Pinned Lean Boundary

The existing `IntakeProbe.lean` was re-elaborated with its three direct imports:

- `Mathlib.MeasureTheory.Integral.Average`
- `Mathlib.MeasureTheory.Integral.Lebesgue.Markov`
- `Mathlib.MeasureTheory.Measure.Lebesgue.Basic`

It checks ten adjacent interfaces for set averages, centered integrals, Euclidean box volumes,
Markov bounds, and positivity of an already integrable exponential. All elaborated. The three
axiom reports contain only `propext`, `Classical.choice`, and `Quot.sound`. These APIs neither
define Euclidean BMO nor state or prove a John-Nirenberg estimate.

A bounded exact-topic search of pinned mathlib and repo-local Lean found no target-specific BMO or
John-Nirenberg declaration. This is statement-feasibility evidence, not the downstream exhaustive
anchor audit. The probe deliberately declares no canonical target, and its imports cannot be
certified minimal for an absent proposition.

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
| `python3 scripts/stage1_target.py show THM-M-0302` | 0 | rank 1305; planned; no legacy slot; legacy artifacts unaccepted; theorem incomplete |
| `git status --short --untracked-files=all`; `git rev-parse HEAD 'HEAD^{tree}'` | 0 | before statement edits, only the automation-provided untracked `.lake` symlink existed; base revision and tree are recorded above |
| source, intake, manifest, blueprint, and execution-DAG inspection | 0 | the family is identified, but the exact proposition and formal target remain null; intake is provisional `[_]` only |
| Crossref DOI JSON query recorded in `statement-blocker.json` | 0 | matching paper metadata and publisher links; metadata only |
| Semantic Scholar DOI JSON query recorded in `statement-blocker.json` | 0 | matching paper ID and title; `openAccessPdf.status` was `CLOSED` |
| Wiley PDF request recorded in `statement-blocker.json` | 22 | curl reported HTTP 403; no primary file was retained |
| Wiley text-mining request recorded in `statement-blocker.json` | 22 | curl reported HTTP 400; no primary file was retained |
| `cd Formalizations/Lean && lake env lean --version && lake --version` | 0 | pinned Lean and Lake versions recorded above |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD 'HEAD^{tree}'` and package status | 0 | pinned mathlib revision/tree recorded above; package worktree clean |
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0302/IntakeProbe.lean` | 0 | ten adjacent pinned APIs elaborated; stdout was 2737 bytes with SHA-256 `0bd430087d7e2d212cfec1ca1eb051a349b132c243bf09f32432fab7fd18d886`; no target statement or proof body was declared |
| bounded exact-topic `rg` search in pinned mathlib and repo-local Lean | 1 | expected no-match result for concrete BMO and John-Nirenberg names; bounded feasibility evidence only |
| `python3 -B Stage1_Instances/THM-M-0302/check_intake.py` | 1 | historical intake replay stops because it freezes the intake-time authority state `[ ]` while current authority records provisional `[_]`; prior evidence was not rewritten |
| prohibited Lean construct scan over the owned path | 1 | expected no-match result; no `sorry`, `admit`, `sorryAx`, `axiom`, bodyless `constant`, `opaque`, or `unsafe` declaration |
| `python3 -m json.tool Stage1_Instances/THM-M-0302/statement-blocker.json` plus scoped blocker assertions | 0 | the structured blocker and phase-specific invariants passed |
| scoped tracked and per-new-file whitespace checks | 0 | no whitespace diagnostics in either blocker artifact |
| `test ! -e .stage1-worker-selftest.json` | 0 | self-test manifest intentionally absent because exact target elaboration did not pass |

The historical intake checker and receipt are not rewritten to manufacture agreement with later
authority or the statement-phase artifact inventory. No generated blueprint, execution DAG,
target manifest, target-local task DAG, dependency, or foreign target was modified.

## Retry Condition And Status Boundary

The integration lane must master-accept the intake dependency. Accountable reviewers must preserve
and hash a complete authoritative source, pinpoint one exact theorem and every incorporated
definition, map constants and quantifier dependencies, audit corrections and errata, choose and
source-map the exponential-integrability or distribution-tail root, resolve all boundary cases,
and independently approve that proposition.

A later statement run can encode that same source claim with concrete Euclidean BMO foundations,
minimize pinned imports, serialize and hash the elaborated expression and environment, compile
every credited transport, and execute all four required mutation classes.

This is a truthful statement-node blocker, not completion of the assigned deliverable. Lifecycle
remains `planned`; `audit_complete: false` and `theorem_complete: false`; no debt-vector change,
statement receipt, worker `[_]`, proof credit, or master acceptance is claimed. Because the assigned
phase is not genuinely self-tested to its completion gate, no `.stage1-worker-selftest.json` is
emitted.
