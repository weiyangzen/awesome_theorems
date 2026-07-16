# THM-M-0432 statement validator-base blocker

## Scope

This is the target-scoped fail-closed result for `S56-M-0432-STATEMENT` at
worker base `0c2274d4ca42a99c4281bd566d19f1db7530a87a` (tree
`d1b6ec259121c90799df53290217af4ee29444b3`). It changes no theorem source,
phase receipt, dependency ledger, validator, task-state authority, theorem-DAG
projection, lifecycle, debt vector, or acceptance state.

The authoritative claim key is
`(v2_execution_rank=294, phase_layer=1, phase_item_id=S56-M-0432-STATEMENT)`.
The theorem-DAG SHA-256 is
`78e8063002c0e50e2b2d5de6f539073b0a91215542ff3ae241b5d03c0bf05e22`,
and the stable dependency-context SHA-256 is
`068170c76abd4579d643ede04d731b974412185bd285e7b40255ec4044adec5c`.

## Authoritative current state

The sole task-state authority, `Docs/Stage1_Blueprint_v2.md`, records both
`S56-M-0432-INTAKE` and this statement item as `[_]` with one attempt. Under
the dual-cursor protocol, `[_]` is unfinished worker-self-tested evidence; it
is not master acceptance and must not be redone or promoted by a worker. The
current theorem-DAG projection agrees and records no direct hard parent,
transitive hard ancestor, hard edge, reuse hint, or shared lemma group.

The tracked statement receipt is truthful historical negative evidence, not a
positive statement result. It has schema `stage1-node-receipt/1.0`, SHA-256
`50fdd0480db8645acd234b23f5707bf26882ec7a76d7667379148d16c1136d17`,
Git blob `56a1568eb324522133200b7ccbdc827794d91666`, `accepted=false`,
`verdict=blocked`, no statement fingerprint, and four unrun mutations. It
binds the earlier base `94009a6bebd743588e09c3b45bfbf18bf9b5c5e3` and the obsolete
theorem-DAG digest
`eaee68bdf9fde9e311db076d1997fd8ef91919def0ba0fb399f1df77080f7153`.
Provider or predecessor acceptance is not inherited.

## First failed gate

`G05-AUTHORITY-REPLAY / validator_base_stale` is the first mechanically
unrepairable worker gate. The mandatory HEAD phase contract has SHA-256
`1e7adf0f4fae0541b3595d4b0bfbb53f7eb17e28a4a889fec14f6df969e0cec4`
and Git blob `84b92df9eaf457ab954b652c3f20f4d513cf0a88`. After substituting this
theorem ID, it declares exactly these scheduler-owned statement candidates:

- `Stage1_Instances/THM-M-0432/check_statement.py`
- `Stage1_Instances/THM-M-0432/check_statement_artifacts.py`

Exactly one exists at this worker base: `check_statement.py`, SHA-256
`8525e4348b8ed4767bd4c3b2bc24b16acc4b2bd192a62e79ead2d015b3cff6b4`,
Git blob `f10e8c331c9d03087e20e7397f88c96dd614385b`. Its current bytes equal
its HEAD and worker-base bytes, so candidate selection is unambiguous and the
worker has not modified it. The exact authority-selected replay was:

```text
/usr/bin/python3 -I -B Stage1_Instances/THM-M-0432/check_statement.py
exit: 1
stdout: {"audit_complete":false,"blocked":false,"first_failed_gate":"VALIDATOR-INTERNAL-CONSISTENCY","item_id":"S56-M-0432-STATEMENT","message":"Validator consistency failure: AssertionError: ","open_obligations":5,"phase":"statement","phase_accepted":false,"phase_predicate_proven":false,"schema_version":"stage1-validator-semantic-result/1.0","stale_inputs":[],"status":"failed","theorem_complete":false,"theorem_id":"THM-M-0432","verdict":"repair_required"}
stderr: traceback ending at `assert git("rev-parse", "HEAD") == BASE_REVISION`
```

The immutable validator hard-codes the old base and tree above, the obsolete
theorem-DAG digest, the old blueprint and execution-skill hashes, and the
historical receipt packet. Its stdout is exactly one typed semantic object,
but that object is a failure with `phase_accepted=false`; its nonzero exit
also fails. Other successful checks cannot replace this semantic replay. The
worker is forbidden to refresh, replace, rename, create, or delete a declared
validator candidate, so the scheduler must repair this gate.

Because the assigned phase is not genuinely self-tested at the current base,
this run writes no replacement `stage1-node-receipt/1.0` and no root
`.stage1-worker-selftest.json`. Refreshing the receipt without a lawful replay
would manufacture evidence rather than repair it.

## Dependency and reuse audit

The exact `parent_inspection_order`, direct-hard-parent list,
transitive-hard-ancestor list, hard-edge list, reuse-hint list, and shared-group
list are all `[]`. The prescribed complete closure was traversed exactly once
as the empty sequence before any proof work. No provider phase state, receipt,
declaration body, reusable artifact, terminal proof body, checkbox state,
proof credit, or acceptance was consumed, copied, transported, or inherited.
No proof work was performed. The empty declared context is not a claim of
mathematical independence.

The tracked `dependency-reuse-ledger.json` uses schema
`stage1-dependency-reuse-ledger/1.1` and truthfully records empty
`inspections`, `reuse_decisions`, and
`unresolved_compatibility_obligations`. It binds the same historical base and
obsolete graph digest as the validator, so it is observation-only evidence,
not a current-base ledger. It is not refreshed here: a ledger-only delta
cannot make the scheduler-owned validator replayable or support a new receipt
and handoff.

