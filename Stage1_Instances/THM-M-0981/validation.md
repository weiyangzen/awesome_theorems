# Intake validation

Base revision: `c6aa0f2ba41dd389c2bcf01dd532923615781719`.

All commands below ran from the repository root on 2026-07-12 and exited 0:

- `python3 Docs/tools/check_stage1_standard.py` reported `ok`, including 1546 uniform-L0 targets.
- `python3 scripts/stage1_target.py check` reported 1546 unique targets, ranks 1 through 1546.
- `python3 scripts/stage1_target.py show THM-M-0981` confirmed rank 261, `planned`, L0/rework-required membership.
- `python3 -m json.tool Stage1_Instances/THM-M-0981/intake.json` accepted the structured intake.
- `rg -n 'THM-M-0981|S56-M-0981-INTAKE|StatementShape' Stage1_Instances/THM-M-0981` confirmed dossier-local identifiers and target references.
- `if rg -n '\b(sorry|axiom|admit)\b' Stage1_Instances/THM-M-0981; then exit 1; fi` found no forbidden proof placeholders.
- `git diff --check -- Stage1_Instances/THM-M-0981` reported no whitespace errors.

These are intake-structure checks only. Lean elaboration and all downstream theorem gates remain open.
