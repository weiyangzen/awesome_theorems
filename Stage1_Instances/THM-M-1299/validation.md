# Intake validation

Base revision: `8046f7febfe203ec958fa24e111f6b730ad8393b`.

Validation is limited to manifest/standard consistency, dossier structure, scoped intake
invariants, JSON syntax, and whitespace. There is no selected canonical proposition, so no Lean
elaboration or kernel result is claimed.

| Command | Result |
|---|---|
| `python3 Docs/tools/check_stage1_standard.py` | exit 0; 15 assurance groups and 1546 uniform-L0 Lean 4 targets |
| `python3 scripts/stage1_target.py check` | exit 0; 1546 unique targets, ranks 1..1546, all L0/rework_required |
| `python3 scripts/stage1_target.py show THM-M-1299` | exit 0; rank 467, L0/rework_required, planned, theorem_complete false |
| `python3 -m json.tool Stage1_Instances/THM-M-1299/instance.json` | exit 0 |
| `python3 -m json.tool Stage1_Instances/THM-M-1299/task-dag.json` | exit 0 |
| scoped Python intake assertions | exit 0; `intake invariant check: ok` |
| `git diff --check -- Stage1_Instances/THM-M-1299` | exit 0; no output |

Known downstream failures: unique source theorem selection, primary-source inspection, exact
domains and parameters, canonical Lean elaboration, anchor audit, obligation registry, proof,
hermetic replay, and independent review remain open. They prevent theorem completion but do not
invalidate this fail-closed planned intake.
