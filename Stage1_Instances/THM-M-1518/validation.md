# Intake validation

Validation was run from the repository root at base revision
`61369637c5db864082a624c34c62a91e6741f9da`.

| Command | Result |
|---|---|
| `python3 Docs/tools/check_stage1_standard.py` | exit 0; standard reports 1546 uniform-L0 targets and the execution skill |
| `python3 scripts/stage1_target.py check` | exit 0; 1546 unique targets, ranks 1 through 1546 |
| `python3 scripts/stage1_target.py show THM-M-1518` | exit 0; rank 187, planned, L0/rework_required, theorem incomplete |
| `python3 -m json.tool Stage1_Instances/THM-M-1518/intake.json` | exit 0 |
| `python3 -m json.tool Stage1_Instances/THM-M-1518/task-dag.json` | exit 0 |
| dossier-local reference and policy check recorded below | exit 0 |
| `git diff --check -- Stage1_Instances/THM-M-1518` | exit 0 |

These checks establish a structurally readable, internally scoped intake dossier only. No Lean
statement exists in this phase, so no Lean build or kernel evidence is claimed.
