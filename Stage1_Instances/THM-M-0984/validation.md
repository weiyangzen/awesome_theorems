# Intake validation record

Base revision: `c6aa0f2ba41dd389c2bcf01dd532923615781719`.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | `ok`: 15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 targets, execution skill present |
| `python3 scripts/stage1_target.py check` | 0 | `ok`: 1546 unique targets, ranks 1..1546, all L0/rework-required |
| `python3 scripts/stage1_target.py show THM-M-0984` | 0 | rank 264, planned, L0/rework-required, legacy artifacts unaccepted, theorem incomplete |
| `python3 -m json.tool Stage1_Instances/THM-M-0984/intake.json >/dev/null` | 0 | structured intake is valid JSON |
| `find Stage1_Instances/THM-M-0984 -type f -name '*.lean' -print` | 0 | no Lean files exist in this intake-only dossier, so no proof body or declaration can hide a forbidden construct |
| `git diff --check -- Stage1_Instances/THM-M-0984 .stage1-worker-selftest.json` | 0 | no scoped whitespace errors |

This is an intake-only validation surface. No Lean file is introduced, no
legacy Lean artifact is revalidated, and no kernel evidence or theorem
completion is claimed. The exact source/statement identity gate, master
acceptance, and all dependent phases remain outstanding.
