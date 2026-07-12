# Intake validation

Base revision: `99f4faa83aef7915bf92b30fe214fdfc98ec26ae`.

Validation is limited to target-set consistency, dossier syntax, scoped intake invariants, and
whitespace. The metadata does not fix the convention-level comparison statement, so elaborating a
Lean proposition now would validate an invented substitute. No kernel, source-review, audit, or
theorem-completion result is claimed. The pre-existing untracked `Formalizations/Lean/.lake` entry
makes this nonrelease evidence; it was not modified.

| Command | Result |
|---|---|
| `python3 Docs/tools/check_stage1_standard.py` | exit 0; 15 assurance groups and 1546 uniform-L0 Lean 4 targets |
| `python3 scripts/stage1_target.py check` | exit 0; 1546 unique targets, ranks 1..1546, all L0/rework_required |
| `python3 scripts/stage1_target.py show THM-M-0614` | exit 0; rank 650, L0/rework_required, planned, theorem_complete false |
| `python3 -m json.tool Stage1_Instances/THM-M-0614/instance.json` | exit 0 |
| `python3 -m json.tool Stage1_Instances/THM-M-0614/task-dag.json` | exit 0 |
| scoped Python assertions over the instance, DAG, dependency chain, and owned file set | exit 0; `intake invariant check: ok` |
| forbidden-token scan over the five dossier inputs other than this validation log | exit 1 (expected no matches) |
| `git diff --check -- Stage1_Instances/THM-M-0614` | exit 0; no output |

Known downstream failures are the missing pinpoint source statement and review, unfrozen conventions
and profiles, absent Lean target/fingerprints/mutations, absent candidate audit and obligation
registry, and all proof, hermetic replay, and independent-review gates. These failures block later
phases but do not invalidate a truthful `planned` intake.
