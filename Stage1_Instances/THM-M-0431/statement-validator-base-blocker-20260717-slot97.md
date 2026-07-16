# THM-M-0431 statement validator-base blocker

## Scope

This is the target-scoped fail-closed result for `S56-M-0431-STATEMENT` at
worker base `9241b064a32cea3e16eb45d156fef8a2577704b0` (tree
`c60b403a3058af0bbf32405a99c931274675784a`). It changes no theorem source,
prior receipt, task-state authority, theorem-DAG projection, lifecycle, debt
vector, or acceptance state.

The exact claim tuple is
`(v2_execution_rank=293, phase_layer=1, phase_item_id=S56-M-0431-STATEMENT)`.
The current theorem-DAG SHA-256 is
`b0d43b142ed4d47aba3b66062c8303e96a736f259e50ef764918040521449c3a`,
and the stable target dependency-context SHA-256 is
`068170c76abd4579d643ede04d731b974412185bd285e7b40255ec4044adec5c`.

## Authoritative current state

The sole task-state authority, `Docs/Stage1_Blueprint_v2.md`, records both
`S56-M-0431-INTAKE` and this statement item as `[_]` with one attempt. Under
the dual-cursor protocol, `[_]` is unfinished worker-self-tested evidence; it
is not master acceptance and must not be redone or promoted by a worker. The
current theorem-DAG projection agrees on those states and records no direct
hard parent, transitive hard ancestor, hard edge, reuse hint, or shared lemma
group.

The tracked statement receipt is truthful negative evidence, not a positive
statement result. It has schema `stage1-node-receipt/1.0`, SHA-256
`090769df640b2115ac5de089b394a04ebe48441e836269a3a31e31715112ab32`,
Git blob `e294d51d63e5b291df8b53f4525f23f32d09bc58`,
`accepted=false`, `verdict=blocked`, no statement fingerprint, and four
unrun mutations. Its source record has no canonical human statement or Lean
declaration/expression. Provider or predecessor acceptance is not inherited.

## First failed gate

`G05-AUTHORITY-REPLAY / validator_base_stale` is the first mechanically
unrepairable worker gate. The mandatory HEAD contract has SHA-256
`1e7adf0f4fae0541b3595d4b0bfbb53f7eb17e28a4a889fec14f6df969e0cec4`
and Git blob `84b92df9eaf457ab954b652c3f20f4d513cf0a88`. For `statement` it declares
these scheduler-owned candidates:

- `Stage1_Instances/THM-M-0431/check_statement.py`
- `Stage1_Instances/THM-M-0431/check_statement_artifacts.py`

Exactly one exists at the worker base: `check_statement.py`, Git blob
`54fdc21cd476f64ba20f2740465956db5f1d5055`. The blob is unchanged in this
worker, so the authority-selected argv is:

```text
/usr/bin/python3 -I -B Stage1_Instances/THM-M-0431/check_statement.py
exit: 1
stderr: empty
stdout: {"audit_complete":false,"blocked":false,"first_failed_gate":"S01-ARTIFACTS","item_id":"S56-M-0431-STATEMENT","message":"Negative statement packet validation failed: repository HEAD differs from the worker base","open_obligations":5,"phase":"statement","phase_accepted":false,"phase_predicate_proven":false,"schema_version":"stage1-validator-semantic-result/1.0","stale_inputs":[],"status":"failed","theorem_complete":false,"theorem_id":"THM-M-0431","verdict":"repair_required"}
```

The validator hard-codes ancestor base
`94009a6bebd743588e09c3b45bfbf18bf9b5c5e3`, ancestor tree
`daabee9f9b2c6e98d84b6290f78a209b950485fc`, and obsolete theorem-DAG
digest `eaee68bdf9fde9e311db076d1997fd8ef91919def0ba0fb399f1df77080f7153`.
It rejects current HEAD before validating its tracked packet. Its typed output
is a semantic failure with `phase_accepted=false`; exit zero cannot be inferred.
The worker is forbidden to refresh, replace, rename, create, or delete a
validator candidate. Consequently this phase is not genuinely self-tested on
the current base. No phase receipt is refreshed and no
`.stage1-worker-selftest.json` is emitted.

## Dependency and reuse audit

The exact `parent_inspection_order`, direct-hard-parent list,
transitive-hard-ancestor list, hard-edge list, reuse-hint list, and shared-group
list are all `[]`. The complete closure was traversed exactly once as the empty
sequence before any proof work. No provider phase state, receipt, declaration
body, reusable artifact, terminal proof body, checkbox state, proof credit, or
acceptance was consumed, copied, transported, or inherited. No proof work was
performed. The empty declared context is not a claim of mathematical
independence.

