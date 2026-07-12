# Intake validation record

Base revision: `9b651a1d3f6c41876f66c5933991b6cbaceeb70d`.

| Command | Exit | Observed result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | `ok`: 15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, execution skill present |
| `python3 scripts/stage1_target.py check` | 0 | `ok`: 1546 unique targets, ranks 1..1546, all L0/rework-required |
| `python3 scripts/stage1_target.py show THM-M-0316` | 0 | rank 818; planned; L0/rework-required; legacy artifacts unaccepted; theorem incomplete |
| `python3 -m json.tool Stage1_Instances/THM-M-0316/intake.json >/dev/null` | 0 | intake is valid JSON |
| `python3 -m json.tool Stage1_Instances/THM-M-0316/task-dag.json >/dev/null` | 0 | dossier-local task DAG is valid JSON |
| dossier consistency assertions (Python heredoc) | 0 | `dossier_consistency: ok (planned, no accepted states, six dependent tasks open)` |
| `cd Formalizations/Lean && lake env lean --version` | 0 | Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740`, Release |
| `test -z "$(find Stage1_Instances/THM-M-0316 -name '*.lean' -print -quit)"` | 0 | intake introduces no Lean declaration or proof content |
| `git diff --check -- Stage1_Instances/THM-M-0316 .stage1-worker-selftest.json` | 0 | no whitespace errors |

This is the smallest real validation for an intake-only node. No Lean declaration is introduced,
so no kernel proof result is claimed. The Lean command fingerprints the available pinned toolchain
without building or mutating `.lake`. Master acceptance and every dependent phase remain
outstanding.
