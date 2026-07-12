# Exact-statement gate: blocked

Item: `S56-M-0042-STATEMENT`

Theorem: `THM-M-0042`

Base revision: `4ecdda4863162748b3ee70bc4ec842789418145d` (tree
`aace54662cd5e9ca38472011f41afdbffdedfa04`).

## Decision

The statement item remains `[ ]`. Its prerequisite `S56-M-0042-INTAKE` has provisional worker
state `[_]`, not master-accepted state `[x]`. Dependency-ordered preparation is possible, but the
intake receipt is unaccepted and deliberately leaves the canonical proposition and Lean target
null.

The received catalog record says only that a complex matrix is similar to Jordan normal form. It
does not define a Jordan block or Jordan normal form, select a dimension or index type, state the
similarity witness and conjugation orientation, choose a block-order convention, decide whether
uniqueness is included, or settle the zero-dimensional and empty-block cases. Each choice changes
the formal proposition or requires an explicit checked equivalence transport; none is merely
unresolved notation.

The inspected modern source lead does not remove that ambiguity. Axler, *Linear Algebra Done
Right*, fourth edition, Definition 8.44 and Theorem 8.46, states an operator-and-Jordan-basis result
under a finite-dimensional nonzero-space convention. The catalog does not cite that edition. Its
definition chain, matrix/operator transport, correction status, immutable preservation, and
independent review remain open. The intake therefore classifies it as an `H1` lead, not an approved
source root.

Selecting `Matrix (Fin n) (Fin n) Complex`, an arbitrary finite index type, or `Module.End Complex
V` from mathematical familiarity would invent missing binders and conventions. Triangularization,
generalized-eigenspace spanning, and Jordan-Chevalley-Dunford decomposition are related but weaker
or different theorems. None may substitute for the catalog claim.

Rev-5.6 makes statement ambiguity and a missing elaborated-expression fingerprint hard blockers.
There is no honest canonical expression whose imports can be certified minimal, no approved
alternate encoding for a checked transport, and no canonical target against which the required
removed-hypothesis, changed-domain, changed-binder-scope, and boundary-case mutations can run.
Those mutation results are undefined, not passed. The root vector remains `[H1, M4, R4]`.

## Pinned Lean Boundary

The existing `IntakeProbe.lean` was re-elaborated using three direct imports:

- `Mathlib.LinearAlgebra.Eigenspace.Triangularizable`
- `Mathlib.LinearAlgebra.JordanChevalley`
- `Mathlib.LinearAlgebra.Matrix.GeneralLinearGroup.Defs`

It checks eight adjacent generalized-eigenspace, Jordan-Chevalley, invertible-matrix,
matrix-representation, diagonal-matrix, and block-matrix interfaces. All checks pass in the pinned
environment. A bounded exact-topic search found no Jordan-block, Jordan-basis, or Jordan-normal-form
target declaration in pinned mathlib or repo-local Lean. The probe declares no target, transport,
or proof body, and its imports cannot be certified minimal for an absent canonical target.

The environment is Lean `4.29.0` at commit
`98dc76e3c0a9b856c9b98726b713fb04fab16740`, Lake `5.0.0-src+98dc76e`, and pinned mathlib revision
`8a178386ffc0f5fef0b77738bb5449d50efeea95` with tree
`bdc39a3123201dae413a9d9be56ec242c19e5c2b`. The automation-provided `.lake` symlink was used
read-only. No update, build, clone, fetch, or dependency mutation was run.

## Validation Record

