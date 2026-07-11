# Intake validation

Base revision: `1a8797e69ff09d2b1e4aa81a7b7e8d2b14e56892`.

Validation is limited to manifest/standard consistency, dossier structure, scoped intake
invariants, JSON syntax, and whitespace. No proposition has been selected, so no Lean elaboration
or kernel result is claimed.

| Command | Result |
|---|---|
| `python3 Docs/tools/check_stage1_standard.py` | exit 0; 15 assurance groups and 1546 uniform-L0 Lean 4 targets |
| `python3 scripts/stage1_target.py check` | exit 0; 1546 unique targets, ranks 1..1546, all L0/rework_required |
| `python3 scripts/stage1_target.py show THM-M-1298` | exit 0; rank 466, L0/rework_required, planned, theorem_complete false |
| `python3 -m json.tool Stage1_Instances/THM-M-1298/instance.json` | exit 0 |
| `python3 -m json.tool Stage1_Instances/THM-M-1298/task-dag.json` | exit 0 |
| scoped Python intake assertions | exit 0; `intake invariant check: ok` |
| `git diff --check -- Stage1_Instances/THM-M-1298` | exit 0; no output |

Known downstream failures: primary-source inspection and unique theorem selection, exact domains
and parameters, canonical Lean elaboration, anchor audit, obligation registry, proof, hermetic
replay, and independent review remain open. They prevent theorem completion but do not invalidate
this fail-closed planned intake.
