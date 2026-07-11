# Intake validation record

Base revision: `c6aa0f2ba41dd389c2bcf01dd532923615781719`.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | Standard passed: 15 assurance groups, 1546 uniform-L0 targets, execution skill present |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1..1546, all L0/rework-required |
| `python3 scripts/stage1_target.py show THM-M-1057` | 0 | Rank 249, planned, L0, theorem incomplete |
| `python3 -m json.tool Stage1_Instances/THM-M-1057/intake.json` | 0 | Intake JSON parses |
| `git diff --check -- Stage1_Instances/THM-M-1057` | 0 | No whitespace errors |

These are the smallest real checks for this docs-and-structured-data intake. No Lean
proof validation is claimed: exact elaboration is owned by the dependent statement phase.
Known open gates are the statement fingerprint, environment pin, source premise/errata
audit, frozen obligation graphs, proof closure, and all release validation.
