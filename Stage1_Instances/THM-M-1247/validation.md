# Intake validation record

Base revision: `056367be3b1cb2e101200085ec5a5fdff670d16b`.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | `ok`: 15 assurance groups, 1546 uniform-L0 Lean 4 targets, execution skill present |
| `python3 scripts/stage1_target.py check` | 0 | `ok`: 1546 unique targets, ranks 1 through 1546, all L0/rework_required |
| `python3 scripts/stage1_target.py show THM-M-1247` | 0 | Rank 427; `planned`; lane `hard_mathlib_anchor_and_wrapper`; theorem incomplete |
| `jq -e . Stage1_Instances/THM-M-1247/intake.json` | 0 | Intake record is valid JSON |
| `rg -n 'THM-M-1247\|S56-M-1247-INTAKE' Stage1_Instances/THM-M-1247` | 0 | Expected item and theorem identifiers found in the dossier |
| `git diff --check -- Stage1_Instances/THM-M-1247` | 0 | No whitespace errors in the owned path |

These are intake-structural checks only. No Lean declaration exists in this phase, so no kernel
validation was applicable or claimed. `git status --short` also showed pre-existing modifications to
`Docs/Stage1_Blueprint_rev-5.6.md` and `Docs/Stage1_Execution_DAG_rev-5.6.json`; they were not modified.
