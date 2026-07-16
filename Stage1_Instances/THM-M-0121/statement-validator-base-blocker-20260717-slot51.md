# THM-M-0121 statement validator-base blocker

## Scope

This is the target-scoped fail-closed result for `S56-M-0121-STATEMENT` at worker base
`0c2274d4ca42a99c4281bd566d19f1db7530a87a` (tree
`d1b6ec259121c90799df53290217af4ee29444b3`). It changes no Lean source, prior receipt,
dependency ledger, task-state authority, theorem-DAG projection, lifecycle, debt vector, or
acceptance state.

The exact claim tuple is
`(v2_execution_rank=274, phase_layer=1, phase_item_id=S56-M-0121-STATEMENT)`. The current
theorem-DAG SHA-256 is
`78e8063002c0e50e2b2d5de6f539073b0a91215542ff3ae241b5d03c0bf05e22`, and the stable target
dependency-context SHA-256 is
`068170c76abd4579d643ede04d731b974412185bd285e7b40255ec4044adec5c`.

## Authoritative state and failed gate

The sole task-state authority, `Docs/Stage1_Blueprint_v2.md`, records the intake predecessor and
this statement item as `[_]` with one attempt each. These states are unfinished worker-self-tested
evidence, not master acceptance. The current theorem-DAG projection agrees. In particular, the
intake predecessor is not `[x]`, and its manifest deliberately leaves the source statement and
formal target null.

`G05-AUTHORITY-REPLAY.validator_semantically_stale_for_current_worker_base` is the first
worker-unrepairable gate. The mandatory HEAD contract has SHA-256
`1e7adf0f4fae0541b3595d4b0bfbb53f7eb17e28a4a889fec14f6df969e0cec4` and Git blob
`84b92df9eaf457ab954b652c3f20f4d513cf0a88`. For `statement`, it declares these two
scheduler-owned candidate paths:

- `Stage1_Instances/THM-M-0121/check_statement.py`
- `Stage1_Instances/THM-M-0121/check_statement_artifacts.py`

Exactly one exists in both worker-base HEAD and the current tree: `check_statement.py`, SHA-256
`c841ab68d902a14de2ba961c98e8ad0a17c9cdbd3e19442587b2dce9d9496e0c`, Git blob
`7ef798a50f2c5b0dbddb63f50a29841ff2baa5e9`. The blob is unchanged. The authority-selected replay
is therefore:

```text
/usr/bin/python3 -I -B Stage1_Instances/THM-M-0121/check_statement.py
exit: 1
stdout: {"audit_complete":false,"blocked":false,"first_failed_gate":"VALIDATOR-INTERNAL-CONSISTENCY","item_id":"S56-M-0121-STATEMENT","message":"Validator consistency failure: AssertionError: ","open_obligations":5,"phase":"statement","phase_accepted":false,"phase_predicate_proven":false,"schema_version":"stage1-validator-semantic-result/1.0","stale_inputs":[],"status":"failed","theorem_complete":false,"theorem_id":"THM-M-0121","verdict":"repair_required"}
```

The stdout is exactly one JSON object with the required semantic-result schema, but its semantics
are `status=failed`, `verdict=repair_required`, `phase_accepted=false`, and
`phase_predicate_proven=false`. Its SHA-256 is
`79a5fb2c76c2ce028d1613cf515df69dfe2d33106bb38eb9afaf9573e6f075ae`. Stderr is the traceback
for the first assertion in `validate_authority`; it has SHA-256
`5b2701d620de84a0bf2802f64b5adffc100900f4f00c0aa5a320a4922b6cd8c3`.

The unchanged validator hard-codes base `307c34d30fc3763c82a944a142ae922b48ff18aa`, tree
`ef45ba442c71959db78ad146a023bcf32946a53f`, theorem-DAG digest
`8be71ef1e4fa1c3de5aa420550ff915dbe0b9f165ac0d98518adf2d1fe25fd47`, and the then-current
statement state `[ ]` with zero attempts. Current authority is base `0c2274d4ca42a99c4281bd566d19f1db7530a87a`,
theorem-DAG digest `78e8063002c0e50e2b2d5de6f539073b0a91215542ff3ae241b5d03c0bf05e22`, and statement state
`[_]` with one attempt. The worker is expressly forbidden to refresh, replace, rename, create, or
delete a validator candidate. Exit code or historical self-test evidence cannot override this typed
negative result. Consequently no receipt is refreshed and no `.stage1-worker-selftest.json` is
emitted.

## DAG and reuse boundary

The exact `parent_inspection_order`, direct-hard-parent list, transitive-hard-ancestor list,
hard-edge list, reuse-hint list, and shared-group list are all `[]`. The complete closure was
traversed exactly once as the empty sequence before any proof work. No provider phase state,
receipt, declaration, proof body, reusable artifact, import, copy, transport, checkbox state,
acceptance, or proof credit was consumed or inherited. No proof work was performed. This empty
declared context is not an independent mathematical-proof claim.

