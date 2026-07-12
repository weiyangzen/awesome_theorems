# Intake validation

Base revision: `8c0f75b6729905650deba42603ef9f59f6b37e2c`.

Validation is limited to target membership, repository standard consistency, dossier structure,
intake invariants, and whitespace. No canonical Lean expression exists in this intake, so a kernel
elaboration command would be unrelated evidence and none is claimed. The pre-existing untracked
`Formalizations/Lean/.lake` link/artifact is outside the owned path and was neither modified nor
used as release evidence.

| Command | Result |
|---|---|
| `python3 Docs/tools/check_stage1_standard.py` | exit 0; standard structure valid, 15 assurance groups, 1546 uniform-L0 targets |
| `python3 scripts/stage1_target.py check` | exit 0; manifest valid with 1546 unique targets and ranks 1..1546 |
| `python3 scripts/stage1_target.py show THM-M-1111` | exit 0; rank 551, `L0`, `rework_required=true`, planned, theorem complete false |
| `python3 -m json.tool Stage1_Instances/THM-M-1111/instance.json` | exit 0 |
| `python3 -m json.tool Stage1_Instances/THM-M-1111/task-dag.json` | exit 0 |
| scoped Python intake assertions | exit 0; `intake invariant check: ok` |
| `git diff --check -- Stage1_Instances/THM-M-1111` | exit 0; no output |

Known downstream failures are intentionally open: immutable primary-source selection and detailed
source review, exact Lean statement and mutation tests, formal-candidate audit, obligation graph,
proof, hermetic replay, trust audit, readable reconstruction, and independent review. They prevent
audit and theorem completion but do not invalidate a fail-closed `planned` intake.
