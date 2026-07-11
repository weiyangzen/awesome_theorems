# Intake validation record

Base revision: `5997161aebf527e8a1e05724d4fbd4ce07dfd815`.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | `ok`: 15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 targets, execution skill present |
| `python3 scripts/stage1_target.py check` | 0 | `ok`: 1546 unique targets, ranks 1 through 1546, all L0/rework-required |
| `python3 scripts/stage1_target.py show THM-M-0432` | 0 | rank 60, planned, L0/rework-required, legacy artifacts unaccepted, theorem incomplete |
| `python3 -m json.tool Stage1_Instances/THM-M-0432/intake.json >/dev/null` | 0 | structured intake is valid JSON |
| `rg -n '(^|[[:space:]])(sorry|axiom)[[:space:]]' Stage1_Instances/THM-M-0432` | 1 | no Lean placeholder declarations or commands found; exit 1 means no matches |
| `rg -n 'THM-M-0432|S56-M-0432-INTAKE|StatementShape' Stage1_Instances/THM-M-0432` | 0 | dossier identifiers and discovery-target references are present |
| `git diff --check -- Stage1_Instances/THM-M-0432 .stage1-worker-selftest.json` | 0 | no whitespace errors |

This is intake-only validation. No Lean declaration is added or accepted, and no kernel proof result
is claimed. Exact statement elaboration is intentionally deferred because the source theorem variant
is unresolved.