## Positive statement gate remains open

Even after scheduler repair, the positive statement predicate is independently
blocked. The repository catalog identifies Vladimir Drinfeld and only the
broad phrase "function-field Langlands correspondence"; it does not admit an
immutable theorem/page or fix the rank-two direction or bijection, object and
quotient classes, character restrictions, exceptional places, or
Frobenius/Hecke normalization. The neighboring `THM-M-0433` owns Lafforgue's
general `GL_n` result, so that result cannot be substituted here.

The pinned environment exposes adjacent function-field, Galois,
representation, general-linear-group, and arithmetic-Frobenius interfaces.
The unchanged target-owned `Statement.lean` elaborates those six checks at
trust level zero but deliberately declares no canonical target. The legacy
`StatementShape` takes caller-supplied parameter types and an unconstrained
`corresponds` predicate; it is discovery scaffolding, not Drinfeld's theorem.
Thus no exact expression, environment or statement fingerprint, checked
transport, canonical import-minimality result, or required statement mutation
exists. `S02-EXACT-TARGET` and `S03-MUTATIONS` remain open;
`audit_complete=false` and `theorem_complete=false`.

The intake predecessor is also only `[_]`, not master-accepted `[x]`, which
independently prevents dependency-ordered master closure under `G02-TOPOLOGY`.

## Checks run

All commands ran in this worker clone on 2026-07-17 (Asia/Shanghai). The
automation-provided untracked `.lake` symlink was reused read-only. No
`lake update`, `lake build`, dependency clone/fetch, checkout, network action,
or `.lake` mutation was performed.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | Rev-5.6 structure, all 1546 uniform-L0 targets, the v2 DAG, phase contract, and execution skill passed. |
| `python3 Docs/tools/check_stage1_theorem_dag_v2.py` | 0 | All 1546 theorem nodes, 10822 phase states, typed relationships, state preservation, and acyclicity passed. |
| `python3 Docs/tools/check_stage1_phase_acceptance_contracts.py` | 0 | Seven phase contracts, twelve common gates, and twenty-three source references passed. |
| `python3 scripts/stage1_target.py check` | 0 | The ordered 1546-target L0/rework-required manifest passed. |
| `python3 scripts/stage1_target.py show THM-M-0432` | 0 | Rank 60, planned lifecycle, legacy artifacts unaccepted, theorem incomplete. |
| Declared candidate enumeration and Git-blob comparison | 0 | Exactly one statement candidate exists, and its worktree, HEAD, and worker-base bytes agree. |
| `/usr/bin/python3 -I -B Stage1_Instances/THM-M-0432/check_statement.py` | 1 | One typed `failed` / `repair_required` JSON object reported the validator's stale embedded base; `phase_accepted=false`. |
| `cd Formalizations/Lean && LC_ALL=C TZ=UTC lake env lean --trust=0 ../../Stage1_Instances/THM-M-0432/Statement.lean` | 0 | The unchanged adjacent-interface probe elaborated; it grants no exact-target credit. |
| `git diff --check -- Stage1_Instances/THM-M-0432 .stage1-worker-selftest.json` | 0 | No whitespace errors in the target-scoped delta. |

The structural and Lean checks are bounded supporting observations. They do
not replace the failed scheduler-selected semantic validator or prove the
positive statement predicate.

## Retry condition and status boundary

The scheduler/master lane must publish a refreshed `check_statement.py`, or
exactly one other declared candidate, in an authoritative commit and issue a
fresh claim whose worker base contains the identical validator blob. A fresh
worker can then bind a current empty dependency ledger and exactly one phase
receipt and replay the contract-selected argv. Positive phase acceptance also
requires master acceptance of intake, an independently approved immutable
Drinfeld source theorem/page, a pinned concrete object model, exact
kernel-elaborated expression and environment fingerprint, checked alternate
transports, minimal canonical imports, and all four required mutation classes.

This artifact grants no state transition, phase acceptance, accepted receipt,
exact-statement credit, proof credit, provider acceptance transfer, audit
completion, theorem completion, or master acceptance.

## Persisted-goal continuation audit

The next automatic continuation re-read the same worker base and tree, the
same `[_]` cursor with one attempt, the same graph/context digests, the same
empty parent closure, and the same unique validator blob. The exact
contract-selected replay again exited `1` and emitted the same single typed
`failed` / `repair_required` object because its embedded base remains
`94009a6bebd743588e09c3b45bfbf18bf9b5c5e3`. The trust-zero Lean probe again
elaborated without creating a canonical target. No scheduler-owned repair or
fresh worker base has appeared, so the same external authority blocker
persists and a lawful receipt or self-test handoff remains impossible.

The third consecutive persisted-goal audit again observed that identical
base/tree, `[_]` cursor, graph/context, empty dependency closure, and unique
validator blob. The exact replay again exited `1` with the same typed
`VALIDATOR-INTERNAL-CONSISTENCY` failure at the embedded-base assertion, while
the narrow trust-zero Lean probe still elaborated only adjacent interfaces.
The blocking condition has therefore repeated unchanged across the original
worker turn and two automatic continuations. The worker is at an external
scheduler-ownership impasse and cannot make a truthful phase receipt or
self-test packet without a new authoritative validator/base.
