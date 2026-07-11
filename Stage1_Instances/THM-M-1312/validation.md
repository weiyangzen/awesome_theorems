# Intake validation record

Base revision: `61369637c5db864082a624c34c62a91e6741f9da`

The following commands were run from the repository root. All returned exit
code 0 unless explicitly noted.

```text
python3 Docs/tools/check_stage1_standard.py
  check_stage1_standard: ok (15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, execution skill present)

python3 scripts/stage1_target.py check
  stage1_target: ok (1546 unique targets, ranks 1..1546, all L0/rework_required)

python3 scripts/stage1_target.py show THM-M-1312
  execution_rank=168; lifecycle_mode=planned; theorem_complete=false

python3 -m json.tool Stage1_Instances/THM-M-1312/intake.json >/dev/null
  exit 0

test "$(python3 -c 'import json; print(json.load(open("Stage1_Instances/THM-M-1312/intake.json"))["item_id"])')" = S56-M-1312-INTAKE
  exit 0

test -f Stage1_Instances/THM-M-1312/README.md && test -f Stage1_Instances/THM-M-1312/source_statement_crosswalk.md
  exit 0

git diff --check -- Stage1_Instances/THM-M-1312
  exit 0
```

This is intake-level structural evidence only. No Lean build was run because
the assigned phase deliberately does not accept or elaborate the legacy
candidate. The dependent statement phase owns that kernel check.
