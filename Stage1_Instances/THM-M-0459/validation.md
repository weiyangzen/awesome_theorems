# Intake validation

Base revision: `2d0ac727836c39cd946970b1ba5903ae1cd8f79d`.

Validation covers manifest consistency, dossier structure, scope invariants, JSON syntax, and
whitespace. No canonical Lean expression exists at intake, so no kernel validation is claimed.

| Command | Result |
|---|---|
| `python3 Docs/tools/check_stage1_standard.py` | exit 0; 15 assurance groups, 1546 uniform-L0 targets |
| `python3 scripts/stage1_target.py check` | exit 0; 1546 unique targets, ranks 1..1546 |
| `python3 scripts/stage1_target.py show THM-M-0459` | exit 0; rank 307, L0/rework_required, planned, theorem_complete false |
| `python3 -m json.tool Stage1_Instances/THM-M-0459/instance.json` | exit 0 |
| `python3 -m json.tool Stage1_Instances/THM-M-0459/task-dag.json` | exit 0 |
| scoped Python intake assertions | exit 0; `intake invariant check: ok` |
| `git diff --check -- Stage1_Instances/THM-M-0459` | exit 0; no output |

Known downstream failures are exact source identification, primary-source assumption review,
canonical Lean elaboration, anchor audit, proof, hermetic replay, and independent review. They do
not invalidate this fail-closed planned intake, but they prevent every theorem-completion claim.
