# Exact-statement gate: blocked

Item: `S56-M-1591-STATEMENT`

Theorem: `THM-M-1591`

Base revision: `2eea98305d46266f078a50cf0e85853bf6a5e702` (tree
`02279a8caa5f31ed8e37e35c8584a336eed9b974`).

## Decision

The statement item remains `[ ]`. Its prerequisite `S56-M-1591-INTAKE` has provisional worker
state `[_]`, not master-accepted state `[x]`. Rev-5.6 section 10.2 permits this dependency-ordered
attempt, so pending master acceptance did not prevent the work. The intake receipt is unsigned and
non-content-addressed, declares `accepted: false`, has no accepted receipt ID, and intentionally
leaves the canonical mathematical statement and Lean target null. Master acceptance remains
required before any eventual accepted statement transition.

Independently, the exact-statement gate cannot pass from the authoritative repository record. It
supplies only the title `BCH码`, the attribution Bose/Chaudhuri/Hocquenghem, the year 1959, and the
gloss `能纠正多个错误的码` (codes capable of correcting multiple errors). It contains no cited
binder-complete proposition, formula, definition chain, ordered binder, hypothesis, exact
conclusion, boundary case, proof boundary, or correction history. Stage0 explicitly leaves the
precise definitions and premises open, and the catalog's `已验证` label is untrusted under rev-5.6.

The inspected Bose-Ray-Chaudhuri 1959 mimeograph identifies a source family but does not resolve the
repository ambiguity. It contains several distinct plausible roots: Lemma 1's weight criterion for
`t`-error correction, Theorem 1's binary rank-matrix criterion, and Theorem 3's construction of a
binary `t`-error-correcting code of length `2^m - 1` with a dimension bound. The report does not state
the modern consecutive-root generator-polynomial BCH bound verbatim. The catalog also names
Hocquenghem, but no authoritative Hocquenghem source was authenticated in the intake. Exact inherited
assumptions and endpoints, journal-version changes, errata, complete mapping, and independent source
approval remain open.

The record consequently does not decide among construction or existence, the BCH designed-distance
bound, an actual minimum-distance result, an error-correction corollary, a dimension estimate, or
decoder correctness. It also leaves open binary versus q-ary scope; base and extension fields;
length; primitive and narrow-sense conventions; root interval or matrix construction; generator,
check polynomial, and orientation; code representation; actual and designed distance; correction
radius and decoder model; quantifier order; and all endpoint and degenerate cases. These choices
produce inequivalent propositions. Selecting a familiar primitive narrow-sense BCH theorem would
invent missing mathematics, not elaborate the exact received target.

Sections 5 and 5.1 of the rev-5.6 blueprint make statement ambiguity and a missing expression
fingerprint hard blockers. There is consequently no honest canonical expression for which minimal
imports, checked transports, or removed-hypothesis, changed-domain, changed-binder-scope, and
boundary-case mutations can be certified. Those mutations are undefined, not passed. The root
vector remains `[H1, M4, R4]`.

## Pinned Lean Boundary

The existing `IntakeProbe.lean` re-elaborates in the pinned environment. Its three direct imports
expose generic Hamming-distance, finite-field, polynomial, and root-of-unity interfaces. All ten
checks pass. This is real substrate validation, but the probe defines no BCH code, canonical target,
checked transport, or proof body. Its imports therefore cannot be certified minimal for an absent
target.

