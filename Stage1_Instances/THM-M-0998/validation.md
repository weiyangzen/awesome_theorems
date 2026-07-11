# Intake validation record

Base revision: `9c650bd6aac0dca129c8bc8ac01e0d7432669386`.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | `ok`: 15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 targets, skill present |
| `python3 scripts/stage1_target.py check` | 0 | `ok`: 1546 unique targets, ranks 1..1546, all L0/rework-required |
| `python3 scripts/stage1_target.py show THM-M-0998` | 0 | rank 278; planned; L0/rework-required; historical status untrusted; theorem incomplete |
| `python3 -m json.tool Stage1_Instances/THM-M-0998/intake.json >/dev/null` | 0 | intake is syntactically valid JSON |
| `find Stage1_Instances/THM-M-0998 -name '*.lean' -print` | 0 | no Lean proof artifact exists in this intake-only dossier |
| `git diff --check` | 0 | no whitespace errors |

These are the smallest real checks for an intake-only dossier. No Lean proposition could truthfully
be elaborated because the source statement is under-specified; no kernel or proof result is claimed.
The intake itself is self-tested, while the dependent statement gate remains blocked pending the
source-selection retry condition documented in `source_statement_crosswalk.md`.
