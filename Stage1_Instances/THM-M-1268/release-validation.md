# THM-M-1268 release decision

Item: `S56-M-1268-RELEASE`  
Intent: `release`  
Verdict: `blocked`

The exact theorem-completion verdict is **false**. Lifecycle remains `planned`; the authoritative
root vector remains `[H2, M4, R4]`; and both `audit_complete` and `theorem_complete` remain false.
No receipt is accepted by this worker.

The provisional validation evidence is real but not release evidence. The exact frozen root, its
composition, local proof, exact wrapper, and a separately implemented same-clone reconstruction
elaborate under pinned Lean 4.29.0 and mathlib `8a178386`. The observed axioms are exactly
`propext`, `Classical.choice`, and `Quot.sound`, and the narrow placeholder and provenance checks
pass. However, the validation receipt has `support_state=provisional_worker_selftest` and
`release_grade=false`.

## Gate reconciliation

| Gate | Decision | Exact boundary |
|---|---|---|
| Validation prerequisite acceptance | fail closed | `S56-M-1268-VALIDATION` remains open and has no master-accepted receipt. |
| Authoritative root state | fail closed | The frozen graph remains `M4`, `root_closed=false`, with three proof bridges in its root cut. |
| Audit and source (`AUDIT-Z` / `H0`) | fail closed | The primary-source edition, theorem/page, assumptions, errata, and independently reviewed node crosswalk are absent. |
| Readable reconstruction (`R0`) | fail closed | No unique anchored reconstruction with independent review exists. |
| Hermetic reproduction | fail closed | The run reused a shared warm `.lake`; no immutable empty-cache cold build or network-denied offline restoration exists. |
| TCB and supply chain | fail closed | Complete transitive TCB, SBOM, licenses, restorable archive, and deterministic bundle are absent. |
| Independent verification | fail closed | Same-clone reconstruction is not two signed, independently provisioned clean-runner attestations or an accepted minimal verifier. |
| Master acceptance | pending | Only the integration lane may accept dependencies, reconcile authority, or promote state. |

The first failed gate is `S56-10.2-DEPENDENCY-ACCEPTANCE`. The first missing release-specific gate
is `S56-10.6-HERMETIC-COLD-BUILD`. Resolving either does not waive the other source, readability,
trust, supply-chain, independent-verification, deterministic-bundle, or master gates.

## Commands and exact results

```text
python3 Docs/tools/check_stage1_standard.py
  exit 0: 15 assurance groups and 1546 uniform-L0 Lean 4 targets passed

python3 scripts/stage1_target.py check
  exit 0: 1546 unique targets, ranks 1 through 1546, all L0/rework_required

python3 scripts/stage1_target.py show THM-M-1268
  exit 0: rank 444; planned; theorem_complete=false

python3 Stage1_Instances/THM-M-1268/check_release.py
  exit 0: validation replay passed; the blocked verdict, unchanged authority, false terminal
  decisions, root cut, and release-gate cut set agree

python3 -m json.tool Stage1_Instances/THM-M-1268/release-decision.json
  exit 0: valid JSON

git diff --check -- Stage1_Instances/THM-M-1268 .stage1-worker-selftest.json
  exit 0: no whitespace errors
```

The checker reuses only the existing narrow `lake env lean` validation recipe and does not update,
build, fetch, clone, or mutate `.lake`. This self-tests an honest negative release reconciliation,
not a theorem release, release receipt, accepted state transition, `AUDIT-Z`, `THEOREM-Z`, or master
acceptance.
