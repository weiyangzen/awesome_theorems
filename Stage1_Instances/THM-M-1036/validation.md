# Intake validation record

Base revision: `c6aa0f2ba41dd389c2bcf01dd532923615781719`.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | `ok`: 15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 targets, skill present |
| `python3 scripts/stage1_target.py check` | 0 | `ok`: 1546 unique targets, ranks 1..1546, all L0/rework-required |
| `python3 scripts/stage1_target.py show THM-M-1036` | 0 | rank 229, planned, L0/rework-required, legacy artifacts unaccepted, theorem incomplete |
| `python3 -m json.tool Stage1_Instances/THM-M-1036/intake.json >/dev/null` | 0 | structured intake is valid JSON |
| `rg -n "sorry\\|axiom\\|placeholder" Stage1_Instances/THM-M-1036/{README.md,intake.json,source_statement_crosswalk.md}` | 1 | no forbidden tokens (`rg` returns 1 for no matches) |
| `git diff --check -- Stage1_Instances/THM-M-1036 .stage1-worker-selftest.json` | 0 | no scoped whitespace errors |

This validation is structural and dossier-local. No Lean declaration is
introduced, so no kernel proof is claimed. Exact statement, source acceptance,
all dependent phases, and master acceptance remain open.
