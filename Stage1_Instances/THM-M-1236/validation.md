# Intake validation

Base revision: `c67df8af765ae58e38b6c8d4ce37668f5a600c6b`.

These checks validate the intake's structure and truthful blocker only; there is no Lean
proposition to elaborate.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | `ok (15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, execution skill present)` |
| `python3 scripts/stage1_target.py check` | 0 | `ok (1546 unique targets, ranks 1..1546, all L0/rework_required)` |
| `python3 scripts/stage1_target.py show THM-M-1236` | 0 | rank 419, baseline L0, `rework_required: true`, lifecycle `planned`, theorem incomplete |
| `python3 -m json.tool Stage1_Instances/THM-M-1236/intake.json` | 0 | valid JSON |
| `rg -n 'THM-M-1236\|intake.json\|source_statement_crosswalk.md\|validation.md' Stage1_Instances/THM-M-1236` | 0 | expected dossier-local anchors found |
| `git diff --check -- Stage1_Instances/THM-M-1236` | 0 | no whitespace errors |

Known failure: exact-claim identification is blocked because the catalog gives a concept rather
than a proposition. Consequently no Lean command is meaningful in this intake phase.
