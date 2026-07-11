# Intake validation

Base revision: `73a92b5e63e8eb3c93a5c95d5aead1658ca24c79`.

Validation is limited to repository/manifest consistency, dossier structure, scoped intake
invariants, and whitespace. The source is not proposition-shaped, so no Lean file or kernel result
is claimed.

| Command | Result |
|---|---|
| `python3 Docs/tools/check_stage1_standard.py` | exit 0; 15 assurance groups and 1546 uniform-L0 targets |
| `python3 scripts/stage1_target.py check` | exit 0; 1546 unique targets, ranks 1..1546 |
| `python3 scripts/stage1_target.py show THM-M-1262` | exit 0; rank 439, L0/rework_required, planned, theorem_complete false |
| `rg -n "wavefront\|Wavefront\|microlocal\|Microlocal" Formalizations Mathlib -g '*.lean'` | exit 1; no matches (negative discovery result) |
| `python3 -m json.tool Stage1_Instances/THM-M-1262/instance.json` | exit 0 |
| `python3 -m json.tool Stage1_Instances/THM-M-1262/task-dag.json` | exit 0 |
| scoped Python intake assertions | exit 0; `intake invariant check: ok` |
| `git diff --check -- Stage1_Instances/THM-M-1262` | exit 0; no output |

Known downstream failures: proposition and primary-source selection, exact source inspection,
canonical Lean elaboration, dependency anchor audit, proof, hermetic replay, and independent review
remain open. They prevent theorem completion but do not invalidate this fail-closed planned intake.
