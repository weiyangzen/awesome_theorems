# Intake validation

Base revision: `7a8e792e568c85805fef02f4071bcc4b5ac9e09d`.

Commands run from the repository root:

```text
python3 Docs/tools/check_stage1_standard.py
  exit 0: check_stage1_standard: ok (15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, execution skill present)
python3 scripts/stage1_target.py check
  exit 0: stage1_target: ok (1546 unique targets, ranks 1..1546, all L0/rework_required)
python3 scripts/stage1_target.py show THM-M-1209
  exit 0: execution rank 402; lane hard_mathlib_anchor_and_wrapper; lifecycle planned; theorem_complete false
python3 -m json.tool Stage1_Instances/THM-M-1209/intake.json >/dev/null
  exit 0
python3 <dossier-local reference check recorded by the worker>
  exit 0: dossier references: ok
git diff --check -- Stage1_Instances/THM-M-1209
  exit 0
```

No Lean command is appropriate at intake because no declaration or expression has yet been frozen.
This is a known open statement-phase gate, not proof evidence.
