# Intake validation

Base revision: `8e78e1b4206fc224e91466efb397811c09205b0e`.

All commands below exited `0`:

```text
python3 Docs/tools/check_stage1_standard.py
# check_stage1_standard: ok (15 assurance groups, 41 legacy rows, 300 legacy slots,
# 1546 uniform-L0 Lean 4 targets, execution skill present)

python3 scripts/stage1_target.py check
# stage1_target: ok (1546 unique targets, ranks 1..1546, all L0/rework_required)

python3 scripts/stage1_target.py show THM-M-1145
# rank 350; L0; rework_required true; planned; theorem_complete false

python3 -m json.tool Stage1_Instances/THM-M-1145/instance.json >/dev/null
python3 -m json.tool Stage1_Instances/THM-M-1145/task-dag.json >/dev/null
git diff --check -- Stage1_Instances/THM-M-1145
```

This is structural intake validation only. No Lean target exists in this phase, so no elaboration or
kernel proof was run or credited. Known failure/open gate: the exact source statement is not yet
identified; statement and every downstream task remain open.
