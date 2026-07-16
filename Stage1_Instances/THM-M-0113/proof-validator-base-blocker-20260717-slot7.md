# THM-M-0113 proof validator-base blocker

## Scope

This is the target-scoped fail-closed result for `S56-M-0113-PROOF` at
worker base `0c2274d4ca42a99c4281bd566d19f1db7530a87a` (tree
`d1b6ec259121c90799df53290217af4ee29444b3`). It changes no theorem source,
phase receipt, dependency ledger, validator candidate, task-state authority,
theorem-DAG projection, lifecycle, debt vector, or item state.

The authoritative claim tuple is
`(v2_execution_rank=262, phase_layer=4,
phase_item_id=S56-M-0113-PROOF)`. The theorem-DAG SHA-256 is
`78e8063002c0e50e2b2d5de6f539073b0a91215542ff3ae241b5d03c0bf05e22`,
and the stable dependency-context SHA-256 is
`068170c76abd4579d643ede04d731b974412185bd285e7b40255ec4044adec5c`.

## Dependency And Reuse Audit

The complete `parent_inspection_order`, direct-parent list,
transitive-ancestor list, hard-edge list, reuse-hint list, and shared-group
list are all empty. The empty sequence was traversed exactly once as the
complete ascending-rank closure before proof inspection. No provider phase
state, receipt, declaration body, reusable artifact, terminal body, checkbox
state, proof credit, or acceptance was consumed, copied, or inherited.

The existing target-owned `dependency-reuse-ledger.json` uses schema
`stage1-dependency-reuse-ledger/1.1`, but it is historical proof evidence
bound to theorem-DAG digest
`eaee68bdf9fde9e311db076d1997fd8ef91919def0ba0fb399f1df77080f7153`
and repository revision `94009a6bebd743588e09c3b45bfbf18bf9b5c5e3`. A current
ledger would bind the graph/context/base above and still contain empty
`inspections`, `reuse_decisions`, and
`unresolved_compatibility_obligations`. It is deliberately not refreshed:
the mandatory semantic replay fails, so no current phase receipt or worker
self-test can truthfully consume a refreshed ledger. The current empty
closure is recorded here without presenting the stale ledger as current.

## First Failed Gate

`G05-AUTHORITY-REPLAY / validator_base_binding_stale` is the first
mechanically unrepairable worker gate. The mandatory proof contract (SHA-256
`1e7adf0f4fae0541b3595d4b0bfbb53f7eb17e28a4a889fec14f6df969e0cec4`)
declares two scheduler-owned candidates:

- `Stage1_Instances/THM-M-0113/check_proof.py`
- `Stage1_Instances/THM-M-0113/check_proof.sh`

Exactly one exists at worker base: `check_proof.py`, SHA-256
`d8699c95e10820abfe28df27ff5e73a1a08783aa76ce3b027d2dacc39429480c`,
Git blob `ba75b9dbf37eb093f982d3f8add2c788c19e439e`. Its current blob equals
the worker-base `HEAD` blob, so selection is unambiguous and the worker has
not changed it. The validator itself still binds obsolete base
`94009a6bebd743588e09c3b45bfbf18bf9b5c5e3`, tree
`daabee9f9b2c6e98d84b6290f78a209b950485fc`, theorem-DAG digest
`eaee68bdf9fde9e311db076d1997fd8ef91919def0ba0fb399f1df77080f7153`,
and an obsolete worker handoff.

The exact contract-selected command was run:

```text
/usr/bin/python3 -I -B Stage1_Instances/THM-M-0113/check_proof.py
```

It exited `1` and emitted exactly one semantic JSON object with schema
`stage1-validator-semantic-result/1.0`, `status=failed`,
`verdict=repair_required`, `phase_accepted=false`, and
`first_failed_gate=P01-ARTIFACTS`. Its message was `repository HEAD differs
from the claimed worker base`:

```json
{"audit_complete":false,"blocked":false,"first_failed_gate":"P01-ARTIFACTS","item_id":"S56-M-0113-PROOF","message":"Proof evidence replay failed: repository HEAD differs from the claimed worker base","open_obligations":26,"phase":"proof","phase_accepted":false,"phase_predicate_proven":false,"schema_version":"stage1-validator-semantic-result/1.0","stale_inputs":[],"status":"failed","theorem_complete":false,"theorem_id":"THM-M-0113","verdict":"repair_required"}
```

