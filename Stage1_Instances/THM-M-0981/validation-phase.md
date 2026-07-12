# THM-M-0981 validation-phase result

Item: `S56-M-0981-VALIDATION`  
Base revision: `8f12ecb893ab86b5c559c53ff8e856de99bdd878`

The exact proof-phase target, frozen child-to-parent composition, and a separately written direct
reconstruction all elaborate. The probe imports only `Statement`, not `Proof` or
`ObligationTree`. This is useful local corroboration, but not rev-5.6 independent verification
because both checks ran in this worker clone against the same warm dependency cache.

## Exact validation

Run from repository root on 2026-07-12. The validator invoked narrow `lake env lean` checks, wrote
`.olean` files only into a fresh system temporary directory, and removed it. It did not update,
build, clone, fetch, or modify `.lake`.

```text
python3 Stage1_Instances/THM-M-0981/check_validation.py
  exit 0
  PASS narrow kernel replay: exact proof, frozen composition, and independent exact-target probe elaborated
  PASS trust observation: six declarations report only propext, Classical.choice, and Quot.sound
  PASS local provenance: frozen hashes, proof receipt, clean pinned mathlib, toolchain, and manifest agree
  STALE authoritative graph: root remains open pending master reconciliation with proof evidence
  BLOCKED release gates: shared warm .lake, incomplete TCB/SBOM archive, and no distinct runner
```

## Gate decisions

| Gate | Decision | Evidence or failure |
|---|---|---|
| Exact kernel replay | provisional pass | Exact proof, all three leaf packages, frozen composition, and separate direct proof elaborate with pinned Lean 4.29.0/mathlib `8a178386`. |
| Placeholder/unsafe scan | pass | Four Lean modules contain no `sorry`, `admit`, `sorryAx`, local `axiom`, or `unsafe` declaration. |
| Trust observation | provisional pass | Six reports list exactly `propext`, `Classical.choice`, and `Quot.sound`; full release TCB closure is absent. |
| Local provenance | pass | Frozen hashes, proof receipt, clean dependency revision, toolchain pin, and Lake manifest pin agree. |
| Structured root state | fail closed / stale | `typed-graphs.json` remains `root_closed=false`; reconciliation is master-controlled. |
| Hermetic release replay | fail closed | Shared warm `.lake`; no cold empty-cache/offline restoration, full TCB inventory, or SBOM/license archive. |
| Independent verification | fail closed | Separate implementation, but no distinct identity, independently provisioned runner, signature, or minimal receipt verifier. |

This is genuinely self-tested validation-phase work, but grants no `E0/E1`, accepted `M0-*`,
`AUDIT-Z`, `THEOREM-Z`, release, or theorem-completion credit. `theorem_complete=false`.
