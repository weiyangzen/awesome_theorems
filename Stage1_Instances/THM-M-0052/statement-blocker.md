# Exact-statement gate: blocked

Item: `S56-M-0052-STATEMENT`

Theorem: `THM-M-0052`

Base revision: `a16267e7165144d202080fb647261658fa75ceb2` (tree
`6edd90c440309a0c5ba277ef62d1733b4b9c05b1`).

## Decision

The statement item remains `[ ]`. Its intake dependency has provisional worker state `[_]`, but
its receipt is not accepted and its structured scope authority deliberately leaves the canonical
statement, formal declaration, expression hash, and canonical-target environment fingerprint null.

The catalog says only that every matrix has a unique generalized inverse. That sentence is false
if "generalized inverse" means only an inner inverse satisfying `A X A = A`, and the catalog does
not define the term. It also does not select complex rather than real scalars, rectangular index
types and binder order, the candidate inverse shape, conjugate-transpose conventions, or empty
dimension behavior.

Penrose's 1955 Theorem 1 is a strong primary-source lead: for every possibly rectangular complex
matrix `A`, there is a unique `X` satisfying `A X A = A`, `X A X = X`, `(A X)* = A X`, and
`(X A)* = X A`. The inspected article also admits zero and nonsquare matrices. The intake did not
approve this as the catalog's exact source root, however. Its OCR-to-symbol transcription,
incorporated finite-matrix conventions, correction history, immutable admission, and independent
review remain open, and the catalog's joint Moore attribution is not crosswalked to a pinpoint Moore
source. Selecting the familiar four-equation `Fin`/`Complex` encoding now would override the intake
authority's explicit `candidate_scope_not_credited` boundary.

Rev-5.6 makes statement ambiguity and a missing elaborated-expression fingerprint hard blockers.
There is consequently no approved canonical expression whose imports can be certified minimal, no
credited alternate encoding for a checked transport, and no target against which the mandatory
removed-hypothesis, changed-domain, changed-binder-scope, and boundary-case mutations can run. The
mutation results are undefined, not passed. The root vector remains `[H1, M4, R4]`.

## Pinned Lean Boundary

The existing discovery-only `IntakeProbe.lean` was re-elaborated using:

- `Mathlib.LinearAlgebra.Matrix.Hermitian`
- `Mathlib.LinearAlgebra.Matrix.NonsingularInverse`

It checks nine adjacent matrix, conjugate-transpose, Hermitian, and ordinary-inverse APIs. All
checks pass in the pinned environment. A bounded exact-topic search found no Moore-Penrose or
matrix-pseudoinverse target in pinned mathlib or repo-local Lean; the nonsingular-inverse module
explicitly says it does not consider pseudoinverses. The probe declares no target, transport, or
proof body, and its two imports are discovery imports, not a minimal-import claim for an absent
canonical statement.

The environment is Lean `4.29.0` at commit
`98dc76e3c0a9b856c9b98726b713fb04fab16740`, Lake `5.0.0-src+98dc76e`, and pinned mathlib revision
`8a178386ffc0f5fef0b77738bb5449d50efeea95` with tree
`bdc39a3123201dae413a9d9be56ec242c19e5c2b`. The automation-provided `.lake` symlink was used
read-only. No update, build, clone, fetch, or dependency mutation was run.

## Validation Record

