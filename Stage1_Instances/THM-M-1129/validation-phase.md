# THM-M-1129 validation-phase result

Item: `S56-M-1129-VALIDATION`. Validation date: 2026-07-12. Base revision:
`767bcb5c33375def04fc8f536c5a5e3f27c31aa0`.

## Gate result

The node-scoped kernel replay passes for the exact statement, the conditional root composition,
and the four local boundary proof bodies. The source fingerprints, frozen registry denominator,
proof-receipt provenance hashes, prohibited-device scan, pinned mathlib revision, and mathlib
cleanliness check also pass. The local proof bodies expose only `propext`, `Classical.choice`, and
`Quot.sound`, consistent with the dossier's declared classical mathlib foundation profile.

This does not validate the theorem root. `poissonFormulaTarget_of_analyticPackage` consumes the
entire open `PoissonAnalyticPackage` as a premise, and none of the four boundary lemmas supplies the
singular-integral, PDE, initial-limit, representation, or uniqueness proof. Consequently the exact
root remains `M3`, `M1129-T-REPRESENT` remains the first open root cut, and theorem completion is
false.

The release-grade hermetic and independent-verification gates were evaluated and fail closed. This
worker reused the canonical pinned, writable, warm `.lake` cache rather than restoring dependencies
into a new empty-cache network-denied environment. It has no complete TCB/SBOM/license archive,
second independently provisioned runner, distinct verifier identity, second attestation, or
independently implemented minimal verifier. A second invocation in this clone would not be
independent evidence.

## Commands and results

```text
python3 Stage1_Instances/THM-M-1129/check_validation.py
  exit 0: fresh-directory elaboration, trust/profile, provenance/hash, denominator,
  placeholder, pin, and open-root checks passed; hermetic and independent gates reported blocked

python3 Docs/tools/check_stage1_standard.py
  exit 0: 15 assurance groups and 1546 uniform-L0 targets passed

python3 scripts/stage1_target.py check
  exit 0: 1546 unique targets, ranks 1..1546, all L0/rework_required

python3 scripts/stage1_target.py show THM-M-1129
  exit 0: rank 334, planned, theorem_complete=false

python3 -m json.tool Stage1_Instances/THM-M-1129/validation-spec.json
python3 -m json.tool Stage1_Instances/THM-M-1129/validation-receipt.json
  exit 0: both structured artifacts are valid JSON

git diff --check -- Stage1_Instances/THM-M-1129 .stage1-worker-selftest.json
  exit 0: no scoped whitespace errors
```

The run used no network and did not run `lake update`, `lake build`, dependency clone/fetch, or any
command that mutates `.lake`. This is provisional worker evidence for a truthful partial validation
result, not `E0/E1`, `M0`, independent verification, release, master acceptance, or theorem
completion.
