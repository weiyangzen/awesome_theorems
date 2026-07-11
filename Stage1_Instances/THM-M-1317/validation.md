# Intake validation

Base revision: `337a6bea341c0f1616a624ad03e440cb829e61e3`.

| Command | Result |
|---|---|
| `python3 Docs/tools/check_stage1_standard.py` | exit 0; standard reports 1546 uniform-L0 Lean 4 targets |
| `python3 scripts/stage1_target.py check` | exit 0; 1546 unique targets, ranks 1..1546 |
| `python3 scripts/stage1_target.py show THM-M-1317` | exit 0; rank 480, `planned`, `L0`, `rework_required`, lane `hard_mathlib_anchor_and_wrapper` |
| `python3 -m json.tool Stage1_Instances/THM-M-1317/intake.json` | exit 0 |
| `git diff --check -- Stage1_Instances/THM-M-1317` | exit 0 |

These checks validate membership, dossier structure at intake, JSON syntax, and whitespace only.
They do not elaborate a Lean proposition, validate the primary source, or establish proof closure.
