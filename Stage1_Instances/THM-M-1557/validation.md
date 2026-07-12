# Intake validation

Base revision: `955bd0889d93d62c132eb6ec63d2d1572479357b`.

Validation is limited to target membership, repository/manifest consistency, dossier structure,
scoped planned-intake invariants, JSON syntax, and whitespace. The exact source equations and
canonical Lean expression are intentionally open, so an unrelated Lean proposition was not created
or elaborated and no kernel-proof result is claimed.

| Command | Result |
|---|---|
| `python3 Docs/tools/check_stage1_standard.py` | exit 0; 15 assurance groups, 1546 uniform-L0 Lean 4 targets, execution skill present |
| `python3 scripts/stage1_target.py check` | exit 0; 1546 unique targets, ranks 1..1546, all L0/rework_required |
| `python3 scripts/stage1_target.py show THM-M-1557` | exit 0; rank 569, L0/rework_required, planned, theorem_complete false |
| `python3 -m json.tool Stage1_Instances/THM-M-1557/instance.json` | exit 0; valid JSON |
| `python3 -m json.tool Stage1_Instances/THM-M-1557/task-dag.json` | exit 0; valid JSON |
| scoped Python intake assertions | exit 0; `intake invariant check: ok` |
| `git diff --check -- Stage1_Instances/THM-M-1557` | exit 0; no output |

Known downstream failures are not intake failures: primary-source edition/equation and errata
inspection, exact statement selection, Lean elaboration and mutation tests, anchor audit, obligation
freeze, proof, hermetic replay, and independent review remain open. They prevent theorem completion.
