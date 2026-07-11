# THM-M-0420 validation-phase result

Item `S56-M-0420-VALIDATION` was run against the integrated proof-phase snapshot. Narrow kernel
replay, placeholder scanning, input binding, recipe coverage, and dependency-pin checks pass. The
exact statement, conditional child-to-root composition, and local `M0420-N1` normalization proof
elaborate against pinned Lean 4.29.0/mathlib. Lean reports `propext`, `Classical.choice`, and
`Quot.sound` for the normalization proof.

## Exact result

The validator ran from the repository root on 2026-07-12:

```text
python3 Stage1_Instances/THM-M-0420/check_validation.py
  exit 0
  ok: exact statement, conditional composition, and M0420-N1 proof kernel-elaborated
  ok: M0420-N1 reports only propext, Classical.choice, and Quot.sound
  ok: placeholder scan, input hashes, recipe coverage, and clean pinned mathlib checks passed
  open: exact Hilbert class field root remains M3; construction and four property bodies are absent
  stale: frozen graph predates the proof phase and does not yet credit M0420-N1
  blocked: cold hermetic replay, complete TCB/provenance closure, and independent verification remain open
```

The validator copies the three Lean modules into a fresh temporary module tree under
`Formalizations/Lean`, invokes only `lake env lean`, and removes the tree afterward. It verifies
that the existing mathlib checkout is clean and pinned at
`8a178386ffc0f5fef0b77738bb5449d50efeea95`. No update, build, clone, fetch, network access, or
dependency mutation was performed.

## Gate decisions

| Gate | Decision | Evidence or failure |
|---|---|---|
| Narrow kernel replay | pass | `Statement.lean`, conditional `root_composition`, and `M0420-N1` elaborate in a fresh temporary module tree. |
| Placeholder and unsafe scan | pass | No `sorry`, `admit`, `sorryAx`, local `axiom`, or `unsafe` declaration occurs in the three checked modules. |
| Axiom observation | provisional pass | `M0420-N1` reports only `propext`, `Classical.choice`, and `Quot.sound`; no accepted complete foundation/TCB profile exists. |
| Input and local provenance binding | pass with stale-state finding | Source hashes, frozen registry denominator, structured recipe coverage, proof-phase record, and clean mathlib pin agree. The frozen graph predates the proof body and omits `M0420-N1` from closed obligations. |
| Exact root kernel closure | fail | `root_composition` requires five explicit premises. Construction and the four substantive Hilbert class field properties have no proof bodies; the root remains `M3`. |
| Transitive trust/provenance closure | fail closed | No complete content-addressed declaration closure, imported compiled-artifact inventory, kernel/compiler/bootstrap provenance, or executable TCB inventory exists. |
| Human source and readability | fail closed | There is no accepted primary-source H0 pinpoint crosswalk or independent R0 readable review. |
| Hermetic release replay | fail closed | The run reused shared writable warm `.lake` artifacts; there was no empty-cache cold build, offline restoration, complete SBOM/license closure, or deterministic release archive. |
| Independent verification | fail closed | This is one worker in one mutable clone, without a separately provisioned runner, distinct verifier identity, second signature/platform, or independently implemented verifier. |

This is a self-tested, truthful negative theorem-validation result. It grants no release-grade
`E0/E1`, accepted `M0-*`, `AUDIT-Z`, `THEOREM-Z`, release, or master-acceptance credit.
`audit_complete=false` and `theorem_complete=false`. The remaining root cut set is `M0420-C`,
`M0420-L1`, `M0420-L2`, `M0420-L3`, and `M0420-L4`; the first unavailable bridge remains
`M0420-X1`.
