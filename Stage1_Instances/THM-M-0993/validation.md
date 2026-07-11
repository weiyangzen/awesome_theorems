# Intake validation

Base revision: `c6aa0f2ba41dd389c2bcf01dd532923615781719`.

Commands and results:

```text
python3 Docs/tools/check_stage1_standard.py
  exit 0: ok; 1546 uniform-L0 Lean 4 targets
python3 scripts/stage1_target.py check
  exit 0: ok; 1546 unique targets, ranks 1..1546
python3 scripts/stage1_target.py show THM-M-0993
  exit 0: rank 273, lifecycle planned, theorem_complete false
python3 -m json.tool Stage1_Instances/THM-M-0993/intake.json
  exit 0
python3 -c "import json; p=json.load(open('Stage1_Instances/THM-M-0993/intake.json')); assert p['item_id']=='S56-M-0993-INTAKE' and p['theorem_id']=='THM-M-0993' and p['lifecycle_mode']=='planned' and p['theorem_complete'] is False"
  exit 0
git diff --check -- Stage1_Instances/THM-M-0993
  exit 0
```

These validate intake structure only. No Lean statement or proof is claimed.

