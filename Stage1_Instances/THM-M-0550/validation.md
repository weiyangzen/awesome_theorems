# Intake validation record

Base revision: `4ded08c944b0cce883dd8b2421be349e11ae9a99`.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | `ok`: 15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, execution skill present |
| `python3 scripts/stage1_target.py check` | 0 | `ok`: 1546 unique targets, ranks 1..1546, all L0/rework-required |
| `python3 scripts/stage1_target.py show THM-M-0550` | 0 | rank 602, planned, L0/rework-required, legacy artifacts unaccepted, theorem incomplete |
| `python3 -m json.tool Stage1_Instances/THM-M-0550/intake.json >/dev/null` | 0 | structured intake is valid JSON |
| `rg -n "sorry\\|admit\\|sorryAx\\|^[[:space:]]*axiom[[:space:]]" Stage1_Instances/THM-M-0550` | 1 | no forbidden proof-escape matches; exit 1 means no matches |
| `git diff --check -- Stage1_Instances/THM-M-0550 .stage1-worker-selftest.json` | 0 | no whitespace errors before self-test manifest creation; rerun after creation below |

This is an intake-only node and introduces no Lean declaration. Consequently,
there is no honest kernel elaboration or proof check to claim in this phase.
The exact-statement gate, all proof gates, and master acceptance remain open.
