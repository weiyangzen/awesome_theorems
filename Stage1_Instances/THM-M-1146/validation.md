# Intake validation record

Base revision: `fe07aee0ce546497b6b69c8f7dcf910f374c09b1`.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | `ok`: 15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 targets, execution skill present |
| `python3 scripts/stage1_target.py check` | 0 | `ok`: 1546 unique targets, ranks 1..1546, all L0/rework-required |
| `python3 scripts/stage1_target.py show THM-M-1146` | 0 | rank 351, planned, L0/rework-required, legacy artifacts unaccepted, theorem incomplete |
| `python3 -m json.tool Stage1_Instances/THM-M-1146/intake.json >/dev/null` | 0 | structured intake is valid JSON |
| `rg -n 'sorry|axiom|placeholder|fake result' Stage1_Instances/THM-M-1146` | 0 | one documentation-only match: the scope table says the foundation axiom profile remains open; no Lean source or proof body exists |
| `git diff --check -- Stage1_Instances/THM-M-1146 .stage1-worker-selftest.json` | 0 | no whitespace errors |

This is the smallest real validation for an intake-only node. The dossier deliberately introduces
no Lean declaration. It therefore makes no elaboration, kernel closure, axiom-freedom, or theorem
completion claim. Primary-source acceptance, all dependent phases, and master acceptance remain
outstanding.
