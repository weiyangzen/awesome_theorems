# THM-M-0105 statement revalidation blocker

## Scope and claim order

This is the target-scoped fail-closed result for
`S56-M-0105-STATEMENT` at worker base
`e19e77ec08fca6a8a9c45a003c9904020dae8382` (tree
`53ff0ebe013670fc0332bf326fd860b29857ddab`). The sole task-state authority,
`Docs/Stage1_Blueprint_v2.md`, records both this item and its intake predecessor
as `[_]`, each with one attempt. This run therefore revalidates unfinished
worker evidence; it does not claim a new state transition or master acceptance.

The exact claim-order tuple is `(v2_execution_rank=264, phase_layer=1,
phase_item_id=S56-M-0105-STATEMENT)`. The authoritative theorem-DAG SHA-256 is
`53622c848d6a0d8327bba8cd22bf45463f0dd8acb7ea0af2884713983e76c91f`,
and the stable dependency-context SHA-256 is
`068170c76abd4579d643ede04d731b974412185bd285e7b40255ec4044adec5c`.

## Dependency and reuse audit

The supplied `parent_inspection_order`, direct-hard-parent list,
transitive-hard-ancestor list, hard-edge list, reuse-hint list, and shared-group
list are all exactly `[]`. I traversed that complete empty sequence exactly once
before any possible proof work. There were no parent phase states, receipts,
declaration bodies, or reusable artifacts to inspect or consume. No proof work
was performed, and no provider acceptance or proof credit was transferred.

The tracked `dependency-reuse-ledger.json` has schema
`stage1-dependency-reuse-ledger/1.1` and truthfully contains empty
`inspections`, `reuse_decisions`, and
`unresolved_compatibility_obligations`. It is historical provisional evidence:
it binds graph `e8472863...` and revision `1cc6aa61...`, not the current graph
and base. It was not refreshed because the immutable validator pins those old
ledger bytes and rejects this base before proving the phase predicate. Editing
the ledger alone could not yield a lawful self-test.

## First failed gate

`G05-AUTHORITY-REPLAY.validator_semantic_freshness` is the first failed gate.
The HEAD phase contract declares two scheduler-owned candidate paths. Exactly
one exists:

- `Stage1_Instances/THM-M-0105/check_statement.py`

Its SHA-256 is
`5772b8c5ba87fc786c143956aa0518a38456ef17a9448e7689b1b0cd7cb4ddeb`,
its Git blob is `24d6d2229cf212365f20e204fb7d3d0547690e4c`, and its worktree
bytes equal the HEAD blob. This worker did not create, refresh, rename, replace,
or delete either declared validator candidate.

The exact contract-selected command was:

```text
/usr/bin/python3 -I -B Stage1_Instances/THM-M-0105/check_statement.py
```

It exited `0` and emitted exactly one JSON object:

```json
{"audit_complete":false,"blocked":false,"first_failed_gate":"S56-M-0105-STATEMENT.validator","item_id":"S56-M-0105-STATEMENT","message":"Statement evidence failed closed: worker base revision or tree changed","open_obligations":1,"phase":"statement","phase_accepted":false,"phase_predicate_proven":false,"schema_version":"stage1-validator-semantic-result/1.0","stale_inputs":[],"status":"failed","theorem_complete":false,"theorem_id":"THM-M-0105","verdict":"repair_required"}
```

Exit zero means only that the validator emitted its semantic result. The typed
result is negative: `status=failed`, `verdict=repair_required`,
`phase_accepted=false`, and `phase_predicate_proven=false`. The candidate pins
base `1cc6aa61bb055a5c032297ee457905c849af7608`, tree
`dc3053b55c5724ccb2e6a247e7deffebca9dbb99`, the old theorem-DAG digest,
the old blueprint and execution-skill digests, and the historical receipt and
ledger. Worker policy forbids repairing a declared validator candidate.

The sole tracked `statement-receipt.json` is exactly one
`stage1-node-receipt/1.0`, but it also binds the historical base and inputs.
Replacing it would not repair the immutable validator, which pins its old
bytes. This run therefore emits no replacement phase receipt.

## Narrow statement replay

The tracked `Stage1Instances.THM_M_0105.RiemannRochTarget` still elaborates in
the pinned environment with its checked definitional expansion and four
distinct `#check_failure` mutations. The command

```text
cd Formalizations/Lean && LC_ALL=C TZ=UTC lake env lean --trust=0 ../../Stage1_Instances/THM-M-0105/Statement.lean
```

exited `0`. Its combined output remains 1853 bytes with SHA-256
`529a043c7b61e5b3956aed4ab1e53ddcf4f7f87955211c62e4db6dcb25117308`;
the canonical expression remains
`e69f2d70cecb6da37ea45e75b35aa3e57b175eb35b8cdf5eb4056ac141815cb2`,
and the statement source remains
`2c5bb3a3e12910b1d9317fa60be408c94037388a4133759615cea0bc9454b33d`.
The printed transport axiom boundary is only `propext`, `Classical.choice`, and
`Quot.sound`; no `sorryAx` is credited.

This replay is supporting evidence only. It cannot override the negative
mandatory semantic validator or refresh acceptance. It proves no
Riemann-Roch body. The typed divisor/cohomology interfaces remain M3
normalization debt, and source/convention review remains H5 debt.

## Checks run

All commands ran in this worker clone on 2026-07-17 (Asia/Shanghai). The
automation-provided canonical `.lake` symlink was reused read-only. No
`lake update`, `lake build`, dependency clone/fetch, or other dependency
mutation was performed.

| Command | Exit | Result boundary |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | `0` | Rev-5.6 structure, manifest, v2 DAG, phase contract, and execution skill passed. |
| `python3 Docs/tools/check_stage1_theorem_dag_v2.py` | `0` | 1546 theorem nodes, 10822 states, typed relationships, and acyclicity passed. |
| `python3 Docs/tools/check_stage1_phase_acceptance_contracts.py` | `0` | Seven phases, twelve common gates, and 23 source references passed. |
| `python3 scripts/stage1_target.py check` | `0` | The ordered 1546-target uniform-L0 manifest passed. |
| `python3 scripts/stage1_target.py show THM-M-0105` | `0` | Rank 27, planned lifecycle, legacy artifacts unaccepted, theorem incomplete. |
| declared-candidate enumeration and HEAD-blob comparison | `0` | Exactly one candidate exists and is unchanged from HEAD. |
| `/usr/bin/python3 -I -B Stage1_Instances/THM-M-0105/check_statement.py` | `0` | One schema-valid object reported `repair_required` and `phase_accepted=false`. |
| `cd Formalizations/Lean && LC_ALL=C TZ=UTC lake env lean --trust=0 ../../Stage1_Instances/THM-M-0105/Statement.lean` | `0` | Exact target, expansion, axiom report, and four mutations elaborated; no proof body is claimed. |

These structural and Lean checks cannot replace the failed
scheduler-selected semantic predicate.

## Retry condition and boundary

The scheduler/master lane must publish a refreshed validator at exactly one
declared statement-validator path, plus a coherent current-graph schema-1.1
ledger and current-base phase receipt, then issue a fresh claim whose base
already contains that identical validator blob. The unchanged selected argv
must emit a positive typed semantic object before a worker self-test handoff
can be written. Dependency-ordered master acceptance of intake remains a
separate closure requirement.

Because this phase is not genuinely current-base self-tested,
`.stage1-worker-selftest.json` is deliberately absent. This blocker grants no
state transition, statement acceptance, accepted receipt, proof credit,
provider acceptance transfer, audit completion, theorem completion, or master
acceptance.
