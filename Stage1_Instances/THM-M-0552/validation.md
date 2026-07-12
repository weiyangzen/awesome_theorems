# Intake validation

Base revision: `c8997e79129038d11a59ae2ad24c3725dcc2d8b9`.

Validation is limited to manifest/standard consistency, dossier syntax, scoped intake invariants,
and whitespace. No exact Lean target is selected, so `lake env lean` would have no truthful
declaration to elaborate and no kernel validation is claimed.

| Command | Result |
|---|---|
| `python3 Docs/tools/check_stage1_standard.py` | exit 0; 15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, execution skill present |
| `python3 scripts/stage1_target.py check` | exit 0; 1546 unique targets, ranks 1..1546, all L0/rework_required |
| `python3 scripts/stage1_target.py show THM-M-0552` | exit 0; rank 604, L0/rework_required, lifecycle planned, theorem_complete false |
| `python3 -m json.tool Stage1_Instances/THM-M-0552/instance.json` | exit 0; no output |
| `python3 -m json.tool Stage1_Instances/THM-M-0552/task-dag.json` | exit 0; no output |
| scoped Python assertions over instance, DAG, and owned file set | exit 0; `intake invariant check: ok` |
| `git diff --check -- Stage1_Instances/THM-M-0552` | exit 0; no output |

Known downstream failures: the metadata does not identify a source theorem and appears to conflate
the usual Pontryagin square with a stable integral cohomology operation. The operation, coefficient
groups, degree, space category, hypotheses, laws, exact Lean expression, and primary-source anchors
remain unfrozen. Source inspection, elaboration, proof, hermetic replay, and independent review are
open. These failures prevent theorem progress but do not invalidate a fail-closed planned intake.
