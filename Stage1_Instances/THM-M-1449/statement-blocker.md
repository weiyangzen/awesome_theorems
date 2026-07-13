# THM-M-1449 exact-statement gate: blocked

Item: `S56-M-1449-STATEMENT`

Base revision: `58fbed45d2c785466ee920c7696f0f7b3686d9a5` (tree
`36198f7c90045b3b21d338a3d0ce47aa4ff930f1`).

## Decision

The statement item remains `[ ]`. Its prerequisite `S56-M-1449-INTAKE` is only in provisional
worker state `[_]`; `intake-receipt.json` has `accepted: false`, is not content-addressed, and has no
accepted receipt IDs. It also binds older blueprint and execution-DAG hashes, so it is not fresh
accepted dependency evidence.

More importantly, intake deliberately leaves the exact human proposition, Lean module, declaration
or expression, expression hash, and canonical-target environment fingerprint unresolved. The
catalog says only "SVD decomposition of a matrix." It does not fix the real or complex scalar
field, dimensions and indices, full/thin/compact factor shape, square factor equations, product
orientation, rectangular diagonal encoding, singular-value ordering/multiplicity/zero padding,
existence versus uniqueness, or empty and rank-deficient cases.

Axler, *Linear Algebra Done Right*, fourth edition, Section 7E, Definition 7.65 and Theorem 7.70 is
an authoritative modern lead for finite-dimensional real or complex linear maps. The observed
author-hosted PDF has SHA-256
`45f821b6f51e1f6c42728db6254699d89c14c90fcdb2443c1341188672815d03`, but the catalog does not cite
it. No immutable admission, complete matrix transport, empty-dimension reconciliation, correction
audit, historical audit, or independent source review is accepted.

The likely duplicate `THM-M-0044` owns a full rectangular Real-and-Complex target of the form
`A = U * Sigma * star V` plus substantive proof and validation candidates. That is useful discovery,
not permission to transfer its source selection, target, receipts, proof, or status. Its statement
receipt has `accepted: false`, and no accepted identity, root-ownership, merge, checked transport,
or evidence-sharing decision connects it to this target. Copying that target would silently choose
one of several inequivalent SVD conventions and violate the source-fidelity boundary.

Rev-5.6 makes this ambiguity a hard statement-gate failure. There is no truthful canonical Lean
expression whose imports can be minimized, no expression to fingerprint, and no approved alternate
encoding to transport. The required removed-hypothesis, changed-domain, changed-binder-scope, and
boundary mutations are therefore not meaningful rather than passed. The root vector remains
`[H1, M3, R4]`.

## Pinned Lean Boundary

The discovery-only `IntakeProbe.lean` was re-elaborated against the existing pinned environment. It
checks twelve singular-value, spectral, diagonal, conjugate-transpose, and unitary interfaces. The
representative axiom reports name only `propext`, `Classical.choice`, and `Quot.sound`. The probe
declares no SVD target, transport, or proof, so its three imports cannot establish minimality for an
absent canonical expression. A bounded search found the sibling target and adjacent APIs but no
accepted source-identical `THM-M-1449` root.

The environment is Lean `4.29.0` at commit
`98dc76e3c0a9b856c9b98726b713fb04fab16740`, Lake `5.0.0-src+98dc76e`, and pinned mathlib revision
`8a178386ffc0f5fef0b77738bb5449d50efeea95` with tree
`bdc39a3123201dae413a9d9be56ec242c19e5c2b`. The automation-provided canonical `.lake` symlink was
used read-only. No dependency update, build, clone, fetch, or other `.lake` mutation was run.

## Validation Record

