# Intake validation

Base revision: `d6333f8365b25d4e77164d475fe735a47cf1e37d`.

Commands run from the repository root on 2026-07-12:

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | `ok`: 15 assurance groups, 1546 uniform-L0 Lean 4 targets, execution skill present |
| `python3 scripts/stage1_target.py check` | 0 | `ok`: 1546 unique targets, ranks 1..1546, all L0/rework_required |
| `python3 scripts/stage1_target.py show THM-M-1061` | 0 | rank 504, planned, hard anchor/wrapper lane, theorem incomplete |
| `python3 -m json.tool Stage1_Instances/THM-M-1061/intake.json >/dev/null` | 0 | valid JSON |
| `rg -n 'sorry\|axiom\|placeholder\|fake results' Stage1_Instances/THM-M-1061 \|\| true` | 0 | no matches |
| `git diff --check -- Stage1_Instances/THM-M-1061` | 0 | no whitespace errors |

These are intake-level structural checks. No Lean target exists yet, so this receipt
does not claim elaboration, kernel checking, source acceptance, or theorem closure.
