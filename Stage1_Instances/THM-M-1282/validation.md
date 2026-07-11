# Intake validation record

Base revision: `73a92b5e63e8eb3c93a5c95d5aead1658ca24c79`.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | `ok`: 15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 targets, execution skill present |
| `python3 scripts/stage1_target.py check` | 0 | `ok`: 1546 unique targets, ranks 1..1546, all L0/rework-required |
| `python3 scripts/stage1_target.py show THM-M-1282` | 0 | rank 453, planned, L0/rework-required, legacy artifacts unaccepted, theorem incomplete |
| `python3 -m json.tool Stage1_Instances/THM-M-1282/intake.json >/dev/null` | 0 | Structured intake is valid JSON |
| `if find Stage1_Instances/THM-M-1282 -name '*.lean' -print -quit \| grep -q .; then rg -n '\\b(sorry\|axiom)\\b' Stage1_Instances/THM-M-1282 -g '*.lean'; else echo 'no Lean files introduced by intake'; fi` | 0 | `no Lean files introduced by intake`; no proof-bearing artifact exists to scan |
| `git diff --check -- Stage1_Instances/THM-M-1282 .stage1-worker-selftest.json` | 0 | No whitespace errors |

This is an intake-only validation surface. No Lean declaration is introduced, so a Lean build would
not test the assigned deliverable. Exact statement elaboration and all kernel gates remain open.
