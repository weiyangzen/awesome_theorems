# Intake validation record

Base revision: `2b65f3efa70ae08a8776a86771b091957de1652e`.

Commands were run from the repository root on 2026-07-12:

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | `ok`: 15 assurance groups, 1546 uniform-L0 Lean 4 targets, execution skill present |
| `python3 scripts/stage1_target.py check` | 0 | `ok`: 1546 unique targets, ranks 1..1546, all L0/rework_required |
| `python3 scripts/stage1_target.py show THM-M-1168` | 0 | Rank 145, planned lifecycle, hard anchor/wrapper lane, theorem incomplete |
| `python3 -m json.tool Stage1_Instances/THM-M-1168/intake.json` | 0 | Intake JSON parsed successfully |
| `git diff --check -- Stage1_Instances/THM-M-1168` | 0 | No whitespace errors |

No Lean command is applicable to this intake node: the exact source statement is
not identified, and this phase intentionally creates no Lean declaration. These
checks validate the dossier structure, not the mathematical theorem or a
canonical statement.
