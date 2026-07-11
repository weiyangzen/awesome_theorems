# Intake validation

Base revision: `ef0dd4cd5367b81a98b8906e3325b55fe5263491`.

Validation covers manifest consistency, dossier structure, scoped intake invariants, JSON syntax,
and whitespace. No canonical Lean declaration exists at this phase, so no kernel result is claimed.

| Command | Result |
|---|---|
| `python3 Docs/tools/check_stage1_standard.py` | exit 0; 15 assurance groups, 1546 uniform-L0 targets |
| `python3 scripts/stage1_target.py check` | exit 0; 1546 unique targets, ranks 1..1546 |
| `python3 scripts/stage1_target.py show THM-M-1290` | exit 0; rank 461, planned, L0/rework_required, theorem_complete false |
| `python3 -m json.tool Stage1_Instances/THM-M-1290/instance.json` | exit 0 |
| `python3 -m json.tool Stage1_Instances/THM-M-1290/task-dag.json` | exit 0 |
| scoped Python intake assertions | exit 0; `intake invariant check: ok` |
| `git diff --check -- Stage1_Instances/THM-M-1290` | exit 0; no output |

Known downstream failures are exact source inspection, canonical Lean elaboration, anchor audit,
obligation expansion, proof, hermetic replay, and independent review. They bar theorem completion but
do not bar a fail-closed planned intake.
