# Intake validation record

Base revision: `8e78e1b4206fc224e91466efb397811c09205b0e`.

The following commands were run from the repository root on 2026-07-12 (Asia/Shanghai):

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | `ok`: 15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 targets |
| `python3 scripts/stage1_target.py check` | 0 | `ok`: 1546 unique targets, ranks 1..1546, all L0/rework_required |
| `python3 scripts/stage1_target.py show THM-M-1188` | 0 | rank 383; planned; L0/rework_required; hard_mathlib_anchor_and_wrapper |
| `python3 -m json.tool Stage1_Instances/THM-M-1188/intake.json` | 0 | valid JSON |
| dossier-local reference checker (recorded in worker self-test) | 0 | every `public_merge_targets` path exists and theorem/item IDs agree |
| `git diff --check -- Stage1_Instances/THM-M-1188` | 0 | no whitespace errors |

These are the smallest real checks appropriate to an intake-only node. No Lean target exists in this
phase, so no Lean compilation was claimed or performed. The statement gate, source audit, proof, and
release gates remain open.
