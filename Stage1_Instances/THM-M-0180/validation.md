# Intake validation

Base revision: `27d1586e034f95cbf63801bb339532733308fd9a`.

Validation is limited to target/standard consistency, dossier structure, scoped intake invariants,
JSON syntax, and whitespace. The repository source does not yet identify one exact proposition, so
no Lean elaboration or proof result is claimed.

| Command | Result |
|---|---|
| `python3 Docs/tools/check_stage1_standard.py` | exit 0; 15 assurance groups and 1546 uniform-L0 Lean 4 targets |
| `python3 scripts/stage1_target.py check` | exit 0; 1546 unique targets, ranks 1..1546, all L0/rework_required |
| `python3 scripts/stage1_target.py show THM-M-0180` | exit 0; rank 671, L0/rework_required, planned, theorem_complete false |
| `python3 -m json.tool Stage1_Instances/THM-M-0180/instance.json` | exit 0; valid JSON |
| `python3 -m json.tool Stage1_Instances/THM-M-0180/task-dag.json` | exit 0; valid JSON |
| scoped Python intake assertions | exit 0; `intake invariant check: ok` |
| `git diff --check -- Stage1_Instances/THM-M-0180` | exit 0; no output |

Known downstream failures: exact primary-source theorem identity, source review, canonical Lean
statement and elaboration, anchor audit, obligation registry, proof, hermetic replay, and independent
review remain open. They prevent theorem completion but do not invalidate this planned intake.
