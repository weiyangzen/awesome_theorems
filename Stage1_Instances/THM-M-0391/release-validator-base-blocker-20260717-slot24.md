# THM-M-0391 release validator-base blocker

## Scope

This is the target-scoped fail-closed result for `S56-M-0391-RELEASE` at
worker base `6cff7bae0e4547cf9ad8b7abaae20d1abb9fe049` (tree
`28c148dbd84fbd549c749f060c92c9a3f00b16d0`). It changes no theorem source,
prior phase receipt, task-state authority, theorem-DAG projection, lifecycle,
debt vector, or acceptance state.

The exact claim tuple is `(v2_execution_rank=5, phase_layer=6,
phase_item_id=S56-M-0391-RELEASE)`. The current theorem-DAG SHA-256 is
`80cf05109d5b3776b7defe95fdb591b216894a57ecbb7180a59f315a67d487d5`,
and the stable dependency-context SHA-256 is
`068170c76abd4579d643ede04d731b974412185bd285e7b40255ec4044adec5c`.

## First Failed Gate

`G05-AUTHORITY-REPLAY / validator_base_stale` is the first mechanically
unrepairable worker gate. The mandatory HEAD release contract declares three
scheduler-owned candidates:

- `Stage1_Instances/THM-M-0391/check_release.py`
- `Stage1_Instances/THM-M-0391/check_release.sh`
- `Stage1_Instances/THM-M-0391/validate_release.py`

Exactly one exists at the worker base: `check_release.py`, Git blob
`ece5308813f987fd3607e90fd71c308c9da5d7e3`. It is unchanged in this worker.
The exact authority-selected command was run:

```text
/usr/bin/python3 -I -B Stage1_Instances/THM-M-0391/check_release.py
exit: 1
stdout: empty
stderr: THM-M-0391 release validator: repository HEAD differs from the claimed worker base
```

The validator hard-codes ancestor revision
`1cc6aa61bb055a5c032297ee457905c849af7608`, ancestor tree
`dc3053b55c5724ccb2e6a247e7deffebca9dbb99`, and obsolete theorem-DAG digest
`e8472863a24609e37868f215bbf0e0654b11a62f912a403ebca5feb8de5a3b9b`.
It exits before producing the contract-mandated single
`stage1-validator-semantic-result/1.0` JSON object. The current validator also
binds obsolete hashes for the task-state blueprint, execution DAG, and
execution skill. The worker is forbidden to refresh, replace, rename, create,
or delete a validator candidate, so the scheduler/master lane must repair the
validator and issue a fresh claim from a base containing that exact blob.

Because the mandatory command did not produce semantic JSON, the assigned
phase is not genuinely self-tested. This worker therefore does not refresh the
release receipt and does not emit `.stage1-worker-selftest.json`.

## Dependency And Reuse Audit

The complete supplied `parent_inspection_order` is exactly empty. The
authoritative theorem node has no direct hard parents, transitive hard
ancestors, hard edges, reuse hints, or shared lemma groups. Its complete closure
was traversed vacuously once, in the required order. No provider declaration,
receipt, reusable body, proof credit, or acceptance was consumed, copied,
imported, transported, or inherited.

The tracked `dependency-reuse-ledger.json` has the required
`stage1-dependency-reuse-ledger/1.1` schema and truthfully contains empty
`inspections`, `reuse_decisions`, and
`unresolved_compatibility_obligations`. It is historical rather than current
release evidence because it binds the obsolete graph digest and ancestor
revision above. A current ledger would retain the same empty audited closure.
Refreshing it cannot substitute for the failed mandatory validator or make a
self-test handoff admissible, so it is left unchanged with the prior release
artifacts.

## Release Boundary

Release independently fails `G02-TOPOLOGY`: the sole task-state authority
records `S56-M-0391-VALIDATION` as `[_]`, not master-accepted `[x]`. Its exact
receipt is provisional ancestor evidence at revision
`66630bedafa43a769b94226b7431188dea47edf1`; it lacks the current contract's
normalized acceptance and self-test fields and cannot support release.

