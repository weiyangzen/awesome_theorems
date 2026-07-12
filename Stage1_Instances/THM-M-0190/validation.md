# Intake validation

Base revision: `e51894725a43642d26ce16e4aad3abaf28393de7`.

Validation is limited to manifest consistency, dossier structure, scoped intake invariants, JSON,
source-tree discovery searches, and whitespace. The source does not yet identify a proposition
precisely enough to elaborate without inventing mathematics, so no Lean statement or kernel result
is claimed.

| Command | Result |
|---|---|
| `python3 Docs/tools/check_stage1_standard.py` | exit 0; 15 assurance groups, 1546 uniform-L0 Lean 4 targets, execution skill present |
| `python3 scripts/stage1_target.py check` | exit 0; 1546 unique targets, ranks 1..1546, all L0/rework_required |
| `python3 scripts/stage1_target.py show THM-M-0190` | exit 0; rank 676, planned, L0/rework_required, theorem_complete false |
| `python3 -m json.tool Stage1_Instances/THM-M-0190/instance.json` | exit 0; valid JSON |
| `python3 -m json.tool Stage1_Instances/THM-M-0190/task-dag.json` | exit 0; valid JSON |
| scoped Python intake assertions | exit 0; `intake invariant check: ok` |
| `git diff --check -- Stage1_Instances/THM-M-0190` | exit 0; no output |

Known downstream failures: primary-source theorem/premise mapping, exact statement selection, Lean
elaboration and mutation tests, anchor audit, obligation registry, proof, hermetic replay, and
independent review remain open. They prevent audit and theorem completion but do not invalidate a
truthful planned intake.
