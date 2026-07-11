# Intake validation

Base revision: `1a30b84c1f86a2bbbf08b36f9afd06912b8f6c06`.

Validation is restricted to metadata consistency, dossier structure, JSON syntax, scoped intake
invariants, and whitespace. The canonical Lean expression is deliberately not frozen, so no kernel
proof result is claimed.

| Command | Result |
|---|---|
| `python3 Docs/tools/check_stage1_standard.py` | exit 0; standard and 1546-target coverage OK |
| `python3 scripts/stage1_target.py check` | exit 0; 1546 unique targets, ranks 1..1546 |
| `python3 scripts/stage1_target.py show THM-M-0441` | exit 0; rank 87, L0/rework_required, planned, theorem_complete false |
| `python3 -m json.tool` on `instance.json` and `task-dag.json` | exit 0 for both files |
| scoped intake invariant assertions | exit 0; `intake invariant check: ok` |
| `git diff --check -- Stage1_Instances/THM-M-0441` | exit 0; no output |

Known downstream failures: pinpoint source inspection and errata search, exact claim and Lean
expression, elaboration and mutation tests, anchor audit, proof architecture and proof, hermetic
replay, and independent acceptance all remain open. These failures prevent theorem completion but
do not invalidate a fail-closed planned intake.
