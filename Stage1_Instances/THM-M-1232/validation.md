# Intake validation record

Base revision: `c67df8af765ae58e38b6c8d4ce37668f5a600c6b`.

This record is completed by the commands below after dossier creation. It covers only the intake
node. No Lean theorem or kernel proof is present.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 targets, skill present |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1..1546, all L0/rework-required |
| `python3 scripts/stage1_target.py show THM-M-1232` | 0 | rank 417, planned, L0/rework-required, theorem incomplete |
| `python3 -m json.tool Stage1_Instances/THM-M-1232/intake.json` | 0 | valid JSON |
| `find Stage1_Instances/THM-M-1232 -type f -name '*.lean' -print` | 0 | no Lean files; intake introduces no proof surface |
| `rg -n 'THM-M-1233|THM-M-1234|THM-M-1235' Docs/Stage0_Blueprint.md` | 0 | neighboring distinct targets confirmed |
| `git diff --check -- Stage1_Instances/THM-M-1232 .stage1-worker-selftest.json` | 0 | no whitespace errors |

The smallest real validation is structural because the exact-statement blocker intentionally
prevents creation of a Lean declaration. Master acceptance and all dependent phases remain open.
