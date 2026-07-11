# Intake validation

Base revision: `c6aa0f2ba41dd389c2bcf01dd532923615781719`.

Validation is limited to repository/manifest consistency, dossier structure, scoped invariants,
and whitespace. The legacy Lean file was inspected but is not modified or credited. No canonical
Lean target has been frozen, so no kernel closure is claimed.

| Command | Result |
|---|---|
| `python3 Docs/tools/check_stage1_standard.py` | exit 0; 15 assurance groups, 1546 uniform-L0 Lean 4 targets |
| `python3 scripts/stage1_target.py check` | exit 0; 1546 unique targets, ranks 1..1546 |
| `python3 scripts/stage1_target.py show THM-M-0612` | exit 0; rank 256, L0/rework_required, planned, theorem_complete false |

| `python3 -m json.tool Stage1_Instances/THM-M-0612/instance.json` | exit 0; valid JSON |
| `python3 -m json.tool Stage1_Instances/THM-M-0612/task-dag.json` | exit 0; valid JSON |
| scoped Python intake assertions | exit 0; `intake invariant check: ok` |
| `git diff --check -- Stage1_Instances/THM-M-0612` | exit 0; no output |

Known downstream failures: exact primary-source inspection, exact local-embedding Lean elaboration,
fresh anchor audit, frozen obligation graphs, proof, hermetic replay, and independent review remain
open. They prevent theorem completion but do not invalidate this fail-closed planned intake.
