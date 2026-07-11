# Intake validation record

Base revision: `dbd29db42090d2fce49f69d84d4631769ef7e9c3`.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | `ok`: 15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, execution skill present |
| `python3 scripts/stage1_target.py check` | 0 | `ok`: 1546 unique targets, ranks 1..1546, all L0/rework-required |
| `python3 scripts/stage1_target.py show THM-M-1031` | 0 | rank 224, planned, L0/rework-required, legacy artifacts unaccepted, theorem incomplete |
| `python3 -m json.tool Stage1_Instances/THM-M-1031/intake.json >/dev/null` | 0 | structured intake is valid JSON |
| `if rg -n 's[o]rry\|a[x]iom\|place[h]older\|fake res[u]lt' Stage1_Instances/THM-M-1031; then exit 1; else test $? -eq 1; fi` | 0 | forbidden-token scan found no match (`rg` returned 1, converted to successful no-match assertion) |
| `git diff --check -- Stage1_Instances/THM-M-1031` | 0 | no whitespace errors |

This is the smallest real validation for an intake-only node. No Lean declaration is introduced,
and no kernel proof, source acceptance, or theorem completion is claimed. The node-specific receipt
and master acceptance remain outside worker authority.
