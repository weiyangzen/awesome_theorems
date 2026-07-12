# Intake validation

Base revision: `f247e0d21ae7b4235e6bc7f78c1fad05b754ff16`.

Validation is limited to target/manifest consistency, dossier structure, scoped intake invariants,
and whitespace. The pre-existing untracked `Formalizations/Lean/.lake` worker artifact makes the
tree dirty and is not modified or treated as release evidence. Because the source label does not
yet identify a unique proposition, no canonical Lean file exists and no elaboration or kernel-proof
result is claimed.

| Command | Result |
|---|---|
| `python3 Docs/tools/check_stage1_standard.py` | exit 0; 15 assurance groups and 1546 uniform-L0 Lean 4 targets |
| `python3 scripts/stage1_target.py check` | exit 0; 1546 unique targets, ranks 1..1546, all L0/rework_required |
| `python3 scripts/stage1_target.py show THM-M-0591` | exit 0; rank 631, L0/rework_required, planned, theorem_complete false |
| `python3 -m json.tool Stage1_Instances/THM-M-0591/instance.json` | exit 0 |
| `python3 -m json.tool Stage1_Instances/THM-M-0591/task-dag.json` | exit 0 |
| scoped Python intake assertions | exit 0; `intake invariant check: ok` |
| `git diff --check -- Stage1_Instances/THM-M-0591` | exit 0; no output |

Known downstream failures are intentional and fail closed: a unique pinpoint source theorem and
independent review, canonical Lean expression and environment fingerprint, mutation tests, anchor
audit, obligation registry, proof, hermetic replay, and release validation remain open. They prevent
statement or theorem completion but do not invalidate a truthful `planned` intake.
