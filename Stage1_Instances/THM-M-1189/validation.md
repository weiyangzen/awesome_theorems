# Intake validation

Base revision: `2b65f3efa70ae08a8776a86771b091957de1652e`.

Validation is limited to manifest consistency, dossier structure, scoped intake invariants, and
whitespace. No canonical Lean expression exists yet, so no elaboration or kernel result is claimed.

| Command | Result |
|---|---|
| `python3 Docs/tools/check_stage1_standard.py` | exit 0; 15 assurance groups, 1546 uniform-L0 targets |
| `python3 scripts/stage1_target.py check` | exit 0; 1546 unique targets, ranks 1..1546 |
| `python3 scripts/stage1_target.py show THM-M-1189` | exit 0; rank 152, L0/rework_required, planned, theorem_complete false |
| `python3 -m json.tool Stage1_Instances/THM-M-1189/instance.json` | exit 0 |
| `python3 -m json.tool Stage1_Instances/THM-M-1189/task-dag.json` | exit 0 |
| scoped Python intake assertions | exit 0; `intake invariant check: ok` |
| `git diff --check -- Stage1_Instances/THM-M-1189` | exit 0; no output |

Known downstream failures: exact primary-source theorem inspection, canonical Lean elaboration,
anchor audit, obligation expansion, proof, hermetic replay, and independent review remain open. They
prevent theorem completion but do not invalidate a truthful planned intake.
