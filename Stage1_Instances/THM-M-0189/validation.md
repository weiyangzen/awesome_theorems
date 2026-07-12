# Intake validation

Base revision: `e51894725a43642d26ce16e4aad3abaf28393de7`.

Validation is intentionally limited to target-set consistency, the planned dossier's structured
invariants, the availability of the pinned Lean executable, and whitespace. No canonical Lean
expression exists at intake, so the Lean version check is environment evidence, not elaboration or
kernel-proof evidence.

| Command | Result |
|---|---|
| `python3 Docs/tools/check_stage1_standard.py` | exit 0; 15 assurance groups, 1546 uniform-L0 Lean 4 targets, execution skill present |
| `python3 scripts/stage1_target.py check` | exit 0; 1546 unique targets, ranks 1..1546, all L0/rework_required |
| `python3 scripts/stage1_target.py show THM-M-0189` | exit 0; rank 675, L0/rework_required, planned, theorem_complete false |
| `cd Formalizations/Lean && lake env lean --version` | exit 0; Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740`, Release |
| `python3 -m json.tool Stage1_Instances/THM-M-0189/instance.json` | exit 0 |
| `python3 -m json.tool Stage1_Instances/THM-M-0189/task-dag.json` | exit 0 |
| scoped Python intake assertions | exit 0; `intake invariant check: ok` |
| `git diff --check -- Stage1_Instances/THM-M-0189` | exit 0; no output |

Known downstream failures are exact primary-source inspection and independent review, canonical
Lean elaboration and mutations, anchor audit, obligation registry, proof, hermetic replay, and
independent release verification. They prevent audit and theorem completion but do not invalidate a
fail-closed `planned` intake with no accepted states.
