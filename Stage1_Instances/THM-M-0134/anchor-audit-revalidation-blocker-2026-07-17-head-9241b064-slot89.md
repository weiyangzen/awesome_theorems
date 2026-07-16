# THM-M-0134 anchor-audit revalidation blocker

Item: `S56-M-0134-ANCHOR_AUDIT`  
Theorem: `THM-M-0134`  
Claim order: `(v2_execution_rank=284, phase_layer=2, phase_item_id=S56-M-0134-ANCHOR_AUDIT)`  
Worker base revision: `9241b064a32cea3e16eb45d156fef8a2577704b0`  
Worker base tree: `c60b403a3058af0bbf32405a99c931274675784a`  
Authoritative item state: `[_]` with `attempts=1` (unchanged)  
Worker verdict: `blocked`  
Phase accepted: `false`  
Audit complete: `false`  
Theorem complete: `false`

## First failed gate

`G05-AUTHORITY-REPLAY.validator_is_scheduler_owned_but_stale_for_current_base`

The mandatory HEAD phase contract has SHA-256
`1e7adf0f4fae0541b3595d4b0bfbb53f7eb17e28a4a889fec14f6df969e0cec4` and declares these
two scheduler-owned candidates for `anchor_audit`:

- `Stage1_Instances/THM-M-0134/check_anchor_audit.py`
- `Stage1_Instances/THM-M-0134/check_anchor.py`

Exactly one exists. `check_anchor_audit.py` is tracked at this worker base with SHA-256
`f53625b4690d1fc6fd88ac6ac945516b0bfce07f936dd8e916e8792c2748f40d` and Git blob
`e0bbc3c9afd841322ed488637cad2bb406c58f1c`; the alias is absent. The worker did not create,
refresh, rename, replace, or delete either candidate.

The exact authority-selected argv was run:

```text
/usr/bin/python3 -I -B Stage1_Instances/THM-M-0134/check_anchor_audit.py
```

It exited `1` and emitted exactly one JSON object:

```json
{"audit_complete": false, "blocked": false, "first_failed_gate": "ANCHOR-AUDIT-SEMANTIC-CHECK", "item_id": "S56-M-0134-ANCHOR_AUDIT", "message": "theorem DAG digest drift", "open_obligations": 1, "phase": "anchor_audit", "phase_accepted": false, "phase_predicate_proven": false, "schema_version": "stage1-validator-semantic-result/1.0", "stale_inputs": [], "status": "failed", "theorem_complete": false, "theorem_id": "THM-M-0134", "verdict": "repair_required"}
```

The stdout is schema `stage1-validator-semantic-result/1.0` and truthfully says
`phase_accepted=false` and `phase_predicate_proven=false`. The validator is hard-bound to worker
revision `778c2db4855d48868391ea236f702e592067e798`, tree
`27abf0ec82dad50561a14d1db471126fb7ac8665`, and theorem-DAG SHA-256
`9db2a7cc29bf218211004677abe45ce1742f597405c2d879675dbc66542c4c8b`. Current HEAD has the base
and tree above and mandatory theorem-DAG SHA-256
`b0d43b142ed4d47aba3b66062c8303e96a736f259e50ef764918040521449c3a`. Because declared
validators are scheduler-owned, this worker cannot repair the stale pins or substitute an adapter.

The integrated phase receipt and dependency ledger are stale for the same reason. Both bind the
older worker base and older theorem-DAG digest. The receipt also describes its selected outputs as
untracked worker files even though they are now tracked at HEAD. They remain historical evidence;
they are not current-base self-test evidence and are not refreshed here because the unchanged
validator cannot validate a current-base receipt or ledger.

## Dependency and reuse audit

The sole task-state authority records this target's `anchor_audit` phase as `[_]` with one attempt.
The assigned claim tuple is therefore exactly rank `284`, layer `2`, and the assigned item ID. The
current theorem node has no direct hard parent, transitive hard ancestor, incoming hard edge, reuse
hint, or shared lemma group. Its stable dependency-context SHA-256 is
`068170c76abd4579d643ede04d731b974412185bd285e7b40255ec4044adec5c`.

The supplied `parent_inspection_order` is `[]`. That complete empty sequence was traversed exactly
once. No parent state, receipt, declaration body, reusable artifact, terminal proof body, import,
copy, checked transport, provider checkbox, proof credit, or acceptance was consumed or inherited.

The existing `dependency-reuse-ledger.json` has schema
`stage1-dependency-reuse-ledger/1.1` and truthfully records empty `inspections`,
`reuse_decisions`, and `unresolved_compatibility_obligations`. It is historical because its
`repository_revision` is `778c2db4...` and `observed_theorem_dag_sha256` is `9db2a7cc...`, not the
required current base and graph. Refreshing it alone would break the scheduler-owned validator's
fixed ledger hash and could not establish the phase predicate. The current graph and context
digests are recorded here for the scheduler-owned repair.

