# Intake validation

Base revision: `509bacaa61c3669c81276814a33094f8f7280f78`.

Validation is limited to target membership, dossier structure, scoped intake invariants, JSON
syntax, and whitespace. No canonical Lean expression exists yet, so `lake env lean` would not check
any claimed target and no kernel result is claimed. The pre-existing untracked
`Formalizations/Lean/.lake` is the automation clone's symlink to canonical pinned artifacts and was
not created or mutated by this intake.

| Command | Result |
|---|---|
| `python3 Docs/tools/check_stage1_standard.py` | exit 0; 15 assurance groups and 1546 uniform-L0 targets |
| `python3 scripts/stage1_target.py check` | exit 0; 1546 unique targets, ranks 1..1546 |
| `python3 scripts/stage1_target.py show THM-M-1564` | exit 0; rank 575, L0/rework_required, planned, theorem_complete false |
| `python3 -m json.tool Stage1_Instances/THM-M-1564/instance.json` | exit 0; valid JSON |
| `python3 -m json.tool Stage1_Instances/THM-M-1564/task-dag.json` | exit 0; valid JSON |
| scoped Python intake assertions | exit 0; `intake invariant check: ok` |
| `git diff --check -- Stage1_Instances/THM-M-1564` | exit 0; no output |

Known downstream failures: a unique source proposition, primary-source theorem/page and errata
inspection, a decision on model, scaling, initial data, convergence mode and limiting object,
canonical Lean elaboration, anchor audit, obligation registry, proof, hermetic replay, and
independent review remain open. They block theorem completion but do not invalidate this fail-closed
planned intake.
