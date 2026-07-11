# Intake validation record

Base revision: `2b65f3efa70ae08a8776a86771b091957de1652e`.

The preflight standard and manifest checks passed before dossier creation. Exact commands and final
results are listed below; these validate intake structure only and provide no kernel-proof credit.

| Command | Expected result |
|---|---|
| `python3 Docs/tools/check_stage1_standard.py` | exit 0; 1546 uniform-L0 targets and execution skill accepted |
| `python3 scripts/stage1_target.py check` | exit 0; 1546 unique ranks, all L0/rework-required |
| `python3 scripts/stage1_target.py show THM-M-1186` | exit 0; rank 151, planned, theorem incomplete |
| `python3 -m json.tool Stage1_Instances/THM-M-1186/intake.json >/dev/null` | exit 0; valid JSON |
| `rg -n 's[o]rry|a[x]iom|p[l]aceholder' Stage1_Instances/THM-M-1186` | exit 1; no forbidden proof markers (the expected no-match status) |
| `git diff --check -- Stage1_Instances/THM-M-1186` | exit 0; no whitespace errors |
