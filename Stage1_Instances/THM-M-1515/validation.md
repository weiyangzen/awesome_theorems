# Intake validation record

Base revision: `61369637c5db864082a624c34c62a91e6741f9da`.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, and 1546 uniform-L0 targets passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets at ranks 1 through 1546; all L0/rework-required |
| `python3 scripts/stage1_target.py show THM-M-1515` | 0 | rank 184, planned, L0/rework-required, legacy artifacts unaccepted, theorem incomplete |
| `python3 -m json.tool Stage1_Instances/THM-M-1515/intake.json >/dev/null` | 0 | intake JSON parsed |
| `python3 -m json.tool Stage1_Instances/THM-M-1515/task-dag.json >/dev/null` | 0 | open task DAG JSON parsed |
| `rg -n '\bsorry\b\|\badmit\b\|sorryAx\|fake results' Stage1_Instances/THM-M-1515` | 1 | no forbidden proof substitutes; exit 1 means no match |
| `git diff --check` | 0 | no whitespace errors |

This is the smallest real validation for an intake-only node. No Lean declaration or proof was
introduced, so kernel validation is not applicable yet. Exact statement, source acceptance, master
acceptance, all dependent phases, audit completion, and theorem completion remain open.
