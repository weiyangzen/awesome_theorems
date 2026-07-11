# Intake validation

Base revision: `9c650bd6aac0dca129c8bc8ac01e0d7432669386`.

Validation is limited to manifest consistency, dossier structure, scoped intake invariants, JSON
syntax, and whitespace. No canonical Lean expression exists in this intake, so no kernel result is
claimed.

The exact commands and results from the self-test run are recorded below.

| Command | Result |
|---|---|
| `python3 Docs/tools/check_stage1_standard.py` | exit 0; 15 assurance groups and 1546 uniform-L0 Lean 4 targets |
| `python3 scripts/stage1_target.py check` | exit 0; 1546 unique targets, ranks 1..1546 |
| `python3 scripts/stage1_target.py show THM-M-0996` | exit 0; rank 276, L0/rework_required, planned, theorem_complete false |
| `python3 -m json.tool Stage1_Instances/THM-M-0996/instance.json` | exit 0 |
| `python3 -m json.tool Stage1_Instances/THM-M-0996/task-dag.json` | exit 0 |
| scoped Python intake assertions | exit 0; `intake invariant check: ok` |
| `git diff --check -- Stage1_Instances/THM-M-0996` | exit 0; no output |

Known downstream failures: exact primary-source inspection and errata review, convention freeze,
canonical Lean elaboration, anchor audit, proof architecture and proof, hermetic replay, and
independent review remain open. They prevent theorem completion but do not invalidate a truthful
fail-closed planned intake.