A bounded lexical search of pinned mathlib and repository-local Lean found no BCH,
Bose-Ray-Chaudhuri, Hocquenghem, or cyclic-code declaration under the recorded terms. This is
discovery-only feasibility evidence, not the downstream immutable anchor audit or a claim of global
absence.

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
| `python3 Docs/tools/check_stage1_standard.py` | 0 | all 15 assurance groups, 41 legacy rows, 300 legacy slots, and 1546 uniform-L0 targets passed; execution skill present |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all `L0/rework_required` |
| `python3 scripts/stage1_target.py show THM-M-1591` | 0 | rank 1212; planned; no legacy slot; legacy artifacts unaccepted; theorem incomplete |
| initial `git status --short --untracked-files=all`; `git rev-parse HEAD 'HEAD^{tree}'` | 0 | only the automation-provided `Formalizations/Lean/.lake` symlink was untracked; base identifiers appear above |
| authority, source, intake, toolchain, manifest, and pinned mathlib source `sha256sum` commands | 0 | current fingerprints are recorded in `statement-blocker.json` |
| `git blame -L 11721,11726 -- Docs/researches/math_theorems.md` | 0 | all six sparse catalog fields originate at `bcf3f9fa...`; no later statement refinement |
| `cd Formalizations/Lean && lake env lean --version`; `lake --version` | 0 | Lean 4.29.0 at the recorded commit; Lake 5.0.0-src+98dc76e |
| pinned mathlib revision/tree and clean package status checks | 0 | mathlib revision and tree recorded above; package worktree clean |
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-1591/IntakeProbe.lean` | 0 | ten generic substrate APIs elaborated; complete stdout SHA-256 `fe164187...85d5d`; no canonical target or proof body |
| bounded BCH/cyclic-code search in pinned mathlib and repo-local Lean | 1 expected no-match | no exact-topic declaration found under the recorded terms |
| `python3 -B Stage1_Instances/THM-M-1591/check_intake.py` | 1 | historical intake replay stops at its stale stored hash for `Docs/Stage1_Blueprint_rev-5.6.md`; the intake evidence was not rewritten |
| `python3 -m json.tool Stage1_Instances/THM-M-1591/statement-blocker.json`; scoped `jq -e` blocker assertions | 0 | valid JSON; identity, blocked `[ ]` state, unchanged `H1/M4/R4`, null target/imports, four undefined mutations, false completion flags, and absent receipt/self-test claims agree |
| prohibited-declaration scan over owned Lean files | 1 expected no-match | no `sorry`, `admit`, `sorryAx`, `axiom`, `constant`, `opaque`, or `unsafe` declaration found |
| `git diff --check -- Stage1_Instances/THM-M-1591`; per-new-file `git diff --no-index --check /dev/null` | 0 / 1 expected differences | no whitespace diagnostics; no-index exit 1 denotes that each untracked file differs from `/dev/null` |
| `test ! -e .stage1-worker-selftest.json`; `test ! -e Stage1_Instances/THM-M-1591/statement-receipt.json` | 0 | no worker self-test or statement receipt was emitted because the statement gate failed |

The historical intake checker is frozen to its original authority bytes and intake-only inventory.
Integration subsequently changed the generated blueprint and execution DAG. Adding these statement
artifacts also makes the intake-only inventory historical. This statement run records the limitation
instead of rewriting the intake checker, receipt, instance, task DAG, generated blueprint, or
authoritative execution DAG to manufacture agreement.

## Retry Condition And Status Boundary

Accountable reviewers must lawfully preserve and hash an immutable primary or authoritative source,
select and independently approve one exact BCH proposition, and transcribe every incorporated
definition, convention, ordered binder, hypothesis, conclusion, proof boundary, correction, erratum,
and degenerate case while preserving neighboring-target boundaries. They must fix the candidate
result, base and extension fields, length, primitive and narrow-sense conventions, root or matrix
construction, generator or check orientation, designed and actual distance, correction radius, code
and decoder models, exact conclusion, quantifier order, and endpoints. The integration lane must also
master-accept the intake dependency before accepting a future statement transition.

A fresh statement worker can then encode precisely that source-selected claim, minimize pinned
imports, serialize and hash the elaborated expression and environment, compile every credited
transport, and execute all four required mutation classes.

This blocker is the assigned phase's truthful result, not completion of the statement node or any
downstream node. Lifecycle remains `planned`; `audit_complete: false` and
`theorem_complete: false`; no debt-vector change is proposed. Because the exact-statement
deliverable did not pass, no `.stage1-worker-selftest.json`, statement receipt, worker `[_]`, or
master acceptance is claimed.
