# Intake validation

Base revision: `056367be3b1cb2e101200085ec5a5fdff670d16b`.

Validation covers manifest consistency, dossier structure, scoped intake invariants, and
whitespace only. There is no canonical Lean expression at intake, so no kernel evidence is claimed.

| Command | Result |
|---|---|
| `python3 Docs/tools/check_stage1_standard.py` | exit 0; 15 assurance groups and 1546 uniform-L0 targets |
| `python3 scripts/stage1_target.py check` | exit 0; 1546 unique targets, ranks 1..1546 |
| `python3 scripts/stage1_target.py show THM-M-1222` | exit 0; rank 413, L0/rework_required, planned, theorem_complete false |
| `python3 -m json.tool Stage1_Instances/THM-M-1222/instance.json` | exit 0 |
| `python3 -m json.tool Stage1_Instances/THM-M-1222/task-dag.json` | exit 0 |
| scoped Python intake assertions | exit 0; `intake invariant check: ok` |
| `git diff --check -- Stage1_Instances/THM-M-1222` | exit 0; no output |

Known downstream failures: exact primary-source selection, source/errata review, canonical Lean
elaboration, anchor audit, obligation registry, proof, hermetic replay, and independent verification
remain open. These expected open tasks prohibit theorem completion.
