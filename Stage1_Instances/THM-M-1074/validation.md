# Intake validation

Base revision: `23e8c7fd5602b359d75252bd4e37074a071f0c68`.

Validation is limited to target-manifest consistency, dossier structure, scoped intake invariants,
JSON syntax, the bounded local-name search recorded in the crosswalk, and whitespace. No canonical
Lean expression exists in this phase, so no elaboration or kernel-proof result is claimed.

| Command | Result |
|---|---|
| `python3 Docs/tools/check_stage1_standard.py` | exit 0; 15 assurance groups, 1546 uniform-L0 Lean 4 targets, execution skill present |
| `python3 scripts/stage1_target.py check` | exit 0; 1546 unique targets, ranks 1..1546, all L0/rework_required |
| `python3 scripts/stage1_target.py show THM-M-1074` | exit 0; rank 516, no legacy slot, L0/rework_required, planned, theorem_complete false |
| `rg -n -i 'compound.?poisson\|compound poisson\|compPoisson\|PoissonProcess' Formalizations/Lean .lake/packages/mathlib/Mathlib` | exit 1 with no output; no obvious local or available pinned-mathlib textual anchor found |
| `python3 -m json.tool Stage1_Instances/THM-M-1074/instance.json` | exit 0 |
| `python3 -m json.tool Stage1_Instances/THM-M-1074/task-dag.json` | exit 0 |
| scoped Python intake assertions | exit 0; `intake invariant check: ok` |
| `git diff --check -- Stage1_Instances/THM-M-1074 .stage1-worker-selftest.json` | exit 0; no output |

Known downstream failures: an exact primary-source theorem/page and independent review, canonical
Lean elaboration and mutation testing, the formal anchor/provenance audit, obligation registry,
proof, composition, hermetic replay, and independent release verification remain open. They prevent
audit and theorem completion but do not invalidate a truthful fail-closed planned intake.
