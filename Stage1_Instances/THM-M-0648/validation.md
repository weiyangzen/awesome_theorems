# Intake validation

Base revision: `5467f527e0c402d2d52235957d4f316892fcfb75`.

Validation is limited to repository/manifest consistency, dossier structure, scope invariants, and
elaboration of discovery-only mathlib API probes. No canonical Lean expression or proof result is
claimed.

| Command | Result |
|---|---|
| `python3 Docs/tools/check_stage1_standard.py` | exit 0; 15 assurance groups, 1546 uniform-L0 Lean 4 targets, execution skill present |
| `python3 scripts/stage1_target.py check` | exit 0; 1546 unique targets, ranks 1..1546, all L0/rework_required |
| `python3 scripts/stage1_target.py show THM-M-0648` | exit 0; rank 694, L0/rework_required, planned, theorem_complete false |
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0648/IntakeProbe.lean` | exit 0; all six pinned model-theory declaration probes elaborated |
| `python3 -m json.tool Stage1_Instances/THM-M-0648/instance.json` | exit 0; valid JSON |
| `python3 -m json.tool Stage1_Instances/THM-M-0648/task-dag.json` | exit 0; valid JSON |
| scoped Python intake assertions | exit 0; `intake invariant check: ok` |
| `git diff --check -- Stage1_Instances/THM-M-0648` | exit 0; no output |

Known downstream failures: exact primary-source pinpoint/errata inspection, canonical statement and
expression fingerprint, checked source transports, mutation tests, anchor/provenance/trust audit,
obligation registry, proof closure, hermetic replay, and independent review remain open. They
prevent theorem completion but do not invalidate this fail-closed planned intake.
