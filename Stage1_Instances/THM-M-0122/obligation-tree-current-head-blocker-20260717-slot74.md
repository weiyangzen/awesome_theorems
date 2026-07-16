# THM-M-0122 obligation-tree current-HEAD blocker

## Scope

This is the target-scoped fail-closed result for
`S56-M-0122-OBLIGATION_TREE` at worker base
`6cff7bae0e4547cf9ad8b7abaae20d1abb9fe049` (tree
`28c148dbd84fbd549c749f060c92c9a3f00b16d0`). It changes no Lean source,
canonical obligation registry, typed graph, validation specification, receipt,
validator candidate, task-state authority, theorem-DAG projection, or item
state.

The exact claim tuple is
`(v2_execution_rank=275, phase_layer=3,
phase_item_id=S56-M-0122-OBLIGATION_TREE)`. The sole task-state authority
records this item as `[_]` with `attempts=1`; the statement and anchor-audit
predecessors are also `[_]`. The current theorem-DAG SHA-256 is
`80cf05109d5b3776b7defe95fdb591b216894a57ecbb7180a59f315a67d487d5`,
and the target dependency-context SHA-256 is
`0c0f6d1bed857aeaad7b4656db6ae6fe5c9c6bde39f7c9fb9ec2f8938eb4a484`.

## Parent, ancestor, and reuse audit

The required `parent_inspection_order` is exactly `[]`. The empty sequence was
traversed exactly once as the complete direct/transitive hard-parent closure in
ascending v2 rank. The current direct-parent, transitive-ancestor, hard-edge,
and reuse-hint lists are also empty, so no parent phase state, receipt,
declaration body, reusable artifact, terminal proof body, checkbox state, or
acceptance was inspected as provider material, copied, consumed, or inherited.

The current graph does contain the nonblocking weak shared-module group
`SHARED-MODULE-dff4d00d3b45e946`. Its canonical identity is
`Atlas.ArithmeticGeometry.code.FaltingsTheorem`, and its members are this
target and `THM-M-0123`. The group's exact graph boundary says that it is a
co-mention only, not a common lemma or proof body. Current member inspection
confirmed that boundary:

- `THM-M-0123` has intake, statement, and anchor audit `[_]`; obligation tree,
  proof, validation, and release are `[ ]`.
- `Stage1_Instances/THM-M-0123/anchor-audit.json` has SHA-256
  `75c729e9697c84b66a2f0c2c11d5c86000417c995f9bdce62fbb5faeef354938`.
- Its anchor receipt has SHA-256
  `245e9e5fe4a7958c22d793676650a272bfeed41b6216d462b8ddf4ece48678dc`,
  is `accepted=false`, and transfers no acceptance.
- Both member audits bind the same Atlas file bytes
  (`b5aca9ae03c178c908fdf0e28d4dd8672643b16390b25e9b9771882726ed8f01`)
  and classify its `faltings_theorem` declaration as a direct `by sorry`
  placeholder with a material statement mismatch. It is not reusable proof
  material.

The truthful current decision for the group is therefore `not_applicable`:
no import, copy, wrapper, or checked transport is used, no compatibility work
remains for this rejected weak hint, and no provider proof or evidence credit
is transferred. The integrated `dependency-reuse-ledger.json` is historical:
it binds graph digest
`8be71ef1e4fa1c3de5aa420550ff915dbe0b9f165ac0d98518adf2d1fe25fd47`,
old context digest
`068170c76abd4579d643ede04d731b974412185bd285e7b40255ec4044adec5c`,
base `307c34d30fc3763c82a944a142ae922b48ff18aa`, and an empty shared-group
list. A positive current receipt would require a refreshed schema-1.1 ledger
containing the decision above. It is deliberately not substituted into the
already integrated proof-phase evidence while the mandatory scheduler-owned
validator cannot validate current inputs.

## First failed gate

`G05-AUTHORITY-REPLAY / validator_base_and_context_binding_stale` is the first
worker-unrepairable gate. The HEAD obligation-tree contract (SHA-256
`1e7adf0f4fae0541b3595d4b0bfbb53f7eb17e28a4a889fec14f6df969e0cec4`)
declares two scheduler-owned candidate paths. Exactly one exists:

```text
Stage1_Instances/THM-M-0122/check_obligation_tree.py
```

Its SHA-256 is
`7ad5b4a29d947ed40f6d740a8aefb9fef3347ea24d4a3dac448af55b62e90f4c`,
and its Git blob is `0e4dce455d894d03c300c65a11b531b3b652c8c5`.
`validate_obligation_tree.py` is absent, so candidate selection is unique.
The existing candidate is unchanged from HEAD, but it hard-binds obsolete
claim inputs: base `2dc5a410b68eff806858fd6ed0cb33d57f6209f7`, tree
`841bdd6114e7436cff4a3a1ff248fc1e884a9ddc`, graph digest
`3d32f808e2914b338c459d52651b69731f0979a90a720f98bc0f31a577e2bafa`,
old context digest
`068170c76abd4579d643ede04d731b974412185bd285e7b40255ec4044adec5c`,
an `[ ]`/attempt-zero phase, and an empty shared-group list. All of those
material claim inputs disagree with the current assignment.

The exact contract-selected argv was run from the repository root without
shell interpolation:

