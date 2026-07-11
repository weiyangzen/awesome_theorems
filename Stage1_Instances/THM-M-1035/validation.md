# Intake validation record

Base revision: `dbd29db42090d2fce49f69d84d4631769ef7e9c3`.

The exact commands and results for this intake are recorded below. These checks establish only
manifest consistency and dossier structure; no Lean/kernel result is claimed.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | rev-5.6 standard check passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique uniform-L0 targets passed |
| `python3 scripts/stage1_target.py show THM-M-1035` | 0 | rank 228, planned, L0/rework-required, theorem incomplete |
| `python3 -m json.tool Stage1_Instances/THM-M-1035/intake.json >/dev/null` | 0 | valid JSON |
| `git diff --check` | 0 | no whitespace errors |

Master acceptance and all dependent phases remain outstanding.
