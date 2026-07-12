# THM-M-0993 validation handoff

## Verdict boundary

Item `S56-M-0993-VALIDATION` is self-tested as provisional, nonrelease worker
evidence. The exact proof root and frozen composition kernel-elaborate, and
`Validation.lean` independently reconstructs the same frozen proposition
without importing `Proof.lean` or `ObligationTree.lean`. Both routes compose
the same three declarations from pinned `Mathlib.Probability.Moments.Basic`
and report exactly `propext`, `Classical.choice`, and `Quot.sound`.

This does not satisfy the full validation or release gate. The proof
prerequisite has no master acceptance receipt here, and the authoritative
typed graph predates proof closure. The worker reused the warm canonical
`.lake` cache, and the independent probe shares this checkout and cache.
Consequently `audit_complete=false` and `theorem_complete=false` remain
mandatory.

## Commands and results

Commands ran from base revision
`36a2c698e6cc9758311ad1c10ecc9d229f7ce613` on 2026-07-12. No command ran
`lake update`, `lake build`, a dependency clone/fetch, or a network operation,
and no command mutated `.lake`.

```text
$ cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0993/Proof.lean
exit 0; all five local proof declarations reported exactly propext,
Classical.choice, and Quot.sound

$ cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0993/Validation.lean
exit 0; the independently reconstructed exact root and all three pinned
terminal declarations reported exactly propext, Classical.choice, and
Quot.sound

$ python3 Stage1_Instances/THM-M-0993/check_validation.py
exit 0; frozen input hashes, recipe policy, statement/registry identity,
placeholder policy, pinned clean mathlib provenance, isolated temporary kernel
replay, exact axiom output, and fail-closed graph boundary passed

$ python3 Docs/tools/check_stage1_standard.py
exit 0; 15 assurance groups and 1546 uniform-L0 targets passed

$ python3 scripts/stage1_target.py check
exit 0; 1546 unique targets, ranks 1..1546, all L0/rework_required

$ python3 scripts/stage1_target.py show THM-M-0993
exit 0; rank 273, planned, theorem_complete=false

$ git diff --check -- Stage1_Instances/THM-M-0993 .stage1-worker-selftest.json
exit 0; no whitespace errors
```

## Failed gates

The first node gate failure is dependency acceptance:
`S56-M-0993-PROOF` has provisional worker evidence but no master receipt, and
`typed-graphs.json` still truthfully records its earlier open-root snapshot.
Release section 10.6 also requires a clean immutable checkout, empty caches,
network-denied cold build, and offline restoration. Section 10.7 requires
distinct verifier identities and separately provisioned runners without shared
writable caches. Complete transitive provenance/TCB, SBOM/licenses,
deterministic bundling, H0/R0 reviews, and master acceptance remain open.
