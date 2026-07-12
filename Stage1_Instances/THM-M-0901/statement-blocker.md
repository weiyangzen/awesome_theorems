# Exact-statement gate: blocked

Item: `S56-M-0901-STATEMENT`

Theorem: `THM-M-0901`

Base revision: `4b93dbd88c5b39d7b83f2f9278c3371f53703d76` (tree
`a526f0ad0273426336b064730ac8b85143e3e5db`).

## Decision

The statement item remains `[ ]`. Its prerequisite `S56-M-0901-INTAKE` has provisional worker
state `[_]`, not master-accepted state `[x]`; the intake receipt declares `accepted: false`, is not
content-addressed, and has no accepted receipt ID. Rev-5.6 section 10.2 permits this
dependency-ordered statement attempt while concurrency is enabled, but any eventual statement
acceptance remains dependency ordered.

Independently and decisively, the exact-statement gate fails. The repository supplies only the
title "Latin squares" and the compound gloss "existence and counting of Latin squares." It gives
no bibliography, definition, order range, ordered binder, hypothesis, formula, conclusion, proof
boundary, computation boundary, correction history, or boundary convention. Its `verified` label
is untrusted metadata under rev-5.6.

The intake correctly leaves the canonical mathematical claim and Lean expression null. The gloss
does not select among materially different roots or decide whether it denotes one conjunction or a
package of separately rooted propositions. In particular, it does not decide:

- whether existence means an ordinary labelled square for every positive order, includes order
  zero, concerns partial-square completion or embedding, or imposes reducedness, orthogonality,
  symmetry, or algebraic data;
- whether rows, columns, and symbols share `Fin n`, use three finite carriers of equal cardinality,
  or use another representation such as a quasigroup table;
- whether the Latin condition is row and column injectivity, bijectivity, unique occurrence of each
  symbol, or a source-approved equivalent with checked transports;
- whether counting means total labelled squares, reduced squares, isomorphism classes, isotopy
  classes, main classes, or another quotient; and
- whether the counting conclusion is a fixed-order value, a general formula or recurrence, a
  divisibility result, a bound, or an asymptotic result.

The inspected McKay-Wanless source lead defines Latin rectangles and squares and states several
distinct counting results. That multiplicity demonstrates the ambiguity; the catalog does not cite
the paper or select one result, and the intake credits no independent source review. The Marshall
Hall existence paper remains a bibliographic lead whose theorem text, incorporated definitions,
scope, proof, and errata were not accepted. Combining a cyclic construction with one convenient
counting theorem would manufacture a compound root rather than elaborate the exact received target.

Rev-5.6 sections 5 and 5.1 make statement ambiguity and a missing elaborated-expression fingerprint
hard blockers. With no approved canonical proposition, there is no honest target import set to
minimize, no expression or canonical-target environment fingerprint, and no credited alternate
transport. The required removed-hypothesis, changed-domain, changed-binder-scope, and boundary-case
mutations are undefined, not passed. The root vector remains `[H5, M4, R4]`; `H5` classifies the
received compound wording as not yet a stable proposition, not as a claim that standard
Latin-square results are false.

## Pinned Lean Boundary

The existing `IntakeProbe.lean` re-elaborates under the pinned environment. Its three imports expose
matrix, finite-cardinality, and bijection interfaces adjacent to a possible future encoding. All
nine checks pass. The probe declares no Latin predicate, canonical target, checked source
transport, or proof body, and its own header marks it as discovery only. Its imports therefore
cannot be certified minimal for the absent target and receive no statement or proof credit.

A bounded exact-topic search over pinned mathlib, repository-local Lean formalizations, and the
owned target (excluding the probe itself) found no Latin-square, quasigroup, or orthogonal-array
declaration under the recorded terms. This is feasibility evidence only, not the downstream
immutable anchor audit or a global absence claim.

The environment is Lean `4.29.0` at commit
`98dc76e3c0a9b856c9b98726b713fb04fab16740`, Lake `5.0.0-src+98dc76e`, and pinned mathlib
revision `8a178386ffc0f5fef0b77738bb5449d50efeea95` with tree
`bdc39a3123201dae413a9d9be56ec242c19e5c2b`. The automation-provided
`Formalizations/Lean/.lake` symlink was reused without an update, build, clone, fetch, or other
dependency-mutation command. The pinned mathlib Git worktree remained clean.

