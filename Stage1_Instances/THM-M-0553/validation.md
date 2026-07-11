# Intake validation

Base revision: `43b8783c62005322690acf2bed800ea3acbd76c6`.

Validation is limited to manifest/standard consistency, dossier syntax, scoped intake invariants,
and whitespace. No exact Lean target is selected, so no kernel validation is claimed.

| Command | Result |
|---|---|
| `python3 Docs/tools/check_stage1_standard.py` | exit 0; 15 assurance groups, 1546 uniform-L0 Lean 4 targets, execution skill present |
| `python3 scripts/stage1_target.py check` | exit 0; 1546 unique targets, ranks 1..1546, all L0/rework_required |
| `python3 scripts/stage1_target.py show THM-M-0553` | exit 0; rank 110, L0/rework_required, lifecycle planned, theorem_complete false |
| `python3 -m json.tool Stage1_Instances/THM-M-0553/instance.json` | exit 0 |
| `python3 -m json.tool Stage1_Instances/THM-M-0553/task-dag.json` | exit 0 |
| scoped Python assertions over instance, DAG, and owned file set | exit 0; `intake invariant check: ok` |
| `git diff --check -- Stage1_Instances/THM-M-0553` | exit 0; no output |

Known downstream failures: the source wording does not identify one Adams spectral-sequence
theorem; the coefficient theory, spectra, hypotheses, convergence, abutment, and Lean expression
are not frozen. Primary-source inspection, elaboration, proof, hermetic replay, and independent
review remain open. These failures prevent theorem progress but do not invalidate a fail-closed
planned intake.