Commands ran inside this worker clone on 2026-07-13 (`Asia/Shanghai`).

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, execution skill present |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all `L0/rework_required` |
| `python3 scripts/stage1_target.py show THM-M-0052` | 0 | rank 1090; planned; no legacy slot; legacy artifacts unaccepted; theorem incomplete |
| `git status --short --untracked-files=all`; `git rev-parse HEAD 'HEAD^{tree}'` (pre-edit) | 0 | only the automation-provided `Formalizations/Lean/.lake` symlink was untracked; base revision and tree appear above |
| `git blame -L 391,396 -- Docs/researches/math_theorems.md` | 0 | all six sparse, uncited catalog fields originate at `bcf3f9fa79ab8c2b6610c9875668c2589b35b74f` |
| `cd Formalizations/Lean && lake env lean --version && lake --version` | 0 | pinned Lean and Lake versions recorded above |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD 'HEAD^{tree}' && git -C Formalizations/Lean/.lake/packages/mathlib status --short` | 0 | pinned revision and tree recorded above; package worktree clean |
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0052/IntakeProbe.lean` | 0 | nine adjacent APIs elaborated; stdout SHA-256 `06a1329734422e9ac8d964af34664f8570ebb7e73640f08238ba085c3806a55c`; no target or proof declared |
| `rg -n -i 'moore.?penrose\|penrose.?moore\|pseudo.?inverse\|generalized inverse' Formalizations/Lean Stage1_Instances/THM-M-0052 --glob '*.lean' --glob '!.lake/**' \|\| true; rg -n -i 'moore.?penrose\|penrose.?moore\|pseudo.?inverse\|generalized inverse' Formalizations/Lean/.lake/packages/mathlib/Mathlib --glob '*.lean' \| head -100` | 0 | only the probe disclaimer, mathlib's explicit nonsupport sentence, and unrelated algebraic pseudo-inverse prose matched; no exact matrix target found |
| `python3 -B Stage1_Instances/THM-M-0052/check_intake.py` | 1 | historical intake checker rejected the integration-updated intake state `[_]`; it is stale statement input and was not modified or represented as passing |
| `python3 -m json.tool Stage1_Instances/THM-M-0052/statement-blocker.json >/dev/null && jq -e '.item_id == "S56-M-0052-STATEMENT" and .theorem_id == "THM-M-0052" and .verdict == "blocked" and .state == "[ ]" and .root_vector_before == {"H":"H1","M":"M4","R":"R4"} and .root_vector_after == .root_vector_before and (.canonical_statement == null) and (.canonical_formal_target == null) and (.minimal_imports == null) and (.statement_gate.mutation_tests \| all(. == "not_meaningful_without_a_canonical_statement")) and (.statement_gate_passed == false) and (.statement_elaborated == false) and (.audit_complete == false) and (.theorem_complete == false) and (.worker_selftest_manifest_emitted == false)' Stage1_Instances/THM-M-0052/statement-blocker.json` | 0 | identity, null target/imports, unchanged vector, four undefined mutations, false completion flags, and absent worker self-test agree |
| `if rg -n '(sorry\|admit\|sorryAx\|^[[:space:]]*(axiom\|constant\|opaque\|unsafe)[[:space:]])' Stage1_Instances/THM-M-0052 --glob '*.lean'; then exit 2; else printf 'no prohibited Lean declarations\n'; fi` | 0 | inner search returned expected no-match; no prohibited declaration found |
| `git diff --check -- Stage1_Instances/THM-M-0052` | 0 | no tracked whitespace diagnostics |
| `git diff --no-index --check /dev/null Stage1_Instances/THM-M-0052/statement-blocker.json` | 1 (expected difference) | empty output; no whitespace error in the new JSON file |
| `git diff --no-index --check /dev/null Stage1_Instances/THM-M-0052/statement-blocker.md` | 1 (expected difference) | empty output; no whitespace error in the new Markdown file |
| `test ! -e .stage1-worker-selftest.json` | 0 | self-test manifest intentionally absent because the statement deliverable did not pass |

The intake checker is content-bound to its intake-time authoritative state. Integration has since
recorded the predecessor as `[_]`, so its fail-closed assertion against the former `[ ]` state is
expected and supplies no statement evidence.

## Retry Condition And Status Boundary

Accountable reviewers must preserve and hash an immutable primary or authoritative source, approve
one exact proposition and every incorporated convention, independently verify the four-equation
transcription, and decide the Moore attribution boundary. They must freeze complex versus real
scalars, dimensions and index types, ordered binders, matrix multiplication association,
conjugate-transpose encoding, `ExistsUnique` shape, and all zero-dimension and rank-deficient cases.
A later statement run can then encode only that approved claim, minimize pinned imports, serialize
the elaborated expression and environment, compile every credited transport, and run all four
mutation classes. Master acceptance of the predecessor and the later statement receipt remains
required for an accepted transition.

This is a truthful blocked attempt, not statement-node completion. Lifecycle remains `planned`;
`audit_complete: false` and `theorem_complete: false`; no debt change, statement receipt, worker
`[_]`, master acceptance, expression fingerprint, proof credit, or `.stage1-worker-selftest.json` is
claimed.
