# Intake validation

Base revision: `c6aa0f2ba41dd389c2bcf01dd532923615781719`.

Validation is limited to manifest consistency, dossier structure, scoped intake invariants, and
whitespace. No canonical Lean expression has been selected, so no kernel result is claimed.

| Command | Result |
|---|---|
| `python3 Docs/tools/check_stage1_standard.py` | exit 0; 15 assurance groups and 1546 uniform-L0 targets |
| `python3 scripts/stage1_target.py check` | exit 0; 1546 unique targets, ranks 1..1546 |
| `python3 scripts/stage1_target.py show THM-M-0990` | exit 0; rank 270, L0/rework_required, planned, theorem_complete false |
| `python3 -m json.tool Stage1_Instances/THM-M-0990/instance.json` | exit 0 |
| `python3 -m json.tool Stage1_Instances/THM-M-0990/task-dag.json` | exit 0 |
| scoped Python intake assertions | exit 0; `intake invariant check: ok` |
| `git diff --check -- Stage1_Instances/THM-M-0990` | exit 0; no output |

Known downstream failures: pinpoint primary-source inspection and errata, canonical Lean
elaboration, mutation tests, anchor audit, obligation registry, proof, hermetic replay, and
independent review remain open. They prevent theorem completion but do not invalidate a truthful
planned intake.
