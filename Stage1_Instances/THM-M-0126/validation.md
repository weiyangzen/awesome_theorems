# Intake validation record

Base revision: `478034dee4145f887a572a3c645a3a2ea81bc883`.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | `ok`: 15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 targets, skill present |
| `python3 scripts/stage1_target.py check` | 0 | `ok`: 1546 unique targets, ranks 1..1546, all L0/rework-required |
| `python3 scripts/stage1_target.py show THM-M-0126` | 0 | rank 45, planned, L0/rework-required, legacy artifacts unaccepted, theorem incomplete |
| `python3 -m json.tool Stage1_Instances/THM-M-0126/intake.json >/dev/null` | 0 | structured intake is valid JSON |
| `test -f` for `README.md` and `source_statement_crosswalk.md` | 0 | required dossier and crosswalk artifacts exist |
| `rg -n '\bsorry\b|\baxiom\b' Stage1_Instances/THM-M-0126` with no-match assertion | 0 | no forbidden Lean escape markers found (`rg` returned 1 as expected) |
| `git diff --check` | 0 | no whitespace errors |

These checks establish membership, repository consistency, and dossier structure only. No Lean
declaration was introduced, and no kernel result is claimed.
