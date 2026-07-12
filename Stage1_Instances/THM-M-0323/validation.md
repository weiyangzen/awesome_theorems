# Intake validation

Base revision: `89d346c6e4d70a887dc4caa607fa8e82a9050b47`.

The pre-existing untracked `Formalizations/Lean/.lake` symlink exposes the canonical pinned build
artifacts and was not created or modified by this intake. This is nonrelease evidence. Validation
is limited to target-set consistency, dossier invariants, JSON syntax, and elaboration of the
representation APIs in `IntakeCheck.lean`. The checked APIs do not establish the unresolved source
theorem.

| Command | Result |
|---|---|
| `python3 Docs/tools/check_stage1_standard.py` | exit 0; 15 assurance groups and 1546 uniform-L0 targets |
| `python3 scripts/stage1_target.py check` | exit 0; 1546 unique targets, ranks 1..1546 |
| `python3 scripts/stage1_target.py show THM-M-0323` | exit 0; rank 679, L0/rework_required, planned, theorem_complete false |
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0323/IntakeCheck.lean` | exit 0; `GeneralSchauderBasis`, `SchauderBasis`, `SchauderBasis.RankOneDecomposition`, `.basis`, and `.expansion` elaborated |
| `python3 -m json.tool Stage1_Instances/THM-M-0323/instance.json` | exit 0 |
| `python3 -m json.tool Stage1_Instances/THM-M-0323/task-dag.json` | exit 0 |
| scoped Python intake assertions | exit 0; `intake invariant check: ok` |
| `git diff --check -- Stage1_Instances/THM-M-0323` | exit 0; no output |

Known downstream failures: the exact primary-source proposition, scalar/function-space and boundary
conventions, canonical Lean expression and fingerprint, exhaustive anchor audit, obligation tree,
proof, hermetic replay, and independent source/formal review remain open. These failures prevent
theorem completion but do not invalidate the fail-closed planned intake.
