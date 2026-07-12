# Intake validation

Base revision: `e7fc1469ef5eb468d13c2ccc07a94982bc51ab75`.

Validation is intentionally limited to target-set consistency, dossier structure, scoped intake
invariants, and whitespace. The repository source phrase does not determine a canonical Lean
proposition, so running `lake env lean` on an invented expression would be false evidence. No
kernel elaboration or theorem result is claimed in this intake.

| Command | Result |
|---|---|
| `python3 Docs/tools/check_stage1_standard.py` | exit 0; 15 assurance groups, 1546 uniform-L0 Lean 4 targets, execution skill present |
| `python3 scripts/stage1_target.py check` | exit 0; 1546 unique targets, ranks 1 through 1546, all L0/rework_required |
| `python3 scripts/stage1_target.py show THM-M-1104` | exit 0; rank 544, no legacy slot, planned, theorem_complete false |
| `python3 -m json.tool Stage1_Instances/THM-M-1104/instance.json` | exit 0 |
| `python3 -m json.tool Stage1_Instances/THM-M-1104/task-dag.json` | exit 0 |
| scoped Python intake and whitespace assertions | exit 0; exact files, IDs, planned lifecycle, empty accepted states, false completion flags, and linear open downstream dependencies verified |
| `git diff --check -- Stage1_Instances/THM-M-1104` | exit 0; no output |

Known downstream failures are the missing unique source proposition and exact source review,
canonical Lean elaboration, anchor audit, frozen obligation graphs, proof, hermetic validation, and
independent review. They prevent theorem completion but do not invalidate a fail-closed `planned`
intake.
