# Intake validation

Base revision: `2b65f3efa70ae08a8776a86771b091957de1652e`.

Validation is limited to manifest consistency, dossier structure, scoped intake invariants, and
whitespace. There is deliberately no Lean kernel claim because the source does not yet determine a
canonical proposition.

| Command | Result |
|---|---|
| `python3 Docs/tools/check_stage1_standard.py` | exit 0; 15 assurance groups and 1546 uniform-L0 Lean 4 targets |
| `python3 scripts/stage1_target.py check` | exit 0; 1546 unique targets, ranks 1..1546, all L0/rework required |
| `python3 scripts/stage1_target.py show THM-M-0084` | exit 0; rank 136, L0/rework required, planned, theorem complete false |
| `python3 -m json.tool Stage1_Instances/THM-M-0084/instance.json` | exit 0 |
| `python3 -m json.tool Stage1_Instances/THM-M-0084/task-dag.json` | exit 0 |
| scoped Python intake assertions | exit 0; `intake invariant check: ok` |
| `git diff --check -- Stage1_Instances/THM-M-0084` | exit 0; no output |

Known downstream failures are the unidentified exact source theorem and assumptions, canonical Lean
elaboration, anchor audit, obligation registry, proof, hermetic replay, and independent review.
These prevent theorem completion but do not invalidate a fail-closed planned intake.
