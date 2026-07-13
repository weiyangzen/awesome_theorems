# THM-M-1029 validation-phase evidence

Item: `S56-M-1029-VALIDATION`

Base revision: `2d334dfd1443fdb9dbdf08b9d53d6c67399ec7af`

The validator re-elaborates the frozen statement, conditional obligation
composition, all 23 proof-phase declarations, and a separately written
conditional adapter. Every Lean elaboration/replay invocation uses `--trust=0`,
writes only fresh target outputs, and runs inside a network-disabled bubblewrap namespace. The
canonical pinned `.lake` inputs are mounted read-only and are not updated,
built, fetched, or cloned.

This is narrow partial validation, not theorem or release validation. The
proof receipt is provisional and `accepted=false`. More importantly,
`M1029-T-INCREMENTS` has no proof body. The proof-phase Gaussian,
independence, and strict-increment packages omit the target's continuity
hypothesis, so they are stronger conditional interfaces and receive no root
proof credit. The separate validation adapter deliberately keeps the strict
law as an explicit premise and only corroborates conditional composition.

## Commands and results

All commands ran from the worker clone on 2026-07-14.

```text
python3 Docs/tools/check_stage1_standard.py
  exit 0; 15 assurance groups and 1546 uniform-L0 targets passed

python3 scripts/stage1_target.py check
  exit 0; 1546 unique targets, ranks 1..1546, all L0/rework_required

python3 scripts/stage1_target.py show THM-M-1029
  exit 0; rank 222, planned, L0/rework_required, theorem_complete false

python3 Stage1_Instances/THM-M-1029/check_obligation_tree.py
  exit 0; 14 obligations and 28 typed edges passed
  root open (M3); M1029-T-INCREMENTS remains M4

python3 -B Stage1_Instances/THM-M-1029/check_validation.py
  exit 0
  PASS network-isolated trust-zero replay of the frozen modules
  PASS 25 axiom reports: propext, Classical.choice, Quot.sound only
  PASS selected frozen hashes, mathlib pin/tree/remote, manifest, and license
  OPEN root at M1029-T-INCREMENTS; audit_complete=false; theorem_complete=false
  BLOCKED cold-offline hermetic, complete trust/provenance, and distinct-runner gates

python3 -m json.tool Stage1_Instances/THM-M-1029/validation-spec.json
python3 -m json.tool Stage1_Instances/THM-M-1029/validation-receipt.json
python3 -m json.tool .stage1-worker-selftest.json
  exit 0 for each JSON document

git diff --check -- Stage1_Instances/THM-M-1029 .stage1-worker-selftest.json
  exit 0; no output
```

## Gate decisions

| Gate | Decision | Boundary |
|---|---|---|
| Exact local kernel replay | partial pass | The statement, one frozen conditional composition, 23 partial bodies, and one differential conditional adapter elaborate. No increment package is inhabited. |
| Placeholder and unsafe scan | pass | The four replayed Lean sources contain no placeholder, local axiom, opaque/unsafe/extern escape, or native-decision shortcut. |
| Observed axiom profile | partial pass | All 25 reports are exactly `propext`, `Classical.choice`, and `Quot.sound`; the instance foundation profile and full TCB profile are still unfrozen. |
| Selected provenance | partial pass | Bound sources, receipt, denominator, toolchain, manifest, clean mathlib revision/tree/remote, and license agree; the complete transitive closure and SBOM do not exist. |
| Proof dependency | fail closed | `S56-M-1029-PROOF` is only `[_]`, its receipt is not accepted, and master acceptance is absent. |
| Exact root | fail closed | `M1029-T-INCREMENTS` and the exact Levy root remain unproved at M3. |
| Hermetic release replay | fail closed | Network denial and fresh target outputs still reuse the warm canonical compiled dependency cache; there is no empty-cache cold build or offline archive restore. |
| Independent verification | fail closed | The separate adapter ran in the same clone and dependency environment; there is no distinct identity, independent provisioning, signature, or independent minimal receipt/graph verifier. |

The validation work is self-tested as a truthful partial gate run and may be
proposed as `[_]` for master review. It grants no accepted obligation, M0/E0,
`AUDIT-Z`, `THEOREM-Z`, release, or theorem-completion credit.
