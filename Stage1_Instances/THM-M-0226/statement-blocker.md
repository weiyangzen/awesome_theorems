# Exact-statement gate: blocked

Item: `S56-M-0226-STATEMENT`

Theorem: `THM-M-0226`

Base revision: `2eea98305d46266f078a50cf0e85853bf6a5e702` (tree
`02279a8caa5f31ed8e37e35c8584a336eed9b974`).

## Decision

The statement item remains `[ ]`. Its prerequisite `S56-M-0226-INTAKE` has provisional state
`[_]`, not a master-accepted receipt. Provisional preparation of this later node does not permit an
accepted state transition. Independently, no exact Lean 4 target can be truthfully elaborated from
the authoritative repository record.

That record supplies only the title Schwarz lemma, Hermann Schwarz, 1869, and the gloss "a
holomorphic map from the unit disk to itself." It gives neither a proposition nor a conclusion.
It also gives no bibliography, exact theorem passage, incorporated definitions, proof boundary,
correction history, or independent review. Stage0 explicitly leaves precise definitions and
premises open. The intake accordingly keeps the canonical human claim, formal target, elaborated
expression hash, and canonical-target environment fingerprint null.

The missing decisions change the proposition rather than merely its notation:

- the essential fixed-origin hypothesis `f 0 = 0`, which is absent from the catalog gloss;
- total functions constrained on `Metric.ball 0 1` versus functions on a unit-disk subtype;
- complex differentiability, analyticity, or another source-selected holomorphicity convention;
- a strict open-disk self-map versus a closed-ball norm bound and the direction of any bridge;
- pointwise contraction, derivative contraction, both inequalities, or a different conclusion;
- equality at a nonzero point, derivative equality, and whether rotation rigidity is included; and
- behavior at zero, on the unit-circle boundary, and outside the disk for a total function.

These omissions are substantive. For example, fix `c : Complex` with `0 < norm c < 1` and let
`f := fun _ => c`. This constant strict disk self-map satisfies the catalog gloss but not the usual
pointwise conclusion `norm (f z) <= norm z` at `z = 0`.
Adding `f 0 = 0` or choosing the familiar two-inequality package from memory would therefore
manufacture a nearby textbook theorem. Choosing one generalized pinned mathlib declaration as the
root would instead substitute an unreviewed variant. Both actions are forbidden by rev-5.6.

There is consequently no canonical expression for which minimal imports, fixed elaboration
context, an expression/environment fingerprint, checked alternate transports, or meaningful
removed-hypothesis, changed-domain, changed-binder-scope, and boundary-case mutations can be
certified. Section 5 makes statement ambiguity and a missing expression fingerprint hard blockers.
The first failed gate is exact authoritative source-statement selection and conclusion-package
review.

## Pinned Lean Boundary

The existing `IntakeProbe.lean` was re-elaborated with its one direct import,
`Mathlib.Analysis.Complex.Schwarz`. It exposes the pinned pointwise, derivative, slope, and affine
equality interfaces and compiles a discovery-only wrapper for the conjunction of the two familiar
inequalities under a strict unit-disk self-map and `f 0 = 0`. The direct axiom reports for the
three explicitly printed candidates and the wrapper are
`[propext, Classical.choice, Quot.sound]`.

That result shows only that strong adjacent APIs are available. The intake explicitly declines to
identify its wrapper or any candidate as the requested root. The import therefore cannot be called
minimal for a source-selected target that does not yet exist, and the wrapper supplies no statement
identity, anchor-audit closure, proof credit, or theorem-completion evidence.

