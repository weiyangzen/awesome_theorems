# THM-M-0105 statement revalidation: current-base validator blocker

## Scope And Claim Order

This is the target-scoped fail-closed result for
`S56-M-0105-STATEMENT` at worker base
`a808e6ec7a16a99e6ab3471085952287d4e24728` (tree
`9a77a1024e5129433c6dc9db23455b64c811abe1`). The sole task-state
authority, `Docs/Stage1_Blueprint_v2.md`, records the item as `[_]` with one
attempt and its intake predecessor as `[_]`. This run therefore revalidates
unfinished worker evidence; it does not repeat a `[ ] -> [_]` transition or
claim master acceptance.

The mandatory claim-order tuple was followed exactly:
`(v2_execution_rank=264, phase_layer=1,
phase_item_id=S56-M-0105-STATEMENT)`. The authoritative theorem-DAG SHA-256
is `de71a3ca00b2ac64f96f4a0b7363cf56d09acb943716310332e693d9c9503c6a`,
and the target dependency-context SHA-256 is
`068170c76abd4579d643ede04d731b974412185bd285e7b40255ec4044adec5c`.

## Dependency And Reuse Audit

The supplied `parent_inspection_order`, direct-hard-parent list,
transitive-hard-ancestor list, hard-edge list, reuse-hint list, and
shared-group list are all exactly `[]`. The complete empty inspection
sequence was traversed exactly once before any possible proof work. There
were no parent phase states, receipts, declaration bodies, terminal proof
bodies, or reusable artifacts to inspect or consume. No proof work was
performed, and no exact import, checked transport, provider checkbox state,
provider acceptance, or proof credit was copied or inherited. The empty
declared context is not a mathematical independence claim.

The tracked `dependency-reuse-ledger.json` uses schema
`stage1-dependency-reuse-ledger/1.1` and truthfully contains empty
`inspections`, `reuse_decisions`, and
`unresolved_compatibility_obligations`. It is historical provisional
evidence: it binds graph `e8472863...` and repository revision
`1cc6aa61...`, not this base. It was not refreshed because the immutable
validator pins those exact old ledger bytes and rejects the current base
before proving the phase predicate. A ledger-only edit cannot produce a
lawful self-test.

## First Failed Gate

`G05-AUTHORITY-REPLAY / validator_semantic_freshness` is the first failed
worker gate. The mandatory HEAD statement contract declares two
scheduler-owned candidates:

- `Stage1_Instances/THM-M-0105/check_statement.py`
- `Stage1_Instances/THM-M-0105/check_statement_artifacts.py`

Exactly one exists at this worker base: `check_statement.py`, SHA-256
`5772b8c5ba87fc786c143956aa0518a38456ef17a9448e7689b1b0cd7cb4ddeb`,
Git blob `24d6d2229cf212365f20e204fb7d3d0547690e4c`. Its worktree bytes equal
the HEAD blob. This worker did not create, refresh, rename, replace, or
delete either candidate.

The exact contract-selected argv was:

```text
/usr/bin/python3 -I -B Stage1_Instances/THM-M-0105/check_statement.py
```

It exited `0`, wrote no stderr, and emitted exactly one typed semantic JSON
object on stdout (476 bytes, SHA-256
`53ad2cc63077b422bc7f3674a4329434963309c13f416a7bf5ef24b93159e026`):

```json
{"audit_complete":false,"blocked":false,"first_failed_gate":"S56-M-0105-STATEMENT.validator","item_id":"S56-M-0105-STATEMENT","message":"Statement evidence failed closed: worker base revision or tree changed","open_obligations":1,"phase":"statement","phase_accepted":false,"phase_predicate_proven":false,"schema_version":"stage1-validator-semantic-result/1.0","stale_inputs":[],"status":"failed","theorem_complete":false,"theorem_id":"THM-M-0105","verdict":"repair_required"}
```

Exit zero means only that the validator emitted its semantic result. The
result is negative: `status=failed`, `verdict=repair_required`,
`phase_accepted=false`, and `phase_predicate_proven=false`. The candidate
hard-codes base `1cc6aa61bb055a5c032297ee457905c849af7608`, tree
`dc3053b55c5724ccb2e6a247e7deffebca9dbb99`, and pre-integration
authority/support hashes. Worker policy forbids repairing a declared
validator candidate, so this assignment cannot lawfully obtain a positive
current-base replay.

