# THM-M-1019 validation-phase result

Item: `S56-M-1019-VALIDATION`  
Base revision: `c53c0bb271060b9242b5ef8982343feb5beecf40`  
Validation time: `2026-07-12T03:57:27Z`

The node-scoped validator replayed the exact frozen statement and proof root in a fresh temporary
module directory. It also elaborated `Validation.lean`, which imports `Statement` but deliberately
does not import `Proof` or consume the proof receipt. That second direct inhabitant is useful
same-workspace differential evidence, not the distinct-runner attestation required by rev-5.6.

## Exact result

```text
$ python3 Stage1_Instances/THM-M-1019/check_validation.py
ok: exact proof root and independently reconstructed frozen root kernel-replayed
ok: pinned clean mathlib provenance and observed classical axiom profile verified; no placeholders or unsafe declarations
stale: frozen architecture graph remains open M1 pending master reconciliation
blocked: cold empty-cache hermetic replay, complete transitive TCB/SBOM closure, and distinct-runner verification
exit 0
```

The validator used `lake env` only to locate the existing pinned Lean executable and `LEAN_PATH`,
then wrote temporary `Statement.olean` output beneath `Formalizations/Lean` and removed the entire
temporary directory. It performed no Lake update/build, clone, fetch, network operation, or `.lake`
mutation.

## Gate decisions

| Gate | Decision | Evidence or failure |
|---|---|---|
| Exact kernel replay | pass | Both `Proof.characteristicFunctionUniqueness` and `Validation.independentlyReconstructedRoot` inhabit the frozen `Statement`. |
| Placeholder and unsafe scan | pass | Comment-stripped local sources and the pinned terminal module contain no `sorry`, `admit`, `sorryAx`, local `axiom`, or `unsafe` declaration. |
| Observed axiom profile | provisional pass | Both root declarations report exactly `propext`, `Classical.choice`, and `Quot.sound`; a complete transitive TCB inventory is not claimed. |
| Local provenance | pass | Statement, proof, registry, graph, proof-receipt, toolchain, manifest, clean mathlib pin, terminal source, and terminal olean hashes agree with the receipt. |
| Proof dependency | pending master | `S56-M-1019-PROOF` has only provisional worker evidence in this clone. |
| Authoritative root state | pending master | The frozen architecture graph still reports no closed obligations, root `M1`, and cut set `M1019-X2`; workers do not rewrite prior phase authority. |
| Hermetic release replay | fail closed | Shared warm `.lake` artifacts were reused; there was no immutable clean checkout, empty-cache cold build, offline restoration, complete TCB/SBOM/license closure, or deterministic bundle. |
| Independent verification | fail closed | The direct probe ran in this mutable worker clone with the shared cache; there is no second identity, independently provisioned runner, signature, or independent minimal verifier. |

This is a truthful self-tested validation-node handoff. It grants no `E0/E1`, accepted `M0-W`,
`AUDIT-Z`, `THEOREM-Z`, theorem completion, release, or master-acceptance credit. Primary-source
`H0` and readable `R0` also remain open.
