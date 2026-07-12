# Intake validation

Base revision: `b8a117cd19ae3b30b59087d7bc9c8071ee7212ab`.

This validation covers target membership, dossier structure, scoped intake invariants, and a narrow
pinned Lean API probe. It does not validate a canonical corona statement or proof. The canonical
`.lake` symlink and existing pinned artifacts were used read-only; no update, build, clone, or fetch
was run.

| Command | Result |
|---|---|
| `python3 Docs/tools/check_stage1_standard.py` | exit 0; 15 assurance groups, 1546 uniform-L0 Lean 4 targets, execution skill present |
| `python3 scripts/stage1_target.py check` | exit 0; 1546 unique targets, ranks 1..1546, all L0/rework_required |
| `python3 scripts/stage1_target.py show THM-M-0373` | exit 0; rank 865, planned, legacy artifacts unaccepted, theorem_complete false |
| `python3 -m json.tool Stage1_Instances/THM-M-0373/instance.json` | exit 0; valid JSON |
| `python3 -m json.tool Stage1_Instances/THM-M-0373/task-dag.json` | exit 0; valid JSON |
| scoped Python intake assertions | exit 0; `intake invariant check: ok` |
| `(cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0373/IntakeProbe.lean)` | exit 0; all six pinned complex-analysis encoding ingredients elaborated under Lean 4.29.0 |
| `rg -n '\\b(sorry|admit)\\b|^[[:space:]]*axiom\\b' Stage1_Instances/THM-M-0373 -g '*.lean'` | exit 1, expected no-match result; no prohibited placeholder or axiom found |
| `git diff --check -- Stage1_Instances/THM-M-0373` | exit 0; no output |

Known downstream failures are intentionally open: exact primary-source passage inspection and
independent review, canonical statement elaboration and mutation tests, discovery and obligation
freezes, formal-anchor audit, proof, hermetic replay, and release acceptance. They prevent theorem
completion but do not invalidate a truthful `planned` intake.
