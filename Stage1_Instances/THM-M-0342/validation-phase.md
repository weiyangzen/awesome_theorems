# THM-M-0342 validation-phase result

Item: `S56-M-0342-VALIDATION`  
Base revision: `7780ee2963f599a6bf06f39a12c6fddb7eafc914`  
Validation time: `2026-07-12T12:02:01Z`

The node-scoped validator elaborated the exact frozen statement, proof-phase
anchor, checked root composition, and a separately written direct proof.
`Validation.lean` imports only `Statement`; it imports neither `Proof` nor
`ObligationTree`. This is same-worker differential evidence, not rev-5.6
independent verification.

## Exact result

```text
python3 Stage1_Instances/THM-M-0342/check_validation.py
  exit 0
  PASS narrow kernel replay: exact statement, proof-phase anchor and composition, and same-worker direct reconstruction elaborated
  PASS trust observation: checked declarations use only propext, Classical.choice, and Quot.sound
  PASS local provenance: statement, registry, proof receipt, clean mathlib pin, and dependency hashes agree
  STALE frozen graph: root remains open M2 pending master reconciliation with proof evidence
  BLOCKED release gates: shared warm .lake, incomplete TCB/SBOM archive, and no distinct independent runner
```

The validator invoked narrow `lake env lean` commands in a fresh temporary
module directory under `Formalizations/Lean`, then removed it. It performed no
update, build, clone, fetch, network operation, or `.lake` mutation. The
mathlib worktree was clean at pinned revision
`8a178386ffc0f5fef0b77738bb5449d50efeea95`.

Additional repository checks run after the receipt was created:

```text
python3 Docs/tools/check_stage1_standard.py
  exit 0: 15 assurance groups and 1546 uniform-L0 targets passed
python3 scripts/stage1_target.py check
  exit 0: 1546 unique targets, ranks 1..1546, all L0/rework_required
python3 scripts/stage1_target.py show THM-M-0342
  exit 0: rank 835, planned, theorem_complete false
python3 Stage1_Instances/THM-M-0342/check_obligation_tree.py
  exit 0: 15 obligations and typed graph checks passed; frozen root remains open M2
```

## Gate decisions

| Gate | Decision | Evidence or failure |
|---|---|---|
| Narrow kernel replay | pass | Exact statement, imported proof body, composition, and direct reconstruction elaborate. |
| Placeholder/unsafe scan | pass | Checked modules contain no `sorry`, `admit`, `sorryAx`, local `axiom`, or `unsafe` declaration. |
| Trust observation | provisional pass | Printed declarations use only `propext`, `Classical.choice`, and `Quot.sound`; no accepted complete foundation/TCB profile exists. |
| Local provenance | pass | Frozen hashes, proof receipt, clean mathlib revision, toolchain pin, and Lake manifest pin agree. |
| Exact root kernel closure | provisional pass | Both the proof-phase composition and separate direct proof close the exact frozen target. Master acceptance remains pending. |
| Structured state freshness | fail closed / stale | The pre-proof graph still calls the exact root open at M2; only the master may reconcile authoritative state. |
| Hermetic release replay | fail closed | Shared warm `.lake`; no clean checkout, empty-cache cold build, offline restoration, full TCB inventory, or SBOM/license archive. |
| Independent verification | fail closed | Separate code ran in the same worker clone and cache; there is no distinct identity, runner, signature, or independent release verifier. |

The first failed validation gate is
`validation.hermetic_cold_offline_replay`. This receipt grants no `E0/E1`,
accepted `M0-*`, `AUDIT-Z`, `THEOREM-Z`, release, or master-acceptance credit.
`audit_complete=false` and `theorem_complete=false`.
