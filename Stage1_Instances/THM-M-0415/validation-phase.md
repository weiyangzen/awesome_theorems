# THM-M-0415 validation-phase result

Item `S56-M-0415-VALIDATION` was run against the integrated proof-phase
snapshot. Narrow kernel replay, placeholder scanning, input binding, recipe
coverage, and dependency-pin checks pass. The exact target, direct mathlib
wrapper, and frozen child-to-parent composition elaborate, and the inspected
declarations report `propext`, `Classical.choice`, and `Quot.sound`.

## Exact result

The validator ran from repository root on 2026-07-12:

```text
python3 Stage1_Instances/THM-M-0415/check_validation.py
  exit 0
  ok: exact target, direct wrapper, and frozen child-to-parent composition kernel-elaborated
  ok: checked declarations report only propext, Classical.choice, and Quot.sound
  ok: placeholder scan, input hashes, recipe coverage, and clean pinned mathlib checks passed
  stale: frozen graph still classifies the root M3 and has no proof evidence edges
  blocked: complete transitive TCB/provenance closure and H0/R0 review remain open
  blocked: cold empty-cache hermetic replay and distinct-runner independent verification remain open
```

The validator invokes `lake env lean` narrowly and copies the three Lean
modules into a fresh temporary directory under `Formalizations/Lean`. It emits
temporary `.olean` files only there and removes the directory. It verifies the
existing mathlib checkout is clean and pinned at
`8a178386ffc0f5fef0b77738bb5449d50efeea95`. No update, build, clone, fetch, or
dependency mutation was performed.

## Gate decisions

| Gate | Decision | Evidence or failure |
|---|---|---|
| Narrow kernel replay | pass | The exact statement, obligation composition, direct wrapper, and composition wrapper elaborate with pinned Lean 4.29.0/mathlib. |
| Placeholder and unsafe scan | pass | No `sorry`, `admit`, `sorryAx`, local `axiom`, or `unsafe` declaration occurs in the checked modules. |
| Axiom observation | provisional pass | The printed local and imported declarations expose `propext`, `Classical.choice`, and `Quot.sound`; no accepted full foundation/TCB profile exists. |
| Input and local provenance binding | pass with stale-state finding | Statement, registry, graph, proof, and proof-receipt hashes agree; all frozen obligations have recipes; pinned mathlib is clean. The graph still reports root `M3` and has no evidence edges. |
| Transitive trust/provenance closure | fail closed | No complete content-addressed declaration closure, imported compiled-artifact inventory, kernel/compiler/bootstrap provenance, or executable TCB inventory exists. |
| Human source and readability | fail closed | `M0415-X-SOURCE` has no accepted pinpoint H0 review, and required readable nodes have no independent R0 receipts. |
| Hermetic release replay | fail closed | The run reused shared writable warm `.lake` artifacts; there was no clean checkout, empty-cache cold build, offline restoration, full SBOM/license closure, or deterministic release archive. |
| Independent verification | fail closed | This is one worker in one mutable clone, without a distinct verifier identity, independently provisioned runner, second signature, second platform, or independently implemented verifier. |

This is a self-tested, truthful negative release-validation result. It grants
no release-grade `E0/E1`, accepted `M0-W`, `AUDIT-Z`, `THEOREM-Z`, release, or
master-acceptance credit. `audit_complete=false` and
`theorem_complete=false`.
