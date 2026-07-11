# Intake validation

Base revision: `2b65f3efa70ae08a8776a86771b091957de1652e`.

Validation covers manifest consistency, dossier structure, scoped invariants, and whitespace only.
There is no canonical Lean expression at intake, so no elaboration or kernel proof is claimed.

| Command | Result |
|---|---|
| `python3 Docs/tools/check_stage1_standard.py` | exit 0; 15 assurance groups, 1546 uniform-L0 Lean 4 targets |
| `python3 scripts/stage1_target.py check` | exit 0; 1546 unique targets, ranks 1..1546 |
| `python3 scripts/stage1_target.py show THM-M-1314` | exit 0; rank 142, L0/rework_required, planned, theorem_complete false |
| `python3 -m json.tool Stage1_Instances/THM-M-1314/instance.json` | exit 0 |
| `python3 -m json.tool Stage1_Instances/THM-M-1314/task-dag.json` | exit 0 |
| scoped Python assertions over IDs, lifecycle, empty accepted states, artifacts, and six open downstream tasks | exit 0; `intake invariant check: ok` |
| `git diff --check -- Stage1_Instances/THM-M-1314` | exit 0; no output |

## Known downstream failures

Exact source/page and claim selection, separation from `THM-M-1315`, canonical Lean elaboration,
anchor audit, obligation registry, proof, hermetic replay, and independent review remain open. These
prevent theorem completion but do not invalidate a fail-closed `planned` intake.
