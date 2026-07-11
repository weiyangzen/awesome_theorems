# Intake validation record

Base revision: `ef0dd4cd5367b81a98b8906e3325b55fe5263491`.

All commands were run from the repository root on 2026-07-12 (Asia/Shanghai).

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | `ok`; 15 assurance groups and 1546 uniform-L0 Lean 4 targets |
| `python3 scripts/stage1_target.py check` | 0 | `ok`; 1546 unique targets, ranks 1..1546 |
| `python3 scripts/stage1_target.py show THM-M-1288` | 0 | rank 459, lane `hard_mathlib_anchor_and_wrapper`, lifecycle `planned`, theorem incomplete |
| `python3 -m json.tool Stage1_Instances/THM-M-1288/intake.json` | 0 | valid JSON |
| `test "$(python3 -c 'import json; print(json.load(open("Stage1_Instances/THM-M-1288/intake.json"))["item_id"])')" = S56-M-1288-INTAKE` | 0 | item identity matches assignment |
| `rg -q 'THM-M-1288' Stage1_Instances/THM-M-1288/README.md Stage1_Instances/THM-M-1288/intake.json` | 0 | dossier identity references present |
| `git diff --check -- Stage1_Instances/THM-M-1288` | 0 | no whitespace errors |

These are intake structural checks. No Lean file exists and no elaboration,
kernel proof, source download, formula verification, or theorem-completion gate
was tested. Known open gates are listed in the dossier; the first is the exact
statement/elaboration gate.