Commands ran from this worker clone on 2026-07-13 (`Asia/Shanghai`).

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, and 1546 uniform-L0 Lean 4 targets passed; execution skill present |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all `L0/rework_required` |
| `python3 scripts/stage1_target.py show THM-M-0042` | 0 | rank 1082; planned; no legacy slot; legacy artifacts unaccepted; theorem incomplete |
| `pwd && git status --short && git rev-parse HEAD`; `git rev-parse HEAD 'HEAD^{tree}'` (pre-edit) | 0 | worker clone confirmed; only the automation-provided `.lake` symlink was untracked; base revision and tree appear above |
| `git blame -L 321,326 -- Docs/researches/math_theorems.md` | 0 | all six sparse catalog fields originate at commit `bcf3f9fa79ab8c2b6610c9875668c2589b35b74f` |
| `cd Formalizations/Lean && lake env lean --version && lake --version` | 0 | pinned Lean and Lake versions recorded above |
| `git -C Formalizations/Lean/.lake/packages/mathlib status --short`; `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD 'HEAD^{tree}'` | 0 | package worktree clean; pinned revision and tree recorded above |
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0042/IntakeProbe.lean` | 0 | eight adjacent interfaces elaborated; stdout SHA-256 `fb397529f72d99215beffb60d06dea6016b944e70072b7a3739c6e3721db7e21`; no canonical target or proof declared |
| `rg -n -i 'jordan (block\|basis\|canonical\|normal form)\|jordanBlock\|jordanBasis\|jordanCanonical\|jordanNormal' Formalizations/Lean --glob '*.lean' --glob '!.lake/**' Stage1_Instances/THM-M-0042 \|\| true; rg -n -i 'jordan (block\|basis\|canonical\|normal form)\|jordanBlock\|jordanBasis\|jordanCanonical\|jordanNormal' Formalizations/Lean/.lake/packages/mathlib/Mathlib --glob '*.lean' \| head -100` | 0 | only the intake disclaimer and one repo-local planning sentence matched; no exact pinned Jordan-form target declaration was found |
| `python3 -B Stage1_Instances/THM-M-0042/check_intake.py` | 1 | historical intake validator is stale against the integration-updated authoritative DAG state and therefore is not statement evidence |
| `if rg -n '(sorry\|admit\|sorryAx\|^[[:space:]]*(axiom\|constant\|opaque\|unsafe)[[:space:]])' Stage1_Instances/THM-M-0042 --glob '*.lean'; then exit 2; else printf 'no prohibited Lean declarations\n'; fi` | 0 | the inner `rg` returned expected no-match exit 1; no prohibited declaration was found |
| `python3 -m json.tool Stage1_Instances/THM-M-0042/statement-blocker.json`; `jq -e '.item_id == "S56-M-0042-STATEMENT" and .verdict == "blocked" and .state == "[ ]" and .root_vector_before == {"H":"H1","M":"M4","R":"R4"} and .root_vector_after == .root_vector_before and (.canonical_statement == null) and (.canonical_formal_target == null) and (.minimal_imports == null) and (.statement_gate.mutation_tests \| all(. == "not_meaningful_without_a_canonical_statement")) and (.statement_gate_passed == false) and (.statement_elaborated == false) and (.audit_complete == false) and (.theorem_complete == false) and (.worker_selftest_manifest_emitted == false)' Stage1_Instances/THM-M-0042/statement-blocker.json` | 0 | valid JSON; identity, null target/imports, unchanged vector, four undefined mutations, false completion flags, and no-self-test boundary agree |
| `git diff --check -- Stage1_Instances/THM-M-0042` | 0 | no tracked whitespace diagnostics; this command does not cover untracked files |
| `git diff --no-index --check /dev/null Stage1_Instances/THM-M-0042/statement-blocker.json` | 1 (expected difference) | empty diagnostic output; no whitespace error in the new JSON file |
| `git diff --no-index --check /dev/null Stage1_Instances/THM-M-0042/statement-blocker.md` | 1 (expected difference) | empty diagnostic output; no whitespace error in the new Markdown file |
| `test ! -e .stage1-worker-selftest.json` | 0 | self-test manifest intentionally absent because the statement deliverable did not pass |

The intake checker is bound to intake-time authority hashes and the intake's original DAG state.
The integration lane has since recorded the intake as `[_]`, so the checker fails closed on that
changed input. It was not edited or represented as passing for this statement attempt.

## Retry Condition And Status Boundary

Accountable reviewers must lawfully preserve and hash an immutable primary or authoritative source,
select and independently approve one exact proposition, and transcribe every incorporated
definition, ordered binder, hypothesis, conclusion, proof boundary, correction, and boundary case.
They must decide the finite complex domain; Jordan-block and block-assembly definitions; similarity
witness and orientation; ordering and uniqueness conventions; matrix/operator transport; and the
zero-dimensional case. A later statement run can then encode precisely that claim, minimize its
pinned imports, serialize the elaborated expression and environment, compile every credited
transport, and execute all four mutation classes. Master acceptance of the intake remains required
before an accepted statement transition.

This blocker is the assigned phase's truthful result, not completion of the statement node or any
downstream node. Lifecycle remains `planned`; `audit_complete: false` and
`theorem_complete: false`; no debt-vector change is proposed. No `.stage1-worker-selftest.json`,
statement receipt, worker `[_]`, master acceptance, statement fingerprint, or proof credit is
claimed.
