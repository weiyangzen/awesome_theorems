# Intake validation record

Base revision: `9c650bd6aac0dca129c8bc8ac01e0d7432669386`.

The following commands were run from the repository root on 2026-07-12 (Asia/Shanghai):

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | Standard structure passed: 15 assurance groups, 1546 uniform-L0 targets, execution skill present |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets with ranks 1 through 1546; all L0/rework-required |
| `python3 scripts/stage1_target.py show THM-M-0607` | 0 | Rank 254, planned lifecycle, theorem completion false |
| `python3 -m json.tool Stage1_Instances/THM-M-0607/intake.json` | 0 | Intake JSON parsed successfully |
| `python3 -c 'import json; d=json.load(open("/tmp/thm-m-0607-show.json")); assert d["theorem_id"]=="THM-M-0607" and d["execution_rank"]==254 and d["lifecycle_mode"]=="planned" and d["theorem_complete"] is False'` | 0 | Target identity and planned-state boundary matched |
| `! rg -n '\b(sorry\|admit\|axiom)\b' Stage1_Instances/THM-M-0607/{README.md,intake.json,source_statement_crosswalk.md}` | 0 | No forbidden proof placeholders in the substantive dossier files |
| `git diff --check -- Stage1_Instances/THM-M-0607` | 0 | No whitespace errors |

This is the smallest real validation for an intake with no elaborable target. It checks dossier
structure and target identity only. No Lean compilation is claimed because exact source recovery is
the explicitly recorded blocker to constructing a truthful Lean proposition.
