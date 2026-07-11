# Intake validation

Base revision: `23e8c7fd5602b359d75252bd4e37074a071f0c68`.

Validation is limited to manifest consistency, dossier structure, scoped intake invariants, JSON
syntax, and whitespace. No canonical Lean expression has been selected, so no elaboration or
kernel-proof result is claimed.

| Command | Result |
|---|---|
| `python3 Docs/tools/check_stage1_standard.py` | exit 0; 15 assurance groups and 1546 uniform-L0 Lean 4 targets |
| `python3 scripts/stage1_target.py check` | exit 0; 1546 unique targets, ranks 1..1546, all L0/rework_required |
| `python3 scripts/stage1_target.py show THM-M-1069` | exit 0; rank 511, L0/rework_required, planned, theorem_complete false |
| `python3 -m json.tool Stage1_Instances/THM-M-1069/instance.json` | exit 0 |
| `python3 -m json.tool Stage1_Instances/THM-M-1069/task-dag.json` | exit 0 |
| scoped Python intake assertions | exit 0; `intake invariant check: ok` |
| `git diff --check -- Stage1_Instances/THM-M-1069 .stage1-worker-selftest.json` | exit 0; no output |

Known downstream failures: exact primary-source inspection and independent review, selection of the
deterministic-versus-stochastic root, canonical Lean elaboration, anchor audit, obligation registry,
proof, hermetic replay, and release validation remain open. They prevent theorem completion but do
not invalidate this fail-closed planned intake.
