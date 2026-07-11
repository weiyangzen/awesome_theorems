# Intake validation

Base revision: `594dbb735284e7b81f51ce813a9c3200fd55f610`.

Validation is limited to manifest consistency, dossier structure, scoped intake invariants, JSON
syntax, and whitespace. There is no canonical Lean declaration in this intake, so no elaboration or
kernel-proof result is claimed.

| Command | Result |
|---|---|
| `python3 Docs/tools/check_stage1_standard.py` | exit 0; 15 assurance groups and 1546 uniform-L0 Lean 4 targets |
| `python3 scripts/stage1_target.py check` | exit 0; 1546 unique targets, ranks 1..1546, all L0/rework_required |
| `python3 scripts/stage1_target.py show THM-M-1544` | exit 0; rank 203, planned, L0/rework_required, theorem_complete false |
| `python3 -m json.tool Stage1_Instances/THM-M-1544/instance.json` | exit 0 |
| `python3 -m json.tool Stage1_Instances/THM-M-1544/task-dag.json` | exit 0 |
| scoped Python assertions over instance and task DAG | exit 0; `intake invariant check: ok` |
| `git diff --check -- Stage1_Instances/THM-M-1544` | exit 0; no output |

Known downstream failures are exact primary-source statement and errata inspection, gauge-group and
quotient choices, canonical Lean elaboration, upstream anchor audit, obligation expansion, proof,
hermetic replay, and independent review. These prevent theorem completion but do not invalidate the
fail-closed `planned` intake.
