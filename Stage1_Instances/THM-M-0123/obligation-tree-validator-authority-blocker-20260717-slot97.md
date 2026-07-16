# THM-M-0123 obligation-tree validator-authority blocker

## Scope

This is the target-scoped fail-closed result for
`S56-M-0123-OBLIGATION_TREE` at worker base
`db2e21b8fec263c5b65014acb1ee2039566e35a3` (tree
`815414c57391f2c12871c05a6e3d2944b0f2fef2`). It changes no Lean source,
prior phase receipt, task-state authority, theorem-DAG projection, lifecycle,
debt vector, or acceptance state.

The authoritative claim tuple is
`(v2_execution_rank=276, phase_layer=3,
phase_item_id=S56-M-0123-OBLIGATION_TREE)`. The assigned theorem-DAG SHA-256 is
`91ea782c662e40b9608f8900ad586114c5ef8e8e5d2d2f13316185bd8f205067`,
and the dependency-context SHA-256 is
`0c0f6d1bed857aeaad7b4656db6ae6fe5c9c6bde39f7c9fb9ec2f8938eb4a484`.

## First Failed Gate

`T01-ARTIFACTS.scheduler_owned_obligation_tree_validator_missing_at_worker_base`
is the first mechanically unrepairable worker gate. The mandatory HEAD phase
contract declares exactly these scheduler-owned candidate paths:

- `Stage1_Instances/THM-M-0123/check_obligation_tree.py`
- `Stage1_Instances/THM-M-0123/validate_obligation_tree.py`

Neither path exists in the immutable worker base or current worktree. The
contract requires exactly one candidate already present at the worker base and
requires its base and HEAD Git blobs to agree. The worker is expressly
forbidden to create, copy, refresh, rename, replace, or delete either path.
Consequently there is no lawful validator argv and no possible semantic stdout
object with schema `stage1-validator-semantic-result/1.0`. JSON checks, Lean
elaboration, or a worker-written adapter cannot replace the missing
authority replay or justify a `[_]` proposal.

The authority-owned role map
`.cron/stage1-v2-app-server/role-maps/S56-M-0123-OBLIGATION_TREE.json` is also
absent. No `.stage1-worker-selftest.json` is emitted, and no phase receipt is
created. The phase remains `[ ]`; this blocker records
`accepted=false`, `phase_predicate_proven=false`, and
`phase_accepted=false`.

## Dependency And Reuse Audit

The complete `parent_inspection_order`, direct-hard-parent list,
transitive-hard-ancestor list, hard-edge list, and reuse-hint list are empty.
The empty sequence was traversed exactly once before architecture analysis.
No provider phase state, receipt, declaration, reusable artifact, terminal
body, checkbox, proof credit, or acceptance was consumed or inherited.

The assigned weak group `SHARED-MODULE-dff4d00d3b45e946` was inspected through
its authoritative DAG entry and both member anchor inventories. It is a
nonblocking shared-module co-mention of
`Atlas.ArithmeticGeometry.code.FaltingsTheorem`, not a shared lemma or terminal
body. Both `THM-M-0122` and `THM-M-0123` classify the Atlas
`faltings_theorem` body as directly `by sorry` and materially mismatched. The
decision is `not_applicable`; no exact import, checked transport, proof credit,
receipt identity, checkbox state, or acceptance transfers.

The tracked `dependency-reuse-ledger.json` uses the required schema but is
historical: it binds graph `8be71ef1...`, context `068170c7...`, base
`307c34d3...`, the layer-2 anchor claim, and no shared group. It therefore
cannot satisfy this assigned layer-3 claim. This blocked snapshot records the
exact required refresh rather than falsely presenting that canonical ledger as
current. A fresh scheduler-provisioned retry must refresh the canonical path
before architecture acceptance or any proof work.

## Target Boundary

The exact selected declaration remains
`Stage1Instances.THM_M_0123.MordellTarget`, with expression fingerprint
`9fa3c7a0bff55098e7cc234793cb06ec1628e84e003ddb273a6dc47094f58dbd`.
The bounded anchor inventory found no valid exact terminal candidate. The root
remains `H4/M3/R3`, and the placeholder-bearing Atlas declaration receives no
credit.

A genuine obligation-tree phase must freeze the status-independent canonical
denominator, all ROOT/S/N/B/C/L/X/T applicability decisions, seven distinct
typed graph families, substantive leaf ledgers of at most 100 steps, readable
open-boundary sentences, and exact child-to-parent composition certificates
where machine-eligible. None of those required roles is manufactured here:
without the scheduler-owned validator and role map, the worker cannot produce
the mandatory semantic replay or a truthful self-tested receipt. This blocker
is not a substitute architecture.

## Checks Run

All commands ran inside this worker clone on 2026-07-17 (Asia/Shanghai). The
pre-existing automation-provided untracked `.lake` symlink was not mutated. No
`lake update`, `lake build`, dependency clone/fetch, network operation, nested
agent, commit, push, or scheduler-owned file edit ran.

| Command | Exit | Result |
| --- | ---: | --- |
| `python3 Docs/tools/check_stage1_standard.py` | 0 before owned edits | rev-5.6 structure, target set, v2 DAG, phase contract, and execution skill passed |
| `python3 Docs/tools/check_stage1_theorem_dag_v2.py` | 0 before owned edits | 1546 theorem nodes, 10822 phase states, typed edges, claim ordering, and acyclicity passed |
| `python3 Docs/tools/check_stage1_phase_acceptance_contracts.py` | 0 | seven phases, twelve common gates, and scheduler-owned validator rules passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ordered ranks, and the uniform L0/rework-required baseline passed |
| `python3 scripts/stage1_target.py show THM-M-0123` | 0 | rank 42, planned lifecycle, legacy evidence unaccepted, theorem incomplete |
| `git cat-file -e HEAD:Stage1_Instances/THM-M-0123/check_obligation_tree.py` | 128 expected | first declared validator is absent from the immutable worker base |
| `git cat-file -e HEAD:Stage1_Instances/THM-M-0123/validate_obligation_tree.py` | 128 expected | second declared validator is absent from the immutable worker base |

Adding target-owned blocker evidence changes the generated theorem-DAG evidence
inventory. Post-edit aggregate DAG freshness checks may therefore report the
expected projection drift until the master integration lane copies this
evidence and regenerates the read-only projection. Such drift is not phase
evidence and cannot replace the missing semantic validator replay.

## Retry Condition

The scheduler/master lane must commit exactly one declared obligation-tree
validator and publish the authority-owned per-item role map, then issue a fresh
claim whose worker base already contains that identical validator blob. A
fresh worker must refresh `dependency-reuse-ledger.json` to the assigned graph,
context, base, layer-3 claim tuple, empty hard closure, and weak shared-group
non-reuse decision before freezing the obligation denominator and executing the
exact contract argv read-only.

Master topology separately requires the anchor-audit predecessor to become
`[x]`; its current `[_]` state and receipt are observation only. This blocker
grants no state transition, obligation-tree acceptance, proof credit, provider
acceptance transfer, audit completion, theorem completion, or master
acceptance.
