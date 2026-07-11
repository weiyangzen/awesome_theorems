# Intake Validation

Base revision: `a8d6489fd935cd71fa4499f2f3f5b051998203f4`.

Executed from the repository root on 2026-07-12:

| Command | Exit | Result |
|---|---:|---|
| `python3 -m json.tool Stage1_Instances/THM-M-0412/instance.json >/dev/null` | 0 | Instance JSON parses |
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups; 1546 uniform-L0 targets; skill present |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1..1546 |
| `python3 scripts/stage1_target.py show THM-M-0412` | 0 | Rank 21, planned, L0/rework required, theorem incomplete |
| `rg -n "sorry\|admit\|axiom\|placeholder" Stage1_Instances/THM-M-0412` | 0 | No matches at validation time |
| `git diff --check` | 0 | No whitespace errors |

No Lean command was run because intake deliberately does not create or claim a canonical Lean
statement. The next statement gate is blocked on exact primary-source identity.
