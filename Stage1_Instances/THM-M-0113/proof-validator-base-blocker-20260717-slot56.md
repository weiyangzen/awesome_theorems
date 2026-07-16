# THM-M-0113 proof validator-base blocker

## Scope

This is the target-scoped fail-closed result for `S56-M-0113-PROOF` at
worker base `db2e21b8fec263c5b65014acb1ee2039566e35a3` (tree
`815414c57391f2c12871c05a6e3d2944b0f2fef2`). It changes no theorem source,
prior receipt, task-state authority, theorem-DAG projection, lifecycle, debt
vector, item state, or scheduler-owned validator candidate.

The sole task-state authority records this item as `[_]` with one attempt and
its obligation-tree predecessor as `[_]` with one attempt. This run is a
current-base revalidation of unfinished worker evidence, not a new state
transition or master acceptance. The exact claim tuple is
`(v2_execution_rank=262, phase_layer=4,
phase_item_id=S56-M-0113-PROOF)`. The current theorem-DAG SHA-256 is
`91ea782c662e40b9608f8900ad586114c5ef8e8e5d2d2f13316185bd8f205067`;
the stable dependency-context SHA-256 is
`068170c76abd4579d643ede04d731b974412185bd285e7b40255ec4044adec5c`.

## Dependency And Reuse Audit

The authoritative `parent_inspection_order`, direct-hard-parent list,
transitive-hard-ancestor list, hard-edge list, reuse-hint list, and shared-group
list are all empty. The complete ordered closure was traversed exactly once,
before proof inspection, by inspecting zero providers. No provider phase
state, receipt, declaration body, reusable artifact, terminal proof body,
checkbox state, proof credit, or acceptance was consumed, copied, transported,
or inherited.

The tracked target-owned `dependency-reuse-ledger.json` has schema
`stage1-dependency-reuse-ledger/1.1` and truthfully records empty
`inspections`, `reuse_decisions`, and
`unresolved_compatibility_obligations`. It is historical proof evidence bound
to repository revision `94009a6bebd743588e09c3b45bfbf18bf9b5c5e3` and
theorem-DAG digest
`eaee68bdf9fde9e311db076d1997fd8ef91919def0ba0fb399f1df77080f7153`,
not current-base evidence. A current ledger would bind the current graph,
context, base, and claim tuple while retaining the same empty collections.
It is deliberately not refreshed: the mandatory semantic replay below fails,
so no truthful current receipt or self-test handoff can consume a refreshed
ledger. This blocker records the current empty closure without presenting the
stale ledger as current evidence.

## First Failed Gate

`G05-AUTHORITY-REPLAY / validator_base_binding_stale` is the first worker gate
that cannot be repaired inside this assignment. The mandatory HEAD proof
contract has SHA-256
`1e7adf0f4fae0541b3595d4b0bfbb53f7eb17e28a4a889fec14f6df969e0cec4`
and declares two scheduler-owned candidates:

- `Stage1_Instances/THM-M-0113/check_proof.py`
- `Stage1_Instances/THM-M-0113/check_proof.sh`

Exactly one exists at the worker base: `check_proof.py`, SHA-256
`d8699c95e10820abfe28df27ff5e73a1a08783aa76ce3b027d2dacc39429480c`,
Git blob `ba75b9dbf37eb093f982d3f8add2c788c19e439e`. Its worktree blob equals
the HEAD blob, so candidate selection is unambiguous. However, the immutable
candidate still requires obsolete base
`94009a6bebd743588e09c3b45bfbf18bf9b5c5e3`, tree
`daabee9f9b2c6e98d84b6290f78a209b950485fc`, theorem-DAG digest
`eaee68bdf9fde9e311db076d1997fd8ef91919def0ba0fb399f1df77080f7153`,
and a worker packet tied to that base.

The exact contract-selected command was run without shell interpolation:

```text
/usr/bin/python3 -I -B Stage1_Instances/THM-M-0113/check_proof.py
```

It exited `1`, wrote no stderr, and wrote exactly this one JSON object on
stdout:

```json
{"audit_complete":false,"blocked":false,"first_failed_gate":"P01-ARTIFACTS","item_id":"S56-M-0113-PROOF","message":"Proof evidence replay failed: repository HEAD differs from the claimed worker base","open_obligations":26,"phase":"proof","phase_accepted":false,"phase_predicate_proven":false,"schema_version":"stage1-validator-semantic-result/1.0","stale_inputs":[],"status":"failed","theorem_complete":false,"theorem_id":"THM-M-0113","verdict":"repair_required"}
```

This typed negative result proves neither the phase predicate nor phase
acceptance. The worker is forbidden to refresh, replace, rename, create, or
delete a validator candidate. Therefore this phase is not genuinely
self-tested at the current base. The historical `proof-receipt.json` remains
bound to base `94009a6b`; it is not refreshed or presented as current
evidence, and no `.stage1-worker-selftest.json` is emitted.

