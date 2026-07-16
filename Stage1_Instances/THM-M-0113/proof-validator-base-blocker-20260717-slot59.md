# THM-M-0113 proof validator-base blocker

## Scope

This is the target-scoped fail-closed result for `S56-M-0113-PROOF` at
worker base `f545339546bf410d5110d7fe44e70bdcf5d8b48e` (tree
`6dc924134293b2674df7324ff98b6fdaf660159e`). It changes no theorem source,
prior phase receipt, task-state authority, theorem-DAG projection, lifecycle,
debt vector, item state, or validator candidate.

The authoritative claim tuple is
`(v2_execution_rank=262, phase_layer=4,
phase_item_id=S56-M-0113-PROOF)`. The theorem-DAG SHA-256 is
`39dc7ce5f668c527de899e74c99840aef50e6be4c576aaf146abed1b6749275c`,
and the stable dependency-context SHA-256 is
`068170c76abd4579d643ede04d731b974412185bd285e7b40255ec4044adec5c`.

## Dependency And Reuse Audit

The complete `parent_inspection_order`, direct-parent list,
transitive-ancestor list, hard-edge list, reuse-hint list, and shared-group
list are all empty. The empty sequence was traversed exactly once as the
complete ascending-rank closure before proof inspection. No provider phase
state, receipt, declaration body, reusable artifact, terminal proof body,
checkbox state, or acceptance was consumed, copied, or inherited.

The existing target-owned `dependency-reuse-ledger.json` has schema
`stage1-dependency-reuse-ledger/1.1` and truthfully records the same empty
closure, but it is historical proof evidence bound to graph digest
`eaee68bdf9fde9e311db076d1997fd8ef91919def0ba0fb399f1df77080f7153`
and repository revision `94009a6bebd743588e09c3b45bfbf18bf9b5c5e3`. A current ledger would bind
the graph/context/base above with empty `inspections`, `reuse_decisions`, and
`unresolved_compatibility_obligations`. It is deliberately not refreshed in
the repository because the mandatory semantic replay below fails and no
current phase receipt or worker self-test can truthfully consume that ledger;
the scheduler's fail-closed blocker lane preserves a new target report rather
than replacing already integrated phase evidence. The complete current
closure is recorded here without presenting the stale ledger as current.

## First Failed Gate

`G05-AUTHORITY-REPLAY / validator_base_binding_stale` is the first
mechanically unrepairable worker gate. The mandatory HEAD proof contract
(SHA-256
`1e7adf0f4fae0541b3595d4b0bfbb53f7eb17e28a4a889fec14f6df969e0cec4`)
declares two scheduler-owned candidates:

- `Stage1_Instances/THM-M-0113/check_proof.py`
- `Stage1_Instances/THM-M-0113/check_proof.sh`

Exactly one exists at the worker base: `check_proof.py`, SHA-256
`d8699c95e10820abfe28df27ff5e73a1a08783aa76ce3b027d2dacc39429480c`,
Git blob `ba75b9dbf37eb093f982d3f8add2c788c19e439e`. Its blob is unchanged from
worker-base `HEAD`, so candidate selection itself is unambiguous. However,
the scheduler-owned validator still binds obsolete claim inputs: base
`94009a6bebd743588e09c3b45bfbf18bf9b5c5e3`, tree
`daabee9f9b2c6e98d84b6290f78a209b950485fc`, and theorem-DAG digest
`eaee68bdf9fde9e311db076d1997fd8ef91919def0ba0fb399f1df77080f7153`.
It also requires a worker handoff packet tied to that obsolete base.

The exact contract-selected command

```text
/usr/bin/python3 -I -B Stage1_Instances/THM-M-0113/check_proof.py
```

exits `1` at the current worker base and emits exactly one semantic JSON
object with schema `stage1-validator-semantic-result/1.0`, `status=failed`,
`verdict=repair_required`, `phase_accepted=false`, and
`first_failed_gate=P01-ARTIFACTS`; its message is `repository HEAD differs
from the claimed worker base`. Exit zero is not inferred, and this typed
negative result cannot support a phase receipt or master acceptance.

The exact stdout object was:

```json
{"audit_complete":false,"blocked":false,"first_failed_gate":"P01-ARTIFACTS","item_id":"S56-M-0113-PROOF","message":"Proof evidence replay failed: repository HEAD differs from the claimed worker base","open_obligations":26,"phase":"proof","phase_accepted":false,"phase_predicate_proven":false,"schema_version":"stage1-validator-semantic-result/1.0","stale_inputs":[],"status":"failed","theorem_complete":false,"theorem_id":"THM-M-0113","verdict":"repair_required"}
```

The worker is expressly forbidden to refresh, replace, rename, or delete the
validator candidate. Therefore no truthful current-base
`stage1-node-receipt/1.0` can record a successful mandatory semantic replay.
Per the worker contract, this run emits no `.stage1-worker-selftest.json`.
The older `proof-receipt.json` remains historical evidence bound to base
`94009a6b`; it is neither refreshed nor presented as current evidence.

## Independent Mathematical Blocker

Even after the scheduler-owned validator is repaired, the assigned positive
proof predicate cannot close for the current frozen statement. The unchanged,
placeholder-free target-owned declaration

```text
Stage1Instances.THMM0113.not_hodgeDecompositionTarget :
  Not Stage1Instances.THMM0113.HodgeDecompositionTarget.{0, 0, 0, 0}
```

