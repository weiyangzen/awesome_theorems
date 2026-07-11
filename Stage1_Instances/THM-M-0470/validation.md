# Intake validation record

Base revision: `2d0ac727836c39cd946970b1ba5903ae1cd8f79d`

All commands below ran from the repository root on 2026-07-12 (Asia/Shanghai).

| Command | Exit | Result |
|---|---:|---|
| `python3 -m json.tool Stage1_Instances/THM-M-0470/intake.json >/dev/null` | 0 | Intake JSON parsed successfully |
| `python3 Docs/tools/check_stage1_standard.py` | 0 | `ok`: 15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, execution skill present |
| `python3 scripts/stage1_target.py check` | 0 | `ok`: 1546 unique targets, ranks 1..1546, all L0/rework_required |
| `python3 scripts/stage1_target.py show THM-M-0470` | 0 | Rank 316; planned; L0/rework_required; theorem_complete false |
| `rg -n "THM-M-0470\|Ullmo\|Bogomolov\|M-0470" Stage1_Instances/THM-M-0470` | 0 | Dossier identifiers and cross-references found |
| `git diff --check -- Stage1_Instances/THM-M-0470` | 0 | No whitespace errors |

This is the smallest real validation for the intake phase. No Lean command is recorded because
intake intentionally has no Lean module or declaration; elaboration is owned by the dependent
statement phase. The checks do not establish H0, M0, theorem completion, or master acceptance.
