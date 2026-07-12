# Intake validation

Base revision: `ea7883ef6f408f3b7b2b0405f3148f403df0509b`.

Validation is limited to manifest consistency, dossier structure, planned-intake invariants, JSON
syntax, and whitespace. The repository wording does not determine a unique canonical Lean
proposition, so `lake env lean` would not elaborate the assigned target and no kernel result is
claimed. The pre-existing untracked `Formalizations/Lean/.lake` artifact was not created or
modified by this task.

| Command | Result |
|---|---|
| `python3 Docs/tools/check_stage1_standard.py` | exit 0; 15 assurance groups, 41 legacy rows, 300 legacy slots, and 1546 uniform-L0 Lean 4 targets |
| `python3 scripts/stage1_target.py check` | exit 0; 1546 unique targets, ranks 1 through 1546, all `L0/rework_required` |
| `python3 scripts/stage1_target.py show THM-M-1106` | exit 0; rank 546, planned, legacy artifacts unaccepted, theorem incomplete |
| `python3 -m json.tool Stage1_Instances/THM-M-1106/instance.json` | exit 0; valid JSON |
| `python3 -m json.tool Stage1_Instances/THM-M-1106/task-dag.json` | exit 0; valid JSON |
| scoped Python intake assertions | exit 0; `intake invariant check: ok` |
| `git diff --check -- Stage1_Instances/THM-M-1106` | exit 0; no output |

Known downstream failures are exact primary-source statement selection and independent review,
canonical Lean elaboration and mutation tests, formal-candidate audit, obligation registry, proof,
hermetic replay, and independent release validation. They prevent audit and theorem completion but
do not invalidate a truthful planned intake.