The sole tracked `statement-receipt.json` is exactly one historical
`stage1-node-receipt/1.0`, but its base and self-test also bind
`1cc6aa61...`. It is not a current-base phase receipt. Replacing it would
not repair the immutable validator, which pins the old receipt bytes.
Consequently this run leaves the historical receipt intact and emits no new
phase receipt.

## Supporting Lean Replay

The tracked source
`Stage1Instances.THM_M_0105.RiemannRochTarget` still elaborates in the
pinned environment with its checked definitional expansion and all four
distinct `#check_failure` mutations. The exact command

```text
cd Formalizations/Lean && LC_ALL=C TZ=UTC lake env lean --trust=0 ../../Stage1_Instances/THM-M-0105/Statement.lean
```

exited `0`. Its combined captured output was 1,853 bytes over 47 lines with
SHA-256
`529a043c7b61e5b3956aed4ab1e53ddcf4f7f87955211c62e4db6dcb25117308`.
The serialized canonical expression remains
`e69f2d70cecb6da37ea45e75b35aa3e57b175eb35b8cdf5eb4056ac141815cb2`;
the source SHA-256 remains
`2c5bb3a3e12910b1d9317fa60be408c94037388a4133759615cea0bc9454b33d`.

This narrow replay is supporting evidence only. It cannot override the
mandatory negative semantic validator, refresh acceptance, or prove
Riemann--Roch. The abstract typed divisor/cohomology interfaces remain M3
normalization debt, and the source/convention review remains open human-source
debt.

## Checks Run

All commands ran in this worker clone on 2026-07-17 (Asia/Shanghai). The
automation-provided canonical `.lake` symlink was reused without dependency
mutation. No `lake update`, `lake build`, dependency clone/fetch, network
operation, or `.lake` write was performed.

| Command | Exit | Result boundary |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | `0` | Rev-5.6 structure, manifest, v2 DAG, phase contract, and execution skill passed. |
| `python3 Docs/tools/check_stage1_theorem_dag_v2.py` | `0` | 1,546 theorem nodes, 10,822 states, typed relationships, state preservation, and acyclicity passed. |
| `python3 Docs/tools/check_stage1_phase_acceptance_contracts.py` | `0` | Seven phases, twelve common gates, and 23 source references passed. |
| `python3 scripts/stage1_target.py check` | `0` | The ordered 1,546-target uniform-L0 manifest passed. |
| `python3 scripts/stage1_target.py show THM-M-0105` | `0` | Rank 27, planned lifecycle, legacy artifacts unaccepted, theorem incomplete. |
| declared-candidate enumeration and HEAD-blob comparison | `0` | Exactly one candidate exists and is unchanged from HEAD. |
| `/usr/bin/python3 -I -B Stage1_Instances/THM-M-0105/check_statement.py` | `0` | One schema-valid typed object reported `repair_required` and `phase_accepted=false`. |
| `cd Formalizations/Lean && LC_ALL=C TZ=UTC lake env lean --trust=0 ../../Stage1_Instances/THM-M-0105/Statement.lean` | `0` | The tracked target, definitional expansion, axiom report, and four mutations elaborated; no proof body is claimed. |
| `cd Formalizations/Lean && lake env lean --version && lake --version` | `0` | Lean 4.29.0 at `98dc76e3...`; Lake 5.0.0-src+98dc76e. |
| pinned mathlib revision/tree and status | `0` | `8a178386...ea95` / `bdc39a31...c2b`; clean dependency worktree. |
| prohibited-token scan over target-owned Lean files | `1` expected no match | No `sorry`, `admit`, custom axiom, unsafe/oracle declaration, or placeholder token was found in source. |

The structural and Lean checks cannot substitute for the failed
scheduler-selected semantic predicate.

## Retry Condition And Boundary

The scheduler/master lane must publish a refreshed validator at exactly one
declared statement-validator path, then issue a fresh claim whose base already
contains that identical blob and a coherent current-graph ledger and
current-base phase receipt. The unchanged contract-selected argv must return
one positive typed semantic object before a worker self-test handoff can be
written. Dependency-ordered master acceptance of the intake remains a
separate master closure requirement.

Because this phase is not genuinely current-base self-tested,
`.stage1-worker-selftest.json` is deliberately absent. This blocker grants no
state transition, statement acceptance, accepted receipt, proof credit,
provider acceptance transfer, audit completion, theorem completion, or
master acceptance.
