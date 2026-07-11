# Intake validation record

Base revision: `8046f7febfe203ec958fa24e111f6b730ad8393b`.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | `ok` with 15 assurance groups, 1546 uniform-L0 targets, and execution skill present |
| `python3 scripts/stage1_target.py check` | 0 | `ok`: 1546 unique targets, ranks 1..1546, all L0/rework_required |
| `python3 scripts/stage1_target.py show THM-M-1306` | 0 | rank 474, planned, L0/rework_required, theorem incomplete |

The dossier-specific syntax and reference checks are recorded by the worker self-test after the
files exist. No Lean command is applicable: the exact proposition is deliberately unresolved, and
inventing an elaboration target would violate the intake gate.
