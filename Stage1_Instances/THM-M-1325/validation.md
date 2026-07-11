# Intake validation

Base revision: `7ea3aa8c0960c44b00d62639e9ddf1321848e342`.

Validation is limited to manifest consistency, dossier structure, scoped intake invariants, JSON
syntax, and whitespace. No canonical Lean expression exists yet, so no kernel result is claimed.

| Command | Result |
|---|---|
| `python3 Docs/tools/check_stage1_standard.py` | exit 0; 15 assurance groups and 1546 uniform-L0 targets |
| `python3 scripts/stage1_target.py check` | exit 0; 1546 unique targets, ranks 1..1546, all L0/rework-required |
| `python3 scripts/stage1_target.py show THM-M-1325` | exit 0; rank 487, L0/rework-required, planned, theorem incomplete |
| `python3 -m json.tool Stage1_Instances/THM-M-1325/instance.json >/dev/null` | exit 0 |
| `python3 -m json.tool Stage1_Instances/THM-M-1325/task-dag.json >/dev/null` | exit 0 |
| scoped Python intake assertions | exit 0; `intake invariant check: ok` |
| `git diff --check -- Stage1_Instances/THM-M-1325` | exit 0; no output |

Known downstream failures: exact primary-source inspection and errata review, statement
normalization, canonical Lean elaboration, anchor audit, obligation registry, proof, hermetic
replay, and independent review remain open. They prevent theorem completion but do not invalidate
this fail-closed planned intake.
