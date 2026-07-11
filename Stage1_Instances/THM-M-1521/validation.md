# Intake validation

Base revision: `61369637c5db864082a624c34c62a91e6741f9da`.

The worker ran these commands from the repository root:

| Command | Result |
|---|---|
| `python3 Docs/tools/check_stage1_standard.py` | exit 0; standard reports 1546 uniform-L0 targets |
| `python3 scripts/stage1_target.py check` | exit 0; 1546 unique targets with ranks 1..1546 |
| `python3 scripts/stage1_target.py show THM-M-1521` | exit 0; rank 180, planned, L0/rework_required |
| `python3 -m json.tool Stage1_Instances/THM-M-1521/intake.json` | exit 0 |
| `git diff --check -- Stage1_Instances/THM-M-1521 .stage1-worker-selftest.json` | exit 0 |

These checks validate intake structure and scope consistency only. No Lean compilation, exact-type
check, axiom audit, source acceptance, or theorem-completion gate is claimed in this phase.
