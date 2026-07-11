# Intake validation record

Base revision: `478034dee4145f887a572a3c645a3a2ea81bc883`.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | `ok`: 15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 targets, execution skill present |
| `python3 scripts/stage1_target.py check` | 0 | `ok`: 1546 unique targets, ranks 1 through 1546, all L0/rework-required |
| `python3 scripts/stage1_target.py show THM-M-0140` | 0 | rank 56, planned, L0/rework-required, legacy artifacts unaccepted, theorem incomplete |
| `python3 -m json.tool Stage1_Instances/THM-M-0140/intake.json >/dev/null` | 0 | structured intake is valid JSON |
| `rg -n --glob '!validation.md' 'sorry\|axiom\|placeholder\|fake results' Stage1_Instances/THM-M-0140` | 1 | no matches; exit 1 is the expected ripgrep no-match result |
| `git diff --check -- Stage1_Instances/THM-M-0140 .stage1-worker-selftest.json` | 0 | no whitespace errors |

This is the smallest real validation for an intake-only node. No Lean theorem is introduced and no
kernel result is claimed. Node-specific master acceptance and all dependent phases remain open.
