# Intake validation

Base revision: `337a6bea341c0f1616a624ad03e440cb829e61e3`.

Validation is limited to manifest consistency, dossier structure, scoped intake invariants, JSON
syntax, and whitespace. No canonical Lean expression exists yet, so no kernel result is claimed.

| Command | Result |
|---|---|
| `python3 Docs/tools/check_stage1_standard.py` | exit 0; 15 assurance groups and 1546 uniform-L0 targets |
| `python3 scripts/stage1_target.py check` | exit 0; 1546 unique targets, ranks 1..1546 |
| `python3 scripts/stage1_target.py show THM-M-1320` | exit 0; rank 482, L0/rework_required, planned, theorem_complete false |
| `python3 -m json.tool Stage1_Instances/THM-M-1320/instance.json` | exit 0 |
| `python3 -m json.tool Stage1_Instances/THM-M-1320/task-dag.json` | exit 0 |
| scoped Python intake assertions | exit 0; `intake invariant check: ok` |
| `git diff --check -- Stage1_Instances/THM-M-1320` | exit 0; no output |

Known downstream failures: exact primary-source theorem inspection and errata review, statement
normalization, canonical Lean elaboration, anchor audit, obligation registry, proof, hermetic replay,
and independent review remain open. They prevent theorem completion but do not invalidate this
fail-closed planned intake.
