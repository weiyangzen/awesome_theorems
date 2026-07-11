# THM-M-0404 validation-phase result

Item `S56-M-0404-VALIDATION` was run against the integrated proof-phase
snapshot. The narrow kernel, placeholder, dependency-pin, and local source
provenance checks pass for the exact statement, conditional composition, and
combinatorial proof. This does not close Skolem-Mahler-Lech: the theorem
`root_of_eventuallyPeriodicZeroSets` still takes
`EventuallyPeriodicZeroSets` as an explicit premise.

## Exact result

The structured recipe in `validation-spec.json` was run from repository root
on 2026-07-12:

```text
python3 Stage1_Instances/THM-M-0404/check_validation.py
  exit 0
  ok: pinned statement, conditional composition, and combinatorial proof elaborated in a fresh temporary module directory
  ok: checked declarations report only propext, Classical.choice, and Quot.sound
  ok: placeholder scan, statement fingerprint, registry denominator, and clean pinned mathlib checks passed
  open: exact root has an explicit EventuallyPeriodicZeroSets premise (M0404-T-EVENTUAL)
  stale: frozen graph still reports M0404-L-COMBINATORIAL open despite the proof-phase body
  blocked: cold hermetic replay, complete TCB/SBOM closure, and distinct-runner independent verification
```

The validator invokes `lake env lean` narrowly and copies the three Lean
modules into a fresh temporary directory under `Formalizations/Lean`. It emits
temporary `.olean` files only there and removes the directory. It verifies the
existing mathlib checkout is clean and pinned at
`8a178386ffc0f5fef0b77738bb5449d50efeea95`. No update, build, clone, fetch, or
dependency mutation is performed.

## Gate decisions

| Gate | Decision | Evidence or failure |
|---|---|---|
| Narrow kernel replay | pass | `Statement.lean`, `ObligationTree.lean`, and `Proof.lean` elaborate against pinned Lean 4.29.0/mathlib. |
| Placeholder and unsafe scan | pass | No `sorry`, `admit`, local `axiom`, or `unsafe` declaration occurs in the three checked modules. |
| Axiom observation | provisional pass | The printed composition and proof declarations use `propext`, `Classical.choice`, and `Quot.sound`; no accepted release foundation/TCB profile exists. |
| Local provenance | pass with stale-state finding | Statement and frozen-registry hashes agree, the dependency pin is clean, and source is checked directly. The frozen graph predates the proof body and still calls `M0404-L-COMBINATORIAL` open. |
| Exact root kernel closure | fail | `root_of_eventuallyPeriodicZeroSets` is conditional on the unproved number-theoretic package `EventuallyPeriodicZeroSets`, corresponding to `M0404-T-EVENTUAL`. |
| Hermetic release replay | fail closed | The run reused shared writable warm `.lake` artifacts; there was no clean checkout, empty-cache cold build, offline restoration, SBOM/license closure, or full executable/olean TCB inventory. |
| Independent verification | fail closed | This is one worker and one mutable clone, without a second identity, independently provisioned runner, second signed attestation, or independently implemented verifier. |

This is a self-tested, truthful negative theorem-validation result. It grants
no `E0/E1`, `M0-*`, `AUDIT-Z`, `THEOREM-Z`, release, or master-acceptance
credit. `theorem_complete=false`; after structured state reconciliation, the
mathematical root cut is at least `M0404-T-EVENTUAL`.