Commands ran from this worker clone on 2026-07-13 (`Asia/Shanghai`).

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, and 1546 uniform-L0 Lean 4 targets passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all `L0/rework_required` |
| `python3 scripts/stage1_target.py show THM-M-1449` | 0 | rank 1126; planned; no legacy slot; legacy artifacts unaccepted; theorem incomplete |
| `git status --short --untracked-files=all; git rev-parse HEAD 'HEAD^{tree}'` | 0 | pre-edit status contained only the automation-provided untracked `Formalizations/Lean/.lake`; base revision and tree appear above |
| `git blame -L 10581,10586 -- Docs/researches/math_theorems.md` | 0 | all six sparse catalog lines originate at commit `bcf3f9fa79ab8c2b6610c9875668c2589b35b74f` |
| `cd Formalizations/Lean && lake env lean --version && lake --version` | 0 | pinned Lean and Lake versions recorded above |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD 'HEAD^{tree}'; git -C Formalizations/Lean/.lake/packages/mathlib status --short` | 0 | pinned revision and tree recorded above; package worktree clean |
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-1449/IntakeProbe.lean` | 0 | twelve adjacent APIs elaborated; stdout SHA-256 `fbfd5026c59f3de1e752c148cb239918dd0c1bd8b0966280c91b3c382b2c50bb`; no target declared |
| bounded SVD search over `Stage1_Instances`, repo-local Lean, and pinned mathlib Lean sources | 0 | 26 matches; output SHA-256 `4c1a640393672c4c21fcc31bcf12b040d861007deb03b74f2224e78c5ccd0f1c`; sibling and prerequisite candidates only |
| `python3 -B Stage1_Instances/THM-M-1449/check_intake.py` | 1 | the historical intake checker fails closed at stale `authoritative_blueprint_sha256`; it is not statement evidence and was not modified |
| prohibited Lean declaration scan over `Stage1_Instances/THM-M-1449/*.lean` | 1 (expected no match) | no `sorry`, `admit`, `sorryAx`, `axiom`, `constant`, `opaque`, or `unsafe` declaration |
| `python3 -m json.tool Stage1_Instances/THM-M-1449/statement-blocker.json` | 0 | finalized blocker is valid JSON |
| scoped blocker invariant command below | 0 | identity, null target/imports, unchanged vector, four undefined mutations, false completion flags, exact two-file scope, and no-self-test boundary agree |
| scoped whitespace command below | 0 | no whitespace diagnostics in the two blocker artifacts |
| `test ! -e .stage1-worker-selftest.json` | 0 | no self-test manifest was emitted because the assigned statement deliverable did not pass |

The two longer scoped commands, recorded here without abbreviation, were:

```bash
jq -e '.item_id == "S56-M-1449-STATEMENT" and .theorem_id == "THM-M-1449" and .execution_rank == 1126 and .phase == "statement" and .verdict == "blocked" and .state == "[ ]" and .root_vector_before == {"H":"H1","M":"M3","R":"R4"} and .root_vector_after == .root_vector_before and (.canonical_statement == null) and (.canonical_formal_target == null) and (.minimal_imports == null) and (.elaborated_expression_hash == null) and (.environment_fingerprint_for_canonical_target == null) and (.statement_gate.mutation_tests | all(. == "not_meaningful_without_a_canonical_statement")) and (.statement_gate_passed == false) and (.statement_elaborated == false) and (.statement_accepted == false) and (.audit_complete == false) and (.theorem_complete == false) and (.worker_selftest_manifest_emitted == false) and (.node_specific_receipt_emitted == false) and (.changed_paths == ["Stage1_Instances/THM-M-1449/statement-blocker.json","Stage1_Instances/THM-M-1449/statement-blocker.md"]) and (.accepted_receipt_ids == []) and (.statement_fingerprints == [])' Stage1_Instances/THM-M-1449/statement-blocker.json

git diff --check -- Stage1_Instances/THM-M-1449 && for f in Stage1_Instances/THM-M-1449/statement-blocker.json Stage1_Instances/THM-M-1449/statement-blocker.md; do git diff --no-index --check /dev/null "$f" >/tmp/thm-m-1449-one.out 2>&1; rc=$?; test "$rc" -eq 1; test ! -s /tmp/thm-m-1449-one.out; done
```

The historical intake validator is intentionally not repaired by this statement-only assignment.
Its freshness failure is recorded rather than hidden.

## Retry Condition

The integration lane must first accept fresh intake evidence. Accountable reviewers must then
preserve and hash a lawful immutable source, independently approve one exact SVD proposition,
resolve `THM-M-0044` identity and root ownership, and freeze every scalar, dimension, index, factor
shape, unitary or orthogonal predicate, star orientation, rectangular diagonal, singular-value
order/multiplicity/zero-padding, uniqueness, binder, hypothesis, conclusion, and boundary choice.
A later statement run can encode only that proposition, minimize its pinned imports, serialize the
elaborated expression and environment, compile every credited transport, and execute all four
mutation classes.

This is a truthful blocked statement attempt, not completion of this node or any downstream node.
No statement receipt, root worker self-test packet, worker `[_]`, master acceptance, proof credit,
audit completion, or theorem completion is claimed.
