# Intake validation

Base revision: `9b651a1d3f6c41876f66c5933991b6cbaceeb70d`.

This validation covers manifest membership, dossier structure, JSON integrity, and a narrow pinned
Lean API probe. Because the repository record does not identify one exact proposition, no canonical
target, expression hash, mutation result, or proof is claimed. The shared canonical `.lake` symlink
and its artifacts were used read-only; no update, build, fetch, or clone was run.

| Command | Result |
|---|---|
| `python3 Docs/tools/check_stage1_standard.py` | exit 0; 15 assurance groups, 1546 uniform-L0 Lean 4 targets, execution skill present |
| `python3 scripts/stage1_target.py check` | exit 0; 1546 unique targets, ranks 1..1546, all L0/rework_required |
| `python3 scripts/stage1_target.py show THM-M-0314` | exit 0; rank 816, planned, legacy artifacts unaccepted, theorem_complete false |
| `python3 -m json.tool Stage1_Instances/THM-M-0314/instance.json` | exit 0 |
| `python3 -m json.tool Stage1_Instances/THM-M-0314/task-dag.json` | exit 0 |
| scoped Python intake assertions | exit 0; `intake invariant check: ok` |
| `(cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0314/IntakeProbe.lean)` | exit 0; all five pinned compact-operator and eigenspace API checks elaborated under Lean 4.29.0 |
| `rg -n '\b(sorry\|admit)\b\|^[[:space:]]*axiom\b' Stage1_Instances/THM-M-0314 -g '*.lean'` | exit 1 as expected for no matches; no prohibited placeholder or axiom found |
| `git diff --check -- Stage1_Instances/THM-M-0314` | exit 0; no output |

Known downstream failures are intentionally open: primary source pinpoint and independent review,
canonical statement elaboration and mutation tests, obligation and discovery freezes, full formal-
anchor audit, proof/composition closure, hermetic replay, and release acceptance. They prevent
theorem completion but do not invalidate a truthful `planned` intake.
