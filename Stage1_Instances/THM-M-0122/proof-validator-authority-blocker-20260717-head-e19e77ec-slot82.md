# THM-M-0122 proof validator-authority blocker at HEAD e19e77ec

## Assigned boundary

This is target-owned negative evidence for `S56-M-0122-PROOF` at worker base
`e19e77ec08fca6a8a9c45a003c9904020dae8382` (tree
`53ff0ebe013670fc0332bf326fd860b29857ddab`). The exact scheduler claim tuple
is `(v2_execution_rank=275, phase_layer=4,
phase_item_id=S56-M-0122-PROOF)`. The sole task-state authority records the
item as `[_]` with `attempts=1`; this worker does not edit that state or infer
master acceptance from it.

The observed theorem-DAG SHA-256 is
`53622c848d6a0d8327bba8cd22bf45463f0dd8acb7ea0af2884713983e76c91f`,
and the target dependency-context SHA-256 is
`0c0f6d1bed857aeaad7b4656db6ae6fe5c9c6bde39f7c9fb9ec2f8938eb4a484`.

## Dependency and reuse audit

The authoritative `parent_inspection_order` is exactly `[]`. The empty
sequence was traversed exactly once before proof inspection. It is the complete
direct/transitive hard-parent closure in ascending v2 rank: direct hard
parents, transitive hard ancestors, hard edges, and reuse hints are all empty.
No provider declaration, receipt, checkbox state, proof credit, or acceptance
is consumed or inherited.

The one nonblocking weak group,
`SHARED-MODULE-dff4d00d3b45e946`, co-mentions
`Atlas.ArithmeticGeometry.code.FaltingsTheorem` for `THM-M-0122` and
`THM-M-0123`. The other member was inspected read-only at current HEAD:

| Artifact | SHA-256 |
|---|---|
| `Stage1_Instances/THM-M-0123/Statement.lean` | `62c3d5936d64ed2225d239246ac8139663bc4f722f896625b94bb9a11e59ca8f` |
| `Stage1_Instances/THM-M-0123/AnchorAudit.lean` | `f86d7581c09d1b4ab226287514146783612cb7b2fe4fdb1d3103650f96da2ea0` |
| `Stage1_Instances/THM-M-0123/anchor-audit.json` | `75c729e9697c84b66a2f0c2c11d5c86000417c995f9bdce62fbb5faeef354938` |
| `Stage1_Instances/THM-M-0123/anchor-audit-receipt.json` | `245e9e5fe4a7958c22d793676650a272bfeed41b6216d462b8ddf4ece48678dc` |

Its phase states are `[_], [_], [_], [ ], [ ], [ ], [ ]`. Its anchor-audit
receipt has `accepted=false`; no evidence credit transfers. Both member audits
reject the Atlas body because it is directly `by sorry`, materially mismatches
the all-number-field scheme/cohomological target, and is outside the pinned
dependency closure. The group decision is therefore `not_applicable`, not
`reused_exact` or `reused_with_transport`.

The integrated `dependency-reuse-ledger.json` is historical and cannot support
this claim: it binds base `307c34d30fc3763c82a944a142ae922b48ff18aa`, graph
digest `8be71ef1e4fa1c3de5aa420550ff915dbe0b9f165ac0d98518adf2d1fe25fd47`,
old context digest
`068170c76abd4579d643ede04d731b974412185bd285e7b40255ec4044adec5c`,
and an empty shared-group list. Refreshing it would create new evidence that
the immutable HEAD validator cannot replay, so this blocked run leaves the
historical ledger and receipt untouched.

## Mandatory validator result

The proof contract declares two candidate patterns. Exactly one HEAD-owned
candidate exists: `Stage1_Instances/THM-M-0122/check_proof.py`.
`check_proof.sh` is absent. The selected candidate is unchanged from HEAD and
has SHA-256
`26ffc3bbac2c1dc29eec11348f1641281c2557c2224fd3831d928cdea6eba18b`
and Git blob `41facc70f16dbb572307b23dd5a347157f8dd35c`.

The validator hard-binds obsolete base
`307c34d30fc3763c82a944a142ae922b48ff18aa`, tree
`ef45ba442c71959db78ad146a023bcf32946a53f`, graph digest
`8be71ef1e4fa1c3de5aa420550ff915dbe0b9f165ac0d98518adf2d1fe25fd47`,
context digest
`068170c76abd4579d643ede04d731b974412185bd285e7b40255ec4044adec5c`,
an unstarted proof cursor, and no weak-group decision. The contract-selected
argv was run exactly from the repository root:

