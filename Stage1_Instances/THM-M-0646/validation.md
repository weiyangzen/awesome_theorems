# Intake validation

Base revision: `609cbc7bf1cbe295038cefb806fb3d4ce8ffa529`.

Validation is limited to repository/manifest consistency, dossier structure, scoped invariants,
JSON syntax, whitespace, and availability of the two pinned mathlib declarations used to
disambiguate the scope. The Lean probe does not elaborate or prove the canonical target.

| Command | Result |
|---|---|
| `python3 Docs/tools/check_stage1_standard.py` | exit 0; 15 assurance groups and 1546 uniform-L0 targets |
| `python3 scripts/stage1_target.py check` | exit 0; 1546 unique targets, ranks 1..1546 |
| `python3 scripts/stage1_target.py show THM-M-0646` | exit 0; rank 692, L0/rework_required, planned, theorem_complete false |
| `python3 -m json.tool Stage1_Instances/THM-M-0646/instance.json` | exit 0 |
| `python3 -m json.tool Stage1_Instances/THM-M-0646/task-dag.json` | exit 0 |
| scoped Python intake assertions | exit 0; `intake invariant check: ok` |
| `lake env lean ../../Stage1_Instances/THM-M-0646/IntakeProbe.lean` from `Formalizations/Lean` | exit 0; pinned upward equivalence/embedding, large-model, and downward declarations printed |
| `git diff --check -- Stage1_Instances/THM-M-0646` | exit 0; no output |

Known downstream failures: pinpoint primary-source inspection and independent review, exact
cardinal and universe conventions, canonical Lean elaboration and mutation tests, source and formal
anchor audit, obligation registry, proof, composition, hermetic replay, and independent validation
remain open. They prevent theorem completion but do not invalidate this fail-closed planned intake.
