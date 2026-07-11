# Intake validation

Base revision: `9c650bd6aac0dca129c8bc8ac01e0d7432669386`.

The following commands were run from the repository root after creating the dossier:

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | Standard structure and the 1546-target projection passed |
| `python3 scripts/stage1_target.py check` | 0 | Target manifest ordering/digest checks passed |
| `python3 scripts/stage1_target.py show THM-M-1003` | 0 | Rank 283, `L0`, `planned`, rework required |
| `python3 -m json.tool Stage1_Instances/THM-M-1003/intake.json >/dev/null` | 0 | Intake JSON is syntactically valid |
| `git diff --check -- Stage1_Instances/THM-M-1003` | 0 | No whitespace errors |

These are intake-only checks. No Lean build, exact-type check, axiom audit, source acceptance,
or theorem-completion gate is claimed.
