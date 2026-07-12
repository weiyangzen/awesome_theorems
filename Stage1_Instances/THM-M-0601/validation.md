# Intake validation

Base revision: `83c1cc0af3ba7bd4612988241849d2949fad9e72`.

Validation is limited to target membership, dossier structure, scoped invariants, the pinned Lean
environment's base manifold vocabulary, and whitespace. `IntakeCheck.lean` is explicitly not a
canonical statement or proof check. No canonical Lean expression has been selected, so no kernel
result about the handle decomposition theorem is claimed.

| Command | Result |
|---|---|
| `python3 Docs/tools/check_stage1_standard.py` | exit 0; 15 assurance groups and 1546 uniform-L0 targets |
| `python3 scripts/stage1_target.py check` | exit 0; 1546 unique targets, ranks 1..1546 |
| `python3 scripts/stage1_target.py show THM-M-0601` | exit 0; rank 639, L0/rework_required, planned, theorem_complete false |
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0601/IntakeCheck.lean` | exit 0; printed pinned types of `IsManifold` and `ContMDiff` |
| `python3 -m json.tool Stage1_Instances/THM-M-0601/instance.json` | exit 0 |
| `python3 -m json.tool Stage1_Instances/THM-M-0601/task-dag.json` | exit 0 |
| scoped Python intake assertions | exit 0; `intake invariant check: ok` |
| `git diff --check -- Stage1_Instances/THM-M-0601 .stage1-worker-selftest.json` | exit 0; no output |

Known downstream failures are the unselected pinpoint source and boundary convention, missing
canonical Lean statement and mutation certificate, candidate audit, obligation registry, proof,
hermetic replay, and independent review. They prevent theorem completion but do not invalidate a
fail-closed planned intake.
