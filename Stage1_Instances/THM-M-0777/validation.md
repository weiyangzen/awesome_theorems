# Intake validation

Base revision: `3159849a5319960dea505779c7c20894ea30487c`.

This validation covers target membership, dossier structure, JSON integrity, and one narrow pinned
Lean API probe. It does not validate a canonical incompleteness statement or proof. The canonical
`.lake` symlink was consumed read-only; no dependency update, build, clone, or fetch was run.

| Command | Result |
|---|---|
| `python3 Docs/tools/check_stage1_standard.py` | exit 0; 15 assurance groups and 1546 uniform-L0 Lean 4 targets accepted |
| `python3 scripts/stage1_target.py check` | exit 0; 1546 unique targets, ranks 1..1546, all L0/rework_required |
| `python3 scripts/stage1_target.py show THM-M-0777` | exit 0; rank 782, planned, no legacy slot, theorem_complete false |
| `python3 -m json.tool Stage1_Instances/THM-M-0777/instance.json` | exit 0 |
| `python3 -m json.tool Stage1_Instances/THM-M-0777/task-dag.json` | exit 0 |
| scoped Python intake assertions | exit 0; `intake invariant check: ok` |
| `(cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0777/IntakeProbe.lean)` | exit 0; all three pinned beta-function API checks elaborated under Lean 4.29.0 |
| `git diff --check -- Stage1_Instances/THM-M-0777 .stage1-worker-selftest.json` | exit 0; no output |

Known downstream gates intentionally remain open: exact primary-source inspection and independent
review, source-variant selection, canonical statement elaboration and mutation tests, discovery and
obligation freezes, anchor audit, proof, hermetic replay, and release acceptance. They block theorem
completion but do not invalidate a truthful `planned` intake.
