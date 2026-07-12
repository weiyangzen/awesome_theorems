# Intake validation

Base revision: `07cadbebc45abaef80eaced8be5323f71613c97a`.

Validation is limited to repository/manifest consistency, dossier structure, scoped intake
invariants, and whitespace. No unique canonical mathematical theorem or Lean expression has been
selected, so no `lake env lean` elaboration or kernel-proof result is applicable or claimed.

| Command | Result |
|---|---|
| `python3 Docs/tools/check_stage1_standard.py` | exit 0; 15 assurance groups and 1546 uniform-L0 Lean 4 targets |
| `python3 scripts/stage1_target.py check` | exit 0; 1546 unique targets, ranks 1..1546 |
| `python3 scripts/stage1_target.py show THM-M-0563` | exit 0; rank 611, L0/rework_required, planned, theorem_complete false |
| `python3 -m json.tool Stage1_Instances/THM-M-0563/instance.json` | exit 0; valid JSON |
| `python3 -m json.tool Stage1_Instances/THM-M-0563/task-dag.json` | exit 0; valid JSON |
| scoped Python intake assertions | exit 0; `intake invariant check: ok` |
| `git diff --check -- Stage1_Instances/THM-M-0563` | exit 0; no output |

Known downstream failures: a unique pinpoint primary theorem and independent source review,
canonical Lean statement and elaboration, formal anchor audit, obligation registry, proof,
hermetic replay, and release validation remain open. They prevent theorem completion but do not
invalidate a truthful planned intake.
