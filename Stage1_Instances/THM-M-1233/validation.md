# Intake validation

Base revision: `c67df8af765ae58e38b6c8d4ce37668f5a600c6b`.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | `ok` with 1546 uniform-L0 targets and execution skill present |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all L0/rework-required |
| `python3 scripts/stage1_target.py show THM-M-1233` | 0 | rank 418; planned; target lane and metadata agree with intake |
| `python3 -m json.tool Stage1_Instances/THM-M-1233/intake.json` | 0 | valid JSON |
| `git diff --check -- Stage1_Instances/THM-M-1233` | 0 | no whitespace errors |

These checks validate only the intake artifact, target membership, and structural consistency. No
Lean command is appropriate yet because the assigned intake phase deliberately records an open
formal target; the statement phase owns elaboration and exact-type evidence.
