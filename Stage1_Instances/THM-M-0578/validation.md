# Intake validation record

Base revision: `9898022a0eed3cf9fb3c55a6affb6176224f33cf`.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | `ok`: 15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, execution skill present |
| `python3 scripts/stage1_target.py check` | 0 | `ok`: 1546 unique targets, ranks 1..1546, all L0/rework-required |
| `python3 scripts/stage1_target.py show THM-M-0578` | 0 | rank 622, planned, L0/rework-required, legacy artifacts unaccepted, theorem incomplete |
| `python3 -m json.tool Stage1_Instances/THM-M-0578/intake.json >/dev/null` | 0 | structured intake is valid JSON |
| `rg -n --glob '!validation.md' "sorry\\|admit\\|sorryAx\\|^[[:space:]]*axiom[[:space:]]" Stage1_Instances/THM-M-0578` | 1 | no forbidden Lean proof escape matches; exit 1 means no matches |
| `git diff --check -- Stage1_Instances/THM-M-0578 .stage1-worker-selftest.json` | 0 | no whitespace errors |

This is the smallest real validation for an intake-only node. No Lean
declaration is introduced, so no kernel proof or exact-type check is claimed.
The exact-statement gate and all dependent phases remain open, as does master
acceptance. The pre-existing untracked `Formalizations/Lean/.lake` path was not
created or modified by this task and makes the worktree nonrelease evidence.
