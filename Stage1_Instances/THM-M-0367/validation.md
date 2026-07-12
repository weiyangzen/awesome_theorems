# Intake validation

Base revision: `ded29702119d0d4880db9fcf1d0a6560a89058fd`.

This validation covers manifest membership, dossier structure, JSON integrity, and a narrow pinned
Lean API probe. Since the source record does not identify a proposition, no canonical target,
expression hash, mutation result, candidate theorem, or proof is claimed. The canonical `.lake`
symlink and pinned packages were used read-only and were not modified.

| Command | Result |
|---|---|
| `python3 Docs/tools/check_stage1_standard.py` | exit 0; 15 assurance groups, 1546 uniform-L0 Lean 4 targets, execution skill present |
| `python3 scripts/stage1_target.py check` | exit 0; 1546 unique targets, ranks 1..1546, all L0/rework_required |
| `python3 scripts/stage1_target.py show THM-M-0367` | exit 0; rank 859, planned, legacy artifacts unaccepted, theorem_complete false |
| `python3 -m json.tool Stage1_Instances/THM-M-0367/instance.json` | exit 0 |
| `python3 -m json.tool Stage1_Instances/THM-M-0367/task-dag.json` | exit 0 |
| scoped Python intake assertions | exit 0; `intake invariant check: ok` |
| `(cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0367/IntakeProbe.lean)` | exit 0; all four generic API types elaborated under Lean 4.29.0 |
| `git diff --check -- Stage1_Instances/THM-M-0367` | exit 0; no output |

Known downstream failures are intentionally open: target correction and exact primary-source
selection, independent source review, canonical statement elaboration and mutation tests,
obligation/discovery freezes, formal-anchor audit, proof, hermetic replay, and release acceptance.
They prevent theorem completion but do not invalidate a truthful `planned` intake.