The environment is Lean `4.29.0` at commit
`98dc76e3c0a9b856c9b98726b713fb04fab16740`, Lake `5.0.0-src+98dc76e`, and pinned
mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95` with tree
`bdc39a3123201dae413a9d9be56ec242c19e5c2b`. The automation-provided `.lake` symlink and canonical
artifacts were used read-only; the mathlib package worktree remained clean. No update, build,
clone, fetch, or other dependency mutation was run.

## Validation Record

Commands ran in the isolated worker checkout on 2026-07-13 (Asia/Shanghai).

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | `check_stage1_standard: ok (15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, execution skill present)` |
| `python3 scripts/stage1_target.py check` | 0 | `stage1_target: ok (1546 unique targets, ranks 1..1546, all L0/rework_required)` |
| `python3 scripts/stage1_target.py show THM-M-0226` | 0 | rank 1239; planned; `L0/rework_required`; no legacy slot; legacy artifacts unaccepted; theorem incomplete |
| `git status --short --untracked-files=all` (pre-edit); `git rev-parse HEAD 'HEAD^{tree}'` | 0 each | only the automation-provided `.lake` symlink was untracked; base revision and tree are recorded above |
| `git blame -L 1633,1638 -- Docs/researches/math_theorems.md` | 0 | all six sparse catalog fields originate at commit `bcf3f9fa79ab8c2b6610c9875668c2589b35b74f` |
| `rg -n 'THM-M-0226\|施瓦茨引理\|单位圆盘到自身的全纯映射' --glob '!Docs/Stage1_Blueprint_rev-5.6.md' --glob '!Docs/Stage1_Execution_DAG_rev-5.6.json' --glob '!Docs/Stage1_Targets_rev-5.6.json' --glob '!Docs/Stage1_Blueprint_Applicable_Theorems.md' --glob '!Stage1_Instances/THM-M-0226/**' .` | 0 | found only the underspecified catalog row and Stage0 projection; no exact source proposition or accepted target mapping |
| `cd Formalizations/Lean && lake env lean --version`; `lake --version` | 0 each | Lean 4.29.0 and Lake 5.0.0 at the revisions above |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD 'HEAD^{tree}'`; package `status --short` | 0 each | pinned mathlib revision and tree above; package status output empty |
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0226/IntakeProbe.lean` | 0 | six adjacent interfaces and the discovery wrapper elaborated; axiom reports were `[propext, Classical.choice, Quot.sound]`; stdout SHA-256 `860f0019f7fba984e2750143cb9921a4dde04f5888fab5da1477d7365d71c955` |
| `python3 -B Stage1_Instances/THM-M-0226/check_intake.py` | 1 | known historical-intake freshness failure: the checker expects the intake node at `[ ]`, while the integrated authority now records provisional `[_]`; historical intake evidence was not rewritten |
| `sha256sum Docs/Stage1_Blueprint_rev-5.6.md Docs/Stage1_Targets_rev-5.6.json Docs/Stage1_Execution_DAG_rev-5.6.json skills/execute-stage1-rev56/SKILL.md Docs/Blueprint_Guidelines.md Docs/researches/math_theorems.md Docs/Stage0_Blueprint.md Formalizations/Lean/lean-toolchain Formalizations/Lean/lake-manifest.json` plus `sha256sum` on the nine intake files and pinned `Mathlib/Analysis/Complex/Schwarz.lean` | 0 | fingerprints are recorded in `statement-blocker.json` |
| scoped prohibited-declaration scan over owned Lean files | 1 | expected no-match exit; no `sorry`, `admit`, `sorryAx`, `axiom`, `constant`, `opaque`, or `unsafe` declaration |
| `python3 -m json.tool Stage1_Instances/THM-M-0226/statement-blocker.json` | 0 | structured blocker parses as JSON |
| `jq -e '.item_id == "S56-M-0226-STATEMENT" and .theorem_id == "THM-M-0226" and .execution_rank == 1239 and .phase == "statement" and .intent == "statement" and .verdict == "blocked" and .state == "[ ]" and .proposed_state == "[ ]" and .accepted == false and .canonical_statement == null and .canonical_human_statement == null and .canonical_formal_target == null and .minimal_imports == null and .elaborated_expression_hash == null and .environment_fingerprint_for_canonical_target == null and .root_vector_before == {H:"H1",M:"M3",R:"R4"} and .root_vector_after == .root_vector_before and all(.statement_gate.mutation_tests[]; . == "not_meaningful_without_a_canonical_statement") and all([.statement_gate_passed,.statement_elaborated,.statement_accepted,.audit_complete,.theorem_complete,.theorem_proved,.worker_selftest_manifest_emitted,.selftest_manifest_emitted,.node_specific_receipt_emitted,.statement_receipt_emitted,.accepted_state_claimed][]; . == false) and .changed_paths == ["Stage1_Instances/THM-M-0226/statement-blocker.json","Stage1_Instances/THM-M-0226/statement-blocker.md"] and .accepted_receipt_ids == [] and .canonical_obligation_ids == [] and .statement_fingerprints == [] and .typed_graph_changes == [] and .composition_certificates == []' Stage1_Instances/THM-M-0226/statement-blocker.json` | 0 | identity, null target/import/hash, unchanged vector, four undefined mutations, false completion flags, exact two-file scope, and no-self-test boundary agree |
| `git diff --check -- Stage1_Instances/THM-M-0226`; separate new-file whitespace checks | 0 / expected difference | no whitespace diagnostics |
| `test ! -e .stage1-worker-selftest.json` | 0 | self-test manifest intentionally absent because the exact-statement deliverable did not pass |

The historical intake checker is not current statement evidence. It freezes its intake worker's
older source snapshot, authority state, and intake-only file inventory. Rewriting it would alter a
different phase's evidence and would not cure the missing proposition.

## Retry Condition And Status Boundary

Before an eventual accepted statement transition, the integration lane must master-accept the
intake. Accountable reviewers must also lawfully preserve and hash an immutable primary or
authoritative source, transcribe its exact theorem with every incorporated definition, ordered
binder, hypothesis, conclusion, equality clause, proof boundary, correction, and erratum, and
independently approve the mapping. A later statement worker can then encode only that claim,
minimize its pinned imports, serialize and hash the elaborated expression and environment, compile
every credited transport, and execute all four required mutation classes.

This records the first failed gate. It does not complete the statement node or any downstream node.
The root remains `[H1, M3, R4]`; `audit_complete` and `theorem_complete` remain false, and no debt
change is proposed. The assigned phase is not genuinely self-tested to its completion gate, so no
`.stage1-worker-selftest.json`, node-specific completion receipt, worker `[_]`, proof credit, or
master-acceptance claim is emitted.
