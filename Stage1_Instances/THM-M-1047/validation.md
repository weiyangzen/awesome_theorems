# Intake validation

Base revision: `dbd29db42090d2fce49f69d84d4631769ef7e9c3`.

All commands ran from the repository root on 2026-07-12 (Asia/Shanghai):

| Command | Exit | Result |
|---|---:|---|
| `python3 -m json.tool Stage1_Instances/THM-M-1047/intake.json >/dev/null` | 0 | Intake JSON parsed successfully |
| `python3 Docs/tools/check_stage1_standard.py` | 0 | `ok`: 15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 targets, execution skill present |
| `python3 scripts/stage1_target.py check` | 0 | `ok`: 1546 unique targets, ranks 1..1546, all L0/rework_required |
| `python3 scripts/stage1_target.py show THM-M-1047` | 0 | Rank 240, planned, L0/rework_required, theorem_complete false |
| `rg -n "sorry\|admit\|axiom\|placeholder\|terminalKazamakiConclusion" Stage1_Instances/THM-M-1047` | 0 | One intentional prose occurrence of the legacy field name; no proof code or forbidden construct |
| `git diff --check -- Stage1_Instances/THM-M-1047` | 0 | No whitespace errors |

These are intake-level structural checks. No Lean theorem was created or credited in this phase, so
a Lean build would not validate the outstanding exact-statement gate. Master acceptance remains
required before the node can become accepted.
