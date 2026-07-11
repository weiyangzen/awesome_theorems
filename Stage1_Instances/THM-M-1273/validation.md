# Intake validation

Base revision: `73a92b5e63e8eb3c93a5c95d5aead1658ca24c79`.

Validation is limited to manifest consistency, dossier structure, scoped intake invariants, and
whitespace. The source label does not determine a canonical proposition, so no Lean elaboration or
kernel-proof result is claimed.

| Command | Result |
|---|---|
| `python3 Docs/tools/check_stage1_standard.py` | exit 0; 15 assurance groups and 1546 uniform-L0 Lean 4 targets |
| `python3 scripts/stage1_target.py check` | exit 0; 1546 unique targets, ranks 1..1546 |
| `python3 scripts/stage1_target.py show THM-M-1273` | exit 0; rank 446, L0/rework_required, planned, theorem_complete false |
| `python3 -m json.tool Stage1_Instances/THM-M-1273/instance.json` | exit 0 |
| `python3 -m json.tool Stage1_Instances/THM-M-1273/task-dag.json` | exit 0 |
| scoped Python intake assertions | exit 0; `intake invariant check: ok` |
| `git diff --check -- Stage1_Instances/THM-M-1273` | exit 0; no output |

Known downstream failures: unique theorem identification, primary-source inspection and independent
review, canonical Lean statement, anchor audit, obligation registry, proof, hermetic replay, and
release validation remain open. They prevent theorem completion but do not invalidate this truthful
planned intake.
