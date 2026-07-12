# Intake validation

Base revision: `40b00afc847f5216750db3225d428712dd401350`.

Validation covers target-set consistency, dossier structure, scoped intake invariants, JSON syntax,
whitespace, and elaboration of the pinned mathlib candidate. The Lean probe does not define or prove
the canonical target. Exact source identification and the statement gate remain open.

| Command | Result |
|---|---|
| `python3 Docs/tools/check_stage1_standard.py` | exit 0; 15 assurance groups and 1546 uniform-L0 Lean 4 targets |
| `python3 scripts/stage1_target.py check` | exit 0; 1546 unique targets, ranks 1..1546, all L0/rework_required |
| `python3 scripts/stage1_target.py show THM-M-1087` | exit 0; rank 529, L0/rework_required, planned, theorem_complete false |
| `lake env lean ../../Stage1_Instances/THM-M-1087/IntakeProbe.lean` (from `Formalizations/Lean`) | exit 0; printed the exact type of `ProbabilityTheory.IsGaussian.exists_integrable_exp_sq` |
| `python3 -m json.tool Stage1_Instances/THM-M-1087/instance.json` | exit 0 |
| `python3 -m json.tool Stage1_Instances/THM-M-1087/task-dag.json` | exit 0 |
| scoped Python intake assertions | exit 0; `intake invariant check: ok` |
| `git diff --check -- Stage1_Instances/THM-M-1087` | exit 0; no output |

Known downstream failures: primary-source identification and independent review, exact canonical
statement and checked transports, obligation registry, anchor audit, proof execution, hermetic
replay, and release validation remain open. These prevent theorem completion but do not invalidate
a truthful planned intake.
