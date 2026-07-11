# Intake validation record

Base revision: `1a30b84c1f86a2bbbf08b36f9afd06912b8f6c06`.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, and 1546 uniform-L0 targets passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets at ranks 1 through 1546; all L0/rework-required |
| `python3 scripts/stage1_target.py show THM-M-0451` | 0 | rank 93, planned, legacy artifacts unaccepted, theorem incomplete |
| `python3 -m json.tool Stage1_Instances/THM-M-0451/intake.json >/dev/null` | 0 | intake JSON parsed |
| `python3 -m json.tool Stage1_Instances/THM-M-0451/task-dag.json >/dev/null` | 0 | open phase DAG JSON parsed |
| `rg -n '\bsorry\b\|\badmit\b\|\baxiom\b\|theorem_complete[^\n]*true' Stage1_Instances/THM-M-0451` | 1 | expected no-match result; no forbidden proof substitute or false completion flag found |
| `git diff --check` | 0 | no whitespace errors |

This is the smallest real validation for an intake-only node. No Lean declaration is introduced, so
there is no kernel claim to test. The exact-statement phase, source review, master acceptance, and
all theorem-completion gates remain open.
