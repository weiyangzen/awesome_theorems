# Intake validation

Base revision: `fe07aee0ce546497b6b69c8f7dcf910f374c09b1`.

Validation is limited to manifest consistency, dossier structure, scoped intake invariants, JSON
syntax, and whitespace. No canonical Lean target exists yet, so no kernel validation is claimed.

The exact commands and results from this clone are recorded below.

| Command | Result |
|---|---|
| `python3 Docs/tools/check_stage1_standard.py` | exit 0; 15 assurance groups, 1546 uniform-L0 targets |
| `python3 scripts/stage1_target.py check` | exit 0; 1546 unique targets, ranks 1..1546 |
| `python3 scripts/stage1_target.py show THM-M-1141` | exit 0; rank 346, L0/rework_required, planned, theorem_complete false |
| `python3 -m json.tool Stage1_Instances/THM-M-1141/instance.json` | exit 0; valid JSON |
| `python3 -m json.tool Stage1_Instances/THM-M-1141/task-dag.json` | exit 0; valid JSON |
| scoped Python intake assertions | exit 0; `intake invariant check: ok` |
| `git diff --check -- Stage1_Instances/THM-M-1141` | exit 0; no output |

Known downstream failures are the exact source anchor, canonical Lean elaboration, immutable anchor
audit, obligation registry, proof, hermetic replay, and independent review. They prevent theorem
completion but do not invalidate a truthful planned intake.
