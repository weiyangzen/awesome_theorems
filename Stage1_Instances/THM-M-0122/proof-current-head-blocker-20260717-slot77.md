# THM-M-0122 proof current-HEAD blocker

## Scope and claim order

This is the target-scoped fail-closed result for `S56-M-0122-PROOF` at
worker base `c6ccce54afcb261a3b4c236a3eb538a1e4b829a8` (tree
`13ac09d107589b9b20956e6d2e4c0696058a0b41`). The exact claim tuple is
`(v2_execution_rank=275, phase_layer=4,
phase_item_id=S56-M-0122-PROOF)`. The sole task-state authority records the
assigned item as `[_]` with `attempts=1`; this worker does not edit that state.

The authoritative theorem-DAG SHA-256 is
`95128825a99c9863fc09b6edc8a4a99ab5fae8e0927e40af88635f8945d2aa3e`,
and the target dependency-context SHA-256 is
`0c0f6d1bed857aeaad7b4656db6ae6fe5c9c6bde39f7c9fb9ec2f8938eb4a484`.

## Parent and reuse audit

The required `parent_inspection_order` is exactly `[]`. The empty sequence was
traversed exactly once as the complete direct/transitive hard-parent closure in
ascending v2 rank. Direct hard parents, transitive hard ancestors, hard edges,
and reuse hints are all empty, so no parent receipt, declaration body, reusable
artifact, checkbox state, or acceptance was consumed or inherited.

The current graph contains one nonblocking weak group,
`SHARED-MODULE-dff4d00d3b45e946`, whose canonical identity is
`Atlas.ArithmeticGeometry.code.FaltingsTheorem` and whose members are
`THM-M-0122` and `THM-M-0123`. It is expressly a shared-module co-mention, not
a common lemma or proof body. Inspection of the other member found:

- current phase states `[_], [_], [_], [ ], [ ], [ ], [ ]` in phase order;
- `Stage1_Instances/THM-M-0123/Statement.lean` SHA-256
  `62c3d5936d64ed2225d239246ac8139663bc4f722f896625b94bb9a11e59ca8f`;
- `Stage1_Instances/THM-M-0123/AnchorAudit.lean` SHA-256
  `f86d7581c09d1b4ab226287514146783612cb7b2fe4fdb1d3103650f96da2ea0`;
- `Stage1_Instances/THM-M-0123/anchor-audit.json` SHA-256
  `75c729e9697c84b66a2f0c2c11d5c86000417c995f9bdce62fbb5faeef354938`;
- `Stage1_Instances/THM-M-0123/anchor-audit-receipt.json` SHA-256
  `245e9e5fe4a7958c22d793676650a272bfeed41b6216d462b8ddf4ece48678dc`,
  with `accepted=false` and no transferable evidence credit.

Both member audits bind the same Atlas source bytes
`b5aca9ae03c178c908fdf0e28d4dd8672643b16390b25e9b9771882726ed8f01`
and reject its `faltings_theorem`: its body is directly `by sorry`, its custom
Q-only statement materially mismatches the frozen all-number-field scheme and
cohomological target, and it is not integrated into the pinned dependency
closure. The truthful group decision is therefore `not_applicable`. No exact
reuse, checked transport, copy, import, wrapper, proof credit, or acceptance is
claimed.

The integrated `dependency-reuse-ledger.json` is historical and stale for this
assignment: it binds graph digest
`8be71ef1e4fa1c3de5aa420550ff915dbe0b9f165ac0d98518adf2d1fe25fd47`,
context digest
`068170c76abd4579d643ede04d731b974412185bd285e7b40255ec4044adec5c`,
base `307c34d30fc3763c82a944a142ae922b48ff18aa`, and an empty shared-group
list. A current positive handoff would require refreshing it with the decision
above. This run deliberately does not refresh it because the immutable
scheduler-owned validator cannot validate any current evidence change.

## First failed gate

`G05-AUTHORITY-REPLAY / validator_base_and_context_binding_stale` is the first
worker-unrepairable gate. The HEAD proof contract has two candidate patterns,
and exactly one HEAD-owned candidate exists:

```text
Stage1_Instances/THM-M-0122/check_proof.py
```

Its SHA-256 is
`26ffc3bbac2c1dc29eec11348f1641281c2557c2224fd3831d928cdea6eba18b`,
and its Git blob is `41facc70f16dbb572307b23dd5a347157f8dd35c`.
`check_proof.sh` is absent, so selection is unique. The worker has not created,
modified, renamed, replaced, or deleted either candidate.

The existing validator hard-binds obsolete claim inputs: base
`307c34d30fc3763c82a944a142ae922b48ff18aa`, tree
`ef45ba442c71959db78ad146a023bcf32946a53f`, graph digest
`8be71ef1e4fa1c3de5aa420550ff915dbe0b9f165ac0d98518adf2d1fe25fd47`,
old context digest
`068170c76abd4579d643ede04d731b974412185bd285e7b40255ec4044adec5c`,
an unstarted proof row, and an empty shared-group list. These disagree with the
current assignment. The exact contract-selected argv was run from the
repository root without shell interpolation:

```text
/usr/bin/python3 -I -B Stage1_Instances/THM-M-0122/check_proof.py
```

It exited `1`, wrote empty stderr, and emitted exactly one JSON object:

```json
{"audit_complete":false,"blocked":false,"first_failed_gate":"P01-ARTIFACTS","item_id":"S56-M-0122-PROOF","message":"proof evidence replay failed: repository HEAD differs from the claimed worker base","open_obligations":6,"phase":"proof","phase_accepted":false,"phase_predicate_proven":false,"schema_version":"stage1-validator-semantic-result/1.0","stale_inputs":[],"status":"failed","theorem_complete":false,"theorem_id":"THM-M-0122","verdict":"repair_required"}
```

