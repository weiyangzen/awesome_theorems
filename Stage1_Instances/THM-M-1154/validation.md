# Intake validation

Base revision: `2b65f3efa70ae08a8776a86771b091957de1652e`.

Validation covers manifest consistency and the fail-closed dossier. No exact Lean expression is
claimed, so a Lean kernel check would not validate this intake and is deliberately deferred.

| Command | Result |
|---|---|
| `python3 Docs/tools/check_stage1_standard.py` | exit 0; 15 assurance groups and 1546 uniform-L0 targets |
| `python3 scripts/stage1_target.py check` | exit 0; 1546 unique targets, ranks 1..1546 |
| `python3 scripts/stage1_target.py show THM-M-1154` | exit 0; rank 144, L0/rework_required, planned, theorem_complete false |
| `python3 -m json.tool Stage1_Instances/THM-M-1154/instance.json` | exit 0 |
| `python3 -m json.tool Stage1_Instances/THM-M-1154/task-dag.json` | exit 0 |
| scoped intake assertions | exit 0; `intake invariant check: ok` |
| `git diff --check -- Stage1_Instances/THM-M-1154` | exit 0; no output |

Known downstream failures are exact source identification, canonical elaboration, anchor audit,
proof architecture and proof, hermetic replay, and independent review. They prevent theorem
completion but do not invalidate a planned intake whose ambiguity is explicit.
