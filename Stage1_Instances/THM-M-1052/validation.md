# Intake validation record

Base revision: `dbd29db42090d2fce49f69d84d4631769ef7e9c3`.

| Command | Exit | Observed result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | `ok`: 15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, execution skill present |
| `python3 scripts/stage1_target.py check` | 0 | `ok`: 1546 unique targets, ranks 1..1546, all L0/rework-required |
| `python3 scripts/stage1_target.py show THM-M-1052` | 0 | rank 219; planned; L0/rework-required; legacy artifacts unaccepted; theorem incomplete |
| `python3 -m json.tool Stage1_Instances/THM-M-1052/intake.json >/dev/null` | 0 | intake is valid JSON |
| `rg -n '\bsorry\b|\baxiom[[:space:]]+[A-Za-z_]|\bplaceholder\b|"theorem_complete"[[:space:]]*:[[:space:]]*true' Stage1_Instances/THM-M-1052/{README.md,intake.json,source_statement_crosswalk.md}` | 1 | no forbidden proof construct or false completion flag (`rg` exit 1 means no matches) |
| `git diff --check -- Stage1_Instances/THM-M-1052 .stage1-worker-selftest.json` | 0 | no whitespace errors |

This is the smallest real validation for the intake-only node. It introduces no
Lean declaration, so no kernel-proof result is claimed. Exact statement,
source, proof, and master-acceptance gates remain open.
