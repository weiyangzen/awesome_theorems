# Intake validation

Validation is limited to target membership, repository-standard consistency,
JSON syntax, dossier invariants, and whitespace. No new Lean declaration is
part of this intake, so no kernel result is claimed.

Base revision: `478034dee4145f887a572a3c645a3a2ea81bc883`.

| Command | Result |
|---|---|
| `python3 Docs/tools/check_stage1_standard.py` | exit 0; 15 assurance groups, 1546 uniform-L0 targets |
| `python3 scripts/stage1_target.py check` | exit 0; 1546 unique targets, ranks 1..1546 |
| `python3 scripts/stage1_target.py show THM-M-0134` | exit 0; rank 50, L0/rework_required, planned, theorem_complete false |
| `python3 -m json.tool Stage1_Instances/THM-M-0134/instance.json` | exit 0 |
| `python3 -m json.tool Stage1_Instances/THM-M-0134/task-dag.json` | exit 0 |
| scoped Python assertions over both JSON files and the owned file set | exit 0; `intake invariant check: ok` |
| `git diff --check -- Stage1_Instances/THM-M-0134` | exit 0; no output |

Known failures/open gates: the primary source and exact historical statement
are not identified; the candidate Lean target is not elaborated; no anchor,
proof, kernel, source-review, or release evidence exists. These truthfully block
downstream assurance but do not prevent creation of a fail-closed planned
intake.
