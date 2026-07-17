# THM-M-0113 proof validator-base blocker

## Scope

This is the target-scoped fail-closed result for `S56-M-0113-PROOF` at
worker base `e19e77ec08fca6a8a9c45a003c9904020dae8382` (tree
`53ff0ebe013670fc0332bf326fd860b29857ddab`). It changes no theorem source,
phase receipt, dependency ledger, validator candidate, task-state authority,
theorem-DAG projection, lifecycle, debt vector, or item state.

The sole task-state authority records the proof item and its obligation-tree
predecessor as `[_]`, each with one attempt. This is a current-base
revalidation of unfinished evidence, not a new state transition or master
acceptance. The exact claim tuple is `(v2_execution_rank=262,
phase_layer=4, phase_item_id=S56-M-0113-PROOF)`. The theorem-DAG SHA-256 is
`53622c848d6a0d8327bba8cd22bf45463f0dd8acb7ea0af2884713983e76c91f`;
the stable dependency-context SHA-256 is
`068170c76abd4579d643ede04d731b974412185bd285e7b40255ec4044adec5c`.

## Dependency And Reuse Audit

The complete `parent_inspection_order`, direct-parent list,
transitive-ancestor list, hard-edge list, reuse-hint list, and shared-group
list are all empty. The empty sequence was traversed exactly once, before
proof inspection, as the complete ascending-rank closure. No provider phase
state, receipt, declaration body, reusable artifact, terminal body, checkbox
state, proof credit, or acceptance was consumed, copied, transported, or
inherited.

The target-owned `dependency-reuse-ledger.json` has schema
`stage1-dependency-reuse-ledger/1.1` and truthfully records empty
`inspections`, `reuse_decisions`, and
`unresolved_compatibility_obligations`. It is historical evidence bound to
theorem-DAG digest
`eaee68bdf9fde9e311db076d1997fd8ef91919def0ba0fb399f1df77080f7153`
and repository revision `94009a6bebd743588e09c3b45bfbf18bf9b5c5e3`, not current-base evidence.
A current ledger would bind the current graph, context, base, and claim tuple
while retaining the same empty collections. It is deliberately not refreshed:
the mandatory semantic replay below fails, so no truthful current receipt or
self-test handoff can consume a refreshed ledger. This blocker records the
current empty closure without presenting the stale ledger as current evidence.

## First Failed Gate

`G05-AUTHORITY-REPLAY / validator_base_binding_stale` is the first
mechanically unrepairable worker gate. The mandatory proof contract (SHA-256
`1e7adf0f4fae0541b3595d4b0bfbb53f7eb17e28a4a889fec14f6df969e0cec4`)
declares these scheduler-owned candidates:

- `Stage1_Instances/THM-M-0113/check_proof.py`
- `Stage1_Instances/THM-M-0113/check_proof.sh`

Exactly one exists at worker base: `check_proof.py`, SHA-256
`d8699c95e10820abfe28df27ff5e73a1a08783aa76ce3b027d2dacc39429480c`,
Git blob `ba75b9dbf37eb093f982d3f8add2c788c19e439e`. Its worktree blob equals
the worker-base HEAD blob, so selection is unambiguous and the worker has not
changed it. The validator itself still requires obsolete base
`94009a6bebd743588e09c3b45bfbf18bf9b5c5e3`, tree
`daabee9f9b2c6e98d84b6290f78a209b950485fc`, theorem-DAG digest
`eaee68bdf9fde9e311db076d1997fd8ef91919def0ba0fb399f1df77080f7153`,
and a handoff tied to that base.

The exact contract-selected command was run without shell interpolation:

```text
/usr/bin/python3 -I -B Stage1_Instances/THM-M-0113/check_proof.py
```

It exited `1`, wrote no stderr, and wrote exactly this one semantic JSON object
on stdout:

```json
{"audit_complete":false,"blocked":false,"first_failed_gate":"P01-ARTIFACTS","item_id":"S56-M-0113-PROOF","message":"Proof evidence replay failed: repository HEAD differs from the claimed worker base","open_obligations":26,"phase":"proof","phase_accepted":false,"phase_predicate_proven":false,"schema_version":"stage1-validator-semantic-result/1.0","stale_inputs":[],"status":"failed","theorem_complete":false,"theorem_id":"THM-M-0113","verdict":"repair_required"}
```

Exit zero is not inferred. The typed result proves neither the assigned phase
predicate nor phase acceptance. The worker is forbidden to refresh, replace,
rename, create, or delete a validator candidate. Therefore the historical
`proof-receipt.json` remains untouched, no current receipt is manufactured,
and no `.stage1-worker-selftest.json` is emitted.

