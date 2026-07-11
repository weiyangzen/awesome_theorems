# Intake validation record

Base revision: `43b8783c62005322690acf2bed800ea3acbd76c6`.

The validation commands below check only manifest membership, repository-standard consistency,
structured dossier syntax, prohibited-token absence, and whitespace. No Lean theorem is introduced,
so no kernel closure is claimed.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | `ok`: 15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 targets, skill present |
| `python3 scripts/stage1_target.py check` | 0 | `ok`: 1546 unique targets, ranks 1..1546, all L0/rework-required |
| `python3 scripts/stage1_target.py show THM-M-0171` | 0 | rank 132, planned, L0/rework-required, legacy artifacts unaccepted, theorem incomplete |
| `python3 -m json.tool Stage1_Instances/THM-M-0171/intake.json >/dev/null` | 0 | structured intake is valid JSON |
| `rg -n '\\b(sorry\|axiom\|placeholder)\\b' Stage1_Instances/THM-M-0171` | 1 | no prohibited proof escape token found; exit 1 is `rg`'s no-match result |
| `git diff --check` | 0 | no whitespace errors |

This is the smallest real validation for an intake-only node. Master acceptance, source
identification, exact statement elaboration, and every proof and release gate remain outstanding.
