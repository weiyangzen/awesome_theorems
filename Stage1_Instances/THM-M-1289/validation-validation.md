# THM-M-1289 validation handoff

Item `S56-M-1289-VALIDATION` was self-tested as provisional, nonrelease worker evidence at base
revision `aaeade67ccb391b2d10e50e766d54427324b3090`. The validator replayed the exact statement, frozen
conditional composition, and the local positivity and smoothness bodies in a fresh temporary module
directory using only the existing pinned Lean artifacts. The checked declarations reported exactly
`propext`, `Classical.choice`, and `Quot.sound`; source scans found no `sorry`, `admit`, `sorryAx`,
`axiom`, or `unsafe` proof mechanism. Pinned mathlib was clean at
`8a178386ffc0f5fef0b77738bb5449d50efeea95`.

## Verdict boundary

The exact root remains open. `aubinTalentiTarget_of_remaining_components` still requires the
critical PDE, function-norm finiteness, gradient-norm finiteness, and sharp-extremal components.
The frozen graph also predates the proof bodies and still lists positivity and smoothness as open.
Consequently `audit_complete=false` and `theorem_complete=false`. This warm shared-cache run is not
the cold hermetic protocol, and no independently implemented or distinctly provisioned verifier was
available. The first failed node gate is `exact_root.kernel_closure`.

## Commands and results

Commands ran on 2026-07-12. No command ran `lake update`, `lake build`, dependency clone/fetch, or a
network operation, and no command intentionally mutated `.lake`.

```text
$ python3 Stage1_Instances/THM-M-1289/check_validation.py
exit 0; exact statement, conditional composition, positivity, and smoothness replayed;
classical axiom profile, placeholder policy, frozen hashes, denominator, pins, and clean
mathlib passed; open root, stale graph, hermetic, and independent gates reported fail-closed

$ python3 Docs/tools/check_stage1_standard.py
exit 0; 15 assurance groups and 1546 uniform-L0 targets passed

$ python3 scripts/stage1_target.py check
exit 0; 1546 unique targets, ranks 1..1546, all L0/rework_required

$ python3 scripts/stage1_target.py show THM-M-1289
exit 0; rank 460, planned lifecycle, theorem_complete=false

$ cd Formalizations/Lean && lake env lean --version
exit 0; Lean 4.29.0, commit 98dc76e3c0a9b856c9b98726b713fb04fab16740

$ git diff --check -- Stage1_Instances/THM-M-1289 .stage1-worker-selftest.json
exit 0; no whitespace errors
```

## Retry condition

Prove the four remaining exact analytic components and have the master reconcile authoritative typed
state. A later release validation must use immutable clean inputs, empty caches, network-denied
offline restoration, a complete transitive TCB/SBOM/license packet, and a distinct independently
provisioned verifier.
