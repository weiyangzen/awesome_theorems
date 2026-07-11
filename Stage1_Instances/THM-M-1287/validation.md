# Intake validation

Base revision: `ef0dd4cd5367b81a98b8906e3325b55fe5263491`.

Validation is limited to repository/manifest consistency, dossier structure, scoped intake
invariants, JSON syntax, and whitespace. No canonical Lean expression exists yet, so no kernel
result is claimed.

| Command | Result |
|---|---|
| `python3 Docs/tools/check_stage1_standard.py` | exit 0; 15 assurance groups, 1546 uniform-L0 Lean 4 targets |
| `python3 scripts/stage1_target.py check` | exit 0; 1546 unique targets, ranks 1..1546 |
| `python3 scripts/stage1_target.py show THM-M-1287` | exit 0; rank 458, L0/rework_required, planned, theorem_complete false |
| `python3 -m json.tool Stage1_Instances/THM-M-1287/instance.json` | exit 0; valid JSON |
| `python3 -m json.tool Stage1_Instances/THM-M-1287/task-dag.json` | exit 0; valid JSON |
| scoped Python intake assertions | exit 0; `intake invariant check: ok` |
| `git diff --check -- Stage1_Instances/THM-M-1287` | exit 0; no output |

Known downstream failures: primary-source inspection, exact domain and equality conventions,
canonical Lean elaboration, formal anchor audit, obligation registry, proof, hermetic replay, and
independent review remain open. They prevent theorem completion but do not invalidate this
fail-closed planned intake.
