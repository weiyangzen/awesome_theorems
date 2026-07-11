# Intake validation record

Base revision: `478034dee4145f887a572a3c645a3a2ea81bc883`.

All commands ran from the repository root on 2026-07-12 (Asia/Shanghai).

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | `ok`: 15 assurance groups, 1546 uniform-L0 targets, execution skill present |
| `python3 scripts/stage1_target.py check` | 0 | `ok`: 1546 unique targets, ranks 1..1546, all L0/rework_required |
| `python3 scripts/stage1_target.py show THM-M-0135` | 0 | rank 51, planned, L0/rework_required, theorem incomplete |
| `python3 -m json.tool Stage1_Instances/THM-M-0135/intake.json` | 0 | JSON parsed successfully |
| `git diff --check -- Stage1_Instances/THM-M-0135` | 0 | no whitespace errors |

The narrowest meaningful intake validation is structural because this phase deliberately does not
freeze or assert a Lean proposition. No Lean kernel result is claimed. Exact elaboration is blocked
until a numbered primary-source identity and its conventions are selected in the dependent
statement phase.
