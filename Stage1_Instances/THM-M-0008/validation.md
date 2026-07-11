# Intake validation

Base revision: `1a30b84c1f86a2bbbf08b36f9afd06912b8f6c06`.

Preflight on 2026-07-12:

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | `ok`: 15 assurance groups, 1546 uniform-L0 targets, skill present |
| `python3 scripts/stage1_target.py check` | 0 | `ok`: 1546 unique targets, ranks 1..1546, all L0/rework-required |
| `python3 scripts/stage1_target.py show THM-M-0008` | 0 | rank 101, planned, L0, theorem_complete false |

These are structural intake checks, not Lean proof validation. No canonical proposition exists yet,
so running the legacy Lean module would not validate an exact source statement. Final scoped JSON,
placeholder scan, and whitespace checks are recorded by the worker self-test manifest.
