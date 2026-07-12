# THM-M-1524 validation-phase result

Item: `S56-M-1524-VALIDATION`  
Base revision: `446447c65190dc818b074bf543171f807e9b4651`

The exact proof-phase components and root elaborate from fresh temporary local `.olean` files. A
separately authored module checks that the exported proof has the frozen exact target type. This is
useful local corroboration, but not rev-5.6 independent verification because both checks ran in this
worker clone against the same warm dependency cache.

## Exact validation

Run from the repository root on 2026-07-12. The validator invoked narrow `lake env lean` checks,
wrote target modules into a fresh temporary directory, and removed it. It did not update, build,
clone, fetch, or modify `.lake`.

```text
python3 Stage1_Instances/THM-M-1524/check_validation.py
  exit 0
  PASS narrow kernel replay: exact components, root proof, and exact-type probe elaborated
  PASS trust observation: four declarations report only propext, Classical.choice, and Quot.sound
  PASS local provenance: frozen hashes, clean pinned mathlib, toolchain, and manifest agree
  STALE authoritative graph: root remains open pending master reconciliation with proof evidence
  BLOCKED release gates: shared warm .lake, incomplete TCB/SBOM archive, and no distinct runner

python3 Docs/tools/check_stage1_standard.py
  exit 0: 15 assurance groups and 1546 uniform-L0 targets passed
python3 scripts/stage1_target.py check
  exit 0: 1546 unique targets, ranks 1..1546, all L0/rework_required
python3 scripts/stage1_target.py show THM-M-1524
  exit 0: rank 192, planned, theorem_complete false
python3 Stage1_Instances/THM-M-1524/check_proof.py
  exit 0: exact Robertson, CCR transport, and root composition elaborated
python3 Stage1_Instances/THM-M-1524/check_obligation_tree.py
  exit 0: 14 obligations and 29 typed edges passed; frozen root remains open (M2)
```

## Gate decisions

| Gate | Decision | Evidence or failure |
|---|---|---|
| Exact kernel replay | provisional pass | Exact components, root proof, and exact-type probe elaborate with pinned Lean 4.29.0 and mathlib `8a178386`. |
| Placeholder/unsafe scan | pass | Four Lean modules contain no `sorry`, `admit`, `sorryAx`, local `axiom`, or `unsafe` declaration. |
| Trust observation | provisional pass | All four proof/probe reports list exactly `propext`, `Classical.choice`, and `Quot.sound`; full release TCB closure is absent. |
| Local provenance | pass | Frozen hashes, clean dependency revision, toolchain pin, and Lake manifest pin agree. |
| Structured root state | fail closed / stale | `typed-graphs.json` remains `root_closed=false`; reconciliation is master-controlled. |
| Hermetic release replay | fail closed | Shared warm `.lake`; no cold empty-cache/offline restoration, full TCB inventory, or SBOM/license archive. |
| Independent verification | fail closed | Separate exact-type probe, but no distinct identity, independently provisioned runner, signature, or minimal receipt/graph verifier. |

This is genuinely self-tested validation-phase work, but grants no `E0/E1`, accepted `M0-*`,
`AUDIT-Z`, `THEOREM-Z`, release, or theorem-completion credit. `theorem_complete=false`.
