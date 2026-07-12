# Intake validation

Base revision: `694b331243d16cc36a69b54661f4bcbd9813e120`.

Validation is limited to repository/manifest consistency, dossier structure,
scoped intake invariants, JSON syntax, and whitespace. The pre-existing
untracked `Formalizations/Lean/.lake` link is outside the owned path and was
not modified. No canonical Lean expression has been selected, so a Lean
elaboration command would validate a substituted statement and is not run or
claimed for this intake.

| Command | Result |
|---|---|
| `python3 Docs/tools/check_stage1_standard.py` | exit 0; 15 assurance groups, 1546 uniform-L0 Lean 4 targets |
| `python3 scripts/stage1_target.py check` | exit 0; 1546 unique targets, ranks 1..1546, all L0/rework_required |
| `python3 scripts/stage1_target.py show THM-M-1113` | exit 0; rank 553, planned, L0/rework_required, theorem_complete false |
| `python3 -m json.tool Stage1_Instances/THM-M-1113/instance.json` | exit 0 |
| `python3 -m json.tool Stage1_Instances/THM-M-1113/task-dag.json` | exit 0 |
| scoped Python intake assertions | exit 0; `intake invariant check: ok` |
| `git diff --check -- Stage1_Instances/THM-M-1113` | exit 0; no output |

Known downstream failures are the exact primary-source theorem inspection,
formal statement elaboration, environment fingerprint, mutation tests, anchor
audit, obligation registry, proof, hermetic replay, and independent review.
They prevent theorem completion but do not invalidate this fail-closed
`planned` intake.
