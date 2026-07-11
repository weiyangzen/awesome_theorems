# Intake validation

Base revision: `a8d6489fd935cd71fa4499f2f3f5b051998203f4`.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | rev-5.6 standard structure passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique ordered L0 targets passed |
| `python3 scripts/stage1_target.py show THM-M-1155` | 0 | membership, rank 358, planned lifecycle, and incomplete status confirmed |
| `python3 -m json.tool Stage1_Instances/THM-M-1155/intake.json` | 0 | pending post-write validation |
| `python3 -m json.tool Stage1_Instances/THM-M-1155/task_dag.json` | 0 | pending post-write validation |
| `git diff --check -- Stage1_Instances/THM-M-1155` | 0 | pending post-write validation |

These checks validate intake structure only. No Lean statement exists in this phase, so there is no
kernel theorem to compile or inspect.
