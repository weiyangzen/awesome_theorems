# Exact-statement gate: blocked

Item: `S56-M-0898-STATEMENT`

Theorem: `THM-M-0898`

Base revision: `4b93dbd88c5b39d7b83f2f9278c3371f53703d76` (tree
`a526f0ad0273426336b064730ac8b85143e3e5db`).

## Decision

The statement item remains `[ ]`. Its prerequisite `S56-M-0898-INTAKE` has only provisional worker
state `[_]` in the authoritative execution DAG, not master-accepted state `[x]`. The intake receipt
declares `accepted: false`, contains no accepted receipt ID, and supports nothing downstream.
Rev-5.6 section 10.2 permits this dependency-ordered attempt, but master closure remains dependency
ordered.

Independently, the exact-statement gate fails. The repository title names `Kirkman女学生问题`
(Kirkman's schoolgirl problem), while its only gloss is `Steiner三元系的存在性` (existence of
Steiner triple systems). It supplies no citation, theorem locator, definitions, ordered binders,
hypotheses, conclusion, proof boundary, correction history, or boundary convention. The catalog's
`已验证` label is untrusted metadata.

The title and gloss do not determine the same proposition. The named schoolgirl problem asks for a
15-point schedule over seven days: each day partitions the points into five triples, and each
unordered pair occurs together exactly once. In design language this is existence of a resolvable
Steiner triple system of order 15, after the schedule/design relationship is checked. The gloss
could instead mean any of these inequivalent claims:

- existence of an ordinary `STS(15)`, with no resolution;
- existence of an ordinary Steiner triple system at some other fixed but unstated order;
- the general admissible-order characterization for ordinary Steiner triple systems; or
- a general existence theorem for resolvable Steiner triple systems.

Selecting the title-faithful schoolgirl theorem would add order 15, five groups per day, seven
parallel classes, daily coverage, and resolvability that the gloss omits. Selecting ordinary or
general Steiner-system existence would discard or broaden the named problem. Either choice would
make a proposition-changing source decision rather than elaborate the exact received target.

The point carrier and universe, equality and finiteness data, unordered-pair encoding, block and
parallel-class representation, block cardinality, exact-once pair incidence, within-day
disjointness and coverage, distinctness or multiplicity policy, quantifier order, witness shape,
isomorphism convention, and all small or degenerate cases also remain unresolved. A structure or
hypothesis that stores the desired schedule would be circular, not a target elaboration.

Sections 5 and 5.1 of the rev-5.6 blueprint make statement ambiguity and a missing elaborated
expression fingerprint hard blockers. Consequently there is no honest canonical declaration whose
imports can be certified minimal. No `Statement.lean`, exact expression, checked alternate
transport, or mutation suite was created. Removed-hypothesis, changed-domain, changed-binder-scope,
and boundary-case mutations are undefined rather than passed. The intake vector remains
`[H5, M4, R4]`; `H5` classifies the catalog wording as not yet one stable proposition and does not
refute any correctly stated classical result.

## Pinned Lean Boundary

The existing `IntakeProbe.lean` re-elaborates under the pinned environment. Its three direct imports
expose generic fixed-cardinality finite-subset, pairwise-disjointness, cardinality, and natural
congruence interfaces. All seven checks pass. The probe defines no Steiner triple system, resolution,
schedule, canonical target, transport, or proof body. Its imports are discovery-only inputs and
cannot be certified minimal for an absent target.

A bounded exact-topic search over pinned mathlib and repository-local Lean found no Kirkman,
schoolgirl, Steiner-triple-system, resolvable-triple-system, `KTS(15)`, or `STS(15)` declaration
under the recorded terms. This is feasibility evidence only, not the downstream immutable anchor
audit or a global absence claim.

The environment is Lean `4.29.0` at commit
`98dc76e3c0a9b856c9b98726b713fb04fab16740`, Lake `5.0.0-src+98dc76e`, and pinned mathlib revision
`8a178386ffc0f5fef0b77738bb5449d50efeea95` with tree
`bdc39a3123201dae413a9d9be56ec242c19e5c2b`. The automation-provided
`Formalizations/Lean/.lake` symlink was reused without running `lake update`, `lake build`, a clone,
a fetch, or another dependency-mutation command. The pinned mathlib worktree was clean after the
checks.

