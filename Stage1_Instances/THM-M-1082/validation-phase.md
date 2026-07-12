# THM-M-1082 validation-phase result

Item: `S56-M-1082-VALIDATION`  
Base revision: `3aea47164cf4c9348fbb584dff8a1197a30fca1e`  
Validation time: `2026-07-12T04:19:25Z`

The node-scoped validator elaborated the exact frozen statement, the three
registered composition declarations, the proof-phase root, and a separately
implemented direct root in a fresh temporary module directory. `Validation.lean`
imports neither `Proof.lean` nor `ObligationTree.lean`; it constructs the exact
target directly from the pinned mathlib definition. This is useful same-worker
differential evidence, not the distinct-runner attestation required by section
10.7.

## Exact result

```text
python3 Stage1_Instances/THM-M-1082/check_validation.py
  exit 0
  PASS THM-M-1082 validation: exact statement, composition, proof root, and direct probe elaborated
  PASS trust: checked roots report only propext, Classical.choice, and Quot.sound
  PASS provenance: frozen local hashes and clean pinned mathlib revision agree
  BLOCKED release gates: cold empty-cache hermetic replay and distinct-runner verification
```

The validator used `lake env lean` with existing pinned Lean 4.29.0 and mathlib
revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`. Temporary compiled output was
created only under an automatically removed `/tmp` directory. The worker ran no
update, build, clone, fetch, network operation, or dependency mutation.

## Gate decisions

| Gate | Decision | Evidence or failure |
|---|---|---|
| Narrow kernel replay | pass | Exact statement, frozen child composition, proof root, and direct root elaborate. |
| Placeholder/unsafe scan | pass | No `sorry`, `admit`, `sorryAx`, local `axiom`, or `unsafe` declaration occurs in checked source. |
| Axiom observation | provisional pass | Checked proof declarations report exactly `propext`, `Classical.choice`, and `Quot.sound`. |
| Local provenance | pass | Frozen source/record hashes and clean pinned mathlib revision agree. |
| Authoritative root state | pending master | Frozen graph predates the proof and truthfully retains M3; workers do not rewrite prior state. |
| Hermetic release replay | fail closed | Shared warm `.lake`; no clean checkout, empty-cache cold build, offline restoration, SBOM/license closure, or full TCB inventory. |
| Independent verification | fail closed | The direct proof ran in this worker clone with a shared cache; no second identity, provisioned runner, signature, or independent release verifier exists. |

This is a truthful, self-tested validation-node handoff. It grants no `E0/E1`,
accepted `M0-*`, `AUDIT-Z`, `THEOREM-Z`, release, or master-acceptance credit.
Primary-source `H0` and readable `R0` also remain open, so
`audit_complete=false` and `theorem_complete=false`.
