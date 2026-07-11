# Intake validation

Validation is limited to target-set integrity, planned-instance structure, JSON parsing, and whitespace checks. No Lean theorem validation is claimed because exact elaboration belongs to the dependent statement phase.

Commands and results are recorded after execution below.

Run from repository root at base revision `a8d6489fd935cd71fa4499f2f3f5b051998203f4` on 2026-07-12:

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | `ok`; 15 assurance groups and 1546 uniform-L0 Lean 4 targets. |
| `python3 scripts/stage1_target.py check` | 0 | `ok`; 1546 unique targets, ranks 1..1546. |
| `python3 scripts/stage1_target.py show THM-M-0406` | 0 | Rank 19, L0/rework_required, planned, theorem_complete false. |
| `python3 -m json.tool Stage1_Instances/THM-M-0406/instance.json` | 0 | Valid JSON. |
| `python3 -m json.tool Stage1_Instances/THM-M-0406/task-dag.json` | 0 | Valid JSON. |
| `git diff --check -- Stage1_Instances/THM-M-0406` | 0 | No whitespace errors. |

Known limitation: the generic repository validator does not yet consume this new dossier. The
node-specific intake evidence is therefore proposed for master acceptance, not an accepted receipt.
