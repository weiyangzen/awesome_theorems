# Intake validation record

Base revision: `8046f7febfe203ec958fa24e111f6b730ad8393b`.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 targets, execution skill present |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1..1546, all L0/rework-required |
| `python3 scripts/stage1_target.py show THM-M-1302` | 0 | rank 470, planned, L0/rework-required, legacy artifacts unaccepted, theorem incomplete |
| `python3 -m json.tool Stage1_Instances/THM-M-1302/intake.json >/dev/null` | 0 | structured intake is valid JSON |
| `python3 - <<'PY' ... PY` (identity, lifecycle, completion boundary, and referenced-file assertions) | 0 | `dossier reference check: ok` |
| `rg -n "sorry\|axiom\|placeholder\|fake result" Stage1_Instances/THM-M-1302 \|\| test $? -eq 1` | 0 | no forbidden proof mechanism or false-result marker found (`rg` returned 1 for no matches) |
| `git diff --check -- Stage1_Instances/THM-M-1302 .stage1-worker-selftest.json` | 0 | no whitespace errors |

This is the narrowest real validation for an intake-only node. There is no Lean proposition to
elaborate, and consequently no kernel result is claimed. Master acceptance and all dependent phases
remain outstanding.
