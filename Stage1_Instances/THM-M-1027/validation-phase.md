# THM-M-1027 validation-phase result

Item: `S56-M-1027-VALIDATION`. Base revision:
`d063bd42d94a2decb5765a8c856f97975ab4f0a8`.

The frozen statement, obligation composition, proof-phase local bodies, and a separately written
conditional reconstruction elaborate against pinned Lean 4.29.0 and mathlib. The independent probe
imports `ObligationTree`, not `Proof`, and reconstructs the component-to-target adapter directly.
Lean reports only `propext`, `Classical.choice`, and `Quot.sound` for the checked composition
declarations. No placeholder, local axiom, or unsafe declaration was found.

## Exact validation

Commands ran from the repository root on 2026-07-12. The validator copied four modules into a fresh
temporary directory under `Formalizations/Lean`, invoked only narrow `lake env lean` elaboration,
and removed the directory. It did not update, build, clone, fetch, or modify `.lake`.

```text
python3 Stage1_Instances/THM-M-1027/check_validation.py
  exit 0
  ok: statement, local proof bodies, and independent conditional reconstruction elaborated in a fresh temporary module directory
  ok: checked composition declarations report only propext, Classical.choice, and Quot.sound
  ok: placeholder scan, proof-receipt hashes, frozen denominator, and clean pinned mathlib checks passed
  open: exact root still requires M1027-X-EXTERNAL; frozen graph predates proof-phase leaf closure
  blocked: cold empty-cache hermetic replay, complete TCB/SBOM closure, and distinct-runner independent verification
```

## Gate decisions

| Gate | Decision | Evidence or failure |
|---|---|---|
| Narrow kernel replay | pass | Frozen statement, conditional composition, local proof bodies, and separate reconstruction elaborate. |
| Placeholder/unsafe scan | pass | No `sorry`, `admit`, `sorryAx`, local `axiom`, or `unsafe` declaration in the four modules. |
| Trust observation | provisional pass | Composition declarations report exactly `propext`, `Classical.choice`, and `Quot.sound`; complete release TCB closure is absent. |
| Local provenance | pass | Proof-receipt source hashes, frozen denominator, clean mathlib tree, manifest pin, and toolchain agree. |
| Exact root kernel closure | fail closed | `M1027-X-EXTERNAL` is absent from the local Lake closure; both root adapters remain conditional. |
| Structured state freshness | fail closed | The frozen graph predates proof closure and reports the coarser `M1027-T-PACKAGE` cut; master reconciliation is required. |
| Hermetic release replay | fail closed | Shared warm `.lake`; no empty-cache cold build, offline restore, complete TCB inventory, or SBOM archive. |
| Independent verification | fail closed | Separate implementation, but no distinct runner, identity, signature, or independently provisioned cache. |

This is genuinely self-tested validation-phase work but grants no `E0/E1`, accepted `M0-*`,
`AUDIT-Z`, `THEOREM-Z`, release, or theorem-completion credit. `audit_complete=false` and
`theorem_complete=false`.
