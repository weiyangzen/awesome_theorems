# THM-M-0128 anchor-audit current-base blocker

## Scope

This is the target-scoped fail-closed result for
`S56-M-0128-ANCHOR_AUDIT` at worker base
`0c2274d4ca42a99c4281bd566d19f1db7530a87a` (tree
`d1b6ec259121c90799df53290217af4ee29444b3`). It changes no Lean source,
prior receipt, dependency ledger, validator candidate, task-state authority,
theorem-DAG projection, lifecycle, debt vector, or item state.

The sole task-state authority records the assigned item as `[_]` with one
attempt. This run is therefore a current-base revalidation of unfinished
worker evidence, not a new `[ ] -> [_]` transition and not master acceptance.
The exact claim tuple is `(v2_execution_rank=280, phase_layer=2,
phase_item_id=S56-M-0128-ANCHOR_AUDIT)`.

## Dependency And Reuse Audit

The authoritative theorem DAG has SHA-256
`78e8063002c0e50e2b2d5de6f539073b0a91215542ff3ae241b5d03c0bf05e22`.
The target dependency-context SHA-256 is
`068170c76abd4579d643ede04d731b974412185bd285e7b40255ec4044adec5c`.
The direct-parent, transitive-ancestor, hard-edge, reuse-hint, shared-group,
and `parent_inspection_order` lists are all empty. The complete ordered
closure was therefore traversed exactly once before any proof work by
inspecting zero providers. There are no parent phase states, receipts,
declaration bodies, reusable artifacts, imports, copies, or transports to
inspect or consume. No proof work was performed, no reuse was accepted, and
no provider checkbox state, acceptance, or proof credit was transferred.

The tracked `dependency-reuse-ledger.json` has the required schema
`stage1-dependency-reuse-ledger/1.1`, the correct stable context digest, and
truthful empty `inspections`, `reuse_decisions`, and
`unresolved_compatibility_obligations`. It is nevertheless historical worker
evidence bound to repository revision
`74d4c272070069bc62df15798895293b4795940a` and graph digest
`cb4b83c4c4a5474fce51f98098f1421315fe7f1bd8cd52205932e57eced9f675`,
not the current claim. Running the repository ledger checker against the
current graph and base fails closed with `dependency reuse ledger does not
match the graph supplied to its worker`.

The ledger is deliberately not refreshed in this blocked run. Its new bytes
would make the immutable scheduler-owned validator's hard-coded ledger hash
stale, while that validator is also hard-coded to the old base, graph, and
pre-integration `[ ]` phase state. Refreshing only the ledger could not yield
a truthful receipt or self-test handoff and would rewrite prior phase evidence
without repairing scheduler authority.

## First Failed Gate

`G05-AUTHORITY-REPLAY / validator_current_base_binding_stale` is the first
worker gate that cannot be repaired within this assignment. The mandatory
HEAD phase contract has SHA-256
`1e7adf0f4fae0541b3595d4b0bfbb53f7eb17e28a4a889fec14f6df969e0cec4`
and declares these scheduler-owned candidates:

- `Stage1_Instances/THM-M-0128/check_anchor_audit.py`
- `Stage1_Instances/THM-M-0128/check_anchor.py`

Exactly one exists at the worker base: `check_anchor_audit.py`, SHA-256
`63c2456d970610ab24229e9be5df45248ddd39b8fcde3ae6af63e630caa4449f`,
Git blob `83f95b0bdddc869182138b1074b6bc549874bb55`. Its HEAD and
worker-base bytes are identical, so candidate selection is unambiguous and
the candidate was not modified.

The immutable candidate hard-codes the obsolete repository revision
`74d4c272070069bc62df15798895293b4795940a`, tree
`6693e584a3d529077306168fe38abd693d210ef0`, theorem-DAG digest
`cb4b83c4c4a5474fce51f98098f1421315fe7f1bd8cd52205932e57eced9f675`,
old ledger digest, and the assertion that the authoritative anchor phase is
still `[ ]`. Current authority records `[_]`, and this claim has a later base
and graph. The worker is expressly forbidden to refresh, replace, rename,
create, or delete a validator candidate.

The exact contract-selected command was run without shell interpolation:

```text
/usr/bin/python3 -I -B Stage1_Instances/THM-M-0128/check_anchor_audit.py
```

It exited `1`, wrote no stderr, and wrote exactly one JSON object on stdout:

```json
{"audit_complete":false,"blocked":false,"first_failed_gate":"ANCHOR-AUDIT-SEMANTIC-CHECK","item_id":"S56-M-0128-ANCHOR_AUDIT","message":"[Errno 2] No such file or directory: '/home/sansha-2/external/awesome_theorems/.cron/stage1-v2-app-server/workers/slot66/.stage1-worker-selftest.json'","open_obligations":1,"phase":"anchor_audit","phase_accepted":false,"phase_predicate_proven":false,"schema_version":"stage1-validator-semantic-result/1.0","stale_inputs":[],"status":"failed","theorem_complete":false,"theorem_id":"THM-M-0128","verdict":"repair_required"}
```

