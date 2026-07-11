# Intake validation record

Base revision: `2b65f3efa70ae08a8776a86771b091957de1652e`.

Executed from the repository root on 2026-07-12 (Asia/Shanghai):

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | `ok` with 15 assurance groups, 1546 uniform-L0 Lean 4 targets, and the execution skill present |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all `L0/rework_required` |
| `python3 scripts/stage1_target.py show THM-M-0544` | 0 | rank 109, lane `hard_mathlib_anchor_and_wrapper`, lifecycle `planned`, theorem incomplete |
| `python3 -m json.tool Stage1_Instances/THM-M-0544/intake.json` | 0 | JSON parsed successfully |
| `test "$(python3 -c 'import json; print(json.load(open("Stage1_Instances/THM-M-0544/intake.json"))["item_id"])')" = S56-M-0544-INTAKE` | 0 | dossier item identity matched |
| `for f in README.md intake.json source_statement_crosswalk.md; do test -s Stage1_Instances/THM-M-0544/$f; done` | 0 | all intake artifacts exist and are nonempty |
| `git diff --check -- Stage1_Instances/THM-M-0544` | 0 | no whitespace errors |

These are intake-only structural checks. No Lean target exists yet, so no elaboration, kernel proof,
axiom audit, or theorem receipt is asserted. The dependent statement phase owns the first Lean
validation.
