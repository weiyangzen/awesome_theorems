# Intake validation

Base revision: `594dbb735284e7b81f51ce813a9c3200fd55f610`.

Validation is limited to manifest consistency, dossier structure, scoped intake invariants, and
whitespace. No canonical Lean expression has been selected, so no kernel result is claimed.

| Command | Result |
|---|---|
| `python3 Docs/tools/check_stage1_standard.py` | exit 0; 15 assurance groups and 1546 uniform-L0 targets |
| `python3 scripts/stage1_target.py check` | exit 0; 1546 unique targets, ranks 1..1546 |
| `python3 scripts/stage1_target.py show THM-M-1092` | exit 0; rank 216, L0/rework_required, planned, theorem_complete false |
| `python3 -m json.tool Stage1_Instances/THM-M-1092/instance.json` | exit 0 |
| `python3 -m json.tool Stage1_Instances/THM-M-1092/task-dag.json` | exit 0 |
| scoped Python intake assertions | exit 0; `intake invariant check: ok` |
| `git diff --check -- Stage1_Instances/THM-M-1092` | exit 0; no output |

Known downstream failures: exact primary-source inspection, formulation and regularity choices,
canonical Lean elaboration, anchor audit, proof, hermetic replay, and independent review remain open.
They prevent theorem completion but do not invalidate this fail-closed planned intake.
