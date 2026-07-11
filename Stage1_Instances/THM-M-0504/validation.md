# Intake validation

Base revision: `c6aa0f2ba41dd389c2bcf01dd532923615781719`.

Commands are run from the repository root:

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | Standard check passed: 15 assurance groups and 1546 uniform-L0 targets |
| `python3 scripts/stage1_target.py check` | 0 | Manifest check passed: 1546 unique targets, ranks 1 through 1546 |
| `python3 scripts/stage1_target.py show THM-M-0504` | 0 | Membership confirmed at execution rank 259, planned, rework required |
| `python3 -m json.tool Stage1_Instances/THM-M-0504/intake.json` | 0 | Intake JSON parsed successfully |
| `git diff --check -- Stage1_Instances/THM-M-0504` | 0 | No whitespace errors |

No Lean command is applicable: the source metadata does not identify a unique proposition to
elaborate. Recording a successful build of a substituted RH equivalence would be false evidence.
