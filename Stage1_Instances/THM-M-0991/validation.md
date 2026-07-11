# Intake validation

Base revision: `c6aa0f2ba41dd389c2bcf01dd532923615781719`.

Validation is limited to manifest consistency, dossier structure, JSON validity, scoped intake
invariants, and whitespace. The legacy Lean module was inspected but is not adopted or credited;
this intake introduces no Lean declaration and makes no kernel-closure claim.

| Command | Result |
|---|---|
| `python3 Docs/tools/check_stage1_standard.py` | exit 0; 15 assurance groups and 1546 uniform-L0 targets |
| `python3 scripts/stage1_target.py check` | exit 0; 1546 unique targets, ranks 1..1546 |
| `python3 scripts/stage1_target.py show THM-M-0991` | exit 0; rank 271, L0/rework_required, planned, theorem_complete false |
| `python3 -m json.tool Stage1_Instances/THM-M-0991/instance.json` | exit 0 |
| `python3 -m json.tool Stage1_Instances/THM-M-0991/task-dag.json` | exit 0 |
| scoped Python intake assertions | exit 0; `intake invariant check: ok` |
| `git diff --check -- Stage1_Instances/THM-M-0991` | exit 0; no output |

Known downstream open gates are primary-source pinpoint and review, correction of the universal
constant quantification, canonical elaboration and mutation tests, anchor and provenance audit,
frozen obligations, terminal proof, hermetic replay, and independent verification. They prevent
theorem completion but do not invalidate this intake phase.
