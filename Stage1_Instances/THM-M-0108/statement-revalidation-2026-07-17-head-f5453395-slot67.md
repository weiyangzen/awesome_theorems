# THM-M-0108 Statement Revalidation: Blocked

Item `S56-M-0108-STATEMENT` was rechecked at base
`f545339546bf410d5110d7fe44e70bdcf5d8b48e` (tree
`6dc924134293b2674df7324ff98b6fdaf660159e`) in claim order
`(v2 rank 267, phase layer 1, S56-M-0108-STATEMENT)`.

## Verdict

`blocked`. The existing reduced-carrier Chow target still elaborates under the
pinned Lean environment. However, the only contract-declared validator cannot
prove the statement predicate on this fresh claim base. Its exact required
invocation exits `1` and emits one schema-valid semantic JSON object with
`verdict=repair_required`, `phase_accepted=false`, and
`phase_predicate_proven=false`.

The validator is the unchanged HEAD/base blob
`cea36f2ee8cdf94cf640c2c8e16cc80a7861e48d` at
`Stage1_Instances/THM-M-0108/check_statement.py`. It hard-binds the original
worker base `2dc5a410...`, tree `841bdd61...`, theorem-DAG digest
`3d32f808...`, receipt, ledger, root worker packet, and original dirty-worktree
path set. The fresh values are base `f5453395...`, tree `6dc92413...`, and DAG
digest `39dc7ce5...`. The first runtime failure is the absent fresh root packet;
even manufacturing an old-shaped packet would only expose the deterministic
revision, tree, graph, receipt, ledger, packet-base, and worktree-delta
mismatches.

A scratch compatibility checkout can reproduce the original positive bootstrap
self-test by checking out `2dc5a410...`, overlaying the later target artifacts,
and reconstructing the original packet. That is historical evidence only. The
validator was absent at `2dc5a410...`, so this construction still fails the
contract's `candidate_must_exist_at_worker_base` rule and cannot substitute for
fresh HEAD replay.

The scheduler owns every validator candidate. This worker therefore did not
edit the validator or create an alternate candidate. Candidate selection is
otherwise valid: exactly one HEAD-tracked candidate exists, and its blob is
unchanged from this worker base. The blocker is semantic freshness, not
candidate absence, ambiguity, or worker tampering.

## Dependency And Reuse Boundary

The supplied direct/transitive hard-parent inspection order is exactly empty.
That complete empty closure was traversed once, in order. There are no hard
edges, reuse hints, or shared groups, so no parent declaration, receipt,
checkbox, proof body, or acceptance credit is consumed or transferred. No
proof work was performed.

The tracked schema-1.1 ledger truthfully has empty `inspections`,
`reuse_decisions`, and unresolved obligations, and its stable context digest
remains `068170c7...`. Its observed graph and repository revision are the
original `3d32f808...` and `2dc5a410...`, not the current `39dc7ce5...` and
`f5453395...`. Refreshing only the ledger cannot pass the protected validator,
which requires all of those old bindings and the old worker delta.

## Narrow Validation

All Lean dependency use was read-only. No network request, Lake update/build,
dependency clone/fetch, or `.lake` mutation was performed.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 pre-edit; 1 post-edit | Preflight passed. After adding the blocker files, fresh theorem-DAG generation includes them; the worker cannot update the checked-in projection |
| `python3 Docs/tools/check_stage1_theorem_dag_v2.py` | 0 pre-edit; 1 post-edit | Preflight passed. Post-edit projection drift is the expected master-integration boundary for new target-owned evidence |
| `python3 Docs/tools/check_stage1_phase_acceptance_contracts.py` | 0 | 7 phases, 12 common gates, and 23 source references passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1..1546, all `L0/rework_required` |
| `python3 scripts/stage1_target.py show THM-M-0108` | 0 | rank 32, planned, theorem incomplete |
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0108/Statement.lean` | 0 | target and four mutations elaborated; expected type-mismatch diagnostics and the recorded axiom boundary were printed |
| `/usr/bin/python3 -I -B Stage1_Instances/THM-M-0108/check_statement.py` | 1 | exactly one typed JSON result; `repair_required`, first failure `STATEMENT-SEMANTIC-CHECK` |

The validator stdout is 579 bytes including its final LF, at SHA-256
`a7178159963baaa889f2ffc51d21454e4ef25177b4fa275edd94c10102416d72`;
stderr is empty.

For diagnostic isolation only, a scratch current-HEAD checkout supplied the
reconstructed historical packet so the validator could pass its eager packet
load. It then failed exactly at `repository revision drift`, with exit `1` and
454-byte stdout SHA-256
`5f494965bd7f9e12fa864e300047c64f63837bdfa14b67da7a10c283a2706f15`.
No fresh packet was written to this worker clone.

A continuation audit at `2026-07-17T07:12:14+08:00` found the same HEAD,
authoritative `[_]` state, validator blob, and 579-byte negative semantic
result. The Lean statement replay again exited `0`; its 10396-byte stdout has
SHA-256 `d69eb504339b3fbae2a7ec7d96f317a81832bec113b374f61f87ddfe84275871`
and empty stderr. No external authority change has made a fresh worker packet
truthful.

The identical immutable-validator failure has now been observed in three
consecutive goal turns, at `07:03:36`, `07:12:14`, and `07:13:54` local time,
with unchanged HEAD and stdout digest. Further worker-local retries cannot make
progress without a scheduler-owned validator change.

## Retry Condition

A scheduler or authority-maintenance action must land one corrected statement
validator that checks immutable HEAD artifacts and a current-base worker packet
without freezing an obsolete repository revision or the original worker's
dirty-worktree delta. It must refresh the empty schema-1.1 ledger and sole
`stage1-node-receipt/1.0` against one graph/base. A later claim whose base
already contains that unchanged validator can then replay it read-only, obtain
independent review, resolve the scheduler-owned role map, and proceed to master
acceptance only after the intake predecessor is `[x]`.

This is current-base, target-scoped revalidation blocker evidence only. It
does not self-test or satisfy the statement phase, replace its sole receipt,
claim H0, prove Chow's theorem, establish audit/theorem completion, change task
state, or claim master acceptance. Because the assigned phase is not genuinely
self-tested, `.stage1-worker-selftest.json` is deliberately absent.
