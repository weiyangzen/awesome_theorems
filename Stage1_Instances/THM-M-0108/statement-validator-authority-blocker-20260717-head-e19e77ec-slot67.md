# THM-M-0108 current-base statement blocker

Item: `S56-M-0108-STATEMENT`

Worker base: `e19e77ec08fca6a8a9c45a003c9904020dae8382`

Worker verdict: `blocked`

Authoritative state: unchanged `[_]` with `attempts=1`

## Scope and order

The exact claim key is `(v2_execution_rank=267, phase_layer=1,
phase_item_id=S56-M-0108-STATEMENT)`. The current theorem-DAG SHA-256 is
`53622c848d6a0d8327bba8cd22bf45463f0dd8acb7ea0af2884713983e76c91f`, and the stable
dependency-context SHA-256 is
`068170c76abd4579d643ede04d731b974412185bd285e7b40255ec4044adec5c`.

The complete `parent_inspection_order` is exactly empty. The target has no direct hard parent,
transitive hard ancestor, incoming hard edge, reuse hint, or shared group. That empty closure was
traversed exactly once before Lean replay. There was no parent phase state, receipt, declaration
body, reusable artifact, import, copy, checked transport, provider checkbox, acceptance, or proof
credit to consume or transfer. No proof work was performed.

The tracked `dependency-reuse-ledger.json` uses schema
`stage1-dependency-reuse-ledger/1.1` and truthfully has empty `inspections`, `reuse_decisions`, and
`unresolved_compatibility_obligations`. It is historical evidence bound to repository revision
`2dc5a410...` and theorem-DAG digest `3d32f808...`, not fresh evidence at this base. It is not
rewritten in this blocked run: the sole integrated receipt binds those exact bytes, while the
immutable validator also demands the historical ledger. A ledger-only refresh would stale the
receipt without making the mandatory replay pass.

## Statement boundary

The existing reduced-carrier source still elaborates with the pinned imports. It declares
`Stage1Instances.THMM0108.ChowTheoremTarget`, includes dimension zero and the empty/full/reducible
set-theoretic cases, and contains the four required mutation declarations. The fresh narrow Lean
replay exited `0`; its expected `#check_failure` type mismatches were printed, and the target
reported only `propext`, `Classical.choice`, and `Quot.sound`.

That observation does not make the integrated evidence fresh. The sole
`stage1-node-receipt/1.0` and the statement record bind the original worker base and earlier graph.
Fresh source elaboration cannot replace the contract-mandated semantic validator, a current
receipt, source-fidelity review, or dependency-ordered master acceptance.

## First failed gate

`G05-AUTHORITY-REPLAY / immutable_validator_base_binding_stale`.

The statement contract declares two possible candidate paths. Exactly one exists at this worker
base: `Stage1_Instances/THM-M-0108/check_statement.py`, SHA-256
`b065466b58113f08ae2703dbb40074c8b7faf62c30e92c84f121c76965dc3fdd`, Git blob
`cea36f2ee8cdf94cf640c2c8e16cc80a7861e48d`. Its current bytes equal its base blob. This worker did
not create, modify, refresh, rename, replace, or delete any validator candidate.

The exact contract-selected invocation was:

```text
/usr/bin/python3 -I -B Stage1_Instances/THM-M-0108/check_statement.py
```

It exited `1`, wrote empty stderr, and emitted exactly one 579-byte JSON object with schema
`stage1-validator-semantic-result/1.0`. Stdout including its final newline has SHA-256
`a7178159963baaa889f2ffc51d21454e4ef25177b4fa275edd94c10102416d72`. The semantic result reports
`status=failed`, `verdict=repair_required`, `phase_accepted=false`,
`phase_predicate_proven=false`, `audit_complete=false`, and `theorem_complete=false`. Its immediate
message is the absence of `.stage1-worker-selftest.json`.

Creating a current packet cannot repair the candidate. After loading a packet, the unchanged
validator explicitly requires base `2dc5a410...`, tree `841bdd61...`, graph `3d32f808...`, the
pre-integration statement state `[ ]`, the historical receipt and ledger, and the original dirty
path set that included creation of the validator itself. Current values are base `e19e77ec...`, tree
`53ff0ebe...`, graph `53622c84...`, and state `[_]`. The validator is scheduler-owned and immutable
in this worker lane, so a new receipt or worker-self-test handoff cannot be truthfully produced.