The authority-owned per-item role map required by `G03-ARTIFACT-BINDING` is
also absent from this clone. That is a downstream master-lane blocker; it does
not supersede the earlier failed validator replay and does not authorize a
worker to manufacture the role map.

## Independent Mathematical Blocker

Even after the scheduler-owned validator is refreshed, the assigned positive
proof predicate cannot close for the current frozen statement. The unchanged,
target-owned declaration

```text
Stage1Instances.THMM0113.not_hodgeDecompositionTarget :
  Not Stage1Instances.THMM0113.HodgeDecompositionTarget.{0, 0, 0, 0}
```

is a placeholder-free kernel-checked countermodel. `HodgeData.isKahler` is an
unconstrained proposition independent of the arbitrary `cohomology` and
`hodgePiece` fields. The countermodel uses the compact zero-dimensional
complex manifold `Fin 0 -> Complex`, sets `isKahler := True`, every
cohomology space to `Complex`, and every Hodge piece to bottom. Degree-zero
spanning would force bottom to equal top and hence `1 = 0`.

This refutes only the frozen abstract encoding, not the mathematical Hodge
decomposition theorem. It closes zero positive obligations, supplies no
positive terminal body, and grants no M0 or acceptance credit. The frozen
obligation registry still has 26 obligations and 49 typed edges with root
`M0113-ROOT` at M4. The predecessor `S56-M-0113-OBLIGATION_TREE` is also
authoritative `[_]`, not master-accepted `[x]`, so topology independently
blocks proof-phase acceptance.

## Checks Run

All checks ran from this worker clone on 2026-07-17 (Asia/Shanghai). The
automation-provided `Formalizations/Lean/.lake` symlink was reused read-only;
no `lake update`, `lake build`, dependency clone/fetch, network command, or
cache mutation ran.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | All 15 assurance groups, the 1546-target set, v2 DAG, seven-phase contract, and execution skill passed. |
| `python3 Docs/tools/check_stage1_theorem_dag_v2.py` | 0 | 1546 theorem nodes, 10822 blueprint states, typed relationships, and acyclicity passed. |
| `python3 Docs/tools/check_stage1_phase_acceptance_contracts.py` | 0 | Seven phase contracts, twelve common gates, and 23 source references passed. |
| `python3 scripts/stage1_target.py check` | 0 | All 1546 ordered L0/rework-required targets passed. |
| `python3 scripts/stage1_target.py show THM-M-0113` | 0 | Rank 25; planned lifecycle; legacy artifacts unaccepted; theorem incomplete. |
| `python3 Stage1_Instances/THM-M-0113/check_anchor_audit.py` | 0 | Frozen target boundary, four candidate rows, twelve Lean probes, and pinned mathlib revision agree. |
| `python3 Stage1_Instances/THM-M-0113/check_obligation_tree.py` | 0 | 26 obligations and 49 typed edges passed; denominator `e509c192...cbd5`; root remains M4. |
| Declared candidate enumeration and HEAD/worktree blob comparison | 0 | Exactly `check_proof.py` exists and its blob is unchanged. |
| `/usr/bin/python3 -I -B Stage1_Instances/THM-M-0113/check_proof.py` | 1 | One typed `repair_required` result reported obsolete validator base binding and `phase_accepted=false`. |
| Scoped prohibited-construct scan over target Lean sources | 1 | Expected no-match: no `sorry`, `admit`, `sorryAx`, `native_decide`, bodyless declaration, unsafe injection, or unverifiable oracle was found. |
| `git diff --check -- Stage1_Instances/THM-M-0113 .stage1-worker-selftest.json` | 0 | No whitespace errors in the target-scoped handoff. |
| `test ! -e .stage1-worker-selftest.json` | 0 | No false self-test handoff was emitted. |

Structural checks and the historical negative proof do not override the
scheduler-selected validator's typed failure. `audit_complete=false` and
`theorem_complete=false`.

## Retry Condition And Status Boundary

The scheduler/master lane must publish a refreshed `check_proof.py` whose
unchanged blob is already present at a fresh worker base and whose bindings
match that base, the current theorem DAG, dependency ledger, target artifacts,
and handoff protocol. The scheduler must also publish the authority-owned role
map. A fresh worker may then execute the exact selected argv and write exactly
one current receipt plus self-test handoff only if the typed result proves the
phase predicate.

That mechanical repair will not make the positive theorem provable. Reopen
`S56-M-0113-STATEMENT`; replace the disconnected `isKahler` proposition and
arbitrary cohomology/Hodge-piece fields with faithful native constructions or
noncircular law-bearing hypotheses; accept a new statement fingerprint and
real mutation-failure evidence; then freshly freeze and master-accept the
anchor audit and obligation tree before resuming proof work. Alternatively,
redirect the item explicitly to the checked counterexample target.

This artifact is a target-scoped blocker only. It grants no state transition,
proof-phase acceptance, accepted receipt ID, provider acceptance transfer,
root closure, validation, release, AUDIT-Z, THEOREM-Z, theorem completion, or
master acceptance.
