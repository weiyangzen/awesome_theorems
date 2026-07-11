# Intake validation record

Base revision: `8e78e1b4206fc224e91466efb397811c09205b0e`.

All commands ran from the repository root on 2026-07-12 and exited `0`:

```text
python3 -m json.tool Stage1_Instances/THM-M-1156/intake.json >/dev/null
python3 Docs/tools/check_stage1_standard.py
  check_stage1_standard: ok (15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, execution skill present)
python3 scripts/stage1_target.py check
  stage1_target: ok (1546 unique targets, ranks 1..1546, all L0/rework_required)
python3 scripts/stage1_target.py show THM-M-1156 >/tmp/thm1156-show.json
rg -n 'THM-M-1156|Newton位势与对数位势' Stage1_Instances/THM-M-1156 Docs/Stage0_Blueprint.md Docs/Stage1_Targets_rev-5.6.json >/tmp/thm1156-refs.txt
git diff --check -- Stage1_Instances/THM-M-1156
```

These checks validate the planned intake structure and its repository references only. No Lean
command is applicable because inventing an expression before source disambiguation would violate
the exact-statement gate. Known failure: the dependent statement phase is blocked by the absence of
a proposition-level primary source.