## Checks

All dependency use was read-only. No `lake update`, `lake build`, dependency clone/fetch, network
operation, or `.lake` mutation was performed.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | Rev-5.6 structure, 1546-target manifest, v2 DAG, contract, and skill passed |
| `python3 Docs/tools/check_stage1_theorem_dag_v2.py` | 0 | 1546 nodes, 10822 states, 2 hard edges, 5 hints, 311 groups, acyclic |
| `python3 Docs/tools/check_stage1_phase_acceptance_contracts.py` | 0 | 7 phases, 12 common gates, and 23 source references passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique ordered targets, all `L0/rework_required` |
| `python3 scripts/stage1_target.py show THM-M-0108` | 0 | rank 32, planned lifecycle, theorem incomplete |
| from `Formalizations/Lean`: `lake env lean ../../Stage1_Instances/THM-M-0108/Statement.lean` | 0 | exact reduced-carrier target and four mutations elaborated |
| `/usr/bin/python3 -I -B Stage1_Instances/THM-M-0108/check_statement.py` | 1 | one typed negative semantic result; repair required |
| post-artifact `python3 Docs/tools/check_stage1_standard.py` | 1 | fresh generation includes this new owned evidence; master must refresh the worker-forbidden DAG projection |
| post-artifact `python3 Docs/tools/check_stage1_theorem_dag_v2.py` | 1 | the checked-in projection is stale after the owned blocker addition |

The Lean subprocess also printed managed-sandbox stream warnings. Its zero exit is evidence for
the scoped elaboration only, not for phase acceptance.

The two structural checks passed at immutable pre-edit HEAD and fail only after these owned blocker
files enter the evidence inventory. This worker may not edit `Docs/Stage1_Theorem_DAG_v2.json`;
projection regeneration is an integration-lane responsibility and is recorded as a known handoff
boundary rather than hidden.

## Retry condition

The scheduler/authority-maintenance lane must publish one corrected statement validator and issue
a fresh claim whose immutable base already contains that unchanged validator. The validator and
one current `stage1-node-receipt/1.0` must bind current tracked artifacts and a current worker packet
without freezing the original revision, `[ ]` cursor, or dirty delta. The empty schema-1.1 ledger
must be refreshed against that same graph/base. After the intake predecessor is `[x]`, the
integration lane can replay the validator read-only, resolve the scheduler-owned role map,
independently review statement identity and the remaining 1949 source-fidelity debt, and decide
master acceptance.

This is current-base target-scoped blocker evidence only. It does not replace the sole phase
receipt, self-test the assigned phase, propose a new `[_]` transition, transfer acceptance, prove
Chow's theorem, decide `AUDIT-Z` or `THEOREM-Z`, change task state, or claim master acceptance.
Because the phase is not genuinely self-tested at this base, `.stage1-worker-selftest.json` is
intentionally absent.

## Continuation audit

The active goal rechecked this blocker at `2026-07-17T08:31:11+08:00`. HEAD, the authoritative
`[_]` state and one attempt, theorem-DAG digest, exact empty parent closure, validator blob, and
missing self-test boundary were unchanged. The mandatory validator again exited `1` with the same
579-byte stdout SHA-256 `a7178159...`, `repair_required`, and
`phase_predicate_proven=false`. A fresh Lean replay again exited `0`; its 10396-byte stdout has
SHA-256 `d69eb504...` and empty stderr.

This is the second consecutive active-goal observation of the identical scheduler-owned
validator-freshness blocker. No external state change has yet made a current receipt or worker
self-test packet truthful.

A third audit at `2026-07-17T08:32:50+08:00` again found the same HEAD, authority state, graph,
empty parent closure, and validator blob. The validator again exited `1` with the identical
579-byte stdout digest and negative semantic fields; Lean again exited `0` with the identical
10396-byte stdout digest. This is the third consecutive active-goal observation of the same
external blocker, so the persisted goal's strict blocked threshold is satisfied.
