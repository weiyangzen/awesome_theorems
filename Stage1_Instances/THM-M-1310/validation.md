# Intake validation record

Base revision: `337a6bea341c0f1616a624ad03e440cb829e61e3`.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | `ok`: 15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, skill present |
| `python3 scripts/stage1_target.py check` | 0 | `ok`: 1546 unique targets, ranks 1..1546, all L0/rework-required |
| `python3 scripts/stage1_target.py show THM-M-1310` | 0 | rank 477, planned, L0/rework-required, legacy artifacts unaccepted, theorem incomplete |
| `python3 -m json.tool Stage1_Instances/THM-M-1310/intake.json >/dev/null` | 0 | Structured intake is valid JSON |
| `python3 -c 'from pathlib import Path; p=Path("Stage1_Instances/THM-M-1310"); required={"README.md","intake.json","source_statement_crosswalk.md","validation.md"}; assert required <= {x.name for x in p.iterdir()}; text="\\n".join(x.read_text() for x in p.iterdir() if x.is_file()); assert "THM-M-1310" in text and "THM-M-1311" in text and "THM-M-1312" in text'` | 0 | Required files exist and target/neighbor boundaries are explicit |
| `git diff --check -- Stage1_Instances/THM-M-1310` | 0 | No whitespace errors |

This is intake-only structural validation. No Lean declaration is introduced because the source
label has not yet been converted into an eligible exact proposition. Consequently there is no
honest kernel command for this phase. Exact statement elaboration and all proof gates remain open.
