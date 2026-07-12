# Intake validation

Base revision: `99f4faa83aef7915bf92b30fe214fdfc98ec26ae`.

Validation is intentionally limited to target-set consistency, dossier syntax, scoped intake
invariants, and whitespace. The metadata does not determine the precise C0-rigidity proposition,
so a Lean elaboration command at intake would test an invented or prematurely selected substitute.
No kernel, source-review, audit, or theorem-completion result is claimed.

Commands and results are recorded after execution below. The pre-existing untracked
`Formalizations/Lean/.lake` link/artifact is outside this target and was not modified.

| Command | Result |
|---|---|
| `python3 Docs/tools/check_stage1_standard.py` | exit 0; 15 assurance groups and 1546 uniform-L0 Lean 4 targets; execution skill present |
| `python3 scripts/stage1_target.py check` | exit 0; 1546 unique targets, ranks 1..1546, all L0/rework_required |
| `python3 scripts/stage1_target.py show THM-M-0613` | exit 0; rank 649, L0/rework_required, planned, theorem_complete false |
| `python3 -m json.tool Stage1_Instances/THM-M-0613/instance.json` | exit 0 |
| `python3 -m json.tool Stage1_Instances/THM-M-0613/task-dag.json` | exit 0 |
| scoped Python assertions over instance, DAG, and exact owned file set | exit 0; `intake invariant check: ok` |
| `git diff --check -- Stage1_Instances/THM-M-0613` | exit 0; no output |
| prohibited-token scan over `Stage1_Instances/THM-M-0613` | exit 0; no prohibited proof construct or fabricated-result marker found |

Known downstream failures: a primary-source pinpoint and statement conventions have not been
selected; the canonical human claim, profiles, Lean expression, and environment fingerprint are
not frozen; source review, statement mutations, elaboration, candidate audit, obligation registry,
proof, hermetic replay, and independent review remain open. These failures prevent all later phases
but do not invalidate a truthful `planned` intake.
