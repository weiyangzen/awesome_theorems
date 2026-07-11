# Intake validation

Base revision: `8e78e1b4206fc224e91466efb397811c09205b0e`.

Validation is limited to manifest consistency, dossier structure, scoped intake invariants, and
whitespace. No canonical Lean expression exists in this phase, so no kernel result is claimed.

| Command | Result |
|---|---|
| `python3 Docs/tools/check_stage1_standard.py` | exit 0; 15 assurance groups and 1546 uniform-L0 Lean 4 targets |
| `python3 scripts/stage1_target.py check` | exit 0; 1546 unique targets, ranks 1..1546, all L0/rework_required |
| `python3 scripts/stage1_target.py show THM-M-1148` | exit 0; rank 353, no legacy slot, L0/rework_required, planned, theorem_complete false |
| `python3 -m json.tool Stage1_Instances/THM-M-1148/instance.json` | exit 0 |
| `python3 -m json.tool Stage1_Instances/THM-M-1148/task-dag.json` | exit 0 |
| scoped Python intake assertions | exit 0; `intake invariant check: ok` |
| `git diff --check -- Stage1_Instances/THM-M-1148` | exit 0; no output |

Known downstream failures: primary-source inspection, exact normalization and Lean elaboration,
anchor/body audit, obligation registry, proof, hermetic replay, and independent review remain open.
They prevent theorem completion but do not invalidate a fail-closed planned intake.
