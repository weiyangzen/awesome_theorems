# Intake validation record

Base revision: `c67df8af765ae58e38b6c8d4ce37668f5a600c6b`.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | `ok`: 15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 targets, execution skill present |
| `python3 scripts/stage1_target.py check` | 0 | `ok`: 1546 unique targets, ranks 1..1546, all L0/rework-required |
| `python3 scripts/stage1_target.py show THM-M-1257` | 0 | rank 435, planned, L0/rework-required, legacy artifacts unaccepted, theorem incomplete |
| `python3 -m json.tool Stage1_Instances/THM-M-1257/intake.json >/dev/null` | 0 | structured intake is valid JSON |
| `rg -n "\\b(sorry|admit)\\b|^\\s*axiom\\b" Stage1_Instances/THM-M-1257 --glob '*.lean'` | 1 | no Lean files or proof holes found; exit 1 is `rg`'s no-match result |
| `git diff --check -- Stage1_Instances/THM-M-1257 .stage1-worker-selftest.json` | 0 | no whitespace errors |

This is the smallest real validation for an intake-only node. No Lean file or declaration is
introduced, so no kernel result is claimed. Exact statement recovery, master acceptance, and every
dependent phase remain outstanding.
