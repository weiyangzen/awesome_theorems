# Intake validation

Base revision: `1a30b84c1f86a2bbbf08b36f9afd06912b8f6c06`.

All commands below were run from the repository root on 2026-07-12.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | `ok`: 15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 targets, execution skill present |
| `python3 scripts/stage1_target.py check` | 0 | `ok`: 1546 unique targets, ranks 1..1546, all L0/rework_required |
| `python3 scripts/stage1_target.py show THM-M-0438` | 0 | Rank 86, planned, L0/rework_required, legacy artifacts unaccepted, theorem incomplete |
| `python3 -m json.tool Stage1_Instances/THM-M-0438/intake.json >/dev/null` | 0 | Intake JSON parses |
| `rg -n "sorry\|axiom\|placeholder\|theorem_complete.*true" Stage1_Instances/THM-M-0438` | 0 | One prose occurrence of `axioms`; no Lean proof, placeholder, or completion claim is present |
| `git diff --check -- Stage1_Instances/THM-M-0438` | 0 | No whitespace errors |

This validates dossier structure and repository membership only. No Lean build is appropriate for
the intake gate: the exact source statement is still unidentified and the legacy Lean candidate is
explicitly ineligible for statement or proof credit.
