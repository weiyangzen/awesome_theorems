# Exact-statement gate: blocked

Item: `S56-M-0036-STATEMENT`

Theorem: `THM-M-0036` (Artin-Wedderburn theorem)

Base revision: `0ea006c25dcbfe400adbb084c0a3476a9b271741` (tree
`ff2e3bde08d7f5d6c83519160a4a6bd2cb7526db`).

## Decision

The statement item remains `[ ]`. Its prerequisite `S56-M-0036-INTAKE` has provisional worker
state `[_]` in the authoritative execution DAG, not master-accepted state `[x]`. The intake
receipt is unsigned, non-content-addressed, declares `accepted: false`, and contains no accepted
receipt ID. Dependency-ordered inspection is possible, but master acceptance of the intake still
precedes any accepted statement transition.

Independently, the exact-statement gate cannot pass from the received claim. The repository gives
only the title "Artin-Wedderburn theorem" and the gloss "classification of central simple
algebras." It supplies no exact source proposition, definitions, ordered binders, hypotheses,
conclusion, proof boundary, correction history, or boundary-case convention. In particular, it
does not decide:

- whether the input is a finite-dimensional central simple algebra over a field, a bundled
  `CSA K`, an algebra with explicit centrality/simplicity/finiteness assumptions, or a simple
  Artinian algebra;
- whether the conclusion is an algebra equivalence or ring equivalence, and whether it asserts
  existence only, a biconditional, or existence plus uniqueness;
- whether the resulting division algebra must explicitly be central over the base field;
- the base-field, characteristic, universe, positive matrix-size, nontriviality, and zero-case
  conventions; or
- the exact ownership boundary with the semisimple-ring theorem `THM-M-0027` and the Brauer
  classification targets `THM-M-0037` and `THM-M-0424`.

The Artin 1927 paper identified at intake is only a bibliographic lead. No lawful immutable copy,
pinpoint theorem and definition passage, translation, premise/proof-node map, Wedderburn genealogy,
correction or errata disposition, or independent review is accepted. Selecting the familiar
matrix-over-division-algebra existence theorem from convention would therefore invent, narrow,
broaden, or substitute mathematics rather than elaborate the exact received target.

Sections 5 and 5.1 of the rev-5.6 blueprint make statement ambiguity and a missing expression
fingerprint hard blockers. There is no canonical expression whose imports can honestly be
certified minimal, no credited alternate encoding to transport, and no meaningful
removed-hypothesis, changed-domain, changed-binder-scope, or boundary-case mutation. Those four
tests are undefined rather than passed. The vector remains `[H1, M3, R4]`.

## Pinned Lean Boundary

Pinned mathlib contains strong members of the theorem family. The existing discovery-only
`IntakeProbe.lean` uses:

```lean
import Mathlib.Algebra.BrauerGroup.Defs
import Mathlib.RingTheory.SimpleModule.WedderburnArtin
```

It re-elaborates `CSA`,
`IsSimpleRing.exists_algEquiv_matrix_divisionRing`,
`IsSimpleRing.exists_algEquiv_matrix_divisionRing_finite`, and the adjacent semisimple finite
candidate. The finite simple-algebra theorem returns a positive-size matrix algebra over a
division algebra finite over the commutative base, but its visible result does not require
`Algebra.IsCentral` for that division algebra. The foreign
`AwesomeTheorems.Stage1.S1_M_078.csa_wedderburn_artin_finite` wrapper specializes the candidate to
mathlib's bundled `CSA K`; it is discovery evidence owned by another target, not a source-identity
or proof-credit transfer.

The two simple-algebra candidate axiom reports are `[propext, Classical.choice, Quot.sound]`. This
is real pinned API validation, but the probe declares no canonical target or proof body for
`THM-M-0036`. Its two imports therefore cannot be certified as the minimal imports for an absent
target.

The environment is Lean `4.29.0` at commit
`98dc76e3c0a9b856c9b98726b713fb04fab16740`, Lake `5.0.0-src+98dc76e`, and pinned mathlib
revision `8a178386ffc0f5fef0b77738bb5449d50efeea95` with tree
`bdc39a3123201dae413a9d9be56ec242c19e5c2b`. The automation-provided canonical `.lake` symlink
was used read-only. No update, build, clone, fetch, or dependency mutation was run.

## Validation Record