was freshly elaborated at trust level zero. `HodgeData.isKahler` is an
unconstrained proposition, independent of the arbitrary `cohomology` and
`hodgePiece` fields. The countermodel uses the compact zero-dimensional
complex manifold `Fin 0 -> Complex`, sets `isKahler := True`, every
cohomology space to `Complex`, and every Hodge piece to bottom. Degree-zero
spanning would force bottom to equal top and hence `1 = 0`.

Lean printed the exact negation and reported only `propext`,
`Classical.choice`, and `Quot.sound`. The statement-output SHA-256 was
`483a37eb70184d0596b11301c4e15018629fd00bbd8a601fdc6ad7691dcd7e84`,
the proof-output SHA-256 was
`ee6378a7e948bc9267ee992aaa0355f1d6717185bddfcf0c3ac7099bd90b2d4c`,
and the scratch `Statement.olean` SHA-256 was
`94fe8a2182ea2776a7f9972ca82cd7c88b50fb2f57091d6527a82eb178d975e0`.
No `sorry`, `admit`, `sorryAx`, bodyless declaration, unsafe injection, or
unverifiable oracle was found in the four target Lean sources.

The narrow kernel replay copied `Statement.lean` and `Proof.lean` to a fresh
`/tmp` directory, resolved `LEAN_PATH` and the Lean binary through `lake env`,
then ran these exact Lean invocations before deleting the scratch directory:

```text
LEAN_NUM_THREADS=1 LEAN_PATH="$PINNED_LEAN_PATH" timeout --foreground 600 "$PINNED_LEAN" --trust=0 -t 0 --root="$TMP" -o "$TMP/Statement.olean" "$TMP/Statement.lean"
LEAN_NUM_THREADS=1 LEAN_PATH="$TMP:$PINNED_LEAN_PATH" timeout --foreground 600 "$PINNED_LEAN" --trust=0 -t 0 --root="$TMP" "$TMP/Proof.lean"
```

This refutes only the frozen abstract encoding, not the mathematical Hodge
decomposition theorem. It closes zero of the 26 positive obligations, adds
no positive terminal proof body, and grants no M0 or acceptance credit.
Moreover, `S56-M-0113-OBLIGATION_TREE` remains authoritative `[_]`, not
master-accepted `[x]`; topology independently blocks proof-phase closure.

## Checks Run

All commands ran from this worker clone on 2026-07-17 (Asia/Shanghai). The
automation-provided pinned `.lake` symlink was reused read-only. No `lake
update`, `lake build`, dependency clone/fetch, network command, or cache
mutation ran.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | All 15 assurance groups, the 1546-target set, v2 theorem DAG, seven-phase contract, and execution skill passed. |
| `python3 Docs/tools/check_stage1_theorem_dag_v2.py` | 0 | 1546 theorem nodes, 10822 blueprint states, typed edges, and acyclicity passed. |
| `python3 Docs/tools/check_stage1_phase_acceptance_contracts.py` | 0 | Seven phase contracts, twelve common gates, and 23 source references passed. |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique ordered L0/rework-required targets passed. |
| `python3 scripts/stage1_target.py show THM-M-0113` | 0 | Rank 25; planned lifecycle; legacy artifacts unaccepted; theorem incomplete. |
| `python3 Stage1_Instances/THM-M-0113/check_anchor_audit.py` | 0 | Frozen target boundary, four candidate rows, twelve Lean probes, and pinned mathlib revision agree. |
| `python3 Stage1_Instances/THM-M-0113/check_obligation_tree.py` | 0 | 26 obligations and 49 typed edges passed; denominator `e509c192...cbd5`; root remains M4. |
| contract candidate enumeration and Git binding | 0 | Exactly `check_proof.py` exists; its current and base blobs are both `ba75b9db...`. |
| `/usr/bin/python3 -I -B Stage1_Instances/THM-M-0113/check_proof.py` | 1 | Typed `repair_required` result: obsolete validator base binding; no phase acceptance inferred. |
| prospective current graph/base empty-ledger validation in `/tmp` | 0 | Schema 1.1, exact graph/context/base identity, and all empty closure collections passed without changing integrated phase evidence. |
| isolated trust-zero `Statement.lean` plus `Proof.lean` replay | 0 | Exact negative specialization checked with the three expected axioms. |
| scoped prohibited-construct scan | 1 | Expected no-match result. |
| `git diff --check -- Stage1_Instances/THM-M-0113 .stage1-worker-selftest.json` | 0 | No whitespace errors. |
| `test ! -e .stage1-worker-selftest.json` | 0 | No false self-test handoff was emitted. |

The pre-existing untracked `Formalizations/Lean/.lake` symlink also makes
these warm checks nonrelease evidence. `audit_complete=false` and
`theorem_complete=false`.

## Retry Condition

First, the scheduler/master lane must publish a refreshed `check_proof.py`
whose immutable bindings match a new authoritative base, then issue a fresh
claim containing that exact unchanged blob. The worker cannot perform this
repair.

That mechanical repair will not make the positive phase provable. Reopen
`S56-M-0113-STATEMENT`; replace the disconnected `isKahler` proposition and
arbitrary cohomology/Hodge-piece fields with faithful native constructions or
noncircular law-bearing hypotheses; accept a new exact statement fingerprint
and real mutation-failure evidence; then freshly freeze and master-accept the
anchor audit and obligation tree before resuming proof work. Alternatively,
redirect the item explicitly to the checked counterexample target.

This blocker grants no state transition, proof-phase acceptance, provider
acceptance transfer, accepted receipt ID, root closure, validation, release,
AUDIT-Z, THEOREM-Z, theorem completion, or master acceptance.
