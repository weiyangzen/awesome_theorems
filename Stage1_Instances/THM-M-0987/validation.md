# Intake validation record

Base revision: `c6aa0f2ba41dd389c2bcf01dd532923615781719`.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | standard structure passed: 1546 uniform-L0 targets and execution skill present |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all L0/rework-required |
| `python3 scripts/stage1_target.py show THM-M-0987` | 0 | rank 267, planned, L0/rework-required, legacy artifacts unaccepted, theorem incomplete |
| `python3 -m json.tool Stage1_Instances/THM-M-0987/intake.json >/dev/null` | 0 | structured intake is valid JSON |
| `rg -n '\bsorry\b\|\baxiom\b\|\badmit\b' Stage1_Instances/THM-M-0987` | 1 | no forbidden proof escape terms found (`rg` exit 1 means no matches) |
| `git diff --check` | 0 | no whitespace errors |

This is an intake-only node. No new Lean declaration is introduced, and no kernel, exact-statement,
source-fidelity, audit-completion, or theorem-completion result is claimed.
