# Intake validation

Base revision: `43b8783c62005322690acf2bed800ea3acbd76c6`.

Validation is limited to manifest/standard consistency, dossier JSON syntax, scoped intake
invariants, and whitespace. This intake contains no Lean declaration, so no elaboration or kernel
proof result is claimed.

| Command | Result |
|---|---|
| `python3 Docs/tools/check_stage1_standard.py` | exit 0; 15 assurance groups and 1546 uniform-L0 Lean 4 targets |
| `python3 scripts/stage1_target.py check` | exit 0; 1546 unique targets, ranks 1..1546 |
| `python3 scripts/stage1_target.py show THM-M-0580` | exit 0; rank 115, L0/rework_required, planned, theorem_complete false |
| `python3 -m json.tool Stage1_Instances/THM-M-0580/instance.json` | exit 0 |
| `python3 -m json.tool Stage1_Instances/THM-M-0580/task-dag.json` | exit 0 |
| scoped Python assertions over instance, DAG, and owned file set | exit 0; `intake invariant check: ok` |
| `git diff --check -- Stage1_Instances/THM-M-0580` | exit 0; no output |

Known downstream failures: the exact cited source formulation and manifold conventions are not
frozen; no Lean expression, source audit, proof, hermetic replay, or independent review exists.
These failures prevent theorem progress but do not invalidate this fail-closed planned intake.
