# Intake validation

Base revision: `43b8783c62005322690acf2bed800ea3acbd76c6`.

Validation is limited to manifest/standard consistency, dossier JSON syntax, scoped intake
invariants, and whitespace. No exact Lean target was selected, so no elaboration or kernel result is
claimed.

<!-- Results below are updated only from commands actually executed in this clone. -->

| Command | Result |
|---|---|
| `python3 Docs/tools/check_stage1_standard.py` | exit 0; 15 assurance groups and 1546 uniform-L0 targets |
| `python3 scripts/stage1_target.py check` | exit 0; 1546 unique targets, ranks 1..1546 |
| `python3 scripts/stage1_target.py show THM-M-0546` | exit 0; rank 107, L0/rework_required, planned, theorem_complete false |
| `python3 -m json.tool Stage1_Instances/THM-M-0546/instance.json` | exit 0 |
| `python3 -m json.tool Stage1_Instances/THM-M-0546/task-dag.json` | exit 0 |
| scoped Python assertions over instance, DAG, and owned file set | exit 0; `intake invariant check: ok` |
| `git diff --check -- Stage1_Instances/THM-M-0546` | exit 0; no output |

Known downstream failures: the coefficient/manifold/boundary variant and canonical human claim are
not frozen; primary-source inspection, exact Lean elaboration, anchor audit, proof, hermetic replay,
and independent review remain open. These prevent theorem progress but do not invalidate a
fail-closed intake.
