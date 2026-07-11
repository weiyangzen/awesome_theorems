# Intake validation record

Base revision: `056367be3b1cb2e101200085ec5a5fdff670d16b`

| Command | Result |
|---|---|
| `python3 Docs/tools/check_stage1_standard.py` | exit 0; `ok` with 1546 uniform-L0 Lean 4 targets |
| `python3 scripts/stage1_target.py check` | exit 0; 1546 unique targets and ranks 1..1546 |
| `python3 scripts/stage1_target.py show THM-M-1265` | exit 0; rank 442, `planned`, `L0`, `rework_required`, theorem incomplete |
| `python3 -m json.tool Stage1_Instances/THM-M-1265/intake.json >/dev/null` | exit 0 |
| dossier-local field/reference check recorded below | exit 0 |
| `git diff --check -- Stage1_Instances/THM-M-1265` | exit 0 |

The working tree already contained modifications to the generated blueprint and execution DAG.
They are outside this item's owned path and were not edited by this worker. These checks establish
only a structurally usable planned intake. The first theorem gate remains blocked because the
source phrase does not determine an exact mathematical proposition.
