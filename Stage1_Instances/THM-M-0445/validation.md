# Intake validation

Base revision: `1a30b84c1f86a2bbbf08b36f9afd06912b8f6c06`.

The worker ran these checks from the repository root:

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | `ok`; 1546 uniform-L0 Lean 4 targets and 15 assurance groups |
| `python3 scripts/stage1_target.py check` | 0 | `ok`; 1546 unique targets, ranks 1..1546 |
| `python3 scripts/stage1_target.py show THM-M-0445` | 0 | rank 91, `planned`, L0/rework required, theorem incomplete |

These are intake-only structural checks. No Lean declaration is claimed as the exact target, so a
Lean proof check would test a substituted statement and is intentionally not reported as evidence.
