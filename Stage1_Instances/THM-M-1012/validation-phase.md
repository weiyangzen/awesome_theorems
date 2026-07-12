# THM-M-1012 validation-phase result

Item: `S56-M-1012-VALIDATION`  
Base revision: `3699e5855e919efdcfc83019c12ef3b883b026f2`  
Validation time: `2026-07-12T02:03:46Z`

The node-scoped validator elaborated the exact frozen statement, obligation-tree composition,
proof root, and an independently implemented direct root proof in a fresh temporary module
directory. `Validation.lean` imports neither `Proof.lean` nor `ObligationTree.lean`; it inhabits the
canonical target directly from the pinned mathlib theorem. This is useful same-worker differential
evidence, not the distinct-runner independent attestation required for release.

## Exact result

```text
python3 Stage1_Instances/THM-M-1012/check_validation.py
  exit 0
  ok: exact statement, frozen composition, proof root, and independent direct root elaborated in a fresh temporary directory
  ok: checked root declarations report only propext, Classical.choice, and Quot.sound; placeholder and unsafe scans passed
  ok: statement, registry, graph, toolchain, dependency pin, and upstream proof-source provenance hashes passed
  stale: the pre-proof frozen graph still records an open M3 root; only the master may reconcile authoritative state
  blocked: cold empty-cache hermetic replay, full TCB/SBOM closure, and distinct-runner independent verification
```

The validator used `lake env lean` against existing pinned Lean 4.29.0 and mathlib revision
`8a178386ffc0f5fef0b77738bb5449d50efeea95`. It emitted temporary oleans only under a temporary
directory inside `Formalizations/Lean` and removed them. It performed no update, build, clone,
fetch, network operation, or dependency mutation.

## Gate decisions

| Gate | Decision | Evidence or failure |
|---|---|---|
| Narrow kernel replay | pass | Exact statement, child composition, proof root, and direct independent root elaborate in a fresh temporary directory. |
| Placeholder/unsafe scan | pass | No `sorry`, `admit`, local `axiom`, or `unsafe` declaration occurs in the four checked modules. |
| Axiom observation | provisional pass | Both proof paths report exactly `propext`, `Classical.choice`, and `Quot.sound`. No release-grade complete TCB profile is claimed. |
| Local provenance | pass | Frozen statement/registry/graph hashes, clean mathlib pin, and pinned upstream source hash agree. |
| Authoritative root state | pending master | The frozen graph predates the proof and truthfully retains its M3 open-root observation. Workers do not rewrite prior evidence. |
| Hermetic release replay | fail closed | Shared warm `.lake` artifacts were reused; there was no clean checkout, empty-cache cold build, offline restoration, SBOM/license closure, or complete executable/olean TCB inventory. |
| Independent verification | fail closed | The independent proof ran in this mutable worker clone with a shared dependency cache; no second identity, provisioned runner, signature, or independent release verifier exists. |

This is a truthful, self-tested validation-node handoff. It grants no `E0/E1`, accepted `M0-*`,
`AUDIT-Z`, `THEOREM-Z`, release, or master-acceptance credit. Primary-source `H0` and readable `R0`
also remain open, so `audit_complete=false` and `theorem_complete=false`.
