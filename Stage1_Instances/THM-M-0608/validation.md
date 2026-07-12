# Intake validation

Base revision: `a755bddf3ef1127293a161eabda268d04a9877b3`.

Validation is intentionally limited to target-set consistency, dossier syntax, scoped intake
invariants, and whitespace. The metadata does not identify one proposition and no exact Lean target
has been selected, so a Lean elaboration command would test an invented substitute. No kernel,
source-review, audit, or theorem-completion result is claimed.

| Command | Result |
|---|---|
| `python3 Docs/tools/check_stage1_standard.py` | exit 0; 15 assurance groups and 1546 uniform-L0 Lean 4 targets |
| `python3 scripts/stage1_target.py check` | exit 0; 1546 unique targets, ranks 1..1546, all L0/rework_required |
| `python3 scripts/stage1_target.py show THM-M-0608` | exit 0; rank 645, L0/rework_required, planned, theorem_complete false |
| `python3 -m json.tool Stage1_Instances/THM-M-0608/instance.json` | exit 0 |
| `python3 -m json.tool Stage1_Instances/THM-M-0608/task-dag.json` | exit 0 |
| scoped Python assertions over the instance, DAG, and owned file set | exit 0; `intake invariant check: ok` |
| `git diff --check -- Stage1_Instances/THM-M-0608` | exit 0; no output |

Known downstream failures: the primary-source statement and theorem variant are not selected; the
canonical human claim, profiles, Lean expression, and environment fingerprint are not frozen;
pinpoint source inspection, statement mutations, elaboration, formal-candidate audit, obligation
registry, proof, hermetic replay, and independent review remain open. These failures prevent every
later phase but do not invalidate a truthful `planned` intake.
