# THM-M-0389 validation-phase record

Item: `S56-M-0389-VALIDATION`  
Base revision: `374a6d495a9b67371555ac2a97fd91a775e7cefe`  
Validation time: `2026-07-11T20:06:39Z`

## Result and boundary

The proof-phase declaration `Stage1Instances.THM_M_0389.integerMarkovClassification`
was re-elaborated against the pinned Lean 4.29.0/mathlib environment. The
validation suffix independently spells the full root expression, checks its
definitional identity with the frozen target, and checks that the proof theorem
inhabits it. Both axiom reports contain exactly `propext`, `Classical.choice`,
and `Quot.sound`; no `sorryAx` is present. The fail-closed verifier also binds
the statement, proof, frozen 16-node registry, typed graphs, proof-unit manifest,
toolchain, and Lake manifest by SHA-256 and rejects local `sorry`, `admit`,
bodyless `axiom`, or `unsafe` declarations.

This is a successful worker self-test of warm-cache kernel, exact-type,
provenance-location, and local trust-hygiene evidence. It is not release-grade
hermetic or independent validation. The prerequisite proof node has not been
master-accepted and `proof-units.json` retains stale pre-proof debt labels. The
run reused the canonical pinned `.lake` symlink and the probe reused this
checkout and proof body. No empty-cache network-denied rebuild, offline archive
restoration, distinct signed runner, independently implemented release verifier,
full transitive TCB/SBOM/license closure, H0/R0 review, or deterministic release
bundle exists. Therefore `audit_complete=false` and `theorem_complete=false`.

First failed node gate: proof dependency master acceptance and structured-state
reconciliation. First failed release gate: rev-5.6 section 10.6 hermetic cold
build. Retry only after proof acceptance/reconciliation, then use an immutable
empty-cache runner with outbound network denied and a distinct signed verifier.

## Commands and exact results

All commands ran inside this worker clone. No update, build, clone, fetch, or
other `.lake` mutation was performed.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 targets |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all L0/rework-required |
| `python3 scripts/stage1_target.py show THM-M-0389` | 0 | rank 20, planned, L0/rework-required, theorem incomplete |
| `cd Formalizations/Lean && lake env lean -R ../../Stage1_Instances/THM-M-0389 ../../Stage1_Instances/THM-M-0389/Proof.lean` | 0 | root depends on `[propext, Classical.choice, Quot.sound]` |
| `python3 Stage1_Instances/THM-M-0389/check_validation.py --probe-only` | 0 | independently spelled root is definitionally exact and inhabited |
| `python3 Stage1_Instances/THM-M-0389/check_validation.py` | 0 | frozen hashes/graph, exact root/probe, axiom profile, and local hygiene passed |
| `python3 -m json.tool Stage1_Instances/THM-M-0389/validation-specs.json` | 0 | structured recipes parse |
| `python3 -m json.tool Stage1_Instances/THM-M-0389/validation-receipt.json` | 0 | provisional receipt parses |
| scoped prohibited-token scan of four Lean sources | 1 | empty output; pass (ripgrep no-match exit) |
| `git diff --check -- Stage1_Instances/THM-M-0389 .stage1-worker-selftest.json` | 0 | no whitespace errors |
