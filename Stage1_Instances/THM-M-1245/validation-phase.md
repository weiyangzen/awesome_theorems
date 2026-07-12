# THM-M-1245 validation-phase result

Item `S56-M-1245-VALIDATION` was run against the integrated proof-phase
snapshot. The exact frozen root kernel-replays both through `Proof.lean` and
through an independently written direct reconstruction that does not import
the proof or obligation-tree module. This is truthful nonrelease evidence,
not theorem completion.

## Exact result

The structured recipe was run from repository root on 2026-07-12:

```text
python3 Stage1_Instances/THM-M-1245/check_validation.py
  exit 0
  ok: exact proof root and independently reconstructed frozen root kernel-replayed
  ok: pinned clean mathlib terminal provenance and classical axiom profile verified; no placeholders
  blocked: proof master acceptance, authoritative graph freshness, cold hermetic replay, and distinct-runner gates remain open
```

The validator invokes the pinned Lean executable discovered with `lake env`
and copies all four Lean modules into a fresh temporary directory. It writes
temporary `.olean` files only there and removes the directory. It verifies
that the existing mathlib checkout is clean and pinned at
`8a178386ffc0f5fef0b77738bb5449d50efeea95`. It performs no update, build,
clone, fetch, or dependency mutation.

## Gate decisions

| Gate | Decision | Evidence or failure |
|---|---|---|
| Narrow kernel replay | pass | Statement, composition, exact proof root, and independent exact-root reconstruction elaborate against pinned Lean 4.29.0/mathlib. |
| Placeholder and unsafe scan | pass | No `sorry`, `admit`, `sorryAx`, local `axiom`, or `unsafe` declaration occurs in the checked modules. |
| Axiom observation | provisional pass | Both exact-root declarations report `propext`, `Classical.choice`, and `Quot.sound`; an accepted release foundation/TCB inventory is still absent. |
| Local provenance | provisional pass | The terminal source and compiled artifact are hashed, and the dependency checkout is clean at its declared pin. Full transitive body provenance remains open. |
| Exact root kernel closure | pass locally | `Stage1Instances.THM_M_1245.sobolevInequalityTarget_proof` and `Stage1Instances.THM_M_1245.Validation.independentlyReconstructedRoot` have the frozen target. |
| Structured-state freshness | fail closed | `typed-graphs.json` predates the proof body and still records `root_closed=false`, `M1`, and cut set `M1245-A-TERMINAL`; workers cannot reconcile it. |
| Dependency acceptance | fail closed | `S56-M-1245-PROOF` has provisional worker evidence but no master acceptance receipt. |
| Hermetic release replay | fail closed | Shared warm `.lake` artifacts were reused; there was no clean immutable checkout, empty-cache cold build, offline restoration, SBOM/license closure, or full TCB inventory. |
| Independent verification | fail closed | The second proof is independently written but ran in the same worker checkout and cache, without a distinct identity, provisioned runner, or signed attestation. |

The first node-specific failure is proof dependency master acceptance. The
first release-level failure is cold empty-cache hermetic replay. Consequently
`audit_complete=false`, `theorem_complete=false`, and the authoritative
machine debt remains `M1` pending master reconciliation.
