# Intake validation

Base revision: `bdfc69baefbe6cfce9a205be72f3d46cb31458e8`.

Validation is limited to manifest/standard consistency, dossier syntax, scoped intake invariants,
and whitespace. No exact Lean target has been selected, so `lake env lean` has no truthful
declaration to elaborate and no kernel validation is claimed. The pre-existing untracked
`Formalizations/Lean/.lake` link/artifact was not created or mutated by this task.

| Command | Result |
|---|---|
| `python3 Docs/tools/check_stage1_standard.py` | exit 0; 15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, execution skill present |
| `python3 scripts/stage1_target.py check` | exit 0; 1546 unique targets, ranks 1..1546, all L0/rework_required |
| `python3 scripts/stage1_target.py show THM-M-0561` | exit 0; rank 609, L0/rework_required, lifecycle planned, theorem_complete false |
| `python3 -m json.tool Stage1_Instances/THM-M-0561/instance.json` | exit 0; no output |
| `python3 -m json.tool Stage1_Instances/THM-M-0561/task-dag.json` | exit 0; no output |
| scoped Python assertions over instance, DAG, and owned file set | exit 0; `intake invariant check: ok` |
| `git diff --check -- Stage1_Instances/THM-M-0561` | exit 0; no output |

Known downstream failures: the metadata does not identify one primary-source proposition. The
domain category, theory axioms, reduced/unreduced convention, grading, representing objects,
loop-equivalence semantics, natural isomorphisms, exact Lean expression, and source anchors remain
unfrozen. Elaboration, anchor audit, proof, hermetic replay, and independent review are open. These
failures prevent theorem progress but do not invalidate a fail-closed planned intake.
