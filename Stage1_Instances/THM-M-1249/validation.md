# Intake validation record

Base revision: `c67df8af765ae58e38b6c8d4ce37668f5a600c6b`.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | `ok`: 15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, execution skill present |
| `python3 scripts/stage1_target.py check` | 0 | `ok`: 1546 unique targets, ranks 1..1546, all L0/rework-required |
| `python3 scripts/stage1_target.py show THM-M-1249` | 0 | rank 429, planned, L0/rework-required, historical artifacts unaccepted, theorem incomplete |
| `python3 -m json.tool Stage1_Instances/THM-M-1249/intake.json >/dev/null` | 0 | structured intake is valid JSON |
| `rg -n '\bsorry\b\|\baxiom\b\|placeholder\|fake results' Stage1_Instances/THM-M-1249` | 1 | no forbidden proof devices or result claims found (`rg` uses exit 1 for no matches) |
| `git diff --check -- Stage1_Instances/THM-M-1249` | 0 | no whitespace errors |

This is an intake-only node and introduces no Lean declaration. Therefore a Lean kernel check would
not validate the actual deliverable. Exact statement elaboration is deliberately deferred because
the supplied target is an umbrella subject rather than a proposition.
