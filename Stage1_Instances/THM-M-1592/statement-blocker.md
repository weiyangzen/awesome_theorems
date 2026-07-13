# Exact-statement gate: blocked

Item: `S56-M-1592-STATEMENT`

Theorem: `THM-M-1592`

Base revision: `db6914155f1f63e835364b89ba0a3b25f1d7f936` (tree
`a5488edccb2687c4ff0bbdccf4650e06b2e45337`).

## Decision

The statement item remains `[ ]`. Its prerequisite `S56-M-1592-INTAKE` has provisional worker
state `[_]`, not master-accepted state `[x]`. Rev-5.6 section 10.2 permits this dependency-ordered
attempt, so pending master acceptance did not prevent the work. The intake receipt is unsigned and
non-content-addressed, declares `accepted: false`, has no accepted receipt ID, and intentionally
leaves the canonical mathematical statement and Lean target null. Master acceptance remains
required before any eventual accepted statement transition.

Independently, the exact-statement gate cannot pass from the authoritative repository record. It
supplies only the title `Reed-Solomon码`, the attribution Reed/Solomon, the year 1960, and the noun
phrase `MDS码` (MDS codes). It contains no cited truth-valued proposition, formula, definition chain,
ordered binder, hypothesis, conclusion, boundary case, proof boundary, or correction history.
Stage0 explicitly leaves the precise definitions and premises open, and the catalog's `已验证`
label is untrusted under rev-5.6.

The primary bibliographic lead, Reed and Solomon's 1960 paper *Polynomial Codes Over Certain Finite
Fields* (DOI `10.1137/0108018`, pages 300-304), identifies a source family but does not select a
single result for this repository item. The paper text was not available in the intake evidence,
the repository gives no internal locator, and no immutable source snapshot with an assumption,
definition, correction, and independent-review crosswalk has been accepted. The record therefore
does not decide among an evaluation-code construction, injectivity or dimension, a distance lower
bound, exact minimum distance, equality in the Singleton bound, an error-correction guarantee, a
decoder theorem, or a bundle of those claims.

It also leaves open ordinary versus generalized or extended Reed-Solomon codes; field and
cardinality; length and message dimension; evaluation points and distinctness; polynomial and code
encodings; Hamming and minimum-distance conventions; the meaning of MDS; quantifier order; and all
endpoint and degenerate cases. These choices produce inequivalent propositions. Selecting the
familiar `[n, k, n-k+1]` theorem from mathematical convention would invent missing mathematics,
not elaborate the exact received target.

Sections 5 and 5.1 of the rev-5.6 blueprint make statement ambiguity and a missing expression
fingerprint hard blockers. There is consequently no honest canonical expression for which minimal
imports, checked transports, or removed-hypothesis, changed-domain, changed-binder-scope, and
boundary-case mutations can be certified. Those mutations are undefined, not passed. The root
vector remains `[H1, M4, R4]`.

## Pinned Lean Boundary

The existing `IntakeProbe.lean` re-elaborates in the pinned environment. Its three direct imports
expose generic Hamming distance and norm, polynomial evaluation and root-cardinality bounds, and
Vandermonde determinant and evaluation-matrix interfaces. All nine checks pass. This is real
substrate validation, but the probe defines no Reed-Solomon code, MDS predicate, canonical target,
checked transport, or proof body. Its imports therefore cannot be certified minimal for an absent
target.

A bounded lexical search of pinned mathlib and repository-local Lean found no Reed-Solomon,
maximum-distance-separable, MDS-code, evaluation-code, or polynomial-code declaration under the
recorded terms. The unrelated local identifier `mds` in a tactic pretty-printer is not coding
theory. This is discovery-only feasibility evidence, not the downstream immutable anchor audit or
a claim of global absence.

The environment is Lean `4.29.0` at commit
`98dc76e3c0a9b856c9b98726b713fb04fab16740`, Lake `5.0.0-src+98dc76e`, and pinned mathlib
revision `8a178386ffc0f5fef0b77738bb5449d50efeea95` with tree
`bdc39a3123201dae413a9d9be56ec242c19e5c2b`. The automation-provided
`Formalizations/Lean/.lake` symlink was used read-only. No update, build, clone, fetch, or dependency
mutation was run.

## Validation Record

