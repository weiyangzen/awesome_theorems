# Intake validation

Validated on 2026-07-12 from base revision
`478034dee4145f887a572a3c645a3a2ea81bc883`.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | `ok`: 15 assurance groups and 1546 uniform-L0 targets |
| `python3 scripts/stage1_target.py check` | 0 | `ok`: 1546 unique targets, ranks 1 through 1546 |
| `python3 scripts/stage1_target.py show THM-M-0116` | 0 | rank 36, planned, L0/rework required, theorem incomplete |
| `python3 -m json.tool Stage1_Instances/THM-M-0116/instance.json` | 0 | valid JSON |
| `python3 -m json.tool Stage1_Instances/THM-M-0116/task-dag.json` | 0 | valid JSON |
| `git diff --check -- Stage1_Instances/THM-M-0116` | 0 | no whitespace errors |

This is the smallest real validation for a prose-only planned intake. No Lean file or declaration
exists in this phase, so no kernel or build result is claimed. Known open gates are exact source
pinning, Lean statement elaboration, anchor audit, obligation freezing, proof, and release review.
