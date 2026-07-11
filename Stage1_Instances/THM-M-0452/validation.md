# Intake validation record

Base revision: `9c650bd6aac0dca129c8bc8ac01e0d7432669386`.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, and 1546 uniform-L0 targets passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets at ranks 1 through 1546; all L0/rework-required |
| `python3 scripts/stage1_target.py show THM-M-0452` | 0 | rank 301, planned, legacy artifacts unaccepted, theorem incomplete |
| `python3 -m json.tool Stage1_Instances/THM-M-0452/intake.json >/dev/null` | 0 | intake JSON parsed |
| `python3 -m json.tool Stage1_Instances/THM-M-0452/task-dag.json >/dev/null` | 0 | open phase DAG JSON parsed |
| `rg -n '\bsorry\b\|\badmit\b\|\baxiom\b\|theorem_complete[^[:cntrl:]]*true' Stage1_Instances/THM-M-0452` | 1 | expected no-match result; no forbidden substitute or false completion flag found |
| `git diff --check` | 0 | no whitespace errors |

This is the smallest real validation for an intake-only node. No Lean declaration was introduced,
so there is no kernel claim to test. Source review, exact elaboration, master acceptance, and every
theorem-completion gate remain open.
