# Intake validation

Base revision: `9b651a1d3f6c41876f66c5933991b6cbaceeb70d`.

This validation covers target membership, planned-dossier structure, JSON integrity, scoped intake
invariants, and a narrow pinned Lean API/candidate probe. The canonical expression and its mutation
suite are deliberately deferred to the statement node, so no exact-statement receipt or proof
credit is claimed. The clone's canonical `.lake` symlink was used read-only; no dependency update,
build, clone, or fetch was run.

| Command | Result |
|---|---|
| `python3 Docs/tools/check_stage1_standard.py` | exit 0; 15 assurance groups, 1546 uniform-L0 Lean 4 targets, execution skill present |
| `python3 scripts/stage1_target.py check` | exit 0; 1546 unique targets, ranks 1..1546, all L0/rework_required |
| `python3 scripts/stage1_target.py show THM-M-0322` | exit 0; rank 819, planned, legacy artifacts unaccepted, theorem_complete false |
| `python3 -m json.tool Stage1_Instances/THM-M-0322/instance.json` | exit 0 |
| `python3 -m json.tool Stage1_Instances/THM-M-0322/task-dag.json` | exit 0 |
| scoped Python intake assertions | exit 0; `intake invariant check: ok` |
| `(cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0322/IntakeProbe.lean)` | exit 0; all five pinned convex-analysis API and candidate checks elaborated under Lean 4.29.0; candidate type printed with compactness and convexity premises and the expected equality |
| `git diff --check -- Stage1_Instances/THM-M-0322` | exit 0; no output |

Known downstream failures are intentionally open: exact primary/modern source inspection and
independent review, full expression hashing, statement mutations, obligation/discovery freezes,
formal-anchor provenance and trust audit, proof-node acceptance, hermetic replay, and independent
release validation. They prevent theorem completion but do not invalidate a truthful `planned`
intake.
