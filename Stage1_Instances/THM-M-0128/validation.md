# Intake validation

Base revision: `478034dee4145f887a572a3c645a3a2ea81bc883`.

All commands below ran from the repository root and exited 0 on 2026-07-12:

```text
python3 Docs/tools/check_stage1_standard.py
  check_stage1_standard: ok (15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, execution skill present)
python3 scripts/stage1_target.py check
  stage1_target: ok (1546 unique targets, ranks 1..1546, all L0/rework_required)
python3 scripts/stage1_target.py show THM-M-0128
  rank 46; L0; rework_required true; lifecycle planned; theorem_complete false
python3 -m json.tool Stage1_Instances/THM-M-0128/intake.json >/dev/null
python3 -m json.tool Stage1_Instances/THM-M-0128/task-dag.json >/dev/null
git diff --check -- Stage1_Instances/THM-M-0128
```

An additional scoped `rg` check found the word `placeholder` only in two
warnings that reject the legacy placeholder-bearing structure. No Lean proof or
statement validation is claimed by these intake checks.

