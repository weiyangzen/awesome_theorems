# Intake validation record

Base revision: `8e78e1b4206fc224e91466efb397811c09205b0e`.

This intake introduces no Lean declaration. Its smallest real validation is
the repository's structural preflight plus JSON and owned-path hygiene checks.
Exact commands and results are recorded after execution below.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | `ok`: 15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, execution skill present |
| `python3 scripts/stage1_target.py check` | 0 | `ok`: 1546 unique targets, ranks 1..1546, all L0/rework-required |
| `python3 scripts/stage1_target.py show THM-M-1176` | 0 | Rank 376; planned; L0/rework-required; historical artifacts unaccepted; theorem incomplete |
| `python3 -m json.tool Stage1_Instances/THM-M-1176/intake.json >/dev/null` | 0 | Structured intake is valid JSON |
| `rg -n '\b(sorry\|axiom\|placeholder)\b' Stage1_Instances/THM-M-1176` | 1 | No forbidden proof escape terms found; exit 1 is `rg`'s no-match result |
| `git diff --check` | 0 | No whitespace errors |

The combined validation shell returned exit 0. These checks establish intake
structure and repository membership only. Kernel evidence is inapplicable
because this phase intentionally creates no formal statement or proof.