## Preserved audit boundary

The integrated bounded inventory remains useful discovery guidance. It classifies six rows across
all seven prescribed lanes and preserves these conclusions:

- The repo-local legacy module supplies a partition-classification statement shape and a
  conditional proof-package wrapper, but no package inhabitant or terminal proof body.
- Pinned mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`, tree
  `bdc39a3123201dae413a9d9be56ec242c19e5c2b`, supplies partitions, Young diagrams/tableaux,
  permutation groups, representations, and irreducibility substrate, but the frozen package scan
  located no exact terminal classification theorem. The Specht documentation row is unbound and
  denotes another theorem.
- No content-bound immutable external Lean 4 terminal candidate is present. Historical public
  search was access-limited, so neither global saturation nor global absence is claimed.
- No admitted primary passage selects one exact Burnside-Young proposition. The canonical statement
  remains null; `H4/M4/R4` and zero root proof credit are unchanged.

These observations do not repair the stale semantic validator, close the predecessor, or establish
the current-base phase predicate. The statement predecessor is independently only `[_]`, not
master-accepted `[x]`; its receipt is a blocked negative statement result with no canonical target.
Thus topology also remains open. No `AUDIT-Z`, `THEOREM-Z`, or theorem completion follows.

## Validation performed

All commands ran in the worker clone on 2026-07-17 (Asia/Shanghai). The automation-provided
`Formalizations/Lean/.lake` symlink was used read-only. No `lake update`, `lake build`, dependency
clone/fetch, checkout, or cache mutation was run.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 1546 uniform-L0 targets, the v2 DAG, seven-phase contract, and execution skill passed. |
| `python3 Docs/tools/check_stage1_theorem_dag_v2.py` | 0 | 1546 theorem nodes, 10822 phase states, 2 hard edges, 5 reuse hints, 311 groups, and acyclicity passed. |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all L0/rework-required. |
| `python3 scripts/stage1_target.py show THM-M-0134` | 0 | Rank 50, planned lifecycle, legacy evidence unaccepted, theorem incomplete. |
| declared candidate enumeration and base-blob comparison | 0 | Exactly one candidate exists and its current blob equals its worker-base blob. |
| `/usr/bin/python3 -I -B Stage1_Instances/THM-M-0134/check_anchor_audit.py` | 1 | Exactly one typed negative JSON result; message `theorem DAG digest drift`; `phase_accepted=false`. |
| `cd Formalizations/Lean && LC_ALL=C TZ=UTC LEAN_NUM_THREADS=1 lake env lean --trust=0 ../../Stage1_Instances/THM-M-0134/StatementInfrastructure.lean` | 0 | The unchanged target-owned representation vocabulary probe elaborated; it supplies no canonical target or proof. |
| `cd Formalizations/Lean && LC_ALL=C TZ=UTC LEAN_NUM_THREADS=1 lake env lean --trust=0 AwesomeTheorems/Stage1/S1_M_050.lean` | 0 | The unchanged legacy discovery module elaborated; it remains a conditional interface without a terminal proof body. |
| `python3 Docs/tools/check_stage1_phase_acceptance_contracts.py` | 0 | Seven phases, twelve common gates, twenty-three source references, and scheduler-owned validator rules passed. |
| `python3 -m json.tool` over the ledger, protocol, evidence, inventory, and historical receipt | 0 | Every integrated target JSON artifact parsed. |
| `git diff --check -- Stage1_Instances/THM-M-0134 .stage1-worker-selftest.json` | 0 | No whitespace errors in the target-scoped handoff. |

The structural passes and preserved inventory are supporting observations only. The mandatory
semantic validator's negative result is authoritative for this attempt, so the phase is not
genuinely self-tested. Per the explicit handoff rule, `.stage1-worker-selftest.json` is absent and
no replacement phase receipt is emitted.

## Retry condition

The scheduler/master lane must publish a refreshed declared anchor-audit validator at a new
authoritative commit, with current graph/base handling and current tracked-role semantics. A fresh
worker base must already contain the identical validator blob. That worker can then refresh the
empty schema-1.1 dependency ledger, bounded inventory bindings, validation record, and exactly one
`stage1-node-receipt/1.0`, run the contract argv, and emit a self-test handoff only if the typed
semantic result passes. Master acceptance separately requires the statement predecessor to become
`[x]`, authority-owned role resolution, independent read-only review/replay, and SSOT CAS.

This is target-scoped blocker evidence only. It grants no new phase transition, acceptance,
provider-credit transfer, proof credit, audit completion, theorem completion, or master acceptance.
