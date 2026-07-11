# Intake validation

Base revision: `5997161aebf527e8a1e05724d4fbd4ce07dfd815`.

The intake used these repository-root commands:

```text
python3 Docs/tools/check_stage1_standard.py
  exit 0: ok; 15 assurance groups, 1546 uniform-L0 Lean 4 targets
python3 scripts/stage1_target.py check
  exit 0: 1546 unique targets, ranks 1..1546, all L0/rework_required
python3 scripts/stage1_target.py show THM-M-0391
  exit 0: rank 5, planned, L0, rework_required=true, theorem_complete=false
python3 -m json.tool Stage1_Instances/THM-M-0391/instance.json
  exit 0
```

These checks validate intake structure and JSON syntax only. They do not elaborate Lean, validate a
proof, establish H0, or satisfy any statement/audit/proof/release node.
