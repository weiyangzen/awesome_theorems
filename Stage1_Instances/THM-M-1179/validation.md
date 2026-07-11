# Intake validation record

Base revision: `8e78e1b4206fc224e91466efb397811c09205b0e`.

This validation covers manifest consistency and the planned dossier only. Because the repository
label does not specify a proposition, no Lean declaration was introduced and no kernel result is
claimed.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups and 1546 uniform-L0 Lean 4 targets; execution skill present |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1..1546, all L0/rework-required |
| `python3 scripts/stage1_target.py show THM-M-1179` | 0 | rank 379, planned, L0/rework-required, theorem incomplete |
| `python3 -m json.tool Stage1_Instances/THM-M-1179/intake.json >/dev/null` | 0 | valid JSON |
| `python3 -m json.tool Stage1_Instances/THM-M-1179/task-dag.json >/dev/null` | 0 | valid JSON |
| scoped Python intake assertions | 0 | IDs/rank/lifecycle agree, canonical statement is null, and all six dependent tasks are open |
| `git diff --check -- Stage1_Instances/THM-M-1179` | 0 | no whitespace errors |

Known downstream failures: primary-source and exact-theorem selection, canonical Lean elaboration,
anchor audit, obligation registry, proof, hermetic replay, and independent acceptance remain open.
They prevent theorem completion but do not invalidate this fail-closed intake.
