# Intake validation

Base revision: `7a8e792e568c85805fef02f4071bcc4b5ac9e09d`.

Validation is limited to manifest consistency, dossier structure, scoped intake invariants, and
whitespace. No canonical Lean target exists, so no elaboration or kernel-proof result is claimed.

| Command | Result |
|---|---|
| `python3 Docs/tools/check_stage1_standard.py` | exit 0; 15 assurance groups, 41 legacy rows, 300 legacy slots, and 1546 uniform-L0 Lean 4 targets |
| `python3 scripts/stage1_target.py check` | exit 0; 1546 unique targets, ranks 1..1546, all L0/rework_required |
| `python3 scripts/stage1_target.py show THM-M-1195` | exit 0; rank 389, no legacy slot, L0/rework_required, planned, theorem_complete false |
| `python3 -m json.tool Stage1_Instances/THM-M-1195/instance.json` | exit 0 |
| `python3 -m json.tool Stage1_Instances/THM-M-1195/task-dag.json` | exit 0 |
| scoped Python intake assertions | exit 0; `intake invariant check: ok` |
| `git diff --check -- Stage1_Instances/THM-M-1195` | exit 0; no output |

Known downstream failures: precise primary-source result selection, exact statement, Lean
elaboration, anchor audit, obligation registry, proof, hermetic replay, and independent review are
open. They prevent theorem completion but do not invalidate a truthful planned intake.
