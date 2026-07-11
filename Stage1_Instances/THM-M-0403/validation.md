# Intake validation record

Base revision: `478034dee4145f887a572a3c645a3a2ea81bc883`.

This record is completed by the commands below after dossier creation. It is
limited to the intake node; no Lean declaration or kernel closure is claimed.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | `ok`: 15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 targets, execution skill present |
| `python3 scripts/stage1_target.py check` | 0 | `ok`: 1546 unique targets, ranks 1..1546, all L0/rework-required |
| `python3 scripts/stage1_target.py show THM-M-0403` | 0 | rank 16, planned, L0/rework-required, legacy artifacts unaccepted, theorem incomplete |
| `python3 -m json.tool Stage1_Instances/THM-M-0403/intake.json >/dev/null` | 0 | structured intake is valid JSON |
| `rg -n <forbidden-proof-gap-pattern> README.md intake.json source_statement_crosswalk.md` | 1 | no forbidden proof-gap terms found in substantive intake artifacts; exit 1 is `rg`'s no-match result |
| `rg -n 'THM-M-0403\|S56-M-0403-INTAKE' Stage1_Instances/THM-M-0403` | 0 | dossier identity and owned-path references present |
| `git diff --check -- Stage1_Instances/THM-M-0403 .stage1-worker-selftest.json` | 0 | no whitespace errors |

These are the smallest real checks for an intake-only node. The statement,
anchor-audit, obligation-tree, proof, validation, release, and master-acceptance
gates remain outstanding.
