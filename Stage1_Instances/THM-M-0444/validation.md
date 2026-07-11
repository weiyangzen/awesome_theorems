# Intake validation record

Base revision: `1a30b84c1f86a2bbbf08b36f9afd06912b8f6c06`.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 1546 uniform-L0 Lean 4 targets, execution skill present |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1..1546, all L0/rework-required |
| `python3 scripts/stage1_target.py show THM-M-0444` | 0 | rank 90, planned, L0/rework-required, legacy artifacts unaccepted, theorem incomplete |
| `python3 -m json.tool Stage1_Instances/THM-M-0444/intake.json >/dev/null` | 0 | valid JSON |
| `python3 -m json.tool Stage1_Instances/THM-M-0444/task-dag.json >/dev/null` | 0 | valid JSON |
| `test -f Stage1_Instances/THM-M-0444/README.md && test -f Stage1_Instances/THM-M-0444/source_statement_crosswalk.md` | 0 | dossier references exist |
| forbidden proof/completion-token scan over the owned directory | 0 | expected no-match condition observed |
| `git diff --check` | 0 | no whitespace errors |

This is intake-only structural validation. No Lean declaration was introduced, so no kernel result
is claimed. Exact statement identification, all dependent phases, and master acceptance remain
open.
