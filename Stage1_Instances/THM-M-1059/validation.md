# Intake validation

Base revision: `c6aa0f2ba41dd389c2bcf01dd532923615781719`.

The following commands were run from the repository root. All exited 0:

```text
python3 Docs/tools/check_stage1_standard.py
python3 scripts/stage1_target.py check
python3 scripts/stage1_target.py show THM-M-1059
python3 -m json.tool Stage1_Instances/THM-M-1059/intake.json
git diff --check -- Stage1_Instances/THM-M-1059
```

The standard checker reported 15 assurance groups, 1546 uniform-L0 targets, and an available
execution skill. The target checker reported 1546 unique targets at ranks 1 through 1546. The target
query confirmed execution rank 251, `planned`, `L0`, and `theorem_complete: false`. JSON parsing and
whitespace validation succeeded. These checks validate intake structure only; no Lean build applies
because this phase intentionally creates no Lean declaration.