```text
/usr/bin/python3 -I -B Stage1_Instances/THM-M-0122/check_proof.py
```

It exited `1`, wrote no stderr, and emitted exactly one semantic-result object:

```json
{"audit_complete":false,"blocked":false,"first_failed_gate":"P01-ARTIFACTS","item_id":"S56-M-0122-PROOF","message":"proof evidence replay failed: repository HEAD differs from the claimed worker base","open_obligations":6,"phase":"proof","phase_accepted":false,"phase_predicate_proven":false,"schema_version":"stage1-validator-semantic-result/1.0","stale_inputs":[],"status":"failed","theorem_complete":false,"theorem_id":"THM-M-0122","verdict":"repair_required"}
```

The first worker-unrepairable gate is
`G05-AUTHORITY-REPLAY / validator_base_and_context_binding_stale`. The worker
is forbidden to create or refresh a validator candidate. Therefore this run
cannot truthfully refresh the ledger, publish a current
`stage1-node-receipt/1.0`, or write `.stage1-worker-selftest.json`.

## Mathematical boundary

The current target-owned `Proof.lean` has SHA-256
`07c9c730d01964dc4aeea81b2af34a8fc59a105301751e78ea0eccfa1a521e1a`.
Its three placeholder-free declarations re-elaborate under the pinned
trust-zero toolchain, but the root composer is conditional on
`FiniteExtensionNormalization`, `AbelJacobiPackage`, and
`MordellLangFinitenessPackage`. It is not a premise-free proof of the canonical
`FaltingsTarget`.

The remaining machine root cut is:

1. `M0122-N-FINITE-EXTENSION`
2. `M0122-C-ABEL-JACOBI`
3. `M0122-L-MORDELL-WEIL`
4. `M0122-L-MORDELL-LANG`
5. `M0122-L-NO-POSITIVE-COSET`
6. `M0122-L-FINITE-INTERSECTION`

No compatible placeholder-free terminal body is present in the audited pinned
or immutable inventory. `P04-KERNEL.M0122-N-FINITE-EXTENSION` remains the
first mathematical proof gate.

## Checks

All checks ran in this worker clone on 2026-07-17. The automation-provided
`.lake` link was reused read-only; no update, build, clone, fetch, checkout, or
network operation ran.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | Rev-5.6 standard, v2 projection, and phase contract passed. |
| `python3 Docs/tools/check_stage1_theorem_dag_v2.py` | 0 | 1546 nodes, 10822 phase states, typed contexts, and acyclicity passed. |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique ordered targets passed. |
| `python3 scripts/stage1_target.py show THM-M-0122` | 0 | Rank 41, planned lifecycle, theorem incomplete. |
| isolated `lake env lean --trust=0 -t0` replay of `Statement.lean`, `ObligationTree.lean`, and `Proof.lean` | 0 | Current declarations elaborated against the pinned closure without changing `.lake`. |
| HEAD validator candidate enumeration and byte check | 0 | Exactly the unchanged `check_proof.py` candidate exists. |
| `/usr/bin/python3 -I -B Stage1_Instances/THM-M-0122/check_proof.py` | 1 | Exact single `repair_required` result above; `phase_accepted=false`. |
| `git diff --check -- Stage1_Instances/THM-M-0122 .stage1-worker-selftest.json` | 0 | No whitespace errors before this artifact was added. |

`audit_complete=false` and `theorem_complete=false`.

## Retry condition

The scheduler/master lane must publish a refreshed, HEAD-tracked proof
validator whose immutable bindings match a fresh claim base, current `[_]`
cursor and attempt, graph/context digests, and weak-group decision. A fresh
worker can then refresh the schema-1.1 ledger, produce exactly one current
phase receipt, and emit a self-test handoff only if the selected validator's
typed result permits it. Completing the proof predicate additionally requires
placeholder-free bodies for the six root-cut obligations or an exact compatible
pinned terminal body with consumer-owned checked transport.

This artifact grants no state transition, proof credit, receipt acceptance,
validation, release, `AUDIT-Z`, `THEOREM-Z`, theorem completion, or master
acceptance.
