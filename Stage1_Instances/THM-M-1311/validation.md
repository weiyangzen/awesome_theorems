# Intake validation record

Base revision: `61369637c5db864082a624c34c62a91e6741f9da`.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | `ok`: 15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, execution skill present |
| `python3 scripts/stage1_target.py check` | 0 | `ok`: 1546 unique targets, ranks 1..1546, all L0/rework-required |
| `python3 scripts/stage1_target.py show THM-M-1311` | 0 | rank 167, planned, L0/rework-required, legacy artifacts unaccepted, theorem incomplete |
| `python3 -m json.tool Stage1_Instances/THM-M-1311/intake.json >/dev/null` | 0 | Structured intake is valid JSON |
| `python3 -c 'from pathlib import Path; p=Path("Stage1_Instances/THM-M-1311"); required={"README.md","intake.json","source_statement_crosswalk.md","validation.md"}; assert required <= {x.name for x in p.iterdir()}; text="\\n".join(x.read_text() for x in p.iterdir() if x.is_file()); assert "THM-M-1311" in text and "THM-M-1312" in text'` | 0 | Required dossier files exist and the target/exclusion IDs are explicit |
| `git diff --check -- Stage1_Instances/THM-M-1311` | 0 | No whitespace errors |

This is intake-only structural validation. No Lean declaration is introduced, so there is no honest
kernel command to run at this phase. Exact statement elaboration and all proof gates remain open.