Exit zero is not inferred. The typed `repair_required` result cannot support a
current receipt or worker self-test. The worker is forbidden to refresh the
validator, so this run produces no new `stage1-node-receipt/1.0` and leaves no
`.stage1-worker-selftest.json`. The old proof receipt remains historical
evidence only and is not represented as current replay evidence.

## Proof boundary

The current `Proof.lean` contains three target-owned, placeholder-free bodies:
two generic injection-finiteness transports and an exact-root composer that is
conditional on `FiniteExtensionNormalization`, `AbelJacobiPackage`, and
`MordellLangFinitenessPackage`. It does not construct those packages and does
not prove a premise-free inhabitant of the canonical `FaltingsTarget`.

The current machine root cut remains:

1. `M0122-N-FINITE-EXTENSION`
2. `M0122-C-ABEL-JACOBI`
3. `M0122-L-MORDELL-WEIL`
4. `M0122-L-MORDELL-LANG`
5. `M0122-L-NO-POSITIVE-COSET`
6. `M0122-L-FINITE-INTERSECTION`

No compatible placeholder-free terminal body exists in the recorded pinned
or immutable candidate inventory. This run therefore makes no claim that the
proof phase predicate, a root-critical obligation, or the theorem is closed.

## Checks

All checks ran in this worker clone on 2026-07-17. No `lake update`, `lake
build`, dependency clone/fetch, or `.lake` mutation ran. The existing
automation-provided `.lake` link was left untouched.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | Current rev-5.6 standard and projections passed. |
| `python3 Docs/tools/check_stage1_theorem_dag_v2.py` | 0 | 1546 theorem nodes, 10822 phase states, typed context, and acyclicity passed. |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique ordered L0/rework-required targets passed. |
| `python3 scripts/stage1_target.py show THM-M-0122` | 0 | Rank 41, planned lifecycle, legacy evidence unaccepted, theorem incomplete. |
| HEAD proof-validator enumeration | 0 | Exactly `check_proof.py` exists and is unchanged from HEAD. |
| `/usr/bin/python3 -I -B Stage1_Instances/THM-M-0122/check_proof.py` | 1 | Exact typed `repair_required` result above. |
| direct/transitive closure reproduction | 0 | Exact ordered parent closure is empty and was traversed once. |
| weak shared-group audit | 0 | The sole co-mention was inspected and rejected as mismatched and placeholder-bearing. |
| `git diff --check -- Stage1_Instances/THM-M-0122/proof-current-head-blocker-20260717-slot77.md` | 0 | Target-owned blocker formatting passed. |

`audit_complete=false` and `theorem_complete=false`.

## Retry condition

The scheduler/master lane must publish a refreshed, HEAD-tracked
`check_proof.py` whose immutable bindings match a fresh worker base, the
current proof item state/attempt, the graph/context digests, and the weak
shared-group decision, then issue a new claim containing that unchanged
validator blob. A fresh worker can then refresh the schema-1.1 dependency
ledger, produce exactly one current phase receipt, replay the selected
validator, and emit a self-test handoff if its typed semantic result permits
one. Mathematical proof completion additionally requires placeholder-free
implementations of the six root-cut obligations or an exact compatible pinned
terminal body and consumer-owned checked transport.

This blocker grants no phase transition, proof or provider acceptance, receipt
acceptance, validation, release, `AUDIT-Z`, `THEOREM-Z`, theorem completion, or
master acceptance.

## Continuation audit

The persisted proof goal was resumed without any authoritative-state change.
HEAD remains `c6ccce54afcb261a3b4c236a3eb538a1e4b829a8`; the proof row remains
`[_]` with one attempt; the graph and dependency-context digests remain the
values recorded above; the exact hard-parent inspection order remains empty;
and the weak shared-group member bytes and provisional receipt state remain
unchanged.

Candidate enumeration again found exactly the same HEAD-owned
`check_proof.py` blob and no `check_proof.sh`. The exact authority-selected
argv was replayed again. It again exited `1`, wrote zero stderr bytes, and
emitted exactly one semantic-result JSON object with
`message="proof evidence replay failed: repository HEAD differs from the
claimed worker base"`, `verdict="repair_required"`, and
`phase_accepted=false`. The standard, theorem-DAG, and target-set structural
checks still pass, so the repeated failure is specifically the immutable
validator's obsolete base/context binding rather than a newly discovered
structural inconsistency.

No scheduler-owned input changed and the worker still may not refresh that
validator. Consequently no current receipt, ledger rewrite, or self-test
handoff can truthfully pass the mandatory authority replay. This is the second
consecutive persisted-goal observation of the same blocker; the target-owned
blocker remains the only new evidence, and `.stage1-worker-selftest.json`
remains absent.

A third consecutive persisted-goal audit again observed the same HEAD and
tree, proof cursor, graph/context digests, empty ordered hard-parent closure,
weak shared-group evidence, unique validator path/blob, and absent alternate
candidate. The authority-selected argv was replayed a third time. It again
exited `1`, wrote zero stderr bytes, and returned the same single typed
`repair_required` object with `phase_accepted=false` and the base-drift
message quoted above. All three structural checks and the target manifest
check again passed.

The blocking condition has therefore repeated for three consecutive goal
turns and cannot be repaired within the worker-owned surface. Progress now
requires an external scheduler-state change: a current-bound immutable
validator (and, for actual root closure, proof-bearing material for the six
open arithmetic-geometric obligations). No receipt or self-test handoff has
been manufactured; this target-scoped report is the final truthful worker
evidence for the blocked goal.
