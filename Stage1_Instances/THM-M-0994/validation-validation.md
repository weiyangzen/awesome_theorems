# THM-M-0994 validation handoff

## Verdict boundary

Item `S56-M-0994-VALIDATION` is self-tested as provisional, nonrelease worker
evidence. The exact proof root kernel-elaborates, and `Validation.lean`
separately reconstructs the same frozen proposition without importing the
local proof or obligation-tree modules. Both routes use the pinned
`Mathlib.Probability.Moments.SubGaussian` declarations and report exactly
`propext`, `Classical.choice`, and `Quot.sound`.

This is not full hermetic or independent-runner validation. The proof
prerequisite has no master acceptance receipt here, the typed graph predates
proof closure, the canonical warm `.lake` cache was reused, and both probes ran
in this worker checkout. Therefore `audit_complete=false` and
`theorem_complete=false` remain mandatory.

## Commands and results

Commands ran from base revision
`11ec0ea4b441f1e6bc5580ca9a037509892e8c92` on 2026-07-12. No command ran
`lake update`, `lake build`, dependency clone/fetch, or a network operation,
and no command mutated `.lake`.

```text
$ cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0994/Proof.lean
exit 0; exact proof root reported propext, Classical.choice, and Quot.sound

$ cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0994/Validation.lean
exit 0; separately reconstructed exact root and both pinned terminal
declarations reported propext, Classical.choice, and Quot.sound

$ python3 Stage1_Instances/THM-M-0994/check_validation.py
exit 0; frozen hashes, recipes, statement/registry identity, placeholder
policy, clean pinned mathlib provenance, temporary-directory kernel replay,
axiom output, and fail-closed graph boundary passed

$ python3 Docs/tools/check_stage1_standard.py
exit 0; 15 assurance groups and 1546 uniform-L0 targets passed

$ python3 scripts/stage1_target.py check
exit 0; 1546 unique targets, ranks 1..1546, all L0/rework_required

$ python3 scripts/stage1_target.py show THM-M-0994
exit 0; rank 274, planned, theorem_complete=false

$ git diff --check -- Stage1_Instances/THM-M-0994 .stage1-worker-selftest.json
exit 0; no whitespace errors
```

## Failed gates

The first node gate failure is dependency acceptance: `S56-M-0994-PROOF`
has provisional evidence but no master receipt. The authoritative frozen graph
also still truthfully records its earlier open-root snapshot. Section 10.6
requires an immutable clean checkout, empty caches, network-denied cold build,
and offline restoration. Section 10.7 requires distinct verifier identities
and independently provisioned runners without shared writable caches.
Complete transitive provenance/TCB, SBOM/licenses, deterministic bundling,
H0/R0 reviews, release, and master acceptance remain open.
