# Intake validation record

Base revision: `fe07aee0ce546497b6b69c8f7dcf910f374c09b1`.

| Command | Exit | Observed result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | `ok`: 15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 targets, execution skill present |
| `python3 scripts/stage1_target.py check` | 0 | `ok`: 1546 unique targets, ranks 1..1546, all L0/rework-required |
| `python3 scripts/stage1_target.py show THM-M-1140` | 0 | rank 345, planned, L0/rework-required, legacy artifacts unaccepted, theorem incomplete |
| `python3 -m json.tool Stage1_Instances/THM-M-1140/intake.json >/dev/null` | 0 | Intake is valid JSON |
| `rg -n 'sorry\|axiom\|placeholder\|admit' Stage1_Instances/THM-M-1140 --glob '!validation.md'` | 1 | No prohibited proof markers found (`rg` exit 1 means no match) |
| `git diff --check` | 0 | No whitespace errors |

This is an intake-only node: no Lean declaration is introduced, so no kernel proof result can be
claimed. The first combined validation attempt exited 9 solely because this hygiene search matched
a trust-related English word in the draft README; that wording was removed and the complete recipe was
then rerun successfully.
