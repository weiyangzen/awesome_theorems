# Intake validation

Base revision: `e3088372b5e523a6cfdb23d80c03e154fefa2f38`.

Validation is limited to manifest consistency, dossier structure, scoped intake invariants, pinned
environment discovery, and whitespace. There is deliberately no Lean target in this intake, so no
elaboration or kernel proof is claimed. The pre-existing untracked `Formalizations/Lean/.lake`
link/artifact was reused read-only and was not modified or accepted as release evidence.

| Command | Result |
|---|---|
| `python3 Docs/tools/check_stage1_standard.py` | exit 0; 15 assurance groups and 1546 uniform-L0 targets |
| `python3 scripts/stage1_target.py check` | exit 0; 1546 unique targets, ranks 1..1546 |
| `python3 scripts/stage1_target.py show THM-M-0528` | exit 0; rank 585, L0/rework_required, planned, theorem_complete false |
| `cd Formalizations/Lean && lake env lean --version` | exit 0; Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740` |
| pinned `rg` inspection of `Mathlib/Topology/Covering/Basic.lean` and `Mathlib/Topology/Homotopy/Lifting.lean` | exit 0; relevant candidate declarations found; no closure credited |
| `python3 -m json.tool Stage1_Instances/THM-M-0528/instance.json` | exit 0; valid JSON |
| `python3 -m json.tool Stage1_Instances/THM-M-0528/task-dag.json` | exit 0; valid JSON |
| scoped Python intake assertions | exit 0; `intake invariant check: ok` |
| `git diff --check -- Stage1_Instances/THM-M-0528 .stage1-worker-selftest.json` | exit 0; no output |

Known downstream failures are exact primary-source selection and review, canonical Lean
elaboration, anchor/provenance audit, obligation expansion, proof, hermetic replay, and independent
review. They prevent theorem completion but do not invalidate this planned intake.