## Validation Record

Commands ran on 2026-07-13 (`Asia/Shanghai`).

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | `check_stage1_standard: ok (15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, execution skill present)` |
| `python3 scripts/stage1_target.py check` | 0 | `stage1_target: ok (1546 unique targets, ranks 1..1546, all L0/rework_required)` |
| `python3 scripts/stage1_target.py show THM-M-0901` | 0 | rank 1043; planned; `L0/rework_required`; no legacy slot; legacy artifacts unaccepted; theorem incomplete |
| `git status --short --untracked-files=all`; `git rev-parse HEAD 'HEAD^{tree}'` (pre-edit) | 0 | only the automation-provided `Formalizations/Lean/.lake` symlink was untracked; base identifiers appear above |
| exact-path `sha256sum` commands recorded in `statement-blocker.json` | 0 | authority, source, intake, probe, toolchain, dependency-lock, and imported pinned-mathlib digests agree with the structured blocker |
| `cd Formalizations/Lean && lake env lean --version`; `lake --version` | 0 | pinned Lean and Lake versions recorded above |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD 'HEAD^{tree}'`; package status | 0 | pinned mathlib revision and tree match the values above; package worktree clean |
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0901/IntakeProbe.lean` | 0 | eight adjacent APIs plus the candidate matrix type elaborated; stdout was 746 bytes with SHA-256 `8bb72f0f3fd684866568beb2368582ea1a9f307197e4e1f61090a3f611ca7bc9`; no target declaration or proof body |
| bounded exact-topic `rg` search excluding `IntakeProbe.lean` | 1 (expected no match) | no target-specific declaration matched the recorded terms |
| `python3 -B Stage1_Instances/THM-M-0901/check_intake.py` | 1 | the historical intake checker stops because it freezes the intake authority state as `[ ]`, while the integrated execution DAG now records `[_]`; its frozen input hashes and intake-only inventory also predate this phase |
| prohibited declaration scan over owned Lean files | 1 (expected no match) | no `sorry`, `admit`, `sorryAx`, `axiom`, `constant`, `opaque`, or `unsafe` declaration |
| `python3 -m json.tool Stage1_Instances/THM-M-0901/statement-blocker.json` | 0 | finalized structured blocker parses as valid JSON |
| scoped `git diff --check` plus per-new-file no-index checks | 0 aggregate | no whitespace diagnostics; each no-index exit 1 is only the expected new-file difference |
| `test ! -e .stage1-worker-selftest.json` | 0 | self-test manifest is absent because the exact-statement deliverable did not pass |

The intake checker is a historical receipt checker. It binds the earlier intake authority state,
shared-input hashes, base revision, and original nine-file intake inventory. This statement attempt
records its exact replay limitation rather than rewriting the intake receipt, checker, instance,
target-local task DAG, generated blueprint, or authoritative execution DAG to manufacture
agreement.

## Retry Condition And Status Boundary

The integration lane must master-accept refreshed intake evidence before a future statement can be
accepted. Accountable reviewers must preserve and hash lawful immutable source editions, decide
whether the catalog target is one proposition or an explicit multi-root package, select and
independently approve every exact root and proof boundary, and transcribe all incorporated
definitions, ordered binders, hypotheses, conclusions, count conventions, equivalence relations,
computation boundaries, corrections, errata, and degenerate cases.

A fresh statement attempt can then encode precisely that approved claim or package, minimize the
pinned imports, serialize and hash each elaborated expression and environment, compile every
credited transport, and run all four required mutation classes.

This blocker is the assigned phase's truthful result, not completion of the statement item or any
downstream item. Lifecycle remains `planned`; `audit_complete: false` and
`theorem_complete: false`; no debt-vector change is proposed. Because the exact-statement
deliverable did not pass, no `.stage1-worker-selftest.json`, statement receipt, worker `[_]`, or
master acceptance is claimed.
