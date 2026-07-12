# Intake validation

Base revision: `84f6634930ba233d7af5d4bce1b8b102c849e30e`.

Validation is limited to target-set consistency, planned-dossier structure, scoped invariants,
pinned environment availability, and whitespace. No canonical Lean expression has been frozen, so
the Lean probe checks only that anticipated vocabulary exists; it is not statement or proof credit.

| Command | Result |
|---|---|
| `python3 Docs/tools/check_stage1_standard.py` | exit 0; 15 assurance groups and 1546 uniform-L0 Lean 4 targets |
| `python3 scripts/stage1_target.py check` | exit 0; 1546 unique targets, ranks 1..1546 |
| `python3 scripts/stage1_target.py show THM-M-0317` | exit 0; rank 683, L0/rework_required, planned, theorem_complete false |
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0317/IntakeProbe.lean` | exit 0; pinned Lean elaborated the component-API probe |
| `python3 -m json.tool Stage1_Instances/THM-M-0317/instance.json` | exit 0 |
| `python3 -m json.tool Stage1_Instances/THM-M-0317/task-dag.json` | exit 0 |
| scoped Python intake assertions | exit 0; `intake invariant check: ok` |
| `git diff --check -- Stage1_Instances/THM-M-0317 .stage1-worker-selftest.json` | exit 0; no output |

Known downstream failures: exact primary-source text and errata inspection, formal target and
mutation tests, complete anchor audit, frozen obligation registry, proof, trust closure, hermetic
replay, and independent review remain open. They prevent theorem completion but do not invalidate
this fail-closed planned intake.