## Validation Record

Commands ran on 2026-07-13 (`Asia/Shanghai`).

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | `check_stage1_standard: ok (15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, execution skill present)` |
| `python3 scripts/stage1_target.py check` | 0 | `stage1_target: ok (1546 unique targets, ranks 1..1546, all L0/rework_required)` |
| `python3 scripts/stage1_target.py show THM-M-0898` | 0 | rank 1040; planned; `L0/rework_required`; no legacy slot; legacy artifacts unaccepted; theorem incomplete |
| pre-edit `git status --short --untracked-files=all`; `git rev-parse HEAD 'HEAD^{tree}'` | 0 | only the automation-provided `Formalizations/Lean/.lake` symlink was untracked; base revision and tree appear above |
| scoped authority, source, manifest, intake, and owned-path inspection | 0 | confirmed the title/gloss conflict, provisional dependency, null target, unresolved variants, and lack of a source-approved proposition |
| `sha256sum` over authority, source, intake, probe, toolchain, dependency lock, and imported mathlib inputs | 0 | exact digests are recorded in `statement-blocker.json` |
| `python3 -B Stage1_Instances/THM-M-0898/check_intake.py` | 1 | historical intake replay stops at stale receipt input hash `Docs/Stage1_Blueprint_rev-5.6.md`; its frozen authority snapshot and intake-only inventory predate integration and this phase |
| `cd Formalizations/Lean && lake env lean --version`; `lake --version` | 0 | pinned Lean and Lake versions recorded above |
| pinned mathlib revision/tree and package status | 0 | revision/tree match the values above; package worktree clean |
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0898/IntakeProbe.lean` | 0 | seven generic APIs elaborated; stdout was 647 bytes with SHA-256 `1d6a399a16cb1ef3f38c9cd579dbbb855a2666f7b822d0b122ab6a22fcd66e03`; no target or proof body |
| bounded exact-topic `rg` search in pinned mathlib and repository-local Lean | 1 (expected no match) | no target-specific declaration matched; discovery-only evidence |
| prohibited declaration scan over owned Lean files | 1 (expected no match) | no `sorry`, `admit`, `sorryAx`, `axiom`, `constant`, `opaque`, or `unsafe` declaration |
| JSON parse and scoped invariant validation for `statement-blocker.json` | 0 | identity, base, null target, unchanged vector, four undefined mutations, false completion fields, exact changed paths, and absent self-test agree |
| scoped `git diff --check` plus per-new-file no-index checks | 0 aggregate | no whitespace diagnostics; each no-index exit 1 was only the expected new-file difference |
| `test ! -e .stage1-worker-selftest.json` | 0 | self-test manifest is absent because the exact-statement deliverable did not pass |

The intake checker is a historical receipt checker. Its receipt binds blueprint and execution-DAG
hashes captured in an earlier worker snapshot, the earlier base revision, and the original
intake-only inventory. This attempt records that limitation rather than rewriting historical intake
evidence, the target task DAG, the generated blueprint, or the authoritative execution DAG to
manufacture agreement.

## Retry Condition And Status Boundary

The integration lane must first refresh and master-accept the intake dependency. Accountable
reviewers must preserve and hash one lawful immutable primary or authoritative source, select and
independently approve one exact proposition and proof boundary, and transcribe every incorporated
definition, ordered binder, hypothesis, conclusion, correction, erratum, and boundary case. The
decision must explicitly resolve the catalog title/gloss conflict and the boundary among the
schoolgirl schedule, resolvable `STS(15)`, ordinary fixed-order STS existence, and general existence
theorems.

A fresh statement attempt can then encode precisely that approved claim, minimize pinned imports,
serialize and hash its elaborated expression and environment, compile every credited transport, and
run all four required mutation classes.

This blocker is the assigned phase's truthful result, not completion of the statement item or any
downstream item. Lifecycle remains `planned`; `audit_complete: false` and
`theorem_complete: false`; no debt-vector change is proposed. Because the exact-statement
deliverable did not pass, no `.stage1-worker-selftest.json`, statement receipt, worker `[_]`, or
master acceptance is claimed.
