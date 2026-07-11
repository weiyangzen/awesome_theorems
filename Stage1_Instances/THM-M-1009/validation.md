# Intake validation record

Base revision: `2d0ac727836c39cd946970b1ba5903ae1cd8f79d`.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | `ok`: 15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 targets, execution skill present |
| `python3 scripts/stage1_target.py check` | 0 | `ok`: 1546 unique targets, ranks 1..1546, all L0/rework-required |
| `python3 scripts/stage1_target.py show THM-M-1009` | 0 | rank 289, planned, L0/rework-required, legacy artifacts unaccepted, theorem incomplete |
| `python3 -m json.tool Stage1_Instances/THM-M-1009/intake.json >/dev/null` | 0 | structured intake is valid JSON |
| `rg -n '\b(sorry|admit)\b|(^|[^A-Za-z])axiom[[:space:]]+[A-Za-z_]' Stage1_Instances/THM-M-1009` | 1 | no proof placeholders or axiom declarations (`rg` exit 1 means no match) |
| `git diff --check` | 0 | no whitespace errors |

This is the smallest real validation for an intake-only node. No new Lean
declaration is introduced, so compiling the legacy candidate would not test an
artifact created by this phase. Exact elaboration and kernel evidence remain
the responsibility of dependent phases. Master acceptance remains outstanding.