Commands ran from this isolated worker clone on 2026-07-13 (`Asia/Shanghai`).

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, and 1546 uniform-L0 Lean 4 targets passed; execution skill present |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all `L0/rework_required` |
| `python3 scripts/stage1_target.py show THM-M-0036` | 0 | rank 1079; planned; no legacy slot; legacy artifacts unaccepted; theorem incomplete |
| `git status --short`; `git rev-parse HEAD 'HEAD^{tree}'` (pre-edit) | 0 | only the automation-provided `.lake` symlink was untracked; base revision and tree appear above |
| `sha256sum Docs/Stage1_Blueprint_rev-5.6.md Docs/Stage1_Targets_rev-5.6.json Docs/Stage1_Execution_DAG_rev-5.6.json skills/execute-stage1-rev56/SKILL.md Docs/Blueprint_Guidelines.md Docs/researches/math_theorems.md Docs/Stage0_Blueprint.md Stage1_Instances/THM-M-0036/{instance.json,source-statement-crosswalk.md,scope-map.md,task-dag.json,intake-receipt.json,IntakeProbe.lean,check_intake.py} Formalizations/Lean/{lean-toolchain,lake-manifest.json,.lake/packages/mathlib/Mathlib/RingTheory/SimpleModule/WedderburnArtin.lean,.lake/packages/mathlib/Mathlib/Algebra/BrauerGroup/Defs.lean,AwesomeTheorems/Stage1/S1_M_078.lean}` | 0 | exact hashes are recorded in `statement-blocker.json` |
| `cd Formalizations/Lean && lake env lean --version && lake --version` | 0 | pinned Lean and Lake versions recorded above |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD 'HEAD^{tree}'` | 0 | pinned mathlib revision and tree recorded above |
| `git -C Formalizations/Lean/.lake/packages/mathlib status --short` | 0 | empty output; pinned mathlib package worktree clean |
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0036/IntakeProbe.lean` | 0 | four adjacent interfaces elaborated; stdout was 1276 bytes with SHA-256 `57ea1aff839886ecd8e0b19695b0415514edc367a075c48624ad309901d33aee`; no canonical target or proof body was declared |
| bounded exact-topic search in pinned mathlib and repo-local Lean | 0 | located the theorem-family module, algebraically closed specialization, CSA definitions, and foreign CSA wrapper; discovery evidence only |
| `python3 -B Stage1_Instances/THM-M-0036/check_intake.py` | 1 | historical intake replay stops at its stale authority assertion: it expects intake state `[ ]` and attempts 0, while current authority records `[_]` and attempts 1 |
| prohibited-construct scan over owned Lean files | 1 | expected no-match result; no `sorry`, `admit`, `sorryAx`, `axiom`, `constant`, `opaque`, or `unsafe` declaration |
| JSON parse and scoped invariant check for `statement-blocker.json` | 0 each | blocker identity, null target/import/hash, unchanged vector, four undefined mutations, false completion fields, exact two-file scope, and absent self-test agree |
| `git diff --check -- Stage1_Instances/THM-M-0036` | 0 | no tracked whitespace diagnostics |
| per-file `git diff --no-index --check /dev/null` for both new blocker files | 1 each | expected new-file differences with empty diagnostics; no whitespace error |
| `test ! -e .stage1-worker-selftest.json` | 0 | self-test manifest intentionally absent because the exact-statement deliverable did not pass |

## Retry Condition And Status Boundary

Accountable source reviewers must preserve and hash a lawful immutable primary or authoritative
source, select and independently approve one exact proposition, transcribe all incorporated
definitions, ordered binders, assumptions, conclusion, proof boundary, corrections, and boundary
cases, and issue the neighbor-target identity decisions. A fresh statement worker can then encode
precisely that claim, minimize pinned imports, serialize and hash the elaborated expression and
environment, compile every credited transport, and execute all four required mutation classes.
The integration lane must also revalidate and master-accept the intake dependency before accepting
that later statement transition.

This blocker is the assigned phase's truthful result, not completion of the statement node or any
downstream node. Lifecycle remains `planned`; `audit_complete: false` and
`theorem_complete: false`; no debt-vector change is proposed. Because the exact-statement
deliverable did not pass, no `.stage1-worker-selftest.json`, statement receipt, worker `[_]`, proof
credit, or master acceptance is claimed.
