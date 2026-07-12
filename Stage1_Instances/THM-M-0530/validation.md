# Intake validation

Base revision: `9a468f5e9a1a136bac76eb92f1c16ea75bfbb5d5`.

Validation is limited to manifest consistency, dossier structure, scoped intake invariants,
availability of the pinned Lean executable, and whitespace. No canonical Lean expression has been
selected, so no target elaboration or kernel-proof result is claimed. The existing `.lake` artifacts
were not mutated.

| Command | Result |
|---|---|
| `python3 Docs/tools/check_stage1_standard.py` | exit 0; 15 assurance groups and 1546 uniform-L0 Lean 4 targets |
| `python3 scripts/stage1_target.py check` | exit 0; 1546 unique targets, ranks 1..1546, all L0/rework_required |
| `python3 scripts/stage1_target.py show THM-M-0530` | exit 0; rank 587, L0/rework_required, planned, theorem_complete false |
| `cd Formalizations/Lean && lake env lean --version` | exit 0; Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740` |
| `python3 -m json.tool Stage1_Instances/THM-M-0530/instance.json` | exit 0 |
| `python3 -m json.tool Stage1_Instances/THM-M-0530/task-dag.json` | exit 0 |
| scoped Python intake assertions | exit 0; `intake invariant check: ok` |
| `git diff --check -- Stage1_Instances/THM-M-0530` | exit 0; no output |

Known downstream failures are exact primary-source selection and independent review, canonical Lean
statement and mutation tests, anchor audit, obligation registry, proof, hermetic replay, and release
validation. They prevent theorem completion but do not invalidate a truthful planned intake.

An earlier development version of the scoped assertion returned exit 1 because it rejected the
English word "axiom" in documentation about unresolved source conventions. The final assertion
checks dossier identity, lifecycle, owned files, empty accepted states, DAG ordering, and forbidden
proof-hole tokens; its passing result above is the applicable intake check. There are no Lean proof
artifacts in this phase.
