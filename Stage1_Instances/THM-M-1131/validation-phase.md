# THM-M-1131 validation-phase result

Item: `S56-M-1131-VALIDATION`  
Base revision: `331f3394ba689a537bffbf8764a780c63caecd72`  
Validation time: `2026-07-12T02:37:39Z`

The node-scoped validator elaborated the exact frozen statement, obligation-tree composition,
proof root, and an independently implemented direct root proof in a fresh temporary module
directory. `Validation.lean` imports neither `Proof.lean` nor `ObligationTree.lean`. This is useful
same-worker differential evidence, not the distinct-runner independent attestation required for
release.

## Exact result

```text
python3 Stage1_Instances/THM-M-1131/check_validation.py
  exit 0
  ok: exact statement, frozen composition, proof root, and independent direct root elaborated in a fresh temporary directory
  ok: both root paths report only propext, Classical.choice, and Quot.sound; placeholder and unsafe scans passed
  ok: frozen hashes, toolchain, mathlib pin, clean dependency checkout, and terminal source provenance passed
  stale: the pre-proof typed graph retains its open M3 root pending master reconciliation
  blocked: cold empty-cache hermetic replay, complete TCB/SBOM closure, and distinct-runner independent verification
```

The validator used `lake env lean` against existing pinned Lean 4.29.0 and mathlib revision
`8a178386ffc0f5fef0b77738bb5449d50efeea95`. It emitted temporary oleans only in a temporary
directory under `Formalizations/Lean` and removed them. It performed no update, build, clone,
fetch, network operation, or dependency mutation.

## Gate decisions

| Gate | Decision | Evidence or failure |
|---|---|---|
| Narrow kernel replay | pass | Exact statement, composition, proof root, and direct independent root elaborate freshly. |
| Placeholder/unsafe scan | pass | No `sorry`, `admit`, local `axiom`, or `unsafe` declaration occurs in the checked modules. |
| Axiom observation | provisional pass | Both roots report exactly `propext`, `Classical.choice`, and `Quot.sound`. |
| Local provenance | pass | Frozen hashes, clean pinned mathlib revision, source digest, and olean digest agree. |
| Authoritative root state | pending master | The frozen graph predates proof closure and truthfully retains its M3 observation. |
| Hermetic release replay | fail closed | No clean checkout, empty-cache cold build, offline restoration, SBOM, or complete TCB inventory ran. |
| Independent verification | fail closed | Both paths ran in this mutable worker clone with the shared dependency cache. |

This self-tested validation-node handoff grants no `E0/E1`, accepted `M0-*`, `AUDIT-Z`,
`THEOREM-Z`, release, or master-acceptance credit. Human-source `H0` and readable `R0` remain open;
therefore `audit_complete=false` and `theorem_complete=false`.
