# Intake validation

Base revision: `c72bad9e8827ffb1ba1a585dbe346c88393b4a3f`.

This validation covers manifest membership, dossier structure, JSON integrity, scoped intake
invariants, and a narrow pinned Lean API probe. Since the exact source formulation and encoding are
open, no canonical expression, mutation test, constructible-universe theorem, or proof is claimed.
The canonical `.lake` symlink was used read-only; no update, build, clone, or fetch was run.

| Command | Result |
|---|---|
| `python3 Docs/tools/check_stage1_standard.py` | exit 0; 15 assurance groups, 1546 uniform-L0 Lean 4 targets, execution skill present |
| `python3 scripts/stage1_target.py check` | exit 0; 1546 unique targets, ranks 1..1546, all L0/rework_required |
| `python3 scripts/stage1_target.py show THM-M-0779` | exit 0; rank 784, planned, legacy artifacts unaccepted, theorem_complete false |
| `python3 -m json.tool Stage1_Instances/THM-M-0779/instance.json` | exit 0 |
| `python3 -m json.tool Stage1_Instances/THM-M-0779/task-dag.json` | exit 0 |
| scoped Python intake assertions | exit 0; `intake invariant check: ok` |
| `(cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0779/IntakeProbe.lean)` | exit 0; all six pinned encoding-ingredient checks elaborated under Lean 4.29.0 |
| `git diff --check -- Stage1_Instances/THM-M-0779` | exit 0; no output |

Known downstream failures remain intentionally open: exact primary-source inspection and
independent review, consistency semantics and theory encoding, canonical statement elaboration and
mutation tests, discovery/obligation freezes, formal-anchor audit, construction of `L`, proof,
hermetic replay, and release acceptance. They prevent theorem completion but do not invalidate this
truthful `planned` intake.
