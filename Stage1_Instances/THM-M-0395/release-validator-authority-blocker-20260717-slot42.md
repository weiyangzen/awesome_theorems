# THM-M-0395 release validator-authority blocker

## Scope

This is the target-scoped fail-closed result for `S56-M-0395-RELEASE` at worker base
`6cff7bae0e4547cf9ad8b7abaae20d1abb9fe049` (tree
`28c148dbd84fbd549c749f060c92c9a3f00b16d0`). It changes no theorem source, prior phase receipt,
task-state authority, theorem-DAG projection, lifecycle, debt vector, or acceptance state.

The exact claim tuple is
`(v2_execution_rank=8, phase_layer=6, phase_item_id=S56-M-0395-RELEASE)`. The authoritative theorem
DAG has SHA-256 `80cf05109d5b3776b7defe95fdb591b216894a57ecbb7180a59f315a67d487d5`; the stable target
dependency-context SHA-256 is
`068170c76abd4579d643ede04d731b974412185bd285e7b40255ec4044adec5c`.

## First failed gate

`G05-AUTHORITY-REPLAY / validator_base_stale` is the first mechanically unrepairable worker gate.
The mandatory HEAD release contract declares these scheduler-owned candidate paths:

- `Stage1_Instances/THM-M-0395/check_release.py`
- `Stage1_Instances/THM-M-0395/check_release.sh`
- `Stage1_Instances/THM-M-0395/validate_release.py`

Exactly one exists at the worker base: `check_release.py`, Git blob
`cb176d3f2c714b9bc94c282876c86545e6a56c57`, SHA-256
`676702bb3816f5fafc3c2d007ec0044a19a47294b8981c34322cc3d802d2071b`. Its worktree, current-HEAD,
and worker-base blobs are identical. The exact authority-selected command was run:

```text
/usr/bin/python3 -I -B Stage1_Instances/THM-M-0395/check_release.py
exit: 1
stdout: empty
stderr: release-decision: FAIL: observed theorem-DAG digest drifted
```

The validator hard-codes obsolete graph SHA-256
`e8472863a24609e37868f215bbf0e0654b11a62f912a403ebca5feb8de5a3b9b` and ancestor revision
`1cc6aa61bb055a5c032297ee457905c849af7608`. It exits before producing the contract-mandated single
`stage1-validator-semantic-result/1.0` JSON object. Structural success, Lean success, and exit-zero
inference cannot replace typed semantic stdout. Workers may not create, refresh, rename, replace, or
delete any candidate, so only the scheduler/master lane can repair this defect and publish that
unchanged repair at a future worker base.

The failed mandatory command means this phase is not genuinely self-tested. This run therefore
refreshes no `release-receipt.json` and emits no `.stage1-worker-selftest.json`.

## DAG and reuse audit

The required `parent_inspection_order` is exactly empty. The authoritative target node has no direct
hard parents, transitive hard ancestors, hard edges, reuse hints, or shared lemma groups. That empty
sequence was traversed exactly once as the complete closure. No provider phase state, receipt,
declaration body, reusable artifact, checkbox state, proof credit, or acceptance was consumed,
copied, imported, transported, or inherited.

The existing target-owned `dependency-reuse-ledger.json` truthfully uses schema
`stage1-dependency-reuse-ledger/1.1` and records empty `inspections`, `reuse_decisions`, and
`unresolved_compatibility_obligations`, but it binds the obsolete graph digest above and ancestor
revision `1cc6aa61bb055a5c032297ee457905c849af7608`. It is historical evidence, not a current release
ledger. Refreshing only this empty ledger cannot supply the missing immutable validator result or a
reviewable release receipt, so it is left untouched.

## Release boundary

Release is independently blocked at `G02-TOPOLOGY`: the sole task-state authority records
`S56-M-0395-VALIDATION` as `[_]`, not master-accepted `[x]`; all seven theorem phases remain `[_]`.
The validation receipt is provisional ancestor evidence, closes no frozen obligation, and does not
satisfy the current release contract.

The exact Faltings root remains `H1/M4/R3`. The local elementary finiteness transports and
same-workspace probes prove neither the root nor any frozen obligation; all seventeen root-relevant
obligations and exact root composition remain open. `AUDIT-Z` is also open because accepted H0 source
review, R0 readable review, complete root provenance/axiom/trust/TCB closure, accepted public
reconciliation, and accepted root cut-set classification are absent. No immutable empty-cache
cold/offline reproduction, SBOM/license closure, deterministic evidence bundle, two qualifying
independent attestations, independently implemented minimal verifier, protected release CI, or
master acceptance exists.

Thus `audit_complete=false` and `theorem_complete=false`. This blocker grants no state transition,
phase acceptance, accepted receipt ID, release grade, theorem completion, or master acceptance.

## Checks run

