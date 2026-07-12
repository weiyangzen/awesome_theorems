# THM-M-0525 validation-phase evidence

Item: `S56-M-0525-VALIDATION`. Base revision:
`79350f6756ac2f7d72136216ef446106f56a6fb9`.

The scoped runner rebuilt `Statement.lean` and `ObligationTree.lean` into a fresh temporary module
directory, then kernel-checked `Proof.lean` and an independently implemented `Validation.lean`.
The latter reconstructs the forward-concatenation group directly and imports neither `Proof` nor
`ObligationTree`. Both exact roots report only `propext`, `Classical.choice`, and `Quot.sound`.
The runner also checked forbidden tokens, the frozen denominator, the clean pinned mathlib revision,
and direct source/olean hashes for the quotient laws and `Group.ofLeftAxioms`.

## Commands and results

| Command | Exit | Result |
|---|---:|---|
| `python3 Stage1_Instances/THM-M-0525/check_validation.py` | 0 | Exact root, frozen composition, independent local reconstruction, axiom observation, direct provenance, and hygiene passed; release gates failed closed. |
| `python3 Docs/tools/check_stage1_standard.py` | 0 | `ok`: 15 assurance groups and 1546 uniform-L0 targets. |
| `python3 scripts/stage1_target.py check` | 0 | `ok`: 1546 unique targets, ranks 1..1546, all L0/rework-required. |
| `python3 scripts/stage1_target.py show THM-M-0525` | 0 | Rank 582, planned, legacy evidence unaccepted, theorem incomplete. |
| `python3 Stage1_Instances/THM-M-0525/check_obligation_tree.py` | 0 | 10 obligations and 38 typed edges; frozen pre-proof root remains open at M2. |
| `python3 -m json.tool Stage1_Instances/THM-M-0525/validation-spec.json >/dev/null` | 0 | Validation specification is valid JSON. |
| `python3 -m json.tool Stage1_Instances/THM-M-0525/validation-receipt.json >/dev/null` | 0 | Provisional receipt is valid JSON. |
| `git diff --check -- Stage1_Instances/THM-M-0525 .stage1-worker-selftest.json` | 0 | No whitespace errors. |

The runner used the existing canonical pinned `.lake` symlink without update, build, clone, fetch,
or dependency modification. Its temporary local oleans were deleted automatically.

## Fail-closed boundary

This is warm-cache, same-workspace, nonrelease worker evidence. The proof dependency is not master
accepted, and the frozen typed graph truthfully predates proof closure. There is no accepted
theorem-specific foundation/TCB policy, full transitive provenance or SBOM/license closure,
empty-cache network-denied cold build, offline restoration, distinct independently provisioned
runner, second signed attestation, or independent minimal release verifier. Human-source H0,
readability R0, AUDIT-Z, THEOREM-Z, release, and master acceptance remain open. Consequently this
phase claims neither accepted M0 nor theorem completion.
