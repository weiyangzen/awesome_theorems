# Intake validation

Base revision: `8046f7febfe203ec958fa24e111f6b730ad8393b`.

Validation is limited to manifest consistency, dossier structure, scoped invariants, JSON syntax,
and whitespace. No canonical Lean target exists yet, so no elaboration or kernel result is claimed.

| Command | Result |
|---|---|
| `python3 Docs/tools/check_stage1_standard.py` | exit 0; 15 assurance groups, 1546 uniform-L0 targets |
| `python3 scripts/stage1_target.py check` | exit 0; 1546 unique targets, ranks 1..1546 |
| `python3 scripts/stage1_target.py show THM-M-1300` | exit 0; rank 468, L0/rework_required, planned, theorem_complete false |
| `python3 -m json.tool Stage1_Instances/THM-M-1300/instance.json` | exit 0 |
| `python3 -m json.tool Stage1_Instances/THM-M-1300/task-dag.json` | exit 0 |
| scoped Python intake assertions | exit 0; `intake invariant check: ok` |
| `git diff --check -- Stage1_Instances/THM-M-1300` | exit 0; no output |

Known downstream failures are exact theorem and source identification, parameter freeze, canonical
Lean elaboration, anchor audit, proof, hermetic replay, and independent review. They prevent theorem
completion but do not invalidate this fail-closed intake.
