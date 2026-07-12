# THM-M-1521 validation-phase result

Item: `S56-M-1521-VALIDATION`  
Base revision: `e291daffd22e3ff6fc8031f413e88a1a41b1af26`

The narrow kernel, observed-axiom, and local provenance checks pass for the
exact proof-phase target. `Validation.lean` independently reconstructs the
direct mathlib proof without importing `Proof.lean` or `ObligationTree.lean`.
This is useful corroboration, but it is not rev-5.6 independent verification:
both proofs ran in the same worker clone and shared writable dependency cache.

## Exact validation

Run from the repository root on 2026-07-12. The validator invoked only narrow
`lake env lean` elaborations, wrote local modules to a fresh temporary cache,
and removed that cache. It did not run update, build, clone, or fetch and did
not modify `.lake`.

```text
python3 Stage1_Instances/THM-M-1521/check_validation.py
  exit 0
  PASS narrow kernel replay: exact proof and independent direct exact-target probe elaborated
  PASS trust observation: six checked declarations report only propext, Classical.choice, and Quot.sound
  PASS provenance: proof inputs, pinned clean mathlib revision, terminal source, and terminal olean hashes agree
  STALE authoritative graph: frozen proof cut remains open although the proof receipt proposes root closure
  BLOCKED release gates: warm shared cache, incomplete TCB/SBOM archive, and no distinct independently provisioned runner
```

## Gate decisions

| Gate | Decision | Evidence or failure |
|---|---|---|
| Exact kernel replay | provisional pass | The exact proof and a separately written direct proof elaborate against pinned Lean 4.29.0 and mathlib `8a178386`. |
| Placeholder/unsafe scan | pass | The four checked Lean modules contain no `sorry`, `admit`, `sorryAx`, local `axiom`, or `unsafe` declaration. |
| Trust observation | provisional pass | Five proof/import reports and one independent-probe report list exactly `propext`, `Classical.choice`, and `Quot.sound`; a complete release TCB closure is absent. |
| Local provenance | pass | Proof input hashes, clean dependency revision, terminal source hash, terminal olean hash, toolchain pin, and Lake manifest pin agree. |
| Structured root state | fail closed / stale | `proof-receipt.json` proposes root closure, but authoritative `typed-graphs.json` still has `root_closed=false` with both bridge nodes in its cut set. The worker does not reconcile master state. |
| Hermetic release replay | fail closed | This used shared warm `.lake`; there is no empty-cache cold checkout, offline restoration, complete executable/bootstrap TCB inventory, or SBOM/license archive. |
| Independent verification | fail closed | The direct proof is independently written, but there is no distinct identity, separately provisioned runner, second signature, or independent graph/receipt verifier. |

This result is genuinely self-tested validation-phase work, but it grants no
`E0/E1`, accepted `M0-*`, `AUDIT-Z`, `THEOREM-Z`, release, or theorem-completion
credit. `theorem_complete=false`; master state reconciliation, H0/R0 review,
hermetic replay, and genuinely independent verification remain required.
