# Intake validation

Base revision: `ef0dd4cd5367b81a98b8906e3325b55fe5263491`.

All commands ran from the repository root on 2026-07-12:

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | `ok`: 15 assurance groups and 1546 uniform-L0 targets |
| `python3 scripts/stage1_target.py check` | 0 | `ok`: 1546 unique targets, ranks 1..1546 |
| `python3 scripts/stage1_target.py show THM-M-1291` | 0 | rank 462, `planned`, `L0/rework_required`, theorem incomplete |
| `python3 -m json.tool Stage1_Instances/THM-M-1291/intake.json` | 0 | valid JSON |
| `rg -n "sorry\|axiom\|placeholder\|admit" Stage1_Instances/THM-M-1291` | 0 | only the descriptive word `axioms` in the open TCB profile; no Lean proof or forbidden construct exists |
| `git diff --check -- Stage1_Instances/THM-M-1291` | 0 | no whitespace errors |

These checks establish only manifest/standard consistency, JSON syntax, and
dossier hygiene. There is deliberately no Lean proof at intake, so they do not
establish statement elaboration or theorem closure.
