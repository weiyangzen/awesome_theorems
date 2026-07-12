# Intake validation

Base revision: `0a66013e1558a3bc4e31c9d7f64c0e8fb1dfebab`.

Validation is limited to manifest consistency, dossier structure, scoped intake invariants, JSON
syntax, and whitespace. No exact Lean target exists at this phase, so running a theorem elaboration
would require inventing the missing proposition and no kernel result is claimed. The preflight tree
already contained untracked `Formalizations/Lean/.lake`; it was not created or mutated by this
intake, and this is nonrelease evidence.

| Command | Result |
|---|---|
| `python3 Docs/tools/check_stage1_standard.py` | exit 0; 15 assurance groups, 1546 uniform-L0 Lean 4 targets, execution skill present |
| `python3 scripts/stage1_target.py check` | exit 0; 1546 unique targets, ranks 1..1546, all L0/rework_required |
| `python3 scripts/stage1_target.py show THM-M-0178` | exit 0; rank 669, L0/rework_required, planned, theorem_complete false |
| `python3 -m json.tool Stage1_Instances/THM-M-0178/instance.json` | exit 0 |
| `python3 -m json.tool Stage1_Instances/THM-M-0178/task-dag.json` | exit 0 |
| scoped Python intake assertions | exit 0; `intake invariant check: ok` |
| `git diff --check -- Stage1_Instances/THM-M-0178` | exit 0; no output |

Known downstream failures are intentional and fail closed: selection and inspection of one exact
primary-source proposition, canonical Lean elaboration, anchor audit, frozen obligation registry,
proof, trust and hermetic validation, source review, and independent release verification remain
open. They prevent theorem completion but do not invalidate this planned intake.
