# THM-M-0395 release validator-base blocker

## Scope

This is the target-scoped fail-closed result for `S56-M-0395-RELEASE` at worker base
`fe1ec5161fd86894fef54d2a1860437053d9e8d7` (tree
`3777ff4ba4b38bc02217f033c19d32763d75d039`). It changes no theorem source, prior phase receipt,
task-state authority, theorem-DAG projection, lifecycle, debt vector, or acceptance state.

The exact claim tuple is
`(v2_execution_rank=8, phase_layer=6, phase_item_id=S56-M-0395-RELEASE)`. The current theorem-DAG
SHA-256 is `6d0668e741eb7f886c28ad37c524f11eb902f5be610ea4e69a68badb80075b39`, and the stable target
dependency-context SHA-256 is
`068170c76abd4579d643ede04d731b974412185bd285e7b40255ec4044adec5c`.

## First failed gate

`G05-AUTHORITY-REPLAY / validator_base_stale` is the first mechanically unrepairable worker gate.
The mandatory HEAD release contract declares these scheduler-owned candidates:

- `Stage1_Instances/THM-M-0395/check_release.py`
- `Stage1_Instances/THM-M-0395/check_release.sh`
- `Stage1_Instances/THM-M-0395/validate_release.py`

Exactly one exists at the worker base: `check_release.py`, Git blob
`cb176d3f2c714b9bc94c282876c86545e6a56c57`. It is unchanged in this worker. The exact
authority-selected command was run:

```text
/usr/bin/python3 -I -B Stage1_Instances/THM-M-0395/check_release.py
exit: 1
stdout: empty
stderr: release-decision: FAIL: observed theorem-DAG digest drifted
```

The validator hard-codes obsolete graph digest
`e8472863a24609e37868f215bbf0e0654b11a62f912a403ebca5feb8de5a3b9b` and ancestor revision
`1cc6aa61bb055a5c032297ee457905c849af7608`. It exits before producing the contract-mandated single
`stage1-validator-semantic-result/1.0` JSON object. Exit-zero cannot be inferred, and structural or
Lean command success cannot replace typed semantic output. The worker is forbidden to create,
refresh, rename, replace, or delete a validator candidate, so this defect must be repaired by the
scheduler/master lane and then replayed from a fresh worker base.

Per the worker contract, the failed mandatory validator means this phase is not genuinely
self-tested. Therefore no release receipt is refreshed and no `.stage1-worker-selftest.json` is
emitted.

## Dependency and reuse audit

The complete `parent_inspection_order` is exactly empty. The authoritative target node has no direct
hard parents, transitive hard ancestors, hard edges, reuse hints, or shared lemma groups. That empty
sequence was traversed exactly once as the complete closure. No provider phase state, receipt,
declaration body, reusable artifact, checkbox state, proof credit, or acceptance was consumed,
copied, imported, transported, or inherited.

The existing target-owned `dependency-reuse-ledger.json` has schema
`stage1-dependency-reuse-ledger/1.1` and truthfully records an empty closure, but it binds the
obsolete graph digest above and ancestor revision `1cc6aa61bb055a5c032297ee457905c849af7608`.
It is historical evidence, not a current release ledger. A current ledger would still have empty
`inspections`, `reuse_decisions`, and `unresolved_compatibility_obligations`; refreshing it without
a valid phase receipt and mandatory validator result would not make this handoff admissible.

## Release boundary

Release is independently blocked at `G02-TOPOLOGY`: the authoritative state of
`S56-M-0395-VALIDATION` is `[_]`, not master-accepted `[x]`. Its receipt is provisional ancestor
evidence, closes no frozen obligation, and does not satisfy the current release contract. All seven
theorem phases remain `[_]`.