All commands ran from this worker clone on 2026-07-17 (Asia/Shanghai). The automation-provided pinned
`.lake` symlink was reused read-only. No `lake update`, `lake build`, dependency clone/fetch, network
operation, or `.lake` mutation was performed.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | All 15 assurance groups, the 1546-target manifest, v2 DAG, seven-phase contract, and execution skill passed. |
| `python3 Docs/tools/check_stage1_theorem_dag_v2.py` | 0 | 1546 theorem nodes, 10822 phase states, typed edges, and acyclicity passed. |
| `python3 Docs/tools/check_stage1_phase_acceptance_contracts.py` | 0 | Seven phases, twelve common gates, and scheduler-owned validator rules passed. |
| `python3 scripts/stage1_target.py check` | 0 | The ordered 1546-target L0/rework-required manifest passed. |
| `python3 scripts/stage1_target.py show THM-M-0395` | 0 | Rank 8, planned lifecycle, L0 baseline, legacy evidence unaccepted, theorem incomplete. |
| Contract candidate enumeration and base/HEAD Git-blob comparison | 0 | Exactly one declared release candidate exists and its current blob equals its worker-base blob. |
| `/usr/bin/python3 -I -B Stage1_Instances/THM-M-0395/check_release.py` | 1 | It emitted no stdout and rejected the current graph digest before semantic JSON. |
| `python3 Stage1_Instances/THM-M-0395/check_anchor_audit.py` | 0 | The immutable mathlib pin and seven non-closing candidates remained coherent. |
| `python3 Stage1_Instances/THM-M-0395/check_obligation_tree.py` | 0 | The 17-obligation, 46-edge tree remained open at M4 with only statement transport `M0395-S3` checked. |
| `python3 Stage1_Instances/THM-M-0395/check_validation.py` | 0 | Receipt freshness, registry identity, partial-support boundary, open root, and hygiene passed. |
| `cd Formalizations/Lean && ELAN_TOOLCHAIN=leanprover/lean4:v4.29.0 /usr/bin/bash ../../Stage1_Instances/THM-M-0395/check_proof.sh` | 0 | The frozen statement and three elementary transports elaborated with `--trust=0`. |
| `cd Formalizations/Lean && ELAN_TOOLCHAIN=leanprover/lean4:v4.29.0 /usr/bin/bash ../../Stage1_Instances/THM-M-0395/check_validation_lean.sh` | 0 | The statement, transports, and three same-workspace probes elaborated with `--trust=0`; reported axioms were `propext`, `Classical.choice`, and `Quot.sound`. |
| `git diff --check -- Stage1_Instances/THM-M-0395 .stage1-worker-selftest.json` | 0 | Target-scoped whitespace hygiene passed. |

The smaller target and Lean checks are valid warm observations only; they cannot self-test release in
place of the failed authority-selected semantic validator.

## Retry condition

The scheduler/master lane must publish a refreshed `check_release.py` whose blob is already present
at the next worker base and whose exact declared command emits one valid semantic JSON object against
the then-current graph and target-owned artifacts. A fresh claim can then refresh the empty
dependency ledger, release specification, decision, and exactly one release receipt on that base.

Even after this mechanical repair, release acceptance remains blocked until every predecessor is
master accepted, the complete audit reaches `AUDIT-Z`, and the immutable cold/offline,
supply-chain, deterministic-bundle, public-reconciliation, independent-attestation,
minimal-verifier, protected-CI, and final master gates pass. `THEOREM-Z` additionally requires exact
kernel closure and composition of the unchanged Faltings root.

## Continuation audit

The persisted goal was resumed against the identical worker base and tree. The sole task-state
authority still records all seven phases as `[_]`; the theorem-DAG and contract digests remain
`80cf05109d5b3776b7defe95fdb591b216894a57ecbb7180a59f315a67d487d5` and
`1e7adf0f4fae0541b3595d4b0bfbb53f7eb17e28a4a889fec14f6df969e0cec4`. Exactly one declared
candidate still exists, and its worktree, HEAD, and worker-base Git blob remains
`cb176d3f2c714b9bc94c282876c86545e6a56c57`. Replaying the exact argv again returned exit `1`, zero
stdout bytes, and `release-decision: FAIL: observed theorem-DAG digest drifted` on stderr. Thus no
typed semantic result, current release receipt, or truthful self-test handoff has become possible;
the scheduler-owned validator blocker repeats unchanged.

A second consecutive persisted-goal continuation again observed the identical base/tree, `[_]`
task cursor, authority digests, candidate count, and immutable candidate blob. The exact replay again
returned exit `1` with zero stdout bytes at the same stale-DAG check. This is the third consecutive
goal turn, counting the original worker turn, with the same scheduler-ownership condition and no
worker-permitted repair. The target is therefore at an actual impasse pending an external
scheduler/master-lane validator refresh and a fresh worker base.
