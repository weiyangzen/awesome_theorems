# Intake validation record

Base revision: `3f82136c3696549591ee6c2bcbea856459213d36`.

This record is completed after running the commands below. It validates only target membership,
structured intake syntax, cross-file identity, forbidden-placeholder hygiene, and whitespace. No
Lean declaration is introduced by this intake, so no elaboration or kernel-proof result is claimed.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, execution skill present |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1..1546, all L0/rework-required |
| `python3 scripts/stage1_target.py show THM-M-1115` | 0 | rank 555, planned, L0/rework-required, legacy artifacts unaccepted, theorem incomplete |
| `python3 -m json.tool Stage1_Instances/THM-M-1115/intake.json >/dev/null` | 0 | structured intake is valid JSON |
| `python3 -m json.tool Stage1_Instances/THM-M-1115/task-dag.json >/dev/null` | 0 | open task DAG is valid JSON |
| `rg -n "sorry\\|admit\\|sorryAx\\|^[[:space:]]*axiom[[:space:]]" Stage1_Instances/THM-M-1115` | 1 | no forbidden Lean proof escapes; exit 1 means no matches |
| `git diff --check -- Stage1_Instances/THM-M-1115 .stage1-worker-selftest.json` | 0 | no whitespace errors |

The exact-statement, source-fidelity, machine, proof, and release gates remain open, as does master
acceptance.
