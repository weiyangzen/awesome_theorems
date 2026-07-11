# Intake validation record

Base revision: `9c650bd6aac0dca129c8bc8ac01e0d7432669386`.

All commands ran from the repository root on 2026-07-12 (Asia/Shanghai).

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | `ok`: 15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 targets, execution skill present |
| `python3 scripts/stage1_target.py check` | 0 | `ok`: 1546 unique targets, ranks 1..1546, all L0/rework_required |
| `python3 scripts/stage1_target.py show THM-M-0652` | 0 | rank 298; lane `hard_statement_first_partial_verification`; lifecycle `planned`; theorem incomplete |
| `python3 -m json.tool Stage1_Instances/THM-M-0652/intake.json` | 0 | intake JSON parsed successfully |
| `rg -n 'THM-M-0652\|S56-M-0652-INTAKE\|StatementShape' Stage1_Instances/THM-M-0652` | 0 | required item, theorem, and candidate declaration references found |
| `git diff --check -- Stage1_Instances/THM-M-0652` | 0 | no whitespace errors |

This is the smallest real validation appropriate to an intake-only node. No Lean compilation is
credited: exact elaboration is owned by the dependent statement node. Known open gates are the
normalized expression and environment fingerprints, exact common-vocabulary semantics, checked
transports and mutations, primary-source pin/audit, obligation registry, proof, and release.