The existing target-owned `dependency-reuse-ledger.json` has the required
`stage1-dependency-reuse-ledger/1.1` schema and truthfully records empty
`inspections`, `reuse_decisions`, and
`unresolved_compatibility_obligations`. It binds the same ancestor revision
and obsolete graph digest as the validator. It is historical packet evidence,
not a current-base ledger. It is not refreshed here because, without lawful
semantic replay, a ledger-only delta cannot support a new receipt or self-test
handoff.

## Positive statement gate remains open

Even after the scheduler-owned validator is repaired, the positive statement
predicate remains blocked. The repository source row says only "the local
Langlands correspondence for local fields." It does not select a group,
local-field class, coefficient field, representation and parameter categories,
equivalence relations, or normalization/compatibility package. The intake's
characteristic-zero `GL_n` formulation is provisional scope guidance and has
no accepted intake receipt.

The pinned environment exposes adjacent local-field, `GL_n`, and ordinary
representation interfaces, but the tracked `Statement.lean` deliberately
declares no target. It supplies neither smooth irreducible admissible
representation classes nor Frobenius-semisimple Weil-Deligne parameter
classes, and no exact expression, fingerprint, checked transport, or required
mutation result exists. The legacy abstract `LocalLanglandsStatementShape`
allows caller-supplied parameter types and predicates, so it cannot substitute
for the source theorem. Thus `S02-EXACT-TARGET` and `S03-MUTATIONS` remain
open; `audit_complete=false` and `theorem_complete=false`.

## Checks run

All commands ran in this worker clone on 2026-07-17 (Asia/Shanghai). No
`lake update`, `lake build`, dependency clone/fetch, network operation, or
`.lake` mutation was performed.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | Rev-5.6 structure, manifest, v2 DAG, phase contract, and execution skill passed. |
| `python3 Docs/tools/check_stage1_theorem_dag_v2.py` | 0 | 1546 theorem nodes, 10822 phase states, typed relationships, state preservation, and acyclicity passed. |
| `python3 Docs/tools/check_stage1_phase_acceptance_contracts.py` | 0 | Seven phases, twelve common gates, and twenty-three source references passed. |
| `python3 scripts/stage1_target.py check` | 0 | The ordered 1546-target L0/rework-required manifest passed. |
| `python3 scripts/stage1_target.py show THM-M-0431` | 0 | Rank 59, planned lifecycle, legacy artifacts unaccepted, theorem incomplete. |
| Declared candidate enumeration and Git-blob comparison | 0 | Exactly one candidate exists, and its current blob equals the worker-base blob. |
| `/usr/bin/python3 -I -B Stage1_Instances/THM-M-0431/check_statement.py` | 1 | One typed semantic JSON object reported `repair_required`, `phase_accepted=false`, and the stale worker base. |
| `cd Formalizations/Lean && LC_ALL=C TZ=UTC lake env lean --trust=0 ../../Stage1_Instances/THM-M-0431/Statement.lean` | 0 | The unchanged declaration-free boundary probe elaborated against the existing pinned artifacts; it grants no exact-target credit. |
| `git diff --check -- Stage1_Instances/THM-M-0431 .stage1-worker-selftest.json` | 0 | No whitespace errors in the target-scoped handoff. |

The structural checks are bounded supporting observations. They cannot replace
the failed scheduler-selected semantic validator or close the exact-statement
predicate.

## Retry condition and status boundary

The scheduler/master lane must publish a refreshed `check_statement.py` whose
unchanged blob is already present at the next worker base and whose exact
declared command validates then-current authority and artifact hashes. A fresh
claim can then bind the current empty dependency ledger and exactly one
statement receipt. Positive phase acceptance additionally requires a
source-selected exact mathematical proposition, concrete pinned object model,
kernel-elaborated expression and fingerprint, checked alternate transports,
and all four contract-required mutation classes.

This blocker grants no state transition, phase acceptance, accepted receipt,
provider acceptance transfer, exact statement credit, proof credit, audit
completion, theorem completion, or master acceptance.

## Continuation audit

The persisted goal was resumed against the same worker base and tree. The
authoritative statement cursor remains `[_]` with one attempt, the dependency
closure remains exactly empty, and the sole declared validator remains the
same unchanged Git blob. Its exact authority-selected replay again exited `1`
with the same typed `repair_required` result because its embedded worker base
is stale. No scheduler-owned repair or fresh base has appeared, so no lawful
receipt refresh or worker self-test handoff has become possible.

A third consecutive persisted-goal audit again observed that identical base,
authority digests, `[_]` cursor, empty dependency context, and validator blob.
The same exact replay failed for the same embedded-base mismatch. This is an
external scheduler-ownership impasse: the worker cannot repair the immutable
candidate and cannot manufacture a valid handoff from its negative result.
