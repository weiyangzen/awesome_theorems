# Intake validation record

Base revision: `7a8e792e568c85805fef02f4071bcc4b5ac9e09d`.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | `check_stage1_standard: ok (15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, execution skill present)` |
| `python3 scripts/stage1_target.py check` | 0 | `stage1_target: ok (1546 unique targets, ranks 1..1546, all L0/rework_required)` |
| `python3 scripts/stage1_target.py show THM-M-1192` | 0 | Rank 386; `L0`, `rework_required=true`, lane `hard_mathlib_anchor_and_wrapper`, lifecycle `planned`, theorem incomplete |
| `python3 -m json.tool Stage1_Instances/THM-M-1192/intake.json >/dev/null` | 0 | JSON syntax valid |
| dossier-local reference and placeholder scan (see worker manifest command) | 0 | Required files and declared merge targets exist; no forbidden proof placeholder tokens found |
| `git diff --check -- Stage1_Instances/THM-M-1192` | 0 | No whitespace errors |

This is the smallest real validation for an intake whose exact statement is truthfully blocked.
There is no Lean target to elaborate yet, so this record supplies no kernel evidence.