## Independent Mathematical Blocker

Even after scheduler-owned validator repair, the assigned positive proof
predicate cannot close for the frozen statement. The unchanged target-owned
declaration

```text
Stage1Instances.THMM0113.not_hodgeDecompositionTarget :
  Not Stage1Instances.THMM0113.HodgeDecompositionTarget.{0, 0, 0, 0}
```

was freshly elaborated at trust level zero. `HodgeData.isKahler` is an
unconstrained proposition independent of its arbitrary `cohomology` and
`hodgePiece` fields. The countermodel uses the compact zero-dimensional
complex manifold `Fin 0 -> Complex`, sets `isKahler := True`, every
cohomology space to `Complex`, and every Hodge piece to bottom. Degree-zero
spanning would force bottom to equal top and hence force `1 = 0`.

Lean printed the exact negation and only the axioms `propext`,
`Classical.choice`, and `Quot.sound`. The statement-output SHA-256 was
`483a37eb70184d0596b11301c4e15018629fd00bbd8a601fdc6ad7691dcd7e84`,
the proof-output SHA-256 was
`ee6378a7e948bc9267ee992aaa0355f1d6717185bddfcf0c3ac7099bd90b2d4c`,
and the scratch `Statement.olean` SHA-256 was
`94fe8a2182ea2776a7f9972ca82cd7c88b50fb2f57091d6527a82eb178d975e0`.
A scoped source scan found no `sorry`, `admit`, `sorryAx`, bodyless
declaration, unsafe injection, or unverifiable oracle in the target Lean
sources.

This refutes only the frozen abstract encoding, not the mathematical Hodge
decomposition theorem. It closes zero of the 26 positive obligations, adds
no positive terminal body, and grants no M0 or acceptance credit. Moreover,
`S56-M-0113-OBLIGATION_TREE` remains authoritative `[_]`, not
master-accepted `[x]`; topology independently prevents proof-phase
acceptance.

## Checks Run

All commands ran from this worker clone on 2026-07-17 (Asia/Shanghai). The
automation-provided pinned `.lake` symlink was reused read-only. No `lake
update`, `lake build`, dependency clone/fetch, network command, or cache
mutation ran. Lean output was confined to a fresh `/tmp` directory and then
removed.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | All 15 assurance groups, target set, v2 DAG, phase contract, and execution skill passed. |
| `python3 Docs/tools/check_stage1_theorem_dag_v2.py` | 0 | 1546 theorem nodes, 10822 states, typed relationships, and acyclicity passed. |
| `python3 Docs/tools/check_stage1_phase_acceptance_contracts.py` | 0 | Seven phase contracts, twelve common gates, and 23 source references passed. |
| `python3 scripts/stage1_target.py check` | 0 | The 1546 unique ordered L0/rework-required targets passed. |
| `python3 scripts/stage1_target.py show THM-M-0113` | 0 | Rank 25; planned lifecycle; legacy artifacts unaccepted; theorem incomplete. |
| `python3 Stage1_Instances/THM-M-0113/check_anchor_audit.py` | 0 | Frozen target boundary, four candidates, twelve Lean probes, and the mathlib pin agree. |
| `python3 Stage1_Instances/THM-M-0113/check_obligation_tree.py` | 0 | 26 obligations and 49 typed edges passed; denominator `e509c192...cbd5`; root remains M4. |
| Validator candidate enumeration and worker-base Git-blob check | 0 | Exactly `check_proof.py` exists; current and HEAD blobs are both `ba75b9db...`. |
| `/usr/bin/python3 -I -B Stage1_Instances/THM-M-0113/check_proof.py` | 1 | One typed `repair_required` result reported obsolete validator-base binding and `phase_accepted=false`. |
| Isolated `lake env lean --trust=0` replay of `Statement.lean` and `Proof.lean` | 0 | The exact negative specialization checked with the three expected axioms. |
| Scoped prohibited-construct scan | 1 | Expected no-match result. |
| `git diff --check -- Stage1_Instances/THM-M-0113 .stage1-worker-selftest.json` | 0 | No whitespace errors. |
| `test ! -e .stage1-worker-selftest.json` | 0 | No false self-test handoff was emitted. |

These are narrow, warm, nonrelease checks. Structural success and the
historical negative proof do not override the scheduler-selected validator's
typed failure. `audit_complete=false` and `theorem_complete=false`.

## Retry Condition And Status Boundary

First, the scheduler/master lane must publish a refreshed `check_proof.py`
whose immutable bindings match a new authoritative base, then issue a fresh
claim containing that exact unchanged blob. The worker cannot perform this
repair.

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
