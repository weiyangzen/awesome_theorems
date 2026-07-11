# Intake validation record

Base revision: `c67df8af765ae58e38b6c8d4ce37668f5a600c6b`.

The exact commands and results are recorded after validation below. These checks cover only manifest
membership, rev-5.6 structural consistency, dossier JSON syntax, and local hygiene. No Lean theorem
was introduced, so no kernel-proof result is claimed.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | `ok`: 15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 targets, execution skill present |
| `python3 scripts/stage1_target.py check` | 0 | `ok`: 1546 unique targets, ranks 1..1546, all L0/rework-required |
| `python3 scripts/stage1_target.py show THM-M-1250` | 0 | rank 430, planned, L0/rework-required, legacy artifacts unaccepted, theorem incomplete |
| `python3 -m json.tool Stage1_Instances/THM-M-1250/intake.json >/dev/null` | 0 | intake record is valid JSON |
| `rg -n "sorry\|axiom\|placeholder" Stage1_Instances/THM-M-1250/{README.md,intake.json,source_statement_crosswalk.md}` | 1 | no forbidden-token matches (`rg` uses exit 1 for no matches) |
| `git diff --check -- Stage1_Instances/THM-M-1250` | 0 | no whitespace errors |

The intake node is self-tested. Master acceptance and all dependent statement, audit, proof, and
release gates remain outstanding.
