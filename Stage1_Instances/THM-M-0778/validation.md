# Intake validation

Base revision: `9864b47f2fbf53d0b642c54f12039877d4635056`.

This validation covers manifest membership, dossier structure, JSON integrity, scoped intake
invariants, and a narrow pinned Lean API probe. It does not validate a canonical second-
incompleteness statement or proof. The canonical `.lake` symlink was consumed read-only; no
dependency update, build, clone, or fetch was run.

| Command | Result |
|---|---|
| `python3 Docs/tools/check_stage1_standard.py` | exit 0; 15 assurance groups and 1546 uniform-L0 Lean 4 targets accepted |
| `python3 scripts/stage1_target.py check` | exit 0; 1546 unique targets, ranks 1..1546, all L0/rework_required |
| `python3 scripts/stage1_target.py show THM-M-0778` | exit 0; rank 783, planned, no legacy slot, legacy artifacts unaccepted, theorem_complete false |
| `python3 -m json.tool Stage1_Instances/THM-M-0778/instance.json` | exit 0 |
| `python3 -m json.tool Stage1_Instances/THM-M-0778/task-dag.json` | exit 0 |
| scoped Python intake assertions | exit 0; `intake invariant check: ok` |
| `(cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0778/IntakeProbe.lean)` | exit 0; all five pinned syntax/coding API checks elaborated under Lean 4.29.0 |
| `rg -n '\\b(sorry\|admit)\\b\|^[[:space:]]*axiom\\b' Stage1_Instances/THM-M-0778 -g '*.lean'` | exit 1 as expected; no prohibited placeholder or axiom occurs in owned Lean source |
| `git diff --check -- Stage1_Instances/THM-M-0778 .stage1-worker-selftest.json` | exit 0; no output |

Known downstream gates intentionally remain open: immutable primary-source inspection and
independent review, exact theory and consistency encoding, canonical statement elaboration and
mutation tests, discovery and obligation freezes, anchor audit, proof, hermetic replay, and release
acceptance. They prevent theorem completion but do not invalidate a truthful `planned` intake.
