# Intake validation

Base revision: `2b65f3efa70ae08a8776a86771b091957de1652e`.

Validation is scoped to manifest consistency and the planned dossier. No canonical Lean expression
was elaborated for this intake, so no kernel or theorem-completion result is claimed.

| Command | Result |
|---|---|
| `python3 Docs/tools/check_stage1_standard.py` | exit 0; 15 assurance groups, 1546 uniform-L0 targets |
| `python3 scripts/stage1_target.py check` | exit 0; 1546 unique targets, ranks 1..1546 |
| `python3 scripts/stage1_target.py show THM-M-0081` | exit 0; rank 138, L0/rework_required, planned, theorem_complete false |
| `python3 -m json.tool Stage1_Instances/THM-M-0081/instance.json` | exit 0; valid JSON |
| `python3 -m json.tool Stage1_Instances/THM-M-0081/task-dag.json` | exit 0; valid JSON |
| scoped Python intake assertions | exit 0; `intake invariant check: ok` |
| `git diff --check -- Stage1_Instances/THM-M-0081` | exit 0; no output |

Known downstream failures are exact source inspection, canonical elaboration, anchor and provenance
audit, proof architecture, hermetic replay, and independent acceptance. They do not invalidate a
fail-closed planned intake, but they prevent every stronger claim.