Commands ran from this isolated worker clone on 2026-07-13 (`Asia/Shanghai`).

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, and 1546 uniform-L0 Lean 4 targets passed; execution skill present |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all `L0/rework_required` |
| `python3 scripts/stage1_target.py show THM-M-1592` | 0 | rank 1213; planned; no legacy slot; legacy artifacts unaccepted; theorem incomplete |
| `git status --short --untracked-files=all`; `git rev-parse HEAD 'HEAD^{tree}'` (pre-edit) | 0 | only the automation-provided `.lake` symlink was untracked; base revision and tree appear above |
| repository, Stage0, intake dossier, and primary-source-lead inspection | n/a | read-only source assessment confirmed the noun-phrase catalog record, multiple inequivalent candidate claims, null intake target, and absence of an approved root selection; this is analysis, not a command result |
| `sha256sum` with the 18 literal authority/source/intake/toolchain paths recorded in `statement-blocker.json`; `sha256sum Formalizations/Lean/.lake/packages/mathlib/Mathlib/{InformationTheory/Hamming,Algebra/Polynomial/Roots,LinearAlgebra/Vandermonde}.lean` | 0 | exact current hashes and replayable argv are recorded in the JSON blocker |
| `git blame -L 11728,11733 -- Docs/researches/math_theorems.md` | 0 | all six sparse catalog fields originate at commit `bcf3f9fa...`; no later source-statement refinement |
| `cd Formalizations/Lean && lake env lean --version && lake --version` | 0 | pinned Lean and Lake versions recorded above |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD 'HEAD^{tree}'` and package status | 0 | pinned mathlib revision and tree recorded above; package worktree clean |
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-1592/IntakeProbe.lean` | 0 | nine generic APIs elaborated; complete stdout SHA-256 `1aec1e60...3c63`; no canonical target or proof body |
| bounded Reed-Solomon/MDS search in pinned mathlib and repo-local Lean | 0 | only the probe disclaimer and unrelated tactic-local `mds` identifier matched; no exact-topic declaration found |
| `python3 -B Stage1_Instances/THM-M-1592/check_intake.py` | 1 | historical intake replay stops at its stale pre-integration blueprint hash; its original nine-file inventory is also intentionally historical after this phase |
| `python3 -m json.tool Stage1_Instances/THM-M-1592/statement-blocker.json`; literal scoped `jq -e` filter recorded in the JSON blocker | 0 | valid JSON; target identity, blocked `[ ]` state, unchanged `H1/M4/R4`, null target/imports, four undefined mutations, false completion flags, and absent receipt/self-test claims agree |
| `rg -n '(sorry\|admit\|sorryAx\|^[[:space:]]*(axiom\|constant\|opaque\|unsafe)[[:space:]])' Stage1_Instances/THM-M-1592 --glob '*.lean'` | 1 expected no-match | no prohibited declaration |
| `git diff --check -- Stage1_Instances/THM-M-1592`; `git diff --no-index --check /dev/null Stage1_Instances/THM-M-1592/statement-blocker.{json,md}` (run separately) | 0 / 1 expected differences | no whitespace diagnostics; no-index exit 1 denotes each untracked file differs from `/dev/null` |
| `test ! -e .stage1-worker-selftest.json`; `test ! -e Stage1_Instances/THM-M-1592/statement-receipt.json` | 0 | no worker self-test or statement receipt was emitted because the statement gate failed |

The historical intake checker is frozen to its original authority bytes and nine-file intake
inventory. Integration subsequently changed the generated blueprint and execution DAG. Adding
these statement artifacts also makes that intake-only inventory historical. This statement run
records the limitation instead of rewriting the intake checker, receipt, instance, task DAG,
generated blueprint, or authoritative execution DAG to manufacture agreement.

## Retry Condition And Status Boundary

Accountable reviewers must lawfully preserve and hash an immutable primary or authoritative source,
select and independently approve one exact Reed-Solomon proposition, and transcribe every
incorporated definition, convention, ordered binder, hypothesis, conclusion, proof boundary,
correction, erratum, and degenerate case while preserving neighboring-target boundaries. They must
in particular fix the code variant, field, `n` and `k`, evaluation points, polynomial and code
representations, distance and MDS definitions, exact conclusion, quantifier order, and endpoints.
The integration lane must also master-accept the intake dependency before accepting a future
statement transition.

A fresh statement worker can then encode precisely that source-selected claim, minimize pinned
imports, serialize and hash the elaborated expression and environment, compile every credited
transport, and execute all four required mutation classes.

This blocker is the assigned phase's truthful result, not completion of the statement node or any
downstream node. Lifecycle remains `planned`; `audit_complete: false` and
`theorem_complete: false`; no debt-vector change is proposed. Because the exact-statement
deliverable did not pass, no `.stage1-worker-selftest.json`, statement receipt, worker `[_]`, or
master acceptance is claimed.
