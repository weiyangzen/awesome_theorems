# Intake validation

Base revision: `2b9e104c20989dcfc29e5ee04edb117f6e1540ce`.

Validation is limited to manifest consistency, dossier structure, JSON syntax, scoped planned-intake
invariants, and whitespace. The source wording denotes a theorem family and no exact canonical Lean
expression has been selected. Running `lake env lean` here would therefore elaborate an invented or
silently narrowed target, so no kernel result is claimed for this intake.

| Command | Result |
|---|---|
| `python3 Docs/tools/check_stage1_standard.py` | exit 0; 15 assurance groups and 1546 uniform-L0 Lean 4 targets |
| `python3 scripts/stage1_target.py check` | exit 0; 1546 unique targets, ranks 1..1546, all L0/rework_required |
| `python3 scripts/stage1_target.py show THM-M-0598` | exit 0; rank 636, L0/rework_required, planned, theorem_complete false |
| `python3 -m json.tool Stage1_Instances/THM-M-0598/instance.json` | exit 0 |
| `python3 -m json.tool Stage1_Instances/THM-M-0598/task-dag.json` | exit 0 |
| scoped Python intake assertions over identity, lifecycle, root vector, accepted states, owned file set, six open downstream tasks, and dependency chain | exit 0; `intake invariant check: ok` |
| `git diff --check -- Stage1_Instances/THM-M-0598` | exit 0; no output |

Known downstream failures: the repository label has not yet been disambiguated to one exact theorem;
no primary-source theorem/page, complete assumption crosswalk, or independent review exists; the
canonical Lean target, anchor audit, obligation registry, proof, hermetic replay, and independent
verification are all open. These failures prevent theorem completion but do not invalidate a
truthful fail-closed planned intake.
