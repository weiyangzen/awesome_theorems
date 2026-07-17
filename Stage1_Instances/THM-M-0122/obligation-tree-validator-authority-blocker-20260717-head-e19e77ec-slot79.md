# THM-M-0122 obligation-tree current-claim blocker

## Scope

This is the target-scoped result for `S56-M-0122-OBLIGATION_TREE` at worker
base `e19e77ec08fca6a8a9c45a003c9904020dae8382` (tree
`53ff0ebe013670fc0332bf326fd860b29857ddab`). The sole task-state authority
records the item as `[_]` with one attempt. Its exact claim tuple is
`(275, 3, S56-M-0122-OBLIGATION_TREE)`. This worker does not edit that state or
any authority-owned projection.

The current theorem-DAG SHA-256 is
`53622c848d6a0d8327bba8cd22bf45463f0dd8acb7ea0af2884713983e76c91f`,
and the target dependency-context SHA-256 is
`0c0f6d1bed857aeaad7b4656db6ae6fe5c9c6bde39f7c9fb9ec2f8938eb4a484`.

## Parent and reuse audit

The supplied `parent_inspection_order` is exactly `[]`. It was traversed
exactly once before proof work as the complete direct/transitive hard-parent
closure in ascending v2 rank. Direct hard parents, transitive hard ancestors,
hard edges, and reuse hints are all empty. No parent phase state, receipt,
declaration body, reusable artifact, proof body, checkbox, or acceptance was
consumed or inherited.

The sole nonblocking weak group is
`SHARED-MODULE-dff4d00d3b45e946`, a co-mention of
`Atlas.ArithmeticGeometry.code.FaltingsTheorem` by `THM-M-0122` and
`THM-M-0123`. Current inspection found the peer phase vector
`[_], [_], [_], [ ], [ ], [ ], [ ]`, no peer obligation registry, no peer
typed graph, and no peer proof body. The peer anchor receipt has SHA-256
`245e9e5fe4a7958c22d793676650a272bfeed41b6216d462b8ddf4ece48678dc`
and `accepted=false`. Both anchor inventories bind the Atlas source whose
`faltings_theorem` is directly `by sorry` and materially mismatches the exact
consumer target. The group decision remains `not_applicable`: no exact reuse,
checked transport, import, wrapper, copy, provider acceptance, or proof credit
is used.

The current schema-1.1 audit is already preserved in
`dependency-reuse-ledger-obligation-tree-head-d25efdf-slot87.json`. Its graph
and repository revision predate this claim, while its dependency context,
empty ordered hard closure, peer HEAD byte hashes, and weak-group non-reuse
decision still match the current assignment. It is blocker history rather
than a current successful canonical ledger. The canonical
`dependency-reuse-ledger.json` is also stale for the current graph/context.
Neither is rewritten because the mandatory immutable validator cannot validate
a current handoff.

## First failed gate

The HEAD obligation-tree contract declares two scheduler-owned candidates.
Exactly one exists and is unchanged from HEAD:

```text
/usr/bin/python3 -I -B Stage1_Instances/THM-M-0122/check_obligation_tree.py
```

`check_obligation_tree.py` has SHA-256
`7ad5b4a29d947ed40f6d740a8aefb9fef3347ea24d4a3dac448af55b62e90f4c`
and Git blob `0e4dce455d894d03c300c65a11b531b3b652c8c5`.
`validate_obligation_tree.py` is absent. The existing candidate hard-binds base
`2dc5a410b68eff806858fd6ed0cb33d57f6209f7`, tree
`841bdd6114e7436cff4a3a1ff248fc1e884a9ddc`, graph
`3d32f808e2914b338c459d52651b69731f0979a90a720f98bc0f31a577e2bafa`,
context
`068170c76abd4579d643ede04d731b974412185bd285e7b40255ec4044adec5c`,
and the former `[ ]`/attempt-zero claim with no shared group. These bindings do
not match the current assigned claim.

The exact contract-selected argv exited `1`, wrote zero stderr bytes, and
emitted exactly one `stage1-validator-semantic-result/1.0` object:

```json
{"audit_complete":false,"blocked":false,"first_failed_gate":"OBLIGATION-TREE-SEMANTIC-CHECK","item_id":"S56-M-0122-OBLIGATION_TREE","message":"repository base revision drift","open_obligations":23,"phase":"obligation_tree","phase_accepted":false,"phase_predicate_proven":false,"schema_version":"stage1-validator-semantic-result/1.0","stale_inputs":[],"status":"failed","theorem_complete":false,"theorem_id":"THM-M-0122","verdict":"repair_required"}
```

Exit zero is not inferred. The typed negative result cannot support a fresh
phase receipt or self-test handoff. Worker policy forbids refreshing,
replacing, renaming, or deleting the candidate. Therefore this run creates no
`stage1-node-receipt/1.0`, leaves the historical receipt unchanged, and leaves
`.stage1-worker-selftest.json` absent.

