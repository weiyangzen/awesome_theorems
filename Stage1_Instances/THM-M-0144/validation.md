# Intake validation

Base revision: `fe07aee0ce546497b6b69c8f7dcf910f374c09b1`.

Validation is limited to manifest consistency, dossier structure, scoped intake invariants, JSON,
and whitespace. The source theorem is unresolved, so no Lean elaboration or kernel result is
claimed.

| Command | Result |
|---|---|
| `python3 Docs/tools/check_stage1_standard.py` | exit 0; 15 assurance groups and 1546 uniform-L0 Lean 4 targets |
| `python3 scripts/stage1_target.py check` | exit 0; 1546 unique targets, ranks 1..1546, all L0/rework_required |
| `python3 scripts/stage1_target.py show THM-M-0144` | exit 0; rank 319, no legacy slot, planned, theorem_complete false |
| `python3 -m json.tool Stage1_Instances/THM-M-0144/instance.json` | exit 0 |
| `python3 -m json.tool Stage1_Instances/THM-M-0144/task-dag.json` | exit 0 |
| scoped Python intake assertions | exit 0; `intake invariant check: ok` |
| `git diff --check -- Stage1_Instances/THM-M-0144` | exit 0; no output |

Known downstream failures: primary-source identification and independent review, exact human and
Lean statements, anchor audit, obligation registry, proof, hermetic replay, and release validation
remain open. They prevent theorem completion but do not invalidate a truthful planned intake.