The frozen exact Faltings root remains `H1/M4/R3`. The local elementary finiteness transports and
same-workspace probes prove neither the root nor any frozen obligation; all seventeen root-relevant
obligations remain open. `AUDIT-Z` is also open: there is no accepted H0 source review, R0 readable
review, complete root provenance/axiom/trust/TCB closure, accepted public reconciliation, or accepted
root cut-set classification. The dossier has no immutable empty-cache cold/offline reproduction,
SBOM/license closure, deterministic release bundle, two qualifying independent attestations,
independently implemented minimal verifier, protected release CI, or master acceptance.

Thus `audit_complete=false` and `theorem_complete=false`. This blocker grants no state transition,
phase acceptance, accepted receipt ID, release grade, theorem completion, or master acceptance.

## Checks run

All commands ran from this worker clone on 2026-07-17 (Asia/Shanghai). No `lake update`, `lake
build`, dependency clone/fetch, network operation, or `.lake` mutation was performed.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | Rev-5.6 structure, manifest, v2 DAG, phase contract, and execution skill passed. |
| `python3 Docs/tools/check_stage1_theorem_dag_v2.py` | 0 | 1546 theorem nodes, 10822 phase states, typed edges, and acyclicity passed. |
| `python3 Docs/tools/check_stage1_phase_acceptance_contracts.py` | 0 | Seven phases, twelve common gates, and scheduler-owned validator rules passed. |
| `python3 scripts/stage1_target.py check` | 0 | The ordered 1546-target L0/rework-required manifest passed. |
| `python3 scripts/stage1_target.py show THM-M-0395` | 0 | Rank 8, planned lifecycle, L0 baseline, legacy evidence unaccepted, theorem incomplete. |
| candidate enumeration and worker-base Git-blob check | 0 | Exactly one declared release candidate exists, and its current blob equals its worker-base blob. |
| `/usr/bin/python3 -I -B Stage1_Instances/THM-M-0395/check_release.py` | 1 | It emitted no stdout and rejected the current graph digest before semantic JSON. |
| `python3 Stage1_Instances/THM-M-0395/check_anchor_audit.py` | 0 | The immutable mathlib pin and seven non-closing candidates remained coherent. |
| `python3 Stage1_Instances/THM-M-0395/check_obligation_tree.py` | 0 | The 17-obligation, 46-edge tree remained open at M4 with only statement transport `M0395-S3` checked. |
| `python3 Stage1_Instances/THM-M-0395/check_validation.py` | 0 | Receipt freshness, registry identity, partial-support boundary, open root, and hygiene passed. |
| `cd Formalizations/Lean && ELAN_TOOLCHAIN=leanprover/lean4:v4.29.0 /usr/bin/bash ../../Stage1_Instances/THM-M-0395/check_proof.sh` | 0 | The frozen statement and three elementary transports elaborated with `--trust=0`. |
| `cd Formalizations/Lean && ELAN_TOOLCHAIN=leanprover/lean4:v4.29.0 /usr/bin/bash ../../Stage1_Instances/THM-M-0395/check_validation_lean.sh` | 0 | The statement, transports, and three same-workspace probes elaborated with `--trust=0`; reported axioms were `propext`, `Classical.choice`, and `Quot.sound`. |

The failed mandatory command is the authoritative worker result. Smaller target-owned and Lean
checks are useful observations only and cannot self-test release in its place. The
automation-provided untracked `Formalizations/Lean/.lake` symlink remains untouched nonrelease
state.

## Retry condition

The scheduler/master lane must publish a refreshed `check_release.py` whose blob is already present
at the next worker base and whose exact declared command emits one valid semantic JSON object
against the then-current graph and target-owned artifacts. A fresh claim can then refresh the empty
dependency ledger, release specification, decision, and exactly one release receipt on that base.

Even after the mechanical validator defect is fixed, release acceptance remains blocked until every
predecessor is master accepted, the complete audit reaches `AUDIT-Z`, and the immutable cold/offline,
supply-chain, deterministic-bundle, public-reconciliation, independent-attestation,
minimal-verifier, protected-CI, and final master gates pass. `THEOREM-Z` additionally requires exact
kernel closure and composition of the unchanged Faltings root.
