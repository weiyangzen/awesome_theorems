# Intake validation

Base revision: `c6aa0f2ba41dd389c2bcf01dd532923615781719`.

The following checks were run from the repository root. They validate only the intake artifact and
repository membership; they do not elaborate or prove the theorem.

| Command | Result |
|---|---|
| `python3 Docs/tools/check_stage1_standard.py` | exit 0: standard reports 15 assurance groups and 1546 uniform-L0 Lean 4 targets |
| `python3 scripts/stage1_target.py check` | exit 0: 1546 unique targets, ranks 1..1546, all L0/rework_required |
| `python3 scripts/stage1_target.py show THM-M-0983` | exit 0: rank 263, planned, L0, rework required, theorem incomplete |
| `python3 -m json.tool Stage1_Instances/THM-M-0983/intake.json` | exit 0 |
| `test "$(find Stage1_Instances/THM-M-0983 -maxdepth 1 -type f \| wc -l)" -eq 4` plus scoped ID/reference and forbidden-token checks | exit 0 |
| `git diff --check -- Stage1_Instances/THM-M-0983` | exit 0 |

Lean compilation is intentionally not claimed: exact elaboration is owned by the dependent
`S56-M-0983-STATEMENT` phase.
