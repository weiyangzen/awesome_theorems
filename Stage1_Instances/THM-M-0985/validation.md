# Intake validation record

Base revision: `c6aa0f2ba41dd389c2bcf01dd532923615781719`.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | `ok`: 15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 targets, execution skill present |
| `python3 scripts/stage1_target.py check` | 0 | `ok`: 1546 unique targets, ranks 1..1546, all L0/rework-required |
| `python3 scripts/stage1_target.py show THM-M-0985` | 0 | rank 265, planned, L0/rework-required, legacy artifacts unaccepted, theorem incomplete |
| `python3 -m json.tool Stage1_Instances/THM-M-0985/intake.json >/dev/null` | 0 | structured intake is valid JSON |
| `test -f` for `README.md`, `source_statement_crosswalk.md`, and `intake.json` | 0 | required dossier artifacts exist |
| `! rg -nw 'sorry\|admit\|axiom\|placeholder\|THM-M-0387' Stage1_Instances/THM-M-0985/{README.md,intake.json,source_statement_crosswalk.md}` | 0 | no forbidden proof-hole token or copied fixture ID appears |
| `git diff --check` | 0 | no whitespace errors |

This is the smallest real validation for an intake-only node. It validates membership, standard
consistency, artifact structure, and honest status boundaries. No Lean declaration is introduced,
so no kernel result is claimed. Master acceptance and all dependent phases remain outstanding.
