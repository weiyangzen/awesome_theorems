# Intake validation record

Base revision: `dbd29db42090d2fce49f69d84d4631769ef7e9c3`.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | `ok`: 15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, execution skill present |
| `python3 scripts/stage1_target.py check` | 0 | `ok`: 1546 unique targets, ranks 1..1546, all L0/rework-required |
| `python3 scripts/stage1_target.py show THM-M-1032` | 0 | rank 225, planned, L0/rework-required, legacy artifacts unaccepted, theorem incomplete |
| `python3 -m json.tool Stage1_Instances/THM-M-1032/intake.json >/dev/null` | 0 | structured intake is valid JSON |
| `rg -n "sorry\|axiom\|placeholder\|admit" README.md intake.json source_statement_crosswalk.md` (from the owned directory) | 1 | no forbidden-token matches (`rg` exit 1 means no match) |
| `git diff --check` | 0 | no whitespace errors |

These are the smallest real checks for an intake-only node. No Lean theorem was introduced, so a
kernel build would not validate the claimed deliverable. Exact-statement elaboration, source audit,
all proof gates, and master acceptance remain outstanding.