The canonical statement and statement transport still elaborate. The only
implemented proof obligation, `M0391-B-EE`, and its independent same-workspace
probe also elaborate with `--trust=0`. This is warm provisional evidence for
one branch only. No declaration proves
`Stage1Instances.THMM0391.MihailescuTarget`; fourteen of fifteen frozen
root-relevant obligations and exact child-to-parent root composition remain
open. The root remains `H1/M4/R4`, with neither `AUDIT-Z` nor `THEOREM-Z`.

The dossier also lacks accepted H0 and R0 review, complete root
provenance/axiom/trust/TCB closure, an immutable clean empty-cache cold and
offline replay, SBOM/license closure, a deterministic release bundle,
bundle-derived accepted public projections, two qualifying independent
attestations, and an independently implemented minimal verifier. Thus
`audit_complete=false` and `theorem_complete=false`; this report grants no
state transition, accepted receipt, release grade, theorem completion, or
master acceptance.

## Checks Run

All commands ran inside this worker clone. No `lake update`, `lake build`,
dependency clone/fetch, network operation, or `.lake` mutation was performed.
The automation-provided untracked `.lake` symlink was reused read-only and is
nonrelease evidence.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | Rev-5.6 structure, target manifest, v2 DAG, phase contract, and skill passed. |
| `python3 Docs/tools/check_stage1_theorem_dag_v2.py` | 0 | 1546 theorem nodes, 10822 states, typed edges, and acyclicity passed. |
| `python3 Docs/tools/check_stage1_phase_acceptance_contracts.py` | 0 | Seven phases, twelve common gates, and scheduler-owned validator rules passed. |
| `python3 scripts/stage1_target.py check` | 0 | The ordered 1546-target uniform-L0 manifest passed. |
| `python3 scripts/stage1_target.py show THM-M-0391` | 0 | Rank 5, planned lifecycle, rework required, theorem incomplete. |
| candidate enumeration and HEAD-blob comparison | 0 | Exactly one declared candidate exists, and its current blob equals its worker-base blob. |
| `/usr/bin/python3 -I -B Stage1_Instances/THM-M-0391/check_release.py` | 1 | Empty stdout; stale validator rejected the current worker base before semantic JSON. |
| `cd Formalizations/Lean && lake env lean --trust=0 ../../Stage1_Instances/THM-M-0391/Statement.lean` | 0 | Exact target, transport, and boundary mutations elaborated. |
| `cd Formalizations/Lean && lake env lean --trust=0 ../../Stage1_Instances/THM-M-0391/Proof.lean` | 0 | `M0391-B-EE` elaborated; reported axioms were `propext` and `Quot.sound`. |
| `cd Formalizations/Lean && lake env lean --trust=0 ../../Stage1_Instances/THM-M-0391/Validation.lean` | 0 | Independent same-workspace branch proof elaborated; reported axioms were `propext`, `Classical.choice`, and `Quot.sound`. |

The Lean processes also printed sandbox stream-fd warnings, but returned zero
and produced the expected declaration and axiom reports. These bounded checks
cannot replace the missing typed release-validator result.

## Retry Condition

The scheduler/master lane must publish a refreshed `check_release.py` whose
blob is already present at the next worker base and whose exact declared
command emits one valid semantic JSON object against the then-current graph,
authorities, and target artifacts. It must also publish the authority-owned
release role map before review.

After that mechanical repair, release remains blocked until dependency-ordered
master acceptance through validation, complete `AUDIT-Z`, exact root kernel
closure and composition, accepted H0/R0 and trust/provenance evidence, and all
immutable cold/offline, supply-chain, deterministic-bundle, public,
independent-attestation, minimal-verifier, and final master release gates pass.
