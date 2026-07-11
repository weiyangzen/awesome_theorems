# Intake validation

Validation is limited to manifest membership, repository-standard consistency, JSON syntax, dossier invariants, and whitespace. There is no canonical Lean declaration in this intake, so no elaboration or kernel-proof result is claimed.

Base revision: `478034dee4145f887a572a3c645a3a2ea81bc883`.

| Command | Result |
|---|---|
| `python3 Docs/tools/check_stage1_standard.py` | exit 0; 15 assurance groups and 1546 uniform-L0 Lean 4 targets |
| `python3 scripts/stage1_target.py check` | exit 0; 1546 unique targets, ranks 1..1546 |
| `python3 scripts/stage1_target.py show THM-M-0141` | exit 0; rank 57, L0/rework_required, planned, theorem_complete false |
| `python3 -m json.tool Stage1_Instances/THM-M-0141/instance.json` | exit 0 |
| `python3 -m json.tool Stage1_Instances/THM-M-0141/task-dag.json` | exit 0 |
| scoped Python assertions over both JSON files and the exact owned file set | exit 0; `intake invariant check: ok` |
| `git diff --check -- Stage1_Instances/THM-M-0141` | exit 0; no output |

Known failures/open gates: the exact source theorem nodes and canonical Lean expression are not frozen; source page audit and independent review are open; no proof or release evidence exists. These are downstream gates, not claims made by this intake.
