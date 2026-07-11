# Intake validation

Base revision: `8046f7febfe203ec958fa24e111f6b730ad8393b`.

Validation is limited to manifest consistency, dossier structure, scoped intake invariants, and
whitespace. The exact source theorem is unresolved, so there is no canonical Lean expression and
no kernel result is claimed.

| Command | Result |
|---|---|
| `python3 Docs/tools/check_stage1_standard.py` | exit 0; 15 assurance groups, 1546 uniform-L0 Lean 4 targets |
| `python3 scripts/stage1_target.py check` | exit 0; 1546 unique targets, ranks 1..1546 |
| `python3 scripts/stage1_target.py show THM-M-1305` | exit 0; rank 473, L0/rework_required, planned, theorem_complete false |
| `python3 -m json.tool Stage1_Instances/THM-M-1305/instance.json` | exit 0 |
| `python3 -m json.tool Stage1_Instances/THM-M-1305/task-dag.json` | exit 0 |
| scoped Python intake assertions | exit 0; `intake invariant check: ok` |
| `git diff --check -- Stage1_Instances/THM-M-1305` | exit 0; no output |

Known downstream failures: exact primary-source identity, theorem/page and assumptions, canonical
Lean elaboration, anchor audit, obligation registry, proof, hermetic replay, and independent review
remain open. They prevent theorem completion but do not invalidate this fail-closed planned intake.
