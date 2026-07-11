# Intake validation

Base revision: `478034dee4145f887a572a3c645a3a2ea81bc883`.

This record is completed by the worker after running the checks below. The checks cover intake
structure only; they do not validate a Lean statement or theorem proof.

| Command | Result |
|---|---|
| `python3 Docs/tools/check_stage1_standard.py` | exit 0: `ok` (15 assurance groups; 1546 uniform-L0 Lean 4 targets) |
| `python3 scripts/stage1_target.py check` | exit 0: `ok` (1546 unique targets, ranks 1..1546, all L0/rework_required) |
| `python3 scripts/stage1_target.py show THM-M-0131` | exit 0: rank 48, baseline L0, `rework_required: true`, lifecycle `planned`, theorem incomplete |
| `python3 -m json.tool Stage1_Instances/THM-M-0131/intake.json` | exit 0; JSON parsed |
| `git diff --check -- Stage1_Instances/THM-M-0131` | exit 0; no whitespace errors |
| `git status --short` | exit 0; only `?? Stage1_Instances/THM-M-0131/` was reported |
