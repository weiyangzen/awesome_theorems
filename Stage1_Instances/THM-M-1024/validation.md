# Intake validation record

Base revision: `d6333f8365b25d4e77164d475fe735a47cf1e37d`.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups; 1546 uniform-L0 Lean 4 targets; skill present |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1..1546, all L0/rework-required |
| `python3 scripts/stage1_target.py show THM-M-1024` | 0 | rank 500, planned, L0/rework-required, theorem incomplete |
| `python3 -m json.tool Stage1_Instances/THM-M-1024/intake.json >/dev/null` | 0 | Intake is valid JSON |
| `rg -n '\\b(sorry|axiom)\\b|placeholder|fake result' Stage1_Instances/THM-M-1024 --glob '!validation.md'` | 1 | No forbidden content; `rg` returns 1 when there are no matches |
| `git diff --check -- Stage1_Instances/THM-M-1024 .stage1-worker-selftest.json` | 0 | No scoped whitespace errors |

This is intake-only validation. It provides no elaboration, kernel proof, source acceptance, or
master receipt. All dependent phases remain open.
