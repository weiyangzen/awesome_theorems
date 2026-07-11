# Intake validation record

Base revision: `594dbb735284e7b81f51ce813a9c3200fd55f610`.

The validation commands below test only this planned intake's structural boundary. No Lean file or
kernel proof is introduced, because the exact source theorem is not identified.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | `ok`: 15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 targets, execution skill present |
| `python3 scripts/stage1_target.py check` | 0 | `ok`: 1546 unique targets, ranks 1..1546, all L0/rework-required |
| `python3 scripts/stage1_target.py show THM-M-1541` | 0 | rank 202, planned, L0/rework-required, legacy artifacts unaccepted, theorem incomplete |
| `python3 -m json.tool Stage1_Instances/THM-M-1541/intake.json >/dev/null` | 0 | structured intake is valid JSON |
| `rg -n "sorry\|admit\|sorryAx" Stage1_Instances/THM-M-1541/{README.md,intake.json,source_statement_crosswalk.md}` | 1 | no forbidden proof-hole tokens found (`rg` exit 1 means no matches) |
| `git diff --check -- Stage1_Instances/THM-M-1541` | 0 | no whitespace errors |

The broader discovery scan for `axiom`/`placeholder` matched only truthful English descriptions of
the open foundation profile and the nearby axiomatized artifact; this dossier contains no Lean
declaration. The exact-statement gate remains blocked as recorded, while the intake node itself is
self-tested and ready for master review.
