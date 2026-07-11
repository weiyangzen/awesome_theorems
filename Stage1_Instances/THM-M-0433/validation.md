# Intake validation

Base revision: `5997161aebf527e8a1e05724d4fbd4ce07dfd815`.

All commands ran from the repository root on 2026-07-12:

| Command | Exit | Result |
|---|---:|---|
| `python3 -m json.tool Stage1_Instances/THM-M-0433/intake.json >/dev/null` | 0 | Intake JSON parsed |
| `python3 Docs/tools/check_stage1_standard.py` | 0 | `ok`; 15 assurance groups and 1546 uniform-L0 targets |
| `python3 scripts/stage1_target.py check` | 0 | `ok`; 1546 unique targets, ranks 1 through 1546 |
| `python3 scripts/stage1_target.py show THM-M-0433` | 0 | Rank 61, `planned`, `L0`, rework required, theorem incomplete |
| `rg -n '\bsorry\b|\badmit\b|theorem_complete[^\n]*true' Stage1_Instances/THM-M-0433/{intake.json,README.md,source_statement_crosswalk.md}` | 1 | Expected no-match result |
| `git diff --check -- Stage1_Instances/THM-M-0433` | 0 | No whitespace errors |

These are intake-level structural checks. No Lean theorem compilation is claimed because exact
elaboration is expressly assigned to the dependent statement node.