## Preserved architecture and boundary

The existing owned artifacts still freeze 23 canonical obligations at
denominator
`fa58b3f6f5f390a8fd776a0d789158582ec5ded0f22616a94460d6eb0306a508`.
The typed bundle contains all seven required graph families and 56 edges.
`ObligationTree.lean` has SHA-256
`c081ee9e08e5bf5aeb3060605ebc9c7f7926d08d04632380e105e8ff1c783c69`
and contains conditional, not premise-producing, composition declarations.
Those bytes remain unchanged.

No obligation is accepted closed. Finite-extension normalization,
Jacobian/Abel-Jacobi construction, Mordell-Weil, Mordell-Lang,
no-positive-coset, finite-intersection, source, provenance, trust, readable,
validation, and release work remain open. `audit_complete=false` and
`theorem_complete=false`.

## Bounded checks

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_phase_acceptance_contracts.py` | 0 | Seven phases, twelve common gates, and twenty-three source references passed. |
| `python3 Docs/tools/check_stage1_theorem_dag_v2.py` | 0 | 1546 nodes, 10822 phase states, typed context, and acyclicity passed. |
| `python3 Docs/tools/check_stage1_standard.py` | 0 | All fifteen assurance groups and current projections passed. |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique ordered L0/rework-required targets passed. |
| `python3 scripts/stage1_target.py show THM-M-0122` | 0 | Rank 41, planned lifecycle, legacy evidence unaccepted, theorem incomplete. |
| exact contract-selected validator argv | 1 | One typed `repair_required` result; `phase_accepted=false`; repository base revision drift. |
| direct/transitive closure and weak-group audit | 0 | Empty ordered hard closure traversed once; sole weak co-mention rejected without reuse. |
| `git diff --check -- Stage1_Instances/THM-M-0122` | 0 | No owned-path whitespace errors. |

No network, `lake update`, `lake build`, dependency clone/fetch, or `.lake`
mutation was used.

## Retry

The scheduler/master lane must publish a current-bound, HEAD-tracked
`check_obligation_tree.py` and issue a fresh claim containing that unchanged
blob. It must bind the fresh base, graph/context, current `[_]` attempt-one
state, and weak-group non-reuse decision. A fresh worker can then refresh the
canonical ledger and exactly one receipt, replay the immutable validator, and
write the required self-test handoff if the typed result passes.

This blocker grants no phase transition, proof or provider acceptance,
`AUDIT-Z`, `THEOREM-Z`, theorem completion, release, or master acceptance.

## Continuation audit 1

The persisted goal was resumed against the same HEAD and tree. The blueprint
still records obligation tree `[_]` with one attempt; the theorem-DAG digest,
dependency-context digest, empty ordered hard-parent closure, weak group, peer
artifact bytes, and `accepted=false` peer receipt are unchanged. Candidate
enumeration again found exactly the same HEAD-owned validator blob and no
alternate candidate.

The exact selected argv was replayed again. It again exited `1`, wrote zero
stderr bytes, and emitted exactly the same single typed `repair_required`
result with `message="repository base revision drift"` and
`phase_accepted=false`. The phase-contract, theorem-DAG, standard, target-set,
peer-byte, and whitespace checks all passed. No scheduler-owned input changed,
so the worker still cannot lawfully refresh the validator, create a current
receipt, or emit `.stage1-worker-selftest.json`. This is the second consecutive
active-goal observation of the same blocker.

## Continuation audit 2

A third consecutive active-goal audit again observed HEAD
`e19e77ec08fca6a8a9c45a003c9904020dae8382`, tree
`53ff0ebe013670fc0332bf326fd860b29857ddab`, the `[_]`/attempt-one item,
graph
`53622c848d6a0d8327bba8cd22bf45463f0dd8acb7ea0af2884713983e76c91f`,
context
`0c0f6d1bed857aeaad7b4656db6ae6fe5c9c6bde39f7c9fb9ec2f8938eb4a484`,
the empty ordered hard-parent closure, the same weak group and peer bytes, the
same unique validator blob, and the absent alternate candidate.

The exact authority-selected argv was replayed a third time. It again exited
`1`, wrote zero stderr bytes, and returned exactly one typed result with
`verdict="repair_required"`, `phase_accepted=false`, and
`message="repository base revision drift"`. The phase-contract, theorem-DAG,
standard, target-manifest, peer-byte, and owned-path whitespace checks again
passed. `.stage1-worker-selftest.json` remains absent, and no current receipt
or canonical-ledger success claim was manufactured.

The identical scheduler-ownership blocker has therefore repeated for three
consecutive active-goal turns. It cannot be repaired within the assigned owned
path because the worker is forbidden to modify the only validator candidate.
Progress requires the external scheduler/master state change described in
Retry. This file is the final truthful target-scoped handoff for the blocked
goal; it transfers no acceptance and changes no authoritative item state.
