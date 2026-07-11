# Statement validation

Validation evidence includes narrow kernel elaboration of the exact target and its checked definitional expansion. No proof of the Roth target is claimed.

Exact commands and results are appended after execution.

Base revision: `c6c14c0add140b98175266dc6421066ea99c79b3`.

| Command | Result |
|---|---|
| `python3 Docs/tools/check_stage1_standard.py` | exit 0; `ok` for 1546 uniform-L0 targets |
| `python3 scripts/stage1_target.py check` | exit 0; 1546 unique targets, ranks 1..1546 |
| `python3 scripts/stage1_target.py show THM-M-0398` | exit 0; rank 11, L0/rework_required, planned, theorem_complete false |
| `python3 -m json.tool Stage1_Instances/THM-M-0398/instance.json` | exit 0 |
| `python3 -m json.tool Stage1_Instances/THM-M-0398/task-dag.json` | exit 0 |
| `(cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0398/Statement.lean)` | exit 0; no output; exact target and interface checks elaborated |
| `rg -n '\\bsorry\\b|\\baxiom\\b|admit|placeholder' Stage1_Instances/THM-M-0398/Statement.lean` | exit 1; no forbidden proof construct found |
| `git diff --check -- Stage1_Instances/THM-M-0398` | exit 0; no output |

Known failures/open gates: page-level primary-source audit and independent review are open; no inhabitant of the canonical target, transitive trust audit, hermetic replay, or release evidence exists. These are downstream gates rather than failures of the assigned statement phase.
