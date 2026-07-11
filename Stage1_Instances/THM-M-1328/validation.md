# Intake validation

Base revision: `7ea3aa8c0960c44b00d62639e9ddf1321848e342`.

All commands below ran from the worker clone root on 2026-07-12 and exited `0`:

```text
python3 Docs/tools/check_stage1_standard.py
  check_stage1_standard: ok (15 assurance groups, 41 legacy rows, 300 legacy slots,
  1546 uniform-L0 Lean 4 targets, execution skill present)

python3 scripts/stage1_target.py check
  stage1_target: ok (1546 unique targets, ranks 1..1546, all L0/rework_required)

python3 scripts/stage1_target.py show THM-M-1328
  execution_rank=490; baseline=L0; rework_required=true; lifecycle_mode=planned;
  theorem_complete=false

python3 -m json.tool Stage1_Instances/THM-M-1328/instance.json >/dev/null
python3 -m json.tool Stage1_Instances/THM-M-1328/task-dag.json >/dev/null
git diff --check -- Stage1_Instances/THM-M-1328
  (no output)
```

This is structural intake validation only. No Lean target exists yet because the source statement is
not uniquely identified, so no Lean/kernel command is applicable to this phase. Known failure:
statement identity and the source-exact formula remain blocked as recorded in the crosswalk. This
does not prevent the deliberately `planned`, all-open intake from being self-tested.

