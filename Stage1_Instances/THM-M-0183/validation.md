# Intake validation

Base revision: `43b8783c62005322690acf2bed800ea3acbd76c6`.

Executed from the worker clone on 2026-07-12:

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | `ok`: 15 assurance groups, 1546 uniform-L0 targets, execution skill present |
| `python3 scripts/stage1_target.py check` | 0 | `ok`: 1546 unique targets, ranks 1..1546, all L0/rework_required |
| `python3 scripts/stage1_target.py show THM-M-0183` | 0 | rank 130, lane `hard_mathlib_anchor_and_wrapper`, lifecycle `planned`, theorem complete false |
| `python3 -m json.tool Stage1_Instances/THM-M-0183/instance.json` | 0 | valid JSON |
| `python3 -m json.tool Stage1_Instances/THM-M-0183/task-dag.json` | 0 | valid JSON |
| `git diff --check -- Stage1_Instances/THM-M-0183` | 0 | no whitespace errors |

This validates a dossier-shaped planned intake and its open DAG only. No Lean source exists in this
phase, so no kernel command is applicable. Primary-source page/errata inspection and all statement,
anchor, proof, and release gates remain open.
