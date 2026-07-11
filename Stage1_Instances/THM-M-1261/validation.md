# Intake validation

Base revision: `056367be3b1cb2e101200085ec5a5fdff670d16b`.

Validation covers manifest consistency, dossier structure, JSON syntax, scoped intake invariants,
and whitespace only. No Lean statement or kernel proof is claimed at intake.

| Command | Result |
|---|---|
| `python3 Docs/tools/check_stage1_standard.py` | exit 0; 15 assurance groups and 1546 uniform-L0 targets |
| `python3 scripts/stage1_target.py check` | exit 0; 1546 unique targets, ranks 1..1546 |
| `python3 scripts/stage1_target.py show THM-M-1261` | exit 0; rank 438, planned, L0/rework-required, theorem incomplete |
| `python3 -m json.tool Stage1_Instances/THM-M-1261/instance.json` | exit 0 |
| `python3 -m json.tool Stage1_Instances/THM-M-1261/task-dag.json` | exit 0 |
| scoped Python intake assertions | exit 0; `intake invariant check: ok` |
| `git diff --check -- Stage1_Instances/THM-M-1261` | exit 0; no output |

Known downstream failures are exact source selection and errata inspection, exact Lean statement,
anchor audit, obligation expansion, proof, hermetic replay, and independent review. They prevent
theorem completion but do not invalidate this fail-closed planned intake.
