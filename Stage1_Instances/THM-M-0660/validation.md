# Intake validation record

Base revision: `9c650bd6aac0dca129c8bc8ac01e0d7432669386`.

The intake was checked with:

```text
python3 Docs/tools/check_stage1_standard.py
# exit 0: check_stage1_standard: ok (15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, execution skill present)

python3 scripts/stage1_target.py check
# exit 0: stage1_target: ok (1546 unique targets, ranks 1..1546, all L0/rework_required)

python3 scripts/stage1_target.py show THM-M-0660
# exit 0: rank 299, planned, L0/rework_required, theorem_complete false

python3 -m json.tool Stage1_Instances/THM-M-0660/intake.json >/dev/null
# exit 0

git diff --check -- Stage1_Instances/THM-M-0660
# exit 0
```

These are structural intake checks. No Lean command is applicable because selecting a formal
expression before identifying the source theorem would be a substituted-statement error.
