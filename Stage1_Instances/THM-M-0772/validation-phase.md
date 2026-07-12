# THM-M-0772 validation-phase result

Item: `S56-M-0772-VALIDATION`  
Base revision: `38aba87433173923511031e270f670c02d0351c6`  
Validation time: `2026-07-12T05:03:10Z`

The node-scoped validator elaborated the exact frozen statement, obligation-tree composition,
proof root, expanded root, and a separately implemented direct root in a fresh temporary directory.
`Validation.lean` imports neither dossier proof module nor obligation-tree module and does not invoke
`maxChain_spec`; it starts with the empty chain and uses the distinct `IsChain.exists_maxChain` API.
This is useful same-worker differential evidence, not release-grade independent attestation.

## Exact result

```text
python3 Stage1_Instances/THM-M-0772/check_validation.py
  exit 0
  ok: exact statement, frozen composition, proof root, expanded root, and independent direct root elaborated in a fresh temporary directory
  ok: checked declarations report only propext, Classical.choice, and Quot.sound; placeholder and unsafe scans passed
  ok: statement, registry, graph, proof receipt, toolchain, dependency pin, and upstream source provenance hashes passed
  stale: the pre-proof frozen graph retains an open M3 root and X-MATHLIB-BODY cut; only the master may reconcile authoritative state
  blocked: cold empty-cache hermetic replay, complete TCB/SBOM closure, and distinct-runner independent verification
```

The validator used `lake env lean` against existing pinned Lean 4.29.0 and mathlib revision
`8a178386ffc0f5fef0b77738bb5449d50efeea95`. It copied inputs into a fresh temporary directory under
`Formalizations/Lean`, emitted no persistent build artifact, and removed the directory. It performed
no update, build, clone, fetch, network operation, or dependency mutation.

## Gate decisions

| Gate | Decision | Evidence or failure |
|---|---|---|
| Narrow kernel replay | pass | Exact statement, conditional composition, proof root, expanded target, and direct independent root elaborate from fresh source copies. |
| Placeholder/unsafe scan | pass | No `sorry`, `admit`, `sorryAx`, local `axiom`, or `unsafe` declaration occurs in the four checked modules. |
| Axiom observation | provisional pass | Checked declarations print exactly `propext`, `Classical.choice`, and `Quot.sound`; no release-grade complete TCB profile is claimed. |
| Local provenance | pass | Frozen statement, registry, graph, proof-receipt, toolchain, manifest, clean mathlib pin, and upstream `Chain.lean` hashes agree. |
| Independent implementation probe | same-worker pass only | A distinct local source route uses `IsChain.exists_maxChain` without importing the dossier proof or invoking its terminal theorem. |
| Authoritative root state | pending master | The frozen graph predates the proof and truthfully retains its M3 root and imported-body cut observation. |
| Hermetic release replay | fail closed | Shared warm `.lake` artifacts were reused; there was no empty-cache cold build, offline restoration, SBOM/license closure, or complete executable/olean TCB inventory. |
| Independent verification | fail closed | Both routes ran in one mutable worker clone with one shared dependency cache; no second identity, provisioned runner, signature, or independent release verifier exists. |

This self-tested validation handoff grants no `E0/E1`, accepted `M0-*`, `AUDIT-Z`, `THEOREM-Z`,
release, or master-acceptance credit. Primary-source `H0` and readable `R0` remain open, so
`audit_complete=false` and `theorem_complete=false`.
