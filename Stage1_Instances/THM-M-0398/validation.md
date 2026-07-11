# Intake validation

Validation evidence is limited to manifest membership, repository-standard consistency, JSON syntax, dossier invariants, and whitespace checks. No Lean theorem exists in this intake, so no kernel result is claimed.

Exact commands and results are appended after execution.

Base revision: `a8d6489fd935cd71fa4499f2f3f5b051998203f4`.

| Command | Result |
|---|---|
| `python3 Docs/tools/check_stage1_standard.py` | exit 0; `ok` for 1546 uniform-L0 targets |
| `python3 scripts/stage1_target.py check` | exit 0; 1546 unique targets, ranks 1..1546 |
| `python3 scripts/stage1_target.py show THM-M-0398` | exit 0; rank 11, L0/rework_required, planned, theorem_complete false |
| `python3 -m json.tool Stage1_Instances/THM-M-0398/instance.json` | exit 0 |
| `python3 -m json.tool Stage1_Instances/THM-M-0398/task-dag.json` | exit 0 |
| scoped Python assertions over both JSON files and the owned file set | exit 0; `intake invariant check: ok` |
| `git diff --check -- Stage1_Instances/THM-M-0398` | exit 0; no output |

Known failures/open gates: the canonical Lean expression is not yet elaborated; page-level primary-source audit and independent review are open; no kernel proof or release evidence exists. These are downstream gates rather than failures of the assigned intake phase.
