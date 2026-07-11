# Intake validation record

Base revision: `fe07aee0ce546497b6b69c8f7dcf910f374c09b1`.

This record is completed by the validation run for this intake. It covers only manifest,
repository-standard, JSON, reference, and whitespace checks; no Lean declaration is introduced.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | `ok`: 15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, execution skill present |
| `python3 scripts/stage1_target.py check` | 0 | `ok`: 1546 unique targets, ranks 1..1546, all L0/rework-required |
| `python3 scripts/stage1_target.py show THM-M-1138` | 0 | rank 343, planned, L0/rework-required, historical label untrusted, theorem incomplete |
| `python3 -m json.tool Stage1_Instances/THM-M-1138/intake.json >/dev/null` | 0 | structured intake parses as JSON |
| `rg -n '\b(sorry\|axiom)\b\|placeholder\|fake results' Stage1_Instances/THM-M-1138` | 1 | no forbidden-token match (`rg` exit 1 denotes no matches) |
| `git diff --check` | 0 | no whitespace errors |

The first failed theorem gate remains exact statement elaboration. Master acceptance and all
dependent nodes remain outstanding.