Exit zero is not inferred. The typed negative result cannot support a current
`stage1-node-receipt/1.0`, proof-phase acceptance, or master acceptance. The
worker is forbidden to refresh, replace, rename, or delete the candidate.
Therefore the historical `proof-receipt.json` remains untouched, and no
`.stage1-worker-selftest.json` is emitted.

## Independent Mathematical Blocker

Even after scheduler-owned validator repair, the assigned positive proof
predicate cannot close for the frozen statement. The unchanged target-owned
declaration

```text
Stage1Instances.THMM0113.not_hodgeDecompositionTarget :
  Not Stage1Instances.THMM0113.HodgeDecompositionTarget.{0, 0, 0, 0}
```

was freshly elaborated at trust level zero. `HodgeData.isKahler` is an
unconstrained proposition, independent of its arbitrary `cohomology` and
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
declaration, unsafe injection, or unverifiable oracle in the four target Lean
sources.

This refutes only the frozen abstract encoding, not the mathematical Hodge
decomposition theorem. It closes zero of the 26 positive obligations, adds
no positive terminal body, and grants no M0 or acceptance credit. Moreover,
`S56-M-0113-OBLIGATION_TREE` is authoritative `[_]`, not master-accepted
`[x]`; topology independently prevents proof-phase acceptance.

## Checks Run

All commands ran from this worker clone on 2026-07-17 (Asia/Shanghai). The
automation-provided pinned `.lake` symlink was reused read-only. No `lake
update`, `lake build`, dependency clone/fetch, network command, or cache
mutation ran. Lean output was confined to a fresh `/tmp` directory and then
removed.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | All 15 assurance groups, target set, v2 DAG, phase contract, and execution skill passed. |
| `python3 Docs/tools/check_stage1_theorem_dag_v2.py` | 0 | 1546 theorem nodes, 10822 states, typed edges, and acyclicity passed. |
| `python3 Docs/tools/check_stage1_phase_acceptance_contracts.py` | 0 | Seven phase contracts, twelve common gates, and 23 source references passed. |
| `python3 scripts/stage1_target.py check` | 0 | The 1546 unique ordered L0/rework-required targets passed. |
| `python3 scripts/stage1_target.py show THM-M-0113` | 0 | Rank 25; planned lifecycle; legacy artifacts unaccepted; theorem incomplete. |
| `python3 Stage1_Instances/THM-M-0113/check_anchor_audit.py` | 0 | Frozen target boundary, four candidates, twelve Lean probes, and mathlib pin agree. |
| `python3 Stage1_Instances/THM-M-0113/check_obligation_tree.py` | 0 | 26 obligations and 49 typed edges passed; the root remains M4. |
| validator candidate enumeration and worker-base Git-blob check | 0 | Exactly `check_proof.py` exists; current and base blobs are both `ba75b9db...`. |
| `/usr/bin/python3 -I -B Stage1_Instances/THM-M-0113/check_proof.py` | 1 | Typed `repair_required`: obsolete validator base binding; no acceptance inferred. |
| isolated `lake env lean --trust=0` replay of `Statement.lean` and `Proof.lean` | 0 | The exact negative specialization checked with the three expected axioms. |
| scoped prohibited-construct scan | 1 | Expected no-match result. |
| scoped tracked/addition whitespace assertions | 0 | `git diff --check` passed, and `git diff --no-index --check /dev/null` reported no whitespace diagnostic for this new blocker. |
| `test ! -e .stage1-worker-selftest.json` | 0 | No false self-test handoff was emitted. |

This is narrow, warm, nonrelease evidence. `audit_complete=false` and
`theorem_complete=false`.

## Retry Condition

First, the scheduler/master lane must publish a refreshed `check_proof.py`
whose immutable bindings match a new authoritative base, then issue a fresh
claim containing that exact unchanged blob. The worker cannot perform this
repair.

That mechanical repair will not make the positive phase provable. Reopen
`S56-M-0113-STATEMENT`; replace the disconnected `isKahler` proposition and
arbitrary cohomology/Hodge-piece fields with faithful native constructions or
noncircular law-bearing hypotheses; accept a new statement fingerprint and
real mutation-failure evidence; then freshly freeze and master-accept the
anchor audit and obligation tree before resuming proof work. Alternatively,
redirect the item explicitly to the checked counterexample target.

This blocker grants no state transition, proof-phase acceptance, provider
acceptance transfer, accepted receipt ID, root closure, validation, release,
AUDIT-Z, THEOREM-Z, theorem completion, or master acceptance.
