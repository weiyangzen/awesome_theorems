# THM-M-0329 validation-phase result

Item: `S56-M-0329-VALIDATION`  
Base revision: `bd0d227173ac95971603f633607751754850337e`  
Validation time: `2026-07-12T11:21:48Z`

The node-scoped validator elaborated the exact frozen statement, frozen
composition, both proof packages, the exact root, and a separately written
direct reconstruction. `Validation.lean` imports only `Statement` and the
pinned mathlib Lax-Milgram module; it imports neither `Proof` nor
`ObligationTree`. This is same-worker differential evidence, not rev-5.6
independent verification.

## Exact result

```text
python3 Stage1_Instances/THM-M-0329/check_validation.py
  exit 0
  PASS narrow kernel replay: exact statement, frozen composition, proof packages, and exact root elaborated
  PASS trust observation: five checked declarations report propext, Classical.choice, and Quot.sound
  PASS local provenance: statement, anchor, registry, graph, source, and clean pinned mathlib hashes agree
  PASS same-worker differential probe: exact root reconstructed without importing Proof or ObligationTree
  STALE frozen graph: root remains candidate/open pending master reconciliation with proof evidence
  BLOCKED release gates: shared warm .lake, incomplete transitive TCB/SBOM archive, and no distinct independent runner
```

The validator invoked narrow `lake env lean` commands in a fresh temporary
module directory under `Formalizations/Lean`, then removed it. It performed no
update, build, clone, fetch, network operation, or `.lake` mutation. The
mathlib worktree was clean at pinned revision
`8a178386ffc0f5fef0b77738bb5449d50efeea95`.

## Gate decisions

| Gate | Decision | Evidence or failure |
|---|---|---|
| Narrow kernel replay | pass | The exact statement, frozen child-to-root composition, proof packages, and exact root elaborate. |
| Placeholder/unsafe scan | pass | The four checked Lean modules contain no `sorry`, `admit`, `sorryAx`, local `axiom`, `unsafe`, or `proof_wanted`. |
| Trust observation | provisional pass | All five printed declarations use exactly `propext`, `Classical.choice`, and `Quot.sound`; no accepted complete foundation/TCB profile exists. |
| Local provenance | pass | Statement, anchor, registry, graph, source, clean mathlib revision, toolchain pin, and Lake manifest pin agree. |
| Same-worker differential check | pass with boundary | The direct proof does not import either proof-phase module, but it used this worker clone and shared cache. |
| Structured state freshness | fail closed / stale | The pre-acceptance graph remains `root_closed=false` and lists source, foundation, provenance, and workflow nodes in its first open cut. Only the master may reconcile it. |
| Hermetic release replay | fail closed | Shared warm `.lake`; no clean checkout, empty-cache cold build, offline restoration, full TCB inventory, or SBOM/license archive. |
| Independent verification | fail closed | There is no distinct identity, independently provisioned runner, second signed attestation, or independently implemented release verifier. |

The first failed release gate is `hermetic.cold_empty_cache`. This receipt
grants no `E0/E1`, accepted `M0-*`, `AUDIT-Z`, `THEOREM-Z`, release, or
master-acceptance credit. `audit_complete=false` and
`theorem_complete=false`.
