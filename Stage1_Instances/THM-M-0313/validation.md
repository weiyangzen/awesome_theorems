# Intake validation

Base revision: `9b651a1d3f6c41876f66c5933991b6cbaceeb70d`.

This validation covers manifest membership, dossier structure, JSON integrity, and a narrow pinned
Lean API probe. Because the source record does not determine an exact proposition, no canonical
target, expression hash, mutation result, or proof is claimed. The pre-existing shared `.lake`
artifact was used read-only and was not modified by the validation.

| Command | Result |
|---|---|
| `python3 Docs/tools/check_stage1_standard.py` | exit 0; 15 assurance groups, 1546 uniform-L0 Lean 4 targets, execution skill present |
| `python3 scripts/stage1_target.py check` | exit 0; 1546 unique targets, ranks 1..1546, all L0/rework_required |
| `python3 scripts/stage1_target.py show THM-M-0313` | exit 0; rank 815, planned, legacy artifacts unaccepted, theorem_complete false |
| `python3 -m json.tool Stage1_Instances/THM-M-0313/instance.json` | exit 0 |
| `python3 -m json.tool Stage1_Instances/THM-M-0313/task-dag.json` | exit 0 |
| scoped Python intake assertions | exit 0; `intake invariant check: ok` |
| `(cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0313/IntakeProbe.lean)` | exit 0; all six pinned operator/CFC API checks elaborated under Lean 4.29.0 |
| `git diff --check -- Stage1_Instances/THM-M-0313` | exit 0; no output |

Known downstream work is intentionally open: pinpoint source selection and independent review,
canonical statement elaboration and mutation tests, discovery and obligation freezes, formal-anchor
audit, proof, hermetic replay, and release acceptance. These prevent theorem completion but do not
invalidate a truthful `planned` intake.
