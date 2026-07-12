# Intake validation

Base revision: `e3d0fd205c9c81486cb86f68cdc66d4d4e5bb264`.

Validation date: `2026-07-12` (`Asia/Shanghai`). This validation covers target membership,
dossier structure and invariants, JSON integrity, and a narrow pinned Lean API probe. The existing
canonical `.lake` artifacts were used read-only; no update, build, clone, or fetch was run.

| Command | Result |
|---|---|
| `python3 Docs/tools/check_stage1_standard.py` | exit 0; 15 assurance groups, 1546 uniform-L0 Lean 4 targets, execution skill present |
| `python3 scripts/stage1_target.py check` | exit 0; 1546 unique targets, ranks 1..1546, all L0/rework_required |
| `python3 scripts/stage1_target.py show THM-M-0023` | exit 0; rank 898, planned, legacy artifacts unaccepted, theorem_complete false |
| `python3 -m json.tool Stage1_Instances/THM-M-0023/instance.json` | exit 0 |
| `python3 -m json.tool Stage1_Instances/THM-M-0023/task-dag.json` | exit 0 |
| scoped Python intake assertions | exit 0; `THM-M-0023 intake invariant check: ok` |
| `(cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0023/IntakeProbe.lean)` | exit 0; six adjacent pinned APIs elaborated under Lean 4.29.0 |
| `rg -n '\\b(sorry\|admit)\\b\|^[[:space:]]*axiom\\b' Stage1_Instances/THM-M-0023 -g '*.lean'` | exit 1 as expected; no prohibited placeholder or axiom found |
| `git diff --check -- Stage1_Instances/THM-M-0023` | exit 0; no whitespace errors |

The probe is not a canonical theorem statement and supplies no proof credit. Known downstream open
gates are immutable source receipt and independent review, exact statement and mutation tests,
obligation/discovery freezes, anchor audit, proof, hermetic replay, and release acceptance. They
prevent theorem completion but do not invalidate this truthful `planned` intake.
