# Intake validation

Base revision: `1c5adf59c0f8176526cb4c9fb281b3ff340c9eeb`.

This validation covers manifest membership, dossier structure, JSON integrity, and a narrow pinned
Lean API probe. Because the repository record does not identify one proposition, no canonical
target, expression hash, mutation result, forcing axiom, or proof is claimed. The pre-existing
canonical `.lake` link and artifacts were used read-only and were not modified.

| Command | Result |
|---|---|
| `python3 Docs/tools/check_stage1_standard.py` | exit 0; 15 assurance groups, 1546 uniform-L0 Lean 4 targets, execution skill present |
| `python3 scripts/stage1_target.py check` | exit 0; 1546 unique targets, ranks 1..1546, all L0/rework_required |
| `python3 scripts/stage1_target.py show THM-M-0795` | exit 0; rank 800, planned, legacy artifacts unaccepted, theorem_complete false |
| `python3 -m json.tool Stage1_Instances/THM-M-0795/instance.json` | exit 0; valid JSON |
| `python3 -m json.tool Stage1_Instances/THM-M-0795/task-dag.json` | exit 0; valid JSON |
| scoped Python intake assertions | exit 0; `intake invariant check: ok` |
| `(cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0795/IntakeProbe.lean)` | exit 0; seven generic encoding-ingredient checks elaborated under Lean 4.29.0 |
| `rg -n '\b(sorry\|admit)\b\|^[[:space:]]*axiom\b' Stage1_Instances/THM-M-0795 -g '*.lean'` | exit 1 as expected; no prohibited placeholder or axiom in the Lean probe |
| `git diff --check -- Stage1_Instances/THM-M-0795` | exit 0; no output |

Known downstream failures are intentionally open: exact source selection and independent review,
canonical statement elaboration and mutation tests, obligation and discovery freezes, formal-anchor
audit, proof, hermetic replay, and release acceptance. They prevent theorem completion but do not
invalidate a truthful `planned` intake.
