# Intake validation record

Base revision: `2d0ac727836c39cd946970b1ba5903ae1cd8f79d`.

Commands were run from the repository root on 2026-07-12.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | `ok`: 15 assurance groups and 1546 uniform-L0 Lean 4 targets |
| `python3 scripts/stage1_target.py check` | 0 | `ok`: 1546 unique targets, ranks 1..1546, all L0/rework-required |
| `python3 scripts/stage1_target.py show THM-M-0453` | 0 | rank 302, planned, L0/rework-required, legacy status unaccepted, theorem incomplete |
| `python3 -m json.tool Stage1_Instances/THM-M-0453/intake.json >/dev/null` | 0 | structured intake is valid JSON |
| `python3 -m json.tool Stage1_Instances/THM-M-0453/task_dag.json >/dev/null` | 0 | open task DAG is valid JSON |
| `rg -n "sorry\|axiom\|placeholder\|admit" Stage1_Instances/THM-M-0453` | 1 | no forbidden proof markers found; exit 1 is `rg`'s no-match result |
| `git diff --check` | 0 | no whitespace errors |

This is the smallest real validation for an intake-only node. An exact proposition is absent from
the repository source, so introducing and compiling a Lean declaration would validate a substituted
claim. No Lean proof, kernel closure, source acceptance, or dependent-phase completion is claimed.
