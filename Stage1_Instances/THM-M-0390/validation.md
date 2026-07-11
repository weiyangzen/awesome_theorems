# Intake validation

Base revision: `5997161aebf527e8a1e05724d4fbd4ce07dfd815`.

Validation is limited to manifest/standard consistency, dossier structure, scoped intake
invariants, JSON syntax, and whitespace. No canonical Lean declaration was authored or checked in
this phase, so no kernel closure is claimed.

| Command | Result |
|---|---|
| `python3 Docs/tools/check_stage1_standard.py` | exit 0; 15 assurance groups, 1546 uniform-L0 targets, execution skill present |
| `python3 scripts/stage1_target.py check` | exit 0; 1546 unique targets, ranks 1..1546 |
| `python3 scripts/stage1_target.py show THM-M-0390` | exit 0; rank 4, L0/rework_required, planned, theorem_complete false |
| `python3 -m json.tool Stage1_Instances/THM-M-0390/instance.json` | exit 0 |
| `python3 -m json.tool Stage1_Instances/THM-M-0390/task-dag.json` | exit 0 |
| scoped Python intake assertions | exit 0; `intake invariant check: ok` |
| `git diff --check -- Stage1_Instances/THM-M-0390` | exit 0; no output |

Known downstream failures: exact primary-source theorem/page and errata review, canonical Lean
elaboration, equivalence transports, hypothesis mutations, anchor audit, proof, hermetic replay, and
independent review remain open. These do not invalidate the deliberately fail-closed intake.