The tracked `dependency-reuse-ledger.json` already uses schema
`stage1-dependency-reuse-ledger/1.1` and truthfully contains empty `inspections`,
`reuse_decisions`, and `unresolved_compatibility_obligations`. It binds the same stable context but
the earlier base and DAG bytes. It is retained as historical packet evidence because a ledger-only
refresh cannot repair scheduler-owned semantic replay and would stale the tracked receipt's exact
input binding. A fresh validator-eligible statement claim must refresh the ledger before proposing
new phase evidence.

## Positive statement boundary

Independently of validator freshness, `S02-EXACT-TARGET` and `S03-MUTATIONS` remain open. Repository
evidence supplies only the label "Mori rationality theorem," Mori attribution, a year, and the gloss
"rationality of Fano varieties." It supplies no immutable theorem passage, theorem/page locator,
definitions, assumptions, corrections, or approved translation. Nef-threshold rationality,
rational curves or uniruledness, rational connectedness, and birational rationality are materially
different propositions. The unqualified claim that every Fano variety is birationally rational is
false in standard meanings.

`Statement.lean` therefore remains a declaration-free negative boundary probe. Its sole import,
`Mathlib.AlgebraicGeometry.RationalMap`, exposes three adjacent rational-map interfaces but no
canonical Mori target, expression fingerprint, environment fingerprint, checked transport, or
required mutation fixture. The tracked statement receipt is correspondingly `accepted=false`,
`verdict=blocked`, with no statement fingerprint and four unexecuted mutation classes. Neither it
nor the `[_]` cursor proves the positive phase predicate.

## Checks run

All commands ran in this worker clone on 2026-07-17 (Asia/Shanghai). The automation-provided pinned
`.lake` symlink was used read-only. No update, build, dependency clone/fetch, network operation, or
dependency mutation was performed.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | Rev-5.6 structure, manifest, v2 DAG, phase contract, and execution skill passed. |
| `python3 Docs/tools/check_stage1_theorem_dag_v2.py` | 0 | 1546 theorems, 10822 states, 2 hard edges, 5 reuse hints, 311 shared groups, and acyclicity passed. |
| `python3 Docs/tools/check_stage1_phase_acceptance_contracts.py` | 0 | Seven phases, twelve common gates, and twenty-three source references passed. |
| `python3 scripts/stage1_target.py check` | 0 | The ordered 1546-target L0/rework-required manifest passed. |
| `python3 scripts/stage1_target.py show THM-M-0121` | 0 | Rank 40, planned lifecycle, legacy artifacts unaccepted, theorem incomplete. |
| Declared candidate enumeration and base/HEAD Git-blob comparison | 0 | Exactly one declared candidate exists and its blob is unchanged. |
| `/usr/bin/python3 -I -B Stage1_Instances/THM-M-0121/check_statement.py` | 1 | Exactly one typed JSON object reported `repair_required` and `phase_accepted=false` because the embedded base is stale. |
| From `Formalizations/Lean`: `env LEAN_NUM_THREADS=1 LC_ALL=C TZ=UTC lake env lean --trust=0 ../../Stage1_Instances/THM-M-0121/Statement.lean` | 0 | The three adjacent rational-map types printed; no canonical target or proof was declared. Nonfatal sandbox stream-fd diagnostics preceded Lean output. |
| `git diff --check -- Stage1_Instances/THM-M-0121 .stage1-worker-selftest.json` | 0 | No whitespace errors in the target-scoped handoff. |

The passing structural and Lean checks are bounded observations. They cannot replace the failed
scheduler-selected semantic replay or satisfy the exact-statement predicate.

## Retry condition and status boundary

The scheduler/master lane must commit a current-authority statement validator and issue a fresh
claim whose worker base contains that exact unchanged blob. A fresh worker must then refresh the
empty dependency ledger and emit exactly one contract-complete receipt. Positive statement closure
also requires master-accepted intake, an independently approved immutable source passage, the exact
mathematical proposition and boundary model, a kernel-elaborated Lean expression with minimal pinned
imports and fingerprints, checked alternate transports, and all four required mutation classes.

This blocker grants no state transition, phase acceptance, accepted receipt, provider acceptance,
exact-statement credit, proof credit, audit completion, theorem completion, or master acceptance.

## Persisted-goal continuation audit

The persisted goal was resumed against the same worker base and tree. Current authority still
records intake and statement as `[_]` with one attempt, the complete dependency and reuse context
remains empty, no primary-source selection or formal target has appeared, and the sole declared
validator remains the identical Git blob. Its exact authority-selected replay again exited `1`
with the same single typed `repair_required` result at the embedded-base assertion. Structural,
contract, theorem-DAG, Lean, and hygiene checks were replayed; none can override the semantic
failure. No scheduler-owned repair or source-authority change has appeared, so no lawful receipt
refresh or worker self-test handoff is possible in this continuation.

A third consecutive persisted-goal audit again observed the identical HEAD/tree, task cursor,
contract and theorem-DAG digests, empty dependency closure, null source/formal target, and validator
blob. The exact replay failed at the same embedded-base assertion with the same typed
`repair_required` semantics. This is now a repeated external-state impasse: only the scheduler can
publish an eligible current-base validator, and only source authority can select the exact theorem
passage without inventing mathematics.
