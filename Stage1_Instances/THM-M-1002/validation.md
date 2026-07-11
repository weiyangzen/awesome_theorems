# Intake validation

Base revision: `9c650bd6aac0dca129c8bc8ac01e0d7432669386`.

Validation is limited to manifest consistency, dossier structure, scoped intake invariants, and
whitespace. No canonical Lean expression is frozen in this phase, so no kernel result is claimed.

| Command | Result |
|---|---|
| `python3 Docs/tools/check_stage1_standard.py` | exit 0; 15 assurance groups and 1546 uniform-L0 targets |
| `python3 scripts/stage1_target.py check` | exit 0; 1546 unique targets, ranks 1..1546 |
| `python3 scripts/stage1_target.py show THM-M-1002` | exit 0; rank 282, L0/rework_required, planned, theorem_complete false |
| `python3 -m json.tool Stage1_Instances/THM-M-1002/instance.json` | exit 0 |
| `python3 -m json.tool Stage1_Instances/THM-M-1002/task-dag.json` | exit 0 |
| scoped Python intake assertions | exit 0; `intake invariant check: ok` |
| `git diff --check -- Stage1_Instances/THM-M-1002` | exit 0; no output |

Known downstream failures are intentionally open: exact source inspection and independent review,
canonical Lean elaboration, anchor/provenance audit, obligation freeze, proof acceptance, hermetic
replay, and release verification. They prevent theorem completion but not this planned intake.
