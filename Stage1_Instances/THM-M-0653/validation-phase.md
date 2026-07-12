# THM-M-0653 validation-phase result

Item: `S56-M-0653-VALIDATION`  
Base revision: `6fb5d7698be077f0e9c0e01fac425d492ec114c8`  
Validation time: `2026-07-12T06:54:20Z`

The node-scoped validator elaborated the exact frozen statement, the frozen
identity boundary, the proof-phase elementary converse and conditional root
assembly, and a separately written direct reconstruction. `Validation.lean`
imports only `Statement`; it imports neither `Proof` nor `ObligationTree`.
This provides same-worker differential evidence, not rev-5.6 independent
verification.

## Exact result

```text
python3 Stage1_Instances/THM-M-0653/check_validation.py
  exit 0
  PASS narrow kernel replay: exact statement, frozen identity boundary, proof-phase converse, and same-worker direct reconstruction elaborated
  PASS trust observation: five declarations report only a subset of propext and Quot.sound
  PASS local provenance: statement, registry, proof receipt, clean mathlib pin, and dependency hashes agree
  OPEN exact root: no unconditional implicit-to-explicit Beth proof body exists (M0653-D-BETH)
  STALE frozen graph: M0653-D-CONVERSE remains open pending master reconciliation with proof evidence
  BLOCKED release gates: shared warm .lake, incomplete TCB/SBOM archive, and no distinct independent runner

python3 Docs/tools/check_stage1_standard.py
  exit 0: 15 assurance groups and 1546 uniform-L0 targets passed
python3 scripts/stage1_target.py check
  exit 0: 1546 unique targets, ranks 1..1546, all L0/rework_required
python3 scripts/stage1_target.py show THM-M-0653
  exit 0: rank 698, planned, theorem_complete false
python3 Stage1_Instances/THM-M-0653/check_obligation_tree.py
  exit 0: 14 obligations and 49 typed edges passed; frozen root remains open M3
```

The validator invoked narrow `lake env lean` commands in a fresh temporary
module directory under `Formalizations/Lean`, then removed it. It performed no
update, build, clone, fetch, network operation, or `.lake` mutation. The
mathlib worktree was clean at pinned revision
`8a178386ffc0f5fef0b77738bb5449d50efeea95`.

## Gate decisions

| Gate | Decision | Evidence or failure |
|---|---|---|
| Narrow kernel replay | pass | The exact statement and all claimed proof-phase declarations elaborate; the separate direct reconstruction agrees. |
| Placeholder/unsafe scan | pass | The four checked Lean modules contain no `sorry`, `admit`, `sorryAx`, local `axiom`, or `unsafe` declaration. |
| Trust observation | provisional pass | The five printed declarations use only a subset of `propext` and `Quot.sound`; no accepted complete foundation/TCB profile exists. |
| Local provenance | pass | Frozen hashes, proof receipt, clean mathlib revision, toolchain pin, and Lake manifest pin agree. |
| Exact root kernel closure | fail | The checked assembly explicitly assumes the implicit-to-explicit Beth direction; `M0653-D-BETH` has no proof body. |
| Structured state freshness | fail closed / stale | The pre-proof graph still lists `M0653-D-CONVERSE` as open; only the master may reconcile authoritative state. |
| Hermetic release replay | fail closed | Shared warm `.lake`; no clean checkout, empty-cache cold build, offline restoration, full TCB inventory, or SBOM/license archive. |
| Independent verification | fail closed | The separate implementation ran in this worker clone and shared cache; there is no distinct identity, runner, signature, or independent release verifier. |

The first failed theorem gate is `proof.root_kernel_closure`. The minimal
mathematical root cut is `M0653-D-BETH`, supported by the still-open two-copy,
compactness, interpolation, vocabulary, and formula-transport obligations.
This receipt grants no `E0/E1`, accepted `M0-*`, `AUDIT-Z`, `THEOREM-Z`,
release, or master-acceptance credit. `audit_complete=false` and
`theorem_complete=false`.
