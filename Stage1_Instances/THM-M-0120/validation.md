# Intake validation

Validated on 2026-07-12 from base revision `478034dee4145f887a572a3c645a3a2ea81bc883`.

| Command | Result |
|---|---|
| `python3 Docs/tools/check_stage1_standard.py` | exit 0; 15 assurance groups, 41 legacy rows, 300 legacy slots, and 1546 uniform-L0 targets accepted |
| `python3 scripts/stage1_target.py check` | exit 0; 1546 unique targets, ranks 1..1546, all L0/rework_required |
| `python3 scripts/stage1_target.py show THM-M-0120` | exit 0; rank 39, planned lifecycle, legacy artifacts unaccepted, theorem incomplete |
| `python3 -m json.tool Stage1_Instances/THM-M-0120/instance.json` | exit 0 |
| `python3 -m json.tool Stage1_Instances/THM-M-0120/task-dag.json` | exit 0 |
| `git diff --check -- Stage1_Instances/THM-M-0120` | exit 0 |

This is structural and intake validation only. No Lean compilation is relevant yet because this phase deliberately creates no canonical Lean declaration or proof. Known open gates are exact source inspection, exact statement elaboration, anchor audit, obligation freezing, proof, and release validation.
