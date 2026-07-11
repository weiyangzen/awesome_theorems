# Intake validation record

Base revision: `fe07aee0ce546497b6b69c8f7dcf910f374c09b1`.

Commands were run from the repository root after creating the dossier:

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | `ok`; 15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 targets |
| `python3 scripts/stage1_target.py check` | 0 | `ok`; 1546 unique targets, ranks 1 through 1546, all L0/rework_required |
| `python3 scripts/stage1_target.py show THM-M-1276` | 0 | rank 327, planned, L0/rework_required, theorem_complete false |
| `python3 -m json.tool Stage1_Instances/THM-M-1276/intake.json` | 0 | JSON parsed successfully |
| dossier-local consistency check recorded by worker | 0 | item/theorem IDs, planned lifecycle, false completion, required files, and README boundary agree |
| `git diff --check -- Stage1_Instances/THM-M-1276` | 0 | no whitespace errors |

These are intake checks, not Lean elaboration or kernel evidence. No `.lean` target exists in this
phase, so the dependent statement gate remains open.
