# Intake validation

Base revision: `a2a2e84e3df5232fa66ec24239fb0ff8079add7c`.

This validation covers manifest membership, dossier structure, JSON integrity, and a narrow pinned
Lean API probe. Because the repository record does not identify a proposition, no canonical target,
expression hash, mutation result, or proof is claimed. The pre-existing shared canonical `.lake`
symlink was used read-only and was not modified.

| Command | Result |
|---|---|
| `python3 Docs/tools/check_stage1_standard.py` | exit 0; 15 assurance groups, 1546 uniform-L0 Lean 4 targets, execution skill present |
| `python3 scripts/stage1_target.py check` | exit 0; 1546 unique targets, ranks 1..1546, all L0/rework_required |
| `python3 scripts/stage1_target.py show THM-M-0688` | exit 0; rank 729, planned, legacy artifacts unaccepted, theorem_complete false |
| `python3 -m json.tool Stage1_Instances/THM-M-0688/instance.json` | exit 0 |
| `python3 -m json.tool Stage1_Instances/THM-M-0688/task-dag.json` | exit 0 |
| scoped Python intake assertions | exit 0; `intake invariant check: ok` |
| `(cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0688/IntakeProbe.lean)` | exit 0; all eight pinned ordinal-notation and Veblen API checks elaborated under Lean 4.29.0 |
| `git diff --check -- Stage1_Instances/THM-M-0688` | exit 0; no output |

Known downstream failures are intentionally open: exact source selection and independent review,
canonical statement elaboration and mutation tests, obligation and discovery freezes, formal-anchor
audit, proof, hermetic replay, and release acceptance. They prevent theorem completion but do not
invalidate a truthful `planned` intake.
