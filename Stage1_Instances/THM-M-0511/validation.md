# Intake validation

Base revision: `aa55669bb59986e08ea8a0d1d77a1e40343d8142`.

This validation covers manifest membership, dossier structure, JSON integrity, and a narrow pinned
Lean API probe. It does not claim an elaborated Rademacher formula or proof. The worker clone's
canonical `.lake` link was used read-only; no dependency update, fetch, or build was run.

| Command | Result |
|---|---|
| `python3 Docs/tools/check_stage1_standard.py` | exit 0; 15 assurance groups, 1546 uniform-L0 Lean 4 targets, execution skill present |
| `python3 scripts/stage1_target.py check` | exit 0; 1546 unique targets, ranks 1..1546, all L0/rework_required |
| `python3 scripts/stage1_target.py show THM-M-0511` | exit 0; rank 885, planned, legacy artifacts unaccepted, theorem_complete false |
| `python3 -m json.tool Stage1_Instances/THM-M-0511/instance.json` | exit 0 |
| `python3 -m json.tool Stage1_Instances/THM-M-0511/task-dag.json` | exit 0 |
| scoped Python intake assertions | exit 0; `intake invariant check: ok` |
| `(cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0511/IntakeProbe.lean)` | exit 0; partition `Fintype` and all seven pinned analytic/summation API checks elaborated under Lean 4.29.0 |
| `git diff --check -- Stage1_Instances/THM-M-0511` | exit 0; no output |

Known downstream failures are intentionally open: immutable primary-source inspection and
independent review, exact formula/convention freeze, canonical statement elaboration and mutation
tests, obligation and discovery freezes, formal-anchor audit, proof, hermetic replay, and release
acceptance. They prevent theorem completion but do not invalidate a truthful `planned` intake.
