# Intake validation

Base revision: `b077d12b80578ad8e0f6d19a4ab2dadabdfe40c8`.

Validation is limited to target-set consistency, dossier structure, scoped intake invariants, the
available pinned Lean executable, bounded source/formal discovery, and whitespace. Source ambiguity
prevents a canonical Lean expression, so no elaboration or kernel-proof result is claimed. The
pre-existing `Formalizations/Lean/.lake` symlink was used read-only and was not modified.

| Command | Result |
|---|---|
| `python3 Docs/tools/check_stage1_standard.py` | exit 0; 15 assurance groups, 41 legacy rows, 300 legacy slots, and 1546 uniform-L0 Lean 4 targets |
| `python3 scripts/stage1_target.py check` | exit 0; 1546 unique targets, ranks 1..1546, all L0/rework_required |
| `python3 scripts/stage1_target.py show THM-M-0187` | exit 0; rank 674, planned, L0/rework_required, legacy artifacts unaccepted, theorem incomplete |
| `(cd Formalizations/Lean && lake env lean --version)` | exit 0; Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740` |
| `rg -n -i 'alexandrov\|aleksandrov\|constant gaussian curvature\|gauss curvature' Formalizations/Lean Formalizations/Lean/.lake/packages/mathlib/Mathlib --glob '*.lean'` | exit 0; unrelated Monge-Ampere `Aleksandrov` mentions found; no theorem-specific `THM-M-0187` or recognizable surface-rigidity declaration found |
| `python3 -m json.tool Stage1_Instances/THM-M-0187/instance.json` | exit 0 |
| `python3 -m json.tool Stage1_Instances/THM-M-0187/task-dag.json` | exit 0 |
| scoped Python intake assertions | exit 0; `intake invariant check: ok` |
| `git diff --check -- Stage1_Instances/THM-M-0187 .stage1-worker-selftest.json` | exit 0; no output |

Known downstream failures are exact primary-source selection and independent review, canonical Lean
elaboration and statement mutation tests, exhaustive formal-anchor audit, obligation registry,
proof, hermetic replay, and independent release validation. They prevent theorem completion but do
not invalidate this truthful fail-closed planned intake.
