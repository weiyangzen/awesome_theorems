# Intake validation record

Base revision: `9c650bd6aac0dca129c8bc8ac01e0d7432669386`.

This record covers the intake node only. No Lean declaration is introduced, so no kernel result is
claimed. The source-identity blocker is intentional and fail-closed.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | `ok`: 15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 targets, skill present |
| `python3 scripts/stage1_target.py check` | 0 | `ok`: 1546 unique targets, ranks 1..1546, all L0/rework-required |
| `python3 scripts/stage1_target.py show THM-M-1000` | 0 | rank 280, planned, L0/rework-required, legacy artifacts unaccepted, theorem incomplete |
| `python3 -m json.tool Stage1_Instances/THM-M-1000/intake.json >/dev/null` | 0 | structured intake is valid JSON |
| `rg -n 'sorry\|admit\|sorryAx\|axiom\|placeholder' Stage1_Instances/THM-M-1000 --glob '!validation.md'` | 1 | no forbidden proof escape or marker found (`rg` returns 1 for no matches) |
| `git diff --check -- Stage1_Instances/THM-M-1000 .stage1-worker-selftest.json` | 0 | no whitespace errors |
