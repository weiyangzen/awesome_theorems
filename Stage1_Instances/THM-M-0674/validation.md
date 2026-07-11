# Intake validation

Base revision: `9c650bd6aac0dca129c8bc8ac01e0d7432669386`.

Validation covers manifest membership, planned-dossier structure, scoped invariants, and whitespace.
No canonical Lean expression is selected, so this intake claims no kernel validation.

| Command | Result |
|---|---|
| `python3 Docs/tools/check_stage1_standard.py` | exit 0; 15 assurance groups, 1546 uniform-L0 targets |
| `python3 scripts/stage1_target.py check` | exit 0; 1546 unique targets, ranks 1..1546 |
| `python3 scripts/stage1_target.py show THM-M-0674` | exit 0; rank 300, L0/rework_required, planned, theorem_complete false |
| `python3 -m json.tool Stage1_Instances/THM-M-0674/instance.json` | exit 0 |
| `python3 -m json.tool Stage1_Instances/THM-M-0674/task-dag.json` | exit 0 |
| scoped Python dossier assertions | exit 0; `intake invariant check: ok` |
| `git diff --check -- Stage1_Instances/THM-M-0674` | exit 0; no output |

The exact primary theorem, statement elaboration, mutation checks, anchor audit, obligation graphs,
proof, hermetic replay, and independent review remain downstream work. These prevent theorem
completion but do not invalidate a fail-closed planned intake.