```text
/usr/bin/python3 -I -B Stage1_Instances/THM-M-0122/check_obligation_tree.py
```

It exited `1`, wrote empty stderr, and emitted exactly one JSON object with
schema `stage1-validator-semantic-result/1.0`:

```json
{"audit_complete":false,"blocked":false,"first_failed_gate":"OBLIGATION-TREE-SEMANTIC-CHECK","item_id":"S56-M-0122-OBLIGATION_TREE","message":"repository base revision drift","open_obligations":23,"phase":"obligation_tree","phase_accepted":false,"phase_predicate_proven":false,"schema_version":"stage1-validator-semantic-result/1.0","stale_inputs":[],"status":"failed","theorem_complete":false,"theorem_id":"THM-M-0122","verdict":"repair_required"}
```

Exit zero is not inferred, and this typed negative result cannot support
current phase acceptance. The worker is expressly forbidden to refresh,
replace, rename, or delete any validator candidate. Consequently this run
produces no new or refreshed `stage1-node-receipt/1.0` and no
`.stage1-worker-selftest.json`. The integrated obligation-tree receipt remains
historical evidence for the earlier base and context; it is not presented as
a current successful replay.

## Preserved architecture evidence

The integrated target artifacts still provide a substantial architecture
candidate: registry v1 freezes 23 canonical obligations under denominator
`fa58b3f6f5f390a8fd776a0d789158582ec5ded0f22616a94460d6eb0306a508`,
and seven typed graph families contain 56 edges. `ObligationTree.lean` has
SHA-256
`c081ee9e08e5bf5aeb3060605ebc9c7f7926d08d04632380e105e8ff1c783c69`.
Those artifacts model open proof debt and conditional composition without
assigning accepted obligation closure. This report leaves their bytes intact.

The mandatory validator failure means the current phase predicate is not
self-tested, not that the mathematical architecture has been silently
discarded. In particular, this report does not infer proof closure from the
later provisional proof receipt or from the current `[_]` workflow state. The
actual root still lacks finite-extension normalization,
Jacobian/Abel-Jacobi, Mordell-Weil, Mordell-Lang, no-positive-coset, and
finite-intersection proof bodies.

## Bounded checks

All checks ran in this worker clone on 2026-07-17. No `lake update`, `lake
build`, dependency clone/fetch, or `.lake` mutation ran. The pre-existing
automation-provided `Formalizations/Lean/.lake` symlink was reused read-only
only through the scheduler-owned validator before its early base check.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 1546 targets, the v2 graph, phase contract, and execution skill passed. |
| `python3 Docs/tools/check_stage1_theorem_dag_v2.py` | 0 | 1546 nodes, 10822 phase states, typed relationships, and acyclicity passed. |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique ordered L0/rework-required targets passed. |
| `python3 scripts/stage1_target.py show THM-M-0122` | 0 | Rank 41, planned lifecycle, legacy evidence unaccepted, theorem incomplete. |
| HEAD contract candidate enumeration | 0 | Exactly `check_obligation_tree.py` exists and is HEAD-unchanged. |
| `/usr/bin/python3 -I -B Stage1_Instances/THM-M-0122/check_obligation_tree.py` | 1 | Exact typed `repair_required` result above; no phase acceptance inferred. |
| direct/transitive closure reproduction | 0 | Exact ordered parent closure is empty and was traversed once. |
| weak shared-group member/bytes audit | 0 | The Atlas co-mention was rejected as placeholder-bearing, mismatched, and non-reusable. |

`audit_complete=false` and `theorem_complete=false`.

## Retry condition

The scheduler/master lane must publish a refreshed, HEAD-tracked
`check_obligation_tree.py` whose immutable bindings match a fresh worker base,
the current graph/context, the current `[_]` attempt, and the weak shared-group
decision, then issue a new claim containing that unchanged validator blob. A
fresh worker can refresh the dependency ledger and the single phase receipt,
replay the exact validator successfully, and emit the required self-test
handoff. Dependency-ordered master acceptance remains separate and cannot be
inherited from any receipt or later provisional phase.

This blocker grants no state transition, proof or provider credit, receipt
acceptance, `AUDIT-Z`, `THEOREM-Z`, theorem completion, release, or master
acceptance.

## Continuation audit

The persisted goal was resumed against the same worker base and tree. The
sole task-state authority still records obligation tree `[_]` with one
attempt; the theorem node still has the same empty ordered hard-parent closure,
the same weak shared-module group, graph digest, and dependency-context digest.
The contract still selects exactly the unchanged `check_obligation_tree.py`
blob recorded above, and the alternate candidate remains absent.

The exact authority-selected argv was replayed again. It again exited `1`,
with empty stderr and exactly one `stage1-validator-semantic-result/1.0`
object whose message is `repository base revision drift`, verdict is
`repair_required`, and `phase_accepted=false`. No scheduler-owned input has
changed, so the same validator-base/context blocker repeats. No receipt or
self-test handoff was manufactured.

A third consecutive persisted-goal audit again observed the identical base,
tree, task cursor, graph/context digests, unique validator blob, absent
alternate candidate, and exact typed failure. The blocker therefore cannot be
repaired from the worker-owned target surface: progress requires the scheduler
to publish a current-bound immutable validator and issue a fresh claim. The
target-scoped evidence remains this report, and `.stage1-worker-selftest.json`
remains absent.