The stdout SHA-256 is
`12741c0ef5e09b4aecf2a27cb177c58064262698a395edc98fb2bc286dc66c77`;
empty stderr has SHA-256
`e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`.
This is a typed negative result. It does not prove the phase predicate and
cannot support a current-base phase receipt or worker self-test handoff.
Creating the handoff first would be circular because the unchanged validator
requires it to equal the historical receipt's old-base command packet; even
then the subsequent base, graph, phase-state, and ledger assertions would
fail.

The topology gate is independently open for master acceptance:
`S56-M-0128-STATEMENT` remains `[_]`, not `[x]`. Its negative receipt is
observation-only and does not supply an accepted canonical statement.

## Existing Audit Boundary

The tracked anchor inventory remains useful historical observation. It
classifies its seven-candidate bounded inventory across all seven prescribed
lanes and explicitly records network/public-discovery limits. It is not fresh
current-base evidence and makes no saturation claim. Its mathematical
boundary remains unchanged:

- No source-authorized exact proposition or expression fingerprint is frozen.
- Repo-local `S1_M_046` assumes the desired reciprocity law as data and has no
  eligible terminal proof body.
- Pinned mathlib provides CM-field and adele-ring substrate, not CM types,
  reflex norms, the Artin action, canonical Shimura models, special points, or
  the desired compatibility equation.
- Adjacent class-field-theory scaffolding and tracked external projects are
  mismatched, incomplete, unpinned in this closure, or otherwise ineligible.
- Primary human sources still lack admitted immutable theorem/page evidence,
  full assumption and convention crosswalks, errata review, and independent
  `H0` review.

No observation establishes an exact target, `H0`, `M0-*`, `M1`, accepted
reuse, root proof credit, `AUDIT-Z`, or `THEOREM-Z`.

## Checks Run

All commands ran in this worker clone on 2026-07-17 (Asia/Shanghai). The
automation-provided pinned `.lake` artifacts were reused without `lake
update`, `lake build`, dependency clone/fetch, or checkout.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | Fifteen assurance groups, 1546 targets, the v2 DAG, phase contracts, and execution skill passed. |
| `python3 Docs/tools/check_stage1_theorem_dag_v2.py` | 0 | 1546 theorem nodes, 10822 blueprint states, typed relations, deterministic order, and acyclicity passed. |
| `python3 Docs/tools/check_stage1_phase_acceptance_contracts.py` | 0 | Seven phase contracts, twelve common gates, and scheduler-owned validator rules passed. |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique ordered targets, all `L0/rework_required`, passed. |
| `python3 scripts/stage1_target.py show THM-M-0128` | 0 | Rank 46, planned, legacy artifacts unaccepted, theorem incomplete. |
| declared validator enumeration and HEAD/base blob comparison | 0 | Exactly one declared candidate exists and is unchanged at the worker base. |
| `/usr/bin/python3 -I -B Stage1_Instances/THM-M-0128/check_anchor_audit.py` | 1 | Exactly one typed semantic JSON object reported `repair_required` and `phase_accepted=false`; stdout/stderr hashes are recorded above. |
| current-base `validate_dependency_reuse_ledger(...)` | 1 | The historical ledger truthfully failed its stale graph/base binding. |
| from `Formalizations/Lean`: `env LEAN_NUM_THREADS=1 LC_ALL=C TZ=UTC timeout --foreground --kill-after=5s 300s lake env lean ../../Stage1_Instances/THM-M-0128/AnchorAudit.lean` | 0 | CM-field, adele-ring, and diagonal-map support anchors elaborated; `algebraMap_injective` reported `[propext, Classical.choice, Quot.sound]`; no target declaration was checked. |

The structural checks and narrow Lean elaboration do not override the
validator's typed negative semantic result. Because this phase is not
genuinely self-tested at the current base, this run creates no replacement
`stage1-node-receipt/1.0` and no root `.stage1-worker-selftest.json`. The sole
historical phase receipt remains bound to its old claim and is not rewritten.

## Retry Condition And Status Boundary

The scheduler/master lane must commit a refreshed validator at exactly one
declared path and issue a fresh claim whose base already contains that
identical blob. The refreshed authority packet must coherently bind the fresh
base/tree, current task state and graph, current empty schema-1.1 ledger,
current target artifacts, and exactly one phase receipt. A worker may then run
the contract argv and emit `.stage1-worker-selftest.json` only if the typed
semantic result proves the phase predicate. Master acceptance separately
requires the statement predecessor `[x]`, authority-owned role mapping,
content-bound HEAD artifacts, independent review, replay, and SSOT CAS.

This artifact is a target-scoped scheduler-ownership blocker only. It grants
no state transition, phase acceptance, source acceptance, reuse, proof credit,
audit completion, theorem completion, provider acceptance, or master
acceptance. The authoritative item remains unfinished at `[_]`.
