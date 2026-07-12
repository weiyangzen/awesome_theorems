# Intake validation

Base revision: `9a5088a76a8219c7df161c5dbaeb2de32d6ce742`.

Validation is limited to manifest consistency, the planned dossier, scoped intake invariants,
the availability of the pinned Lean executable, JSON syntax, and whitespace. No canonical Lean
expression exists yet, so the Lean version check is environment evidence and not elaboration or
kernel proof evidence.

| Command | Result |
|---|---|
| `python3 Docs/tools/check_stage1_standard.py` | exit 0; 15 assurance groups, 1546 uniform-L0 Lean 4 targets, execution skill present |
| `python3 scripts/stage1_target.py check` | exit 0; 1546 unique targets, ranks 1..1546, all L0/rework_required |
| `python3 scripts/stage1_target.py show THM-M-0537` | exit 0; rank 594, L0/rework_required, planned, theorem_complete false |
| `cd Formalizations/Lean && lake env lean --version` | exit 0; Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740`, Release |
| `python3 -m json.tool Stage1_Instances/THM-M-0537/instance.json` | exit 0 |
| `python3 -m json.tool Stage1_Instances/THM-M-0537/task-dag.json` | exit 0 |
| scoped Python intake assertions | exit 0; `intake invariant check: ok` |
| `git diff --check -- Stage1_Instances/THM-M-0537` | exit 0; no output |

Known downstream failures are intentional and explicit: exact primary-source inspection and
independent review, selection and elaboration of one theorem root, environment-expression hash,
mutation tests, anchor audit, frozen obligation registry, proof, hermetic replay, and release
receipts remain open. They prevent theorem completion but do not invalidate this planned intake.
