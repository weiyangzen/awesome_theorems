# Intake validation

Base revision: `8e78e1b4206fc224e91466efb397811c09205b0e`.

All commands ran from the repository root on 2026-07-12 (Asia/Shanghai).

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | `ok`; 15 assurance groups and 1546 uniform-L0 targets |
| `python3 scripts/stage1_target.py check` | 0 | `ok`; 1546 unique targets, ranks 1..1546 |
| `python3 scripts/stage1_target.py show THM-M-1178` | 0 | rank 378, L0/rework-required, planned, theorem incomplete |

These are structural intake checks, not Lean theorem validation. No exact Lean target yet exists
because the source input is an umbrella label. The dossier is self-tested only for the assigned
intake deliverable; statement, anchor, proof, and release gates remain open.
